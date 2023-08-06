About
=====

Python library that dynamically constructs a PyTables where condition from the
supplied keyword arguments.

This work is a part of the investigation within the research project
[ON174027]_, supported by the Ministry for Science and Technology, Republic of
Serbia. This support is gratefully acknowledged.

References
----------

.. [ON174027]
   "Computational Mechanics in Structural Engineering"

Installation
============

To install dynamic_pytables_where_condition run::

    $ pip install dynamic_pytables_where_condition

Usage examples
==============

Quick start::

    >>> from dynamic_pytables_where_condition import construct_where_condition

    >>> construct_where_condition()
    ''

    >>> construct_where_condition(t_b_min=4.0, t_b_max=8.0, a_min=2000.0)
    '(a >= 2000.0) & (t_b <= 8.0) & (t_b >= 4.0)'

    >>> construct_where_condition(t_b_fix=4.0, t_b_max=None, a_min=None)
    '(t_b == 4.0)'

Please see the `fsm_modal_analysis`_ source code for more examples.

.. _`fsm_modal_analysis`: https://bitbucket.org/petar/fsm_modal_analysis/src/

Contribute
==========

If you find any bugs, or wish to propose new features `please let us know`_.

If you'd like to contribute, simply fork `the repository`_, commit your changes
and send a pull request. Make sure you add yourself to `AUTHORS`_.

.. _`please let us know`: https://bitbucket.org/petar/dynamic_pytables_where_condition/issues/new
.. _`the repository`: http://bitbucket.org/petar/dynamic_pytables_where_condition
.. _`AUTHORS`: https://bitbucket.org/petar/dynamic_pytables_where_condition/src/default/AUTHORS
