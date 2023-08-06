===========
 writefile
===========

Write stdin to a given path, creating directories as necessary.

Examples
========

.. code:: bash

   $ echo 'Hello World!' | writefile greeting.txt

This is similar to a ubiquitous shell idiom:

.. code:: bash

   $ echo 'Hello World!' > greeting.txt

However, ``writefile`` is convenient in various cases, such as:

Creating Intermediate Directories
---------------------------------

.. code:: bash

   $ echo 'Hello World!' | writefile ./intermediate/directories/created/as/necessary/greeting.txt

With sudo
---------

Generate contents with an unprivileged process, but write to a root-owned file:

.. code:: bash

   $ do-unprivileged-thing-to-generate-contents | sudo writefile root-owned-path

With ssh
--------

Generate contents locally and write to a remote file:

.. code:: bash

   $ generate-local-data | ssh myhost writefile







