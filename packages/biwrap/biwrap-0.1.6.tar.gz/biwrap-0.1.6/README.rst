******
biwrap
******
Yet simple util to make wrapper with optional arguments

Installation
############

Master branch

.. code-block:: bash

    pip install git+https://github.com/ferrine/biwrap

Latest release

.. code-block:: bash

    pip install biwrap

Problem outlined
################
**Readability and transparent implementation is important.** Wrappers is an advanced topic in programming and making them readable in some cases is difficult. The particular case is parametrizable wrapper. It can either be called with or without arguments. Implementation to handle this case is often tricky and looks weird (see `SO thread <https://stackoverflow.com/questions/3888158/making-decorators-with-optional-arguments>`__). This package solves the problem and provides with simple and generic solution.

API
###
A minimal snippet to apply it to your problem.

.. code-block:: python

    import biwrap

    @biwrap.biwrap
    def wrapper(fn, arg1='default', arg2='default'):
        def wrapped(*fn_args, **fn_kwargs):
            ...  # depends on `arg1`, `arg2`
        return wrapped

    @wrapper  # use defaults
    def func1(a, b):
        ...

    @wrapper(arg1='non default')  # change defaults
    def func2(a, b):
        ...

Example
#######

Let's discuss a case when it is needed to put functions into a registry. Some functions can have alias names.

Naive Solution
**************

.. code-block:: python

    def register(alias=None):
        def inner(fn):
            if fn.__name__ not in register.storage:
                register.storage[fn.__name__] = fn
            elif register.storage[fn.__name__] is not fn:
                raise KeyError('{} is already in storage'.format(fn.__name__))
            if alias is not None and alias not in register.storage:
                register.storage[alias] = fn
            elif alias is not None:
                raise KeyError('{} is already in storage'.format(alias))
            return fn
        return inner
    register.storage = {}


    @register()
    def f1(a):
        return a

    print(register.storage)
    #> {'f1': <function f1 at 0x11ff519d8>}


    @register(alias='fn3')
    def f2(a):
        return a

    print(register.storage)
    #> {'f1': <function f1 at 0x11ff519d8>, 'f2': <function f2 at 0x10a87d0d0>, 'fn3': <function f2 at 0x10a87d0d0>}


Analysis
========

The above example shows redundancy in

-   decorator definition has double nesting (double ``def``)
-   usage requires trailing parenthesis ``@register()`` even in case we do not use optional argument

More readable code should avoid these two points and look like:

.. code-block:: python

    def register(fn, alias=None):
        ...

    @register
    def f1(a):
        return a

    @register(alias='fn3')  # <- (1)
    def f2(a):
        return a

Naive implementation of the above API won't work. Line marked above as ``(1)`` will fail as first argument ``fn`` is not passed. But we want the output to be the same.

Better solution
***************

.. code-block:: python

    import biwrap

    @biwrap.biwrap
    def register(fn, alias=None):
        if fn.__name__ not in register.storage:
            register.storage[fn.__name__] = fn
        elif register.storage[fn.__name__] is not fn:
            raise KeyError('{} is already in storage'.format(fn.__name__))
        if alias is not None and alias not in register.storage:
            register.storage[alias] = fn
        elif alias is not None:
            raise KeyError('{} is already in storage'.format(alias))
        return fn
    register.storage = {}

    @register
    def f1(a):
        return a

    print(register.storage)
    #> {'f1': <function f1 at 0x10f45a048>}

    @register(alias='fn3')
    def f2(a):
        return a

    print(register.storage)
    #> {'f1': <function f1 at 0x10f45a048>, 'f2': <function f2 at 0x10f45a488>, 'fn3': <function f2 at 0x10f45a488>}


Functionality Overview
######################
Some corner cases may exist and custom coding can create a boilerplate for each usecase (see this `SO thread <https://stackoverflow.com/questions/3888158/making-decorators-with-optional-arguments>`__). This package takes the best and implements yet simple but generic solution to resolve them all(?).

Setup
*****

Let's take a simple wrapper as an example. It will print ``hi`` or ``bye`` depending on parametrization, default is ``hi``.

.. code-block:: python

    import biwrap

    @biwrap.biwrap
    def hiwrap(fn, hi=True):
        def new(*args, **kwargs):
            if hi:
                print('hi')
            else:
                print('bye')
            return fn(*args, **kwargs)
        return new

Cases
*****

Function wrapping
=================
Defined wrapper can be used in both ways

.. code-block:: python

    @hiwrap
    def fn(n):
        print(n)
    fn(1)
    #> hi
    #> 1

    @hiwrap(hi=False)
    def fn(n):
        print(n)
    fn(1)
    #> bye
    #> 1


Bound method wrapper
=====================

``biwrap`` also works for bound methods. As seen in `SO thread <https://stackoverflow.com/questions/3888158/making-decorators-with-optional-arguments>`__ this can be a problem as first positional argument is ``self`` instead of a function.

.. code-block:: python

    class W:
        def __init__(self, n):
            self.n = n

        @biwrap.biwrap
        def wrap(self, fn, text='hi'):
            def wrapped(*args, **kwargs):
                for _ in range(self.n):
                    print(text)
                return fn(*args, **kwargs)
            return wrapped
    wr = W(3)

    @wr.wrap
    def fn(n):
        print(n)

    fn(1)
    #> hi
    #> hi
    #> hi
    #> 1

    @wr.wrap(text='bye')
    def fn(n):
        print(n)

    wr.n = 2
    fn(2)
    #> bye
    #> bye
    #> 2

Class methods / properties wrapping
===================================

Implementation deals with these cases as well

.. code-block:: python

    class O:
        def __init__(self, n):
            self.n = n

        @classmethod
        @hiwrap
        def fn(cls, n):
            print(n)

        @property
        @hiwrap(hi=False)
        def num(self):
            return self.n


    o = O(2)
    o.fn(1)
    #> hi
    #> 1
    print(o.num)
    #> bye
    #> 2

Wrapper as a function
=====================

Function like call is OK too

.. code-block:: python

    def fn(n):
        print(n)

    fn = hiwrap(fn, hi=False)
    fn(1)
    #> bye
    #> 1

