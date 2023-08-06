.. exh.rst
.. Copyright (c) 2013-2018 Pablo Acosta-Serafini
.. See LICENSE for details
.. py:module:: pexdoc.exh

##########
exh module
##########

This module can be used to register exceptions and then raise them if a given
condition is true. For example:

.. literalinclude:: ./support/exh_example.py
    :language: python
    :tab-width: 4
    :lines: 1,6-

.. code-block:: python

	>>> import docs.support.exh_example
	>>> docs.support.exh_example.my_func('Tom')
	My name is Tom
	>>> docs.support.exh_example.my_func(5)	#doctest: +ELLIPSIS
	Traceback (most recent call last):
	    ...
	TypeError: Argument `name` is not valid

When :code:`my_func()` gets called with anything but a string as an argument
a :code:`TypeError` exception is raised with the message
:code:`'Argument \`name\` is not valid'`. While adding an exception with
:py:meth:`pexdoc.exh.addex` and conditionally raising it takes the same number
of lines of code as an exception raised inside an :code:`if` block (or less
since the raise condition can be evaluated in the same
:py:meth:`pexdoc.exh.addex` call) and incurs a slight performance penalty, using
the :py:mod:`pexdoc.exh` module allows for automatic documentation of the
exceptions raised by any function, method or class property with the help of
the :py:mod:`pexdoc.exdoc` module.

*********
Functions
*********

.. autofunction:: pexdoc.exh.addex
.. autofunction:: pexdoc.exh.addai
.. autofunction:: pexdoc.exh.get_exh_obj
.. autofunction:: pexdoc.exh.get_or_create_exh_obj
.. autofunction:: pexdoc.exh.del_exh_obj
.. autofunction:: pexdoc.exh.set_exh_obj

*******
Classes
*******

.. autoclass:: pexdoc.exh.ExHandle
	:members: add_exception, callables_db, callables_separator,
                  decode_call, encode_call, exceptions_db,
                  raise_exception_if,save_callables,
                  __add__, __bool__, __copy__, __eq__, __iadd__,
                  __nonzero__, __str__
	:show-inheritance:
