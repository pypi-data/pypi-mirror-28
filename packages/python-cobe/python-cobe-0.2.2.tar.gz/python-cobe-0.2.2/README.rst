========================
Python Bindings for Cobe
========================

`Cobe <https://cobe.io/>`_ is a platform for monitoring applications and
services. It provides a live, searchable view of your infrastructure
components, and their relationships, decorated with metrics and alarms.

This library provides an interface to topologically model custom Python
applications using Cobe. Both Python 2 and 3 are supported.


Example
=======

.. code-block:: python

    import cobe

    with cobe.Source(destination='stream.cobe.io') as source:
        model = cobe.Model()
        application = cobe.Update('MyApplication')
        subsystem = cobe.Update('MyApplication:SubSystem')
        subsystem.attributes['performance'].set(9001)
        subsystem.attributes['performance'].traits.add('metric:gauge')
        model.relate(parent=application, child=subsystem)
        model.relate(parent=cobe.identify_process(), child=application)
        source.send(model)


Getting Started
===============

Firstly you will need `a Cobe account and Topology
<https://cobe.io/register>`_. Once you've created your topology, read the
`getting started documentation <https://cobe.io/docs/python/getting-started/>`_
to start monitoring your own Python applications.

If you come across any bugs please do `report them
<https://bitbucket.org/cobeio/python-cobe/issues/new>`_.
