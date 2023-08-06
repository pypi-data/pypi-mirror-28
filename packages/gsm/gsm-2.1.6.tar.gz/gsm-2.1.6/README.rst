The Global Sky Model
====================


The Global Sky Model (GSM) is generated from a database that 
contains all sources from the VLSS, TGSS, WENSS (main and polar)
and NVSS survey catalogs. 
For the LOFAR calibration pipeline(s) these tools can be used to create a sky model 
catalog file in ``makesourcedb`` format.
The ``gsm`` script extracts sources in a cone of a given radius around a given position 
on the sky from the Global Sky Model database, 
cross-matches these sources, fits the spectral index, curvature and
higher-order terms. Then it writes the results to a plain text ``makesourcedb`` file,
that can be used by other programs.


GSM Database
------------

The GSM relies on the `MonetDB database system`_. 
If you want to run it yourself you have to install it 
and get the catalog ``csv`` files from `here`_.
With the ``setup.db.batch`` script you can create
the database, schema, tables, functions and load the data.
Copy ``template_dbconfig.cfg`` somewhere to ``dbconfig.cfg``
and specify the database parameters.
Note that you can also specify a remote GSM database.
Provide it to the ``gsm`` script by setting the 
``--dbconf relpath/to/dbconfig.cfg`` option.
Default, it checks for the dbconfiguration file
in the working directory.

Run ``gsm.py``
--------------

The gsm-parameters configuration file needs to be copied
from ``template_conf.cfg`` somewhere to ``config.cfg``. 
Here you specify the parameters like central ra and dec, 
fov radius, etc.
Default ``gsm.py`` will
look for the file in the working diectory. Otherwise
it should be specified by the option ``--conf relpath/to/config.cfg``.

The python wrapper script ``gsm.py`` can be used to generate a 
Global Sky Model file 
in ``makesourcedb`` format and can be run as:

``python gsm.py [-h] [-d dbconfig.cfg] [-c config.cfg] [--version]``

Note that since the last version we introduced the ``basecat`` argument. This 
can be set in the gsm-parameters config file to 
either VLSS or TGSS as the base catalogue for which counterparts will
be searched in the other catalogues.

``pip install gsm`` and run the ``gsm`` script
----------------------------------------------

In your virtualenv you can ``pip install gsm`` and then simply use
the ``bin/gsm`` script to run the GSM from the command line:

``gsm [-d dbconfig] [-c config] [-v version] [-h help]``

Documentation
-------------

See the `LOFAR Imaging Cookbook`_ for more information.

.. _MonetDB database system: https://www.monetdb.org
.. _here: https://homepages.cwi.nl/~bscheers/gsm/
.. _LOFAR Imaging Cookbook: https://support.astron.nl/LOFARImagingCookbook/

