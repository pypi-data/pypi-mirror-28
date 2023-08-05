import logging
import sys
from collections import UserList
from copy import deepcopy, copy

from pyha.common.context_managers import RegisterBehaviour, AutoResize, SimulationRunning, SimPath
from pyha.common.fixed_point import Sfix, resize, default_sfix
from six import with_metaclass

# functions that will not be decorated/converted/parsed
SKIP_FUNCTIONS = ('__init__', 'model_main')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('core')


class PyhaFunc:
    """ All functions of a Pyha class will be wrapped in this object, calls to original function are done with 'profiler hack' in
    order to save the local variables. """

    class TraceManager:
        """ Enables nested functions calls, thanks to ref counting """
        last_call_locals = {}
        refcount = 0

        @classmethod
        def tracer(cls, frame, event, arg):
            # Note: this runs for ALL returns, only the LAST frame is valid info
            if event != 'return':
                return

            cls.last_call_locals = frame.f_locals

        @classmethod
        def set_profile(cls):
            cls.refcount += 1
            sys.setprofile(cls.tracer)

        @classmethod
        def remove_profile(cls):
            cls.refcount -= 1
            sys.setprofile(None)

        @classmethod
        def restore_profile(cls):
            if cls.refcount > 0:
                sys.setprofile(cls.tracer)

    def __init__(self, func):
        self.class_name = func.__self__.__class__.__name__
        self.function_name = func.__name__
        self.func = func
        self.calls = 0
        self.locals = {}

        # used for top_generator
        self.last_args = {}
        self.last_kwargs = {}
        self.last_return = {}

        self.is_main = self.function_name == 'main'

    def call_with_locals_discovery(self, *args, **kwargs):
        """ Call decorated function with tracing to read back local values """
        self.TraceManager.set_profile()
        res = self.func(*args, **kwargs)

        sys.setprofile(None)  # without this things get fucked up
        self.TraceManager.remove_profile()

        # TODO: why remove self?
        self.TraceManager.last_call_locals.pop('self')

        self.locals.update(self.TraceManager.last_call_locals)

        # in case nested call, restore the tracer function
        self.TraceManager.restore_profile()
        return res

    def __call__(self, *args, **kwargs):

        self.last_args = args
        self.last_kwargs = kwargs
        real_self = self.func.__self__
        self.calls += 1

        # CALL IS HERE!
        with SimPath(f'{self.class_name}.{self.function_name}()'):
            with RegisterBehaviour.enable():
                with AutoResize.enable():
                    ret = self.call_with_locals_discovery(*args, **kwargs)
                    # ret = self.func(*args, **kwargs)

        # ret = tuple(ret)
        # ret = (ret,)
        self.last_return = ret

        real_self._pyha_outputs.append(ret)
        return ret


class Meta(type):
    """
    https://blog.ionelmc.ro/2015/02/09/understanding-python-metaclasses/#python-2-metaclass
    """
    instance_count = 0
    instances = []

    # ran when instance is made
    def __call__(cls, *args, **kwargs):
        ret = super(Meta, cls).__call__(*args, **kwargs)

        ret._pyha_instance_id = cls.instance_count
        # if this object was CREATED during simulation, so it must be local object (or input/output)
        # anyways for local objects register and sfix behavour stuff must be disabled
        ret._pyha_is_local = SimulationRunning.is_enabled()
        cls.instance_count += 1
        cls.instances = copy(cls.instances + [ret])
        # cls.instances[cls.__name__] = ret

        for k, v in ret.__dict__.items():
            if isinstance(v, list):
                ret.__dict__[k] = PyhaList(v, ret.__class__.__name__, k)

        # make ._pyha_next variable that holds 'next' state for elements that dont know how to update themself
        ret._pyha_next = {}
        for k, v in ret.__dict__.items():
            if k == '__dict__' or k.startswith('_pyha'):
                continue
            if hasattr(v, '_pyha_update_registers'):
                continue
            ret._pyha_next[k] = deepcopy(v)

        ret._pyha_updateable = []
        for k, v in ret.__dict__.items():
            if hasattr(v, '_pyha_update_registers'):
                ret._pyha_updateable.append(v)

        # save the initial self values - all registers and initial values will be derived from these values!
        ret.__dict__['_pyha_initial_self'] = deepcopy(ret)

        # every call to 'main' will append returned values here
        ret._pyha_outputs = []

        # decorate all methods -> for locals discovery
        for method_str in dir(ret):
            if method_str in SKIP_FUNCTIONS:
                continue
            method = getattr(ret, method_str)
            if method_str[:2] != '__' and method_str[:1] != '_' and callable(
                    method) and method.__class__.__name__ == 'method':
                new = PyhaFunc(method)
                setattr(ret, method_str, new)

        return ret


def auto_resize(target, value):
    if not AutoResize.is_enabled() or not isinstance(target, Sfix) or Sfix._float_mode.enabled:
        return value

    left = target.left if target.left is not None else value.left
    right = target.right if target.right is not None else value.right

    return resize(value, left, right, round_style=target.round_style,
                  overflow_style=target.overflow_style, wrap_is_ok=target.wrap_is_ok)


