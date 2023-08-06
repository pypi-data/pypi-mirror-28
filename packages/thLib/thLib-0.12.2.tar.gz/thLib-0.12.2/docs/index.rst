thLib - Documentation
=====================

*thLib* is a library for scientific data analysis.

It is hosted under https://pypi.python.org/pypi/thLib, and contains the following modules:

*fits*  Contains examples for a number of fitting applications, for fitting
    - lines
    - circles (with RANSAC, or directly)
    - exponential decays
    - sine waves
    - ellipses
    - regressions (including confidence intervals)

*signals*  Has functions that manipulate data
    - a Savitzky-Golay for data smoothing and derivatives
    - a power spectrum
    - a function to calculate and show mean and standard error for
      time series data.
    - a visualization for cross- and auto-correlations

*ui*  Provides GUIs for
    - file- and directory selection, and for saving files
    - a listbox (item selection from a list)
    - a progress bar
    - a waitbar

Installation
------------

The simplest way to install thLib is

>>> pip install thLib

For upgrading to the latest version, you have to type

>>> pip install thLib -U

Dependencies
^^^^^^^^^^^^
numpy, scipy, matplotlib, pandas, statsmodels, skimage


Notes
-----

The functionality to work with sound-files has been moved to *scikit-sound*
(http://work.thaslwanter.at/sksound/html/)

Modules relating to

    - *quaternions*
    - *rotation matrices*
    - *vectors*
    - *IMUs*
    - *Marker-based recording systems*
    - *3d data viewers*

have been moved into *scikit-kinematics* (http://work.thaslwanter.at/skinematics/html/)

Modules
-------

.. toctree::
   :maxdepth: 2

   fits
   signals
   ui


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. note::
    | *Author:*     Thomas Haslwanter
    | *Version:*    0.12.2
    | *Date:*       Feb-2018
    | *email:*      thomas.haslwanter@fh-linz.at
    | *Copyright (c):*      2018, Thomas Haslwanter. All rights reserved.
    | *Licence:*    This work is licensed under the `BSD 2-Clause License <http://opensource.org/licenses/BSD-2-Clause>`_

.. image:: _static/cc_licence.png
   :scale: 100 %

