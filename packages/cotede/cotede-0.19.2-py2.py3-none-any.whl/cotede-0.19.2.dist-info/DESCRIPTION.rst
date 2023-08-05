=============
CoTe De l'eau
=============

.. image:: https://zenodo.org/badge/10284681.svg
   :target: https://zenodo.org/badge/latestdoi/10284681

.. image:: https://readthedocs.org/projects/cotede/badge/?version=latest
   :target: https://readthedocs.org/projects/cotede/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/travis/castelao/CoTeDe.svg
        :target: https://travis-ci.org/castelao/CoTeDe

.. image:: https://codecov.io/gh/castelao/CoTeDe/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/castelao/CoTeDe

.. image:: https://img.shields.io/pypi/v/cotede.svg
        :target: https://pypi.python.org/pypi/cotede


`CoTeDe<http://cotede.castelao.net>`_ is an Open Source Python package to quality control (QC) hydrographic data such as temperature and salinity. 
It was designed to attend individual scientists as well as operational systems with large databases, reading the inputs from different formats and types of sensors, and processing those in parallel for high performance. 
To achieve that, CoTeDe is highly customizable, allowing the user to compose the desired set of tests, as well as the specific parameters of each test. 
Otherwise there are preset QC procedures conforming with GTSPP, EuroGOOS and ARGO recommendations. 
It is also implemented innovating approaches to QC like the Fuzzy Logic (Timms 2011, Morello 2014) and Anomaly Detection (Castelão 2015). 

At this point it is operational for profiles (CTD, XBT and Argo) and tracks (TSG). 
For CTD profiles and TSG time series it uses `PySeabird package <http://seabird.castelao.net>`_ to interpret directly the SeaBird's .cnv output file, and for argo it uses `PyARGO package <https://github.com/castelao/pyARGO>`_ to interpret the netCDF files.

This is the result from several generations of quality control systems,
which started in 2006, when I developed from scratch an automatic quality 
control system for realtime evaluation of thermosalinographs at AOML-NOAA, USA. 
Later I was advising the quality control of the brazilian hydrography of PIRATA.

My vision is that we can do better than we do today with more flexible classification techniques, which includes machine learning, to minimize the burden on manual expert QC improving the consistency, performance and reliability of the QC procedure for oceanographic data, especially for realtime operations.

Why use CoTeDe
--------------

CoTeDe can apply different quality control procedures:
  - The default GTSPP, EGOOS or Argo procedures;
  - A custom set of tests, including user defined thresholds;
  - A novel approach based on Anomaly Detection, described by `Castelao 2015 <http://arxiv.org/abs/1503.02714>`_;
  - Two different fuzzy logic approaches: as proposed by Timms 2011 & Morello 2014, and using usual defuzification by the bisector.

Process multiple files in parallel, ideal for large datasets.

Export output, original data plus flags, into netCDF files following OCEANSites data structure.

Quick howto
-----------

To evaluate the records of a profile:

        import cotede.qc

        pqc = cotede.qc.fProfileQC('example.cnv')

To see the temperature records of the primary sensor:

        pqc['temperature']

To see the flags of all tests applied on the secondary sensor of salinity:

        pqc.flags['salinity2']

To evaluate a full set of profiles at once, like all profiles from a cruise, use the class ProfileQCCollection, like:

        dataset = ProfileQCCollection('/path/to/data/', inputpattern=".*\.cnv")

        dataset.flags['temperature'].keys()

Check the notebooks gallery for more examples and functionalities: http://nbviewer.ipython.org/github/castelao/CoTeDe/tree/master/docs/notebooks/

Documentation
-------------

http://cotede.readthedocs.org




History
=======

0.17 - Mar, 2016
----------------

* Implementing fuzzy procedures inside CoTeDe, thus removing dependency on scikit-fuzzy. scikit-fuzzy is broken, hence compromising tests and development of CoTeDe.

0.16 - Mar, 2016
----------------

* Using external package OceansDB to handle climatologies and bathymetry.

0.15 - Dec, 2015
----------------

* Moved procedures to handle climatology to external standalone packages.

0.14 - Aug, 2015
----------------

* Interface for human calibration of anomaly detection
* Implemented fuzzy logic criteria

0.13 - July, 2015
-----------------

* Major improvements in the anomaly detection submodule
* Partial support to thermosalinographs (TSG)
* Working on WOA test to generalize for profiles and tracks
* Adding .json to default QC configuration filenames
* Moved load_cfg from qc to utils

0.12
----

Since 0.9 some of the most important changes.

* Following CF vocabulary for variables names (PRES, TEMP, PSAL...)
* Partial support to ARGO profiles
* Added density invertion test
* Included haversine to avoid dependency on MAUD.
* tox and travis support.

0.9 - Dec, 2013
---------------

* Going public

0.7.3
-----

* Creating fProfileQC()

0.5.4 - Nov, 2013
-----------------

* Including Tukey53H test

0.5.0
-----

* Implemented ProfileQCCollection

0.4 - Sep, 2013
---------------

* gradient and spike tests with depth conditional thresholds
* CruiseQC
* Use default threshold values for the QC tests.

0.1 - May 24, 2013
------------------

* Initial release.

QC_ML - 2011
------------

* QC_ML, a machine learning approach to quality control hydrographic data, the initial prototype of CoTeDe. I refactored the system I developed to quality control TSG, to evaluate the PIRATA's CTD stations for INPE. At this point I migrated from my personal Subversion server to Bitbucket, and I lost the history and logs before this point.

2006
----

* A system to automaticaly quality control TSG data on realtime for AOML-NOAA. The data was handled in a PostgreSQL database, and only the traditional tests were applied, i.e. a sequence of binary tests (spike, gradient, valid position ...).


