Sf Tools for Python3 Development
================================

.. image:: https://travis-ci.org/SF-Zhou/st.svg?branch=master
    :target: https://travis-ci.org/SF-Zhou/st

.. image:: https://app.wercker.com/status/601315e1243b000f0a38ff0c0d143921/s/master
    :target: https://app.wercker.com/project/byKey/601315e1243b000f0a38ff0c0d143921

A project that include my own (SF-Zhou) tools for Python3 development.

I hope it is useful for you, too. :D


=======
install
=======

.. code-block:: bash

    pip3 install st

=====
tools
=====

* singleton decorator
* dynamic code runner
* complex partial function decorator
* serialize to & deserialize from ascii string
* code running time measure
* quicker foreach operator

=========
singleton
=========

.. code-block:: python

    import st


    @st.singleton
    class A:
        pass

    assert A() == A()

======
runner
======

.. code-block:: python

    import st


    a, b = 1, 2
    ret = st.run('c = a + b', key='c', a=a, b=b)
    assert ret == 1 + 2

================
partial function
================

.. code-block:: python

    import st


    h = st.partial_back(int, 16)

    a = h('A')
    assert a == 10

    func = st.partial_front(int, '11')
    assert func(2) == 3
    assert func(10) == 11
    assert func(16) == 17

=======================
serialize & deserialize
=======================

.. code-block:: python

    >>> import st
    >>> st.serialize([1, 2, 3])
    '80035d7100284b014b024b03652e'
    >>> st.deserialize('80035d7100284b014b024b03652e')
    [1, 2, 3]

==================
time point measure
==================

.. code-block:: python

    import st
    import time


    st.set_time_point('start')
    time.sleep(0.1)
    assert 100 <= st.microsecond_from('start') <= 110

=======
foreach
=======

.. code-block:: python

    import st


    objects = ['1', '2', '3']
    assert st.foreach(int, objects) == [1, 2, 3]

The foreach operator can get the attribute of objects more quickly.
It also can run the objects function with specific arguments.

.. code-block:: python

    import st


    class A:
        def __init__(self, v):
            self.v = v

        def plus(self, p):
            return self.v + p

    objects = [A(0), A(1), A(2)]
    assert st.foreach('.v', objects) == [0, 1, 2]        # obj.v
    assert st.foreach('#plus', objects, 1) == [1, 2, 3]  # obj.plus(1)

=====
chain
=====

chain(a, b, c)(\*args, \*\*kwargs) = a(b(c(\*args, \*\*kwargs))). In other word, it connect several function to a chain func.

.. code-block:: python

    import st


    int_str_to_hex_str = st.chain(hex, int)
    assert int_str_to_hex_str('0') == '0x0'
    assert int_str_to_hex_str('1') == '0x1'
    assert int_str_to_hex_str('10') == '0xa'
    assert int_str_to_hex_str('16') == '0x10'
    assert int_str_to_hex_str.__name__ == 'chain<hex, int>'
