=====
thLib
=====

*thLib* contains functions for working with sound, and for fitting circles,
lines, sine-waves, and exponential decays. For signal processing, a
Savitzky-Golay filter is included, as well as a demonstration of the
calculation of a power spectrum. UI utilities, and a few useful vector
functions (e.g. an implementation of the Savitzky-Golay algorithm) round off
*thLib*.

**Note:** All functions for working with 3D kinematics have been moved into
the new package "scikit-kinematics"!
(http://work.thaslwanter.at/skinematics/html)

Compatible with Python 2 and 3.

Dependencies
------------
numpy, scipy, matplotlib, pandas, statsmodels, skimage, sympy

Homepage
--------
http://work.thaslwanter.at/thLib/html/

Author:  Thomas Haslwanter
Date:    09-02-2018
Ver:     0.12.2
Licence: BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause)
        Copyright (c) 2018, Thomas Haslwanter
        All rights reserved.

Installation
------------
You can install thlib with

    pip install thLib

and upgrade to a new version with

    pip install thLib -U

Fits
====

Functions
---------

- fits.demo_ransac ... RANSAC fit of best circle in image
- fits.fit_circle ... basic circle fit
- fits.fit_exp ... exponential fit
- fits.fit_line ... linear regression fit, complete with confidence intervals for mean and values, and with plotting
- fits.fit_sin ... sine fit
- fits.fit_ellipse ... ellipse fit (Taubin's method)
- fits.regress ... multilinear regression fit, similar to MATLAB
    
Signal Processing Utilities
===========================

- signals.pSpect ... simple power spectrum from FFT
- signals.savgol ... Savitzky-Golay filter


GUI Utilities
=============

- ui.getfile ... GUI for selecting an existing file
- ui.getdir ... GUI for selecting a directory
- ui.listbox ... GUI for item selection
- ui.progressbar ... Show a progressbar, for longer loops
- ui.savefile ... GUI for saving a file
- ui.get_screensize ... width and height of screen
