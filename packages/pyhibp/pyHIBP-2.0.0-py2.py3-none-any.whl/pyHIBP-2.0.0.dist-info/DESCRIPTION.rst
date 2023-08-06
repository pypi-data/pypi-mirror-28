pyHIBP (pyHave I Been Pwned)
============================

An interface to Troy Hunt's 'Have I Been Pwned?' (herein referred to as HIBP) public API. A full reference to the API specification can be found at https://haveibeenpwned.com/API/v2.
Additionally, the full API reference contains all information types and sample return values for each API endpoint.

This module detects when the rate limit of the API has been hit, and raises a RuntimeError when the limit is exceeded.
``pyHIBP._process_response`` contains the full list of items that will result in a raised exception. In summary, a call
to the module returning Boolean ``True`` or the object as decoded from the API query (currently, lists), represent
a detection that a breached account/paste/password was found; Boolean ``False`` means that the item was not found.

Installing
----------

.. code::

    pip install pyHIBP

Example usage
-------------

.. code-block:: python

    import pyHIBP

    # Check a password to see if it has been disclosed in a public breach corpus
    resp = pyHIBP.is_password_breached(password="secret")
    if resp:
        print("Password breached!")

    # Get breaches that affect a given account
    resp = pyHIBP.get_account_breaches(account="test@example.com", truncate_response=True)

    # Get all breach information
    resp = pyHIBP.get_all_breaches()

    # Get a single breach
    resp = pyHIBP.get_single_breach(breach_name="Adobe")

    # Get pastes affecting a given email address
    resp = pyHIBP.get_pastes(email_address="test@example.com")

    # Get data classes in the HIBP system
    resp = pyHIBP.get_data_classes()

Developing
----------
This project desires compatibility with Python 2 and Python 3. As such, we use virtual environments via ``pipenv``.
To develop or test, execute the following:

.. code:: python

    # Install the pre-requisite virtual environment provider
    pip install pipenv
    # Initialize the pipenv environment and install the moduled within it
    make dev
    # To run PEP8, tests, and check the manifest
    make tox

Other commands can be found in the ``Makefile``.

Goals
-----
* Synchronize to the latest HIBP API.
* For breaches and pastes, act as an intermediary; return the JSON as received from the service.
* For passwords, return True or False based on the result of the query.
* Raise appropriate exceptions for other errors.

Regarding password checking
---------------------------
* For passwords, the option to supply a plaintext password to check is provided as an implementation convenience.
* However, passwords will always be SHA1 hashed prior to submission for checking.
* The SHA1 hash will be submitted to the HIBP backend via POST-submission of the SHA1 hash.

Package version scheme
----------------------
The major version will always target the latest version of the pyHIBP API. Minor and micro will be used for incremental
changes.


