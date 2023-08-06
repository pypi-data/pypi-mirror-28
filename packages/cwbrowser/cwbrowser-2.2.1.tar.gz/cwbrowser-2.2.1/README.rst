=========
CWBrowser
=========

Summary
=======

This Python package allows remote quering to a CubicWeb instance that inherit the RQL DOWNLOAD cube features.
This cube allows to setup a SFTP service on the server hosting your database. Thus, all query results are accessible (we use the python_fuse_ package or Twisted_ to build the filesystem) through a predefinite SFTP repository. Users can then access and download their data using the SFTP protocol.
Check `this link <https://neurospin.github.io/rql_download/>`_ for the complete
documentation.