class PyhaList(UserList):
    """ All the lists in the design will be wrapped in this in order to
     override __setitem__ for array element assigns, like a[1] = 1 """

    # TODO: Conversion should select only one element. Help select this, may some elements are not fully simulated.
    def __init__(self, data, class_name='None', var_name='None'):
        super().__init__(data)
        self.var_name = var_name
        self.class_name = class_name
        self._pyha_next = deepcopy(data)

    def __setitem__(self, i, y):
        """ Implements auto-resize feature, ie resizes all assigns to Sfix registers.
        Also implements the register behaviour i.e saves assigned value to shadow variable, that is later used by the '_pyha_update_registers' function.
        """
        if hasattr(self.data[0], '_pyha_update_registers'):
            # object already knows how to handle registers
            self[i] = y
        else:
            if isinstance(self.data[0], Sfix):
                with SimPath(f'{self.var_name}[{i}]='):
                    y = auto_resize(self.data[0], y)

                # lazy bounds feature, if bounds is None, take the bound from assgned value
                if self.data[0].left is None:
                    for x, xn in zip(self.data, self._pyha_next):
                        x.left = y.left
                        xn.left = y.left

                if self.data[0].right is None:
                    for x, xn in zip(self.data, self._pyha_next):
                        x.right = y.right
                        xn.right = y.right

            if RegisterBehaviour.is_enabled():
                self._pyha_next[i] = y
            else:
                self.data[i] = y

    def _pyha_update_registers(self):
        """ Update registers (eveyrthing in self), called after the return of toplevel 'main' """
        if RegisterBehaviour.is_force_disabled():
            return
        if hasattr(self.data[0], '_pyha_update_registers'):  # is submodule
            for x in self.data:
                x._pyha_update_registers()
        else:
            self.data = self._pyha_next[:]

    def _pyha_floats_to_fixed(self, silence=False):
        """ Go over the datamodel and convert floats to sfix, this is done before RTL/GATE simulation """
        if hasattr(self.data[0], '_pyha_update_registers'):  # is submodule
            for x in self.data:
                x._pyha_floats_to_fixed(silence)
        else:
            if not isinstance(self.data[0], float):
                return

            new = []
            for x in self.data:
                item = default_sfix(x)
                item.round_style = 'truncate'
                item.overflow_style = 'wrap'
                new.append(item)

            if not silence:
                logger.info(
                    f'Converted {self.class_name}.{self.var_name} = {self.data} -> {new}')
            self.data = new
            self._pyha_next = deepcopy(new)


class Hardware(with_metaclass(Meta)):
    def __deepcopy__(self, memo):
        """ http://stackoverflow.com/questions/1500718/what-is-the-right-way-to-override-the-copy-deepcopy-operations-on-an-object-in-p """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            # todo: maybe this also works for 'next'
            if k == '_pyha_initial_self':  # dont waste time on endless deepcopy
                setattr(result, k, copy(v))
            else:
                setattr(result, k, deepcopy(v, memo))
        return result

    def _pyha_update_registers(self):
        """ Update registers (everything in self), called after the return of toplevel 'main' """
        if RegisterBehaviour.is_force_disabled() or self._pyha_is_local:
            return
        # update atoms
        self.__dict__.update(self._pyha_next)

        # update all childs
        for x in self._pyha_updateable:
            x._pyha_update_registers()

    def _pyha_floats_to_fixed(self, silence=False):
        """ Go over the datamodel and convert floats to sfix, this is done before RTL/GATE simulation """
        # update atoms
        for k, v in self.__dict__.items():
            if isinstance(v, float):
                new = default_sfix(v)
                new.round_style = 'truncate'
                new.overflow_style = 'wrap'

                if not silence:
                    logger.info(
                        f'Converted {self.__class__.__name__}.{k} = {v} -> {new}')
                self.__dict__[k] = new
                self._pyha_next[k] = deepcopy(new)

        # update all childs
        for x in self._pyha_updateable:
            x._pyha_floats_to_fixed(silence)

        # update initial self
        try:
            self._pyha_initial_self._pyha_floats_to_fixed(silence=True)
        except:
            pass

    def __setattr__(self, name, value):
        """ Implements auto-resize feature, ie resizes all assigns to Sfix registers.
        Also implements the register behaviour i.e saves assigned value to shadow variable, that is later used by the '_pyha_update_registers' function.
        """

        if not hasattr(self, '_pyha_is_local'):  # this happend in some deepcopy situations..
            self.__dict__[name] = value
            return

        if AutoResize.is_enabled() and not self._pyha_is_local:
            target = getattr(self._pyha_initial_self, name)
            with SimPath(f'{name}='):
                value = auto_resize(target, value)

        if not RegisterBehaviour.is_enabled() or self._pyha_is_local:
            self.__dict__[name] = value
            return

        if isinstance(value, list):
            # list assign
            # example: self.i = [i] + self.i[:-1]
            assert isinstance(self.__dict__[name], PyhaList)
            if hasattr(self.__dict__[name][0], '_pyha_update_registers'):
                # list of submodules -> need to copy each value to submodule next
                for elem, new in zip(self.__dict__[name], value):
                    # for deeper submodules, deepcopy was not necessary..
                    elem.__dict__['_pyha_next'] = copy(new.__dict__)
            else:
                self.__dict__[name]._pyha_next = value
            return

        self._pyha_next[name] = value
