API Reference
=============

The package is mainly composed of a low level API Client :py:class:`parble.ParbleAPIClient` and a higher level SDK class :py:class:`parble.ParbleSDK` exposing useful features on top on the API CLient.


It is recommended to use the SDK as it provides an abstraction over the API; however it is possible to use the API Client directly in rare cases requiring finer control over the API usage.



CLI
---

.. click:: parble.commands:parble
    :prog: parble
    :nested: full


SDK
---


.. autoclass:: parble.ParbleSDK
    :members:
    :inherited-members:


Client
------


.. autoclass:: parble.ParbleAPIClient
    :members:
    :inherited-members:


Models
------

.. automodule:: parble.models
    :members:



Session
-------

.. autoclass:: parble.session.BaseSession
    :members:
