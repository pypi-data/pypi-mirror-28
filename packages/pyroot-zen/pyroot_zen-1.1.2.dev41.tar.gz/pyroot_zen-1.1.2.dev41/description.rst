 
==============
``pyroot-zen``
==============

As the Zen of Python said: **Readability counts**.

``pyroot_zen`` is a wrapper around ``PyROOT`` with better syntax simplification. By design, it does NOT introduce any new APIs, in order to make its usage more intuitive, as well as being compatible with other packages.

To use, you need only one line::

    >> import pyroot_zen

where all objects in ``ROOT`` namespace are now patched.

Features at a glance:

- Pythonic property instead of Getter/Setter.
    - e.g., ``hist.xaxis.title = "mass"`` instead of ``hist.GetAxis().SetTitle("mass")``
- Automatic (awkward ``C++`` to ``python``) arguments conversion.
    - e.g., ``ROOT.TPolyLine(3, [1,2,3], [1,4,9])`` without using ``array``.
- Pythonic iterable as expected.

How does it work? Basically intercepting ``__getattr__, __getattribute__, __init__`` call where necessary.

Tested with: ROOT 6.08.06 (OSX homebrew), python 2.7.13, pytest 3.1.1.

Relationship with other packages
--------------------------------

- ``ROOT``: This is required to be installed by the user, and ``PyROOT`` should also be available.

- ``RooStats``: If this is installed, the features will also be available automatically.

- ``rootpy``: While on the surface it looks like they share a lot of similarity, the 2 packages usages are very different: ``rootpy`` requires the user to use the new classes/functions from its namespace to benefit from its functionality, whereas ``pyroot_zen`` injects the functionality into objects in ``PyROOT`` directly, and focusing only on syntaxes reduction.
