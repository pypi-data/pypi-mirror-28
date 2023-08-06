r"""
********
Function
********
"""
from __future__ import unicode_literals

import collections

from ._unicode import unicode_airlock
from .variables import Variables, merge_variables


class Function(object):
    r"""Base-class for object representing functions.

    Parameters
    ----------
    kwargs : dict
        Map of variable name to variable value.
    """

    def __init__(self, **kwargs):
        self._variables = Variables(kwargs)
        self._data = dict()
        self._name = kwargs.get('name', 'unamed')
        self._factr = 1e5
        self._pgtol = 1e-7

    def value(self, *args):
        r"""Evaluate the function at the ``args`` point.

        Parameters
        ----------
        args : tuple
            Point at the evaluation. The length of this :func:`tuple` is
            defined by the user.

        Returns
        -------
        float or array_like
            Function evaluated at ``args``.
        """
        raise NotImplementedError

    def gradient(self, *args):
        r"""Evaluate the gradient at the ``args`` point.

        Parameters
        ----------
        args : tuple
            Point at the gradient evaluation. The length of this :func:`tuple`
            is defined by the user.

        Returns
        -------
        dict
            Map between variables to their gradient values.
        """
        raise NotImplementedError

    @property
    def name(self):
        return self._name

    def feed(self, purpose='learn'):
        r"""Return a function with attached data."""
        purpose = unicode_airlock(purpose)
        f = FunctionDataFeed(self, self._data[purpose], self._name)
        f.factr = self._factr
        f.pgtol = self._pgtol
        return f

    def fix(self, var_name):
        r"""Set a variable fixed.

        Args:
            var_name (str): variable name.
        """
        self._variables[var_name].fix()

    def unfix(self, var_name):
        r"""Set a variable unfixed.

        Args:
            var_name (str): variable name.
        """
        self._variables[var_name].unfix()

    def isfixed(self, var_name):
        r"""Return whether a variable it is fixed or not.

        Args:
            var_name (str): variable name.
        """
        return self._variables[var_name].isfixed

    def variables(self):
        r"""Function variables."""
        return self._variables

    def set_nodata(self, purpose='learn'):
        r"""Disable data feeding.

        Parameters
        ----------
        purpose : str
            Name of the data source.
        """
        purpose = unicode_airlock(purpose)
        self._data[purpose] = tuple()

    def set_data(self, data, purpose='learn'):
        r"""Set a named data source.

        Parameters
        ----------
        purpose : str
            Name of the data source.
        """
        purpose = unicode_airlock(purpose)
        if not isinstance(data, collections.Sequence):
            data = (data, )
        self._data[purpose] = data

    def unset_data(self, purpose='learn'):
        r"""Unset a named data source.

        Parameters
        ----------
        purpose : str
            Name of the data source.
        """
        purpose = unicode_airlock(purpose)
        del self._data[purpose]


class FunctionReduce(object):
    def __init__(self, functions, name='unamed'):
        self.functions = functions
        self.__name = name
        self._factr = 1e5
        self._pgtol = 1e-7

    def operand(self, i):
        return self.functions[i]

    def feed(self, purpose='learn'):
        purpose = unicode_airlock(purpose)
        fs = [f.feed(purpose) for f in self.functions]
        f = FunctionReduceDataFeed(self, fs, self.__name)
        f.factr = self._factr
        f.pgtol = self._pgtol
        return f

    def variables(self):
        vars_list = [l.variables() for l in self.functions]
        vd = dict()
        for (i, vs) in enumerate(vars_list):
            vd['%s[%d]' % (self.__name, i)] = vs
        return merge_variables(vd)


class FunctionDataFeed(object):
    def __init__(self, target, data, name):
        self._target = target
        self.raw = data
        self._name = name
        self._factr = 1e5
        self._pgtol = 1e-7

    @property
    def factr(self):
        return self._factr

    @factr.setter
    def factr(self, v):
        self._factr = v

    @property
    def pgtol(self):
        return self._pgtol

    @pgtol.setter
    def pgtol(self, v):
        self._pgtol = v

    @property
    def name(self):
        return self._name

    def value(self):
        return self._target.value(*self.raw)

    def gradient(self):
        return self._target.gradient(*self.raw)

    def variables(self):
        return self._target.variables()

    def maximize(self, verbose=True):
        from .optimize import maximize as _maximize
        return _maximize(
            self, verbose=verbose, factr=self.factr, pgtol=self.pgtol)

    def minimize(self, verbose=True):
        from .optimize import minimize as _minimize
        return _minimize(
            self, verbose=verbose, factr=self.factr, pgtol=self.pgtol)


class FunctionReduceDataFeed(object):
    def __init__(self, target, functions, name='unamed'):
        self._target = target
        self.functions = functions
        self.__name = name
        self._factr = 1e5
        self._pgtol = 1e-7

    @property
    def factr(self):
        return self._factr

    @factr.setter
    def factr(self, v):
        self._factr = v

    @property
    def pgtol(self):
        return self._pgtol

    @pgtol.setter
    def pgtol(self, v):
        self._pgtol = v

    @property
    def name(self):
        return self.__name

    def value(self):
        value = dict()
        for (i, f) in enumerate(self.functions):
            value['%s[%d]' % (self.__name, i)] = f.value()
        vr = self._target.value_reduce
        return vr(value)

    def gradient(self):
        value = dict()
        for (i, f) in enumerate(self.functions):
            value['%s[%d]' % (self.__name, i)] = f.value()

        grad = collections.defaultdict(dict)
        for (i, f) in enumerate(self.functions):
            for gn, gv in iter(f.gradient().items()):
                grad['%s[%d]' % (self.__name, i)][gn] = gv
        gr = self._target.gradient_reduce
        return gr(value, grad)

    def variables(self):
        return self._target.variables()

    def maximize(self, verbose=True):
        from .optimize import maximize as _maximize
        return _maximize(
            self, verbose=verbose, factr=self.factr, pgtol=self.pgtol)

    def minimize(self, verbose=True):
        from .optimize import minimize as _minimize
        return _minimize(
            self, verbose=verbose, factr=self.factr, pgtol=self.pgtol)
