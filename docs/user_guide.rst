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

To upload a file, the easiest is to directly specify a path where the file is located, using :py:func:`parble.ParbleSDK.files.post`.

You need to explicitly provide the filename and can optionally also include the inbox id where you want to send the file to, if you have set this up in Parble wizard.

Alternatively, you can choose to pass a file-like object to :py:func:`parble.ParbleSDK.files.post_file`.
Here you can also optionally specify the content type of your file - this gives a hint about your file type; if not set it will be inferred during processing.


.. code-block:: python

    from parble import ParbleSDK

    sdk = ParbleSDK()  # Loading settings from envvars

    # The easiest way is to directly upload from a file path, without additional options
    file = sdk.files.post("files/demo.pdf")

    # Alternatively, you can open the file yourself and pass the file-like object
    with open("files/demo.pdf", "rb") as f:
        file = sdk.files.post_file(f, "demo.pdf", "application/pdf")

    # If you want to send the file to a specific inbox, you can also choose to pass an inbox id explicitly during upload
    file = sdk.files.post("files/demo.pdf", inbox_id="<your_inbox_id>")

    # Or with a file-like object
    with open("files/demo.pdf", "rb") as f:
        file = sdk.files.post_file(f, "demo.pdf", "application/pdf", inbox_id="<your_inbox_id>")

    # Print the returned file id
    print(file.id)



Command Line Interface
----------------------

The SDK installs a CLI utility allowing you to upload files straight from a shell.

You need to define the URL and the API-Key as environment variables beforehand:

.. code-block:: console

    # Set the environment variables
    export PARBLE_URL="https://api.parble.com/v1/<tenant id>"
    export PARBLE_API_KEY="xxx"

    # Upload a file named Invoice.pdf in this folder
    parble file upload Invoice.pdf

    # Optionally specify the inbox id during upload
    parble file upload Invoice.pdf --inbox-id <your_inbox_id>


The command will upload the file then wait for the result and outputs the raw json result directly on stdout by default.

You can pass the --output / -o option to the command to save the result in a file instead: See :option:`parble file upload --output`
