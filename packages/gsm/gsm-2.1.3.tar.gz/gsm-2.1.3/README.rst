The Global Sky Model
====================


The Global Sky Model (GSM) contains all sources from the VLSS, TGSS, WENSS (main and polar)
and NVSS survey catalogs. 
For the LOFAR BBS calibration pipeline these tools can be used to create a sky model 
catalog file in ``makesourcedb`` format.
The ``gsm.py`` script
extracts sources in a cone of a given radius around a given position 
on the sky from the Global Sky Model database.

Run gsm
-------

Install the required packages. Best is to run the script in 
virtual env.

If you want to run your own GSM database (locally), you can get the 
catalog ``csv`` files from `here`_. 
Copy ``template_config.cfg`` to ``config.cfg``
and fill in the database parameters, either for the local or remote 
GSM database.

The python wrapper script ``gsm.py`` can be used to generate a catalog file 
in ``makesourcedb`` format and can be run as:

``python gsm.py [-p patchname] basecat outfile RA DEC radius [vlssFluxCutoff [assocTheta]]``

Note that since the last version we introduced the ``basecat`` argument. This allows
you to set either VLSS or TGSS as the base catalogue for which counterparts will
be searched in the other catalogues.

Documentation
-------------

See the `LOFAR Imaging Cookbook`_ for more information.

.. _LOFAR Imaging Cookbook: https://support.astron.nl/LOFARImagingCookbook/
.. _here: https://homepages.cwi.nl/~bscheers/gsm/

