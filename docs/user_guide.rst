User Guide
==========

Official python SDK for `Parble <https://parble.com/home>`_ intelligent document processing API.

To access the API you will need a Parble account. Sign up for free at `signup <https://parble.com/signup>`_.

Installation
------------

To use the Parble SDK, first install it using pip:

.. code-block:: console

    pip install parble

Quickstart
----------

Configuration
^^^^^^^^^^^^^

The SDK requires 2 settings to connect and authenticate to the Parble API:

- The URL of your specific tenant, you can find it on your portal
- API-Key to use, generated via the portal

You can either explicitly pass it to the SDK :

.. code-block:: python

    from parble import ParbleSDK

    sdk = ParbleSDK(url="https://api.parble.com/v1/<tenant id>", api_key="xxx")


or rely on environments variables - it will be automatically read:

.. code-block:: console

    export PARBLE_URL="https://api.parble.com/v1/<tenant id>"
    export PARBLE_API_KEY="xxx"

File Upload
^^^^^^^^^^^

To upload a file, you just need to pass a file-like object to :py:func:`parble.ParbleSDK.files.post_file`.

You need to explicitly provide the filename, and optionally the content type of your file - this gives an hint about your file type; if not set it will be inferred during processing.



You can also use :py:func:`parble.ParbleSDK.files.post` to upload a file located at the provided path.


.. code-block:: python

    from parble import ParbleSDK

    sdk = ParbleSDK()  # Loading settings from envvars

    file = sdk.files.post("files/demo.pdf")

    with open("files/demo.pdf", "rb") as f:
        file = sdk.files.post_file(f, "demo.pdf", "application/pdf")

    print(file.id)



Command Line Interface
----------------------

The SDK installs a CLI utility allowing you to upload files straight from a shell.

You need to define the URL and the API-Key as environments variables beforehand:

.. code-block:: console

    export PARBLE_URL="https://api.parble.com/v1/<tenant id>"
    export PARBLE_API_KEY="xxx"
    parble file upload Invoice.pdf


The command will upload the file then wait for the result and outputs the raw json result directly on stdout by default.

You can pass the --output / -o option to the command to save the result in a file instead: See :option:`parble file upload --output`
