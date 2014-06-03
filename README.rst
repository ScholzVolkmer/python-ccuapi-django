    
Python CCU REST API
===================

My take on implementing the Akamai CCU REST API.

Alot of Code/Ideas from https://github.com/dpetzel/python-ccuapi 

Requirements
------------

* `Requests <http://www.python-requests.org/en/latest/>`_
* `Docopt <http://www.docopt.org/>`_


Tests
-----

None! Literally!!! 

I should use https://github.com/patrys/httmock or something like that 
to implement tests. Setup Travis, get a rtd account and such...


Usage
=====

You can use the CLI Tool to purge by cpcode or ARL/URL.

Configuration
-------------

Set these in your environemt or in your django settings module.
AKAMAI_USERNAME, AKAMAI_PASSWORD, AKAMAI_CPCODE

CLI
----

There is a command Line Tool that allows purging and requesting Status for 
purge Requests. 


.. code ::
	# Purge 
	cuapi purge --cpcode=<cpcode>


Integration with Code
---------------------


.. code ::
    
    from ccuapi import APIRequest
    request = APIRequest()

    # either cpcodes
    request.add_cpcode('12343')
    request.purge()

    # either add urls or cpcodes
    request.add_cpcode('12343')


TODO
====

* Tests
* More Documentation
