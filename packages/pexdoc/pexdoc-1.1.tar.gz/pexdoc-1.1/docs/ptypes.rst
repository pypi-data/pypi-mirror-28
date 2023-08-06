.. ptypes.rst
.. Copyright (c) 2013-2018 Pablo Acosta-Serafini
.. See LICENSE for details
.. py:module:: pexdoc.ptypes

#############
ptypes module
#############

The pseudo-types defined below can be used in contracts of the
`PyContracts <https://andreacensi.github.io/contracts>`_ library or
:py:mod:`pexdoc.pcontracts` module. As an example, with the latter:

    .. code-block:: python

        >>> from __future__ import print_function
        >>> import pexdoc
        >>> from pexdoc.ptypes import non_negative_integer
        >>> @pexdoc.pcontracts.contract(num='non_negative_integer')
        ... def myfunc(num):
        ...     print('Number received: '+str(num))
        ...
        >>> myfunc(10)
        Number received: 10
        >>> myfunc('a')
        Traceback (most recent call last):
            ...
        RuntimeError: Argument `num` is not valid

Alternatively each pseudo-type has a :ref:`checker function <ContractCheckers>`
associated with it that can be used to verify membership. For example:

    .. code-block:: python

        >>> import pexdoc
        >>> # None is returned if object belongs to pseudo-type
        >>> pexdoc.ptypes.non_negative_integer(10)
        >>> # ValueError is raised if object does not belong to pseudo-type
        >>> pexdoc.ptypes.non_negative_integer('a') # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        ValueError: [START CONTRACT MSG: non_negative_integer]...

***********
Description
***********

.. _FileName:

FileName
--------

Import as :code:`file_name`. String with a valid file name

.. _FileNameExists:

FileNameExists
--------------

Import as :code:`file_name_exists`. String with a file name that exists in the file system

.. _Function:

Function
--------

Import as :code:`function`. Callable pointer or :code:`None`

.. _NonNegativeInteger:

NonNegativeInteger
------------------

Import as :code:`non_negative_integer`. Integer greater or equal to zero

.. _NonNullString:

NonNullString
-------------

Import as :code:`non_null_string`. String of length 1 or higher

.. _OffsetRange:

OffsetRange
-----------

Import as :code:`offset_range`. Number in the [0, 1] range

.. _PositiveRealNum:

PositiveRealNum
---------------

Import as :code:`positive_real_num`. Integer or float greater than zero or :code:`None`

.. _RealNum:

RealNum
-------

Import as :code:`real_num`. Integer, float or :code:`None`

.. _ContractCheckers:

*****************
Checker functions
*****************

.. autofunction:: pexdoc.ptypes.file_name
.. autofunction:: pexdoc.ptypes.file_name_exists
.. autofunction:: pexdoc.ptypes.function
.. autofunction:: pexdoc.ptypes.non_negative_integer
.. autofunction:: pexdoc.ptypes.non_null_string
.. autofunction:: pexdoc.ptypes.offset_range
.. autofunction:: pexdoc.ptypes.positive_real_num
.. autofunction:: pexdoc.ptypes.real_num
