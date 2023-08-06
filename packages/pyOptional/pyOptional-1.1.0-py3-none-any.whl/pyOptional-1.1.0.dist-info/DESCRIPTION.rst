pyOptional
==========

Description
-----------

Library provided implementation Optional object similar to `Java
optional <https://docs.oracle.com/javase/8/docs/api/java/util/Optional.html>`__.
Using this object, You will never check ``if x is None``.

Install
-------

``pip install pyOptional``

Usage
-----

Examples
~~~~~~~~

.. code:: python

    from pyOptional.optional import Optional

    optional_with_value = Optional('ABC')
    optional_empty = Optional(None)

    print(optional_with_value)
    print(optional_empty)

**output:**

::

    Optional of: ABC
    Optional empty

Methods:
~~~~~~~~

get()
^^^^^

Returns value or throw ``NoneValueError`` exception on empty optional

.. code:: python

    print(optional_with_value.get())
    print(optional_empty.get())

**output**:

::

    ABC
    Traceback (most recent call last):
    ...
    pyOptional.exceptions.NoneValueError: Called get on empty optional

get\_or\_else(default\_value)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns value if exists or default\_value when empty

.. code:: python

    print(optional_with_value.get_or_else('XYZ'))
    print(optional_empty.get_or_else('XYZ'))

**output**:

::

    ABC
    XYZ

get\_or\_else\_get(callable\_for\_generate\_default\_value)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns value if exists, otherwise result of
``callable_for_generate_default_value``

.. code:: python

    def gen_value():
        return 'QWERTY'

    print(optional_with_value.get_or_else_get(gen_value))
    print(optional_empty.get_or_else_get(gen_value))
    print(optional_empty.get_or_else_get(lambda: 'From lambda'))

**output**:

::

    ABC
    QWERTY
    From lambda

get\_or\_raise(exception\_class, \*args, \*\*kwargs) Returns value if exists or raise provided exception
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    print(optional_with_value.get_or_raise(FileNotFoundError, 'Some message'))
    print(optional_empty.get_or_raise(FileNotFoundError, 'Some message'))

**output**:

::

    ABC
    Traceback (most recent call last):
    ...
    FileNotFoundError: Some message

map(callable\_to\_transform\_value)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns optional of other value (result returned by
``callable_to_transform_value``) or Optional empty if source Optional
was empty

.. code:: python

    print(optional_with_value.map(lambda val: val*2))
    print(optional_empty.map(lambda val: val*2))

**output**:

::

    Optional of: ABCABC
    Optional empty

flat\_map(callable\_to\_transform\_value)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Similar to map, but if source Optional contains another Optionals,
result will contain single Optional

.. code:: python

    nested_val_optional = Optional(Optional(Optional(8)))
    nested_empty_optional = Optional(Optional(Optional(None)))
    print(nested_val_optional.map(lambda val: val*3))
    print('---------------------')
    print(nested_empty_optional.map(lambda val: val*3))
    print('---------------------')
    print(nested_val_optional.flat_map(lambda val: val*3))
    print('---------------------')
    print(nested_empty_optional.flat_map(lambda val: val*3))

**output**:

::

    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type(s) for *: 'Optional' and 'int'
    ---------------------
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type(s) for *: 'Optional' and 'int'
    ---------------------
    Optional of: 24
    ---------------------
    Optional empty

if\_present(func)
^^^^^^^^^^^^^^^^^

Call func with optional value if exists. If optional is empty, do
nothing.

.. code:: python

    optional_with_value.if_present(lambda val: print('found value ' + val))
    optional_empty.if_present(lambda val: print('found value ' + val))

**output**:

::

    found value ABC

is\_present()
^^^^^^^^^^^^^

return True if Optional not empty, otherwise False

.. code:: python

    print(optional_with_value.is_present())
    print(optional_empty.is_present())

**output**:

::

    True
    False


