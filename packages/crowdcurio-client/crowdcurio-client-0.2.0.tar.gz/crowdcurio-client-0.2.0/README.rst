CrowdCurio Client
=======================

The CrowdCurio Client is a Python library for interfacing directly with the 
CrowdCurio crowdsourcing platform. The library facilitates the functionality
for managing projects and experiments on the platform programmatically.

Documentation for this client is available on `ReadTheDocs.org
<http://crowdcurio-client.readthedocs.io/>`.


Updating Documentation
----------------------
.. code-block:: bash

	cd docs

	# .. modify index.rst 

	make html 


Deploying Changes
----------------------
.. code-block:: bash

	python setup.py sdist
	twine upload dist/