========
thrift4p
========

Installation
============

Install with pip.

.. code:: bash

    $ pip install thrift4p
    
Code Demo
=========

.. code:: python

	from thrift4p import generate_client_from_zk
	
	client = generate_client("com.didapinche.thrift.dm.hub.holder.DmOperationHubService","192.168.1.48:2282,192.168.1.49:2282")
