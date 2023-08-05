.. _reference:

+++++++++
Reference
+++++++++

This is the mujpy Reference Manual

------
Header
------
The top part of the mujpy gui contains a logo together with the information on the loaded run (in `single run mode`_) or the master loaded run (in the `suite mode`_). The information contains the run number, the run title, the total conuts, the total counts over the selected `grouping`_ of detectors.

----
Tabs
----
The lower part of the gui is divided in tabs: `setup`_, `suite`_, `fit`_, `output`_, `fft`_, `plots`_, `about`_.
Click on the tab to see its content and methods, activated by widget controls (buttons, checkboxes, input text field, etc.)

-----
setup
-----
The setup tab contains preliminary information and fields in three boxes. 

.. image:: setup.png

The first box contains paths on the right: 

* the data path (the folder where the data files are stored), 
* the temperature log path (optional), 
* the log path (the folder where log files will be saved). 

On the left the two strings that compose the data file name, e.g. for stardard filename ``deltat_tdc_gps_0432.bin``

* *fileprefix* is ``deltat_tdc_gps_``
* *extension* is `bin`
* the run number is ``433``

The working directory (wd), i.e. the path from which the jupyter notebook is lauched is saved automatically. 

The second box is related to the :math:`t_0=0` bin iminuit fit, minimizing the :math:`\chi^2` of the initial data slice and the best fit function  `muprompt`_.

* *prepeak*  and *postpeak* are the peak interval span (the number of bins) respectively before and after the maximum;
* the *prompt plot* checkbox to produce a plot; 
* the *prompt fit* button launches iminuit
* the *save setup* and *load setup* buttons save and load a setup file that stores the setup information in/from the  ``mujpy_setup.pkl`` file
* click on the *t0 bins and remainders* and *Total counnte* accordions to show individual counter values

muprompt
--------

.. math::

     \frac {A_1} {\sqrt{2\pi\sigma}}  \exp\left[-\frac 1 2 \left(\frac{t-t_0} \sigma\right)^2\right] + A_0 +\frac {A_2} 2 \left[1+\mathrm{erf} \left(\frac{t-t_0} {\sqrt 2 \sigma}\right)\right]


-----
suite
-----
The suite tab is the data load interface.

.. image:: suite_single.png

* *Run[run suite]* is a Text area where single run numbers can be written. The data file is loaded upon hitting return
* more complex syntax allows storing suites of runs, with any combination of *,:+*

 * ``432,433`` loads the suite of runs 432, 433
 * ``432:434`` loads the suite of runs 432, 433, 434
 * ``432,433, 435:437`` loads the suite of runs 432, 433, 435, 436, 437
 * ``432+433`` loads the sum of these two runs as a single run, etc.
 
If a single run is loaded 

* *Next run* displays the next run number, if the file exists
* *Load nxt* loads it
* *Load prv* loads the previous, if it exists
* *Add nxt* adds next run
* *Add prv* adds the previous, if it exists


single run mode
---------------
Individual data set are fitted to models

suite mode
----------
Individual data set are fitted to the model (defined in `fit`_) in sequence, according to the loaded run suite.

Run-specific guess values can be selected with the following syntax (see first the `fit`_ description):

* if the parameter symbol is ``l`` and the function Text area contains ``0.2*3, 2.0*2, 20.0`` for the first three runs in the suite this parameter will receive guess value 0.2, for the next two guess value 2.0, and for any remaining run guess value 20.0


---
fit
---
The fit tab selects the fit model and its parameters.

.. image:: daml.png

The top box selects the model and conditions, such as

.. _grouping:

grouping
--------
the set of conters that form the Forward and Backward detectors, and

alpha
-----
the ratio of count rates between Backward and Forward grouping.

* The *Load* button opens a file selection widget for the ``pkl`` files containing fit results. Loading one such file  reproduces the input for obtaining again the same fit.
* *Guess* checkbox, for ploting initial conditions instead of fit results.
* *alpha* Float Text input, see above
* *version* Integer, distinguishes fits of the same model, to allow for different parameter relations (fixed/variable/global/functions).
* *Plot* button, produces a plot with either best fit or guess values.
* *forward*, *backward* text area define the grouping, defining groups of counters according to the following syntax

 * ``2,3`` or ``2:3`` menas that counters 2,3 are grouped together
 * ``1:5, 10, 15:19`` means that counters 1,2,3,4,5,10,15,16,17,18,19 are grouped together

* *plot range* 

 * *start, stop* to plot data between *start* and *stop* bin, with no rebinning
 * *start,stop,pack* to plot data between *start* and *stop* bin, rebinned by factor *pack*
 * *start,stop,late,pack* to plot ata in two successive ranges, between *start* and *stop* bin, with no rebinning, between *stop* and *last*  bin, rebinned by factor *pack*
 * *start,stop,packe,late,packl* to plot data in two successive ranges, between *start* and *stop*,  rebinned by factor *packe*, between *stop* and *last* rebinned by factor *packl*
 * see also `graphic zoom`_



* *fit range* has only the *start, stop* and  *start,stop,pack* options, to define the interval and packing for the fdata minimization. 

* *Update* button, to transfer best fit values to parameter guess values
* *loadmodel* Text area, to define new model: e.g. ```blmgmg`` is a three component model, ``bl``, ``mg``, ``mg``
* *offset* is the first good bin, counting from the center prompt peak  (*start* = k means that the fit starts from  bin *offest* + k.
* *Fit* button launches iminuit migrad minimization of the model.
* *Animate* checkbutton, if selected the suite of runs is plotted as frames of an animation, if unselected they are tiled with an offset in a single multirun plot.
* *Delay* between frames [ms].   
 
The lower frame contains the fit components selected either by the *loadmodel* syntax or by loding a saved fit. The frame is divided in components boxes, whose first line is the component label and the :ref:`FFT-checKbox`. The other lines list their parameters, each indentified by an index, a unique name, a Text area for the starting guess value, a symbol:

 - *~*    free minuit parameter, 
 - *!*    fixed parameter 
 - *=*    the function text area on the right is activated. You can input symple expressions, such as ``p[1]``, implying that the present parameter and parameter 1 share the same value. For instance two *ml* components in model *damlml* could share their phase parameters. Slightly more complex functions may be written, such as ``p[2]-p[3]``, or ``p[0]*exp(p[2]/p[3])``, etc.

* parameter names are automatically generated and pretty obvious if you are not new to MuSR. E.g. *ml* has a (partial) *asymmetry*, a *field* value (in Tesla), a *phase* (in degrees) and a Lorentzian relaxation *Lor_rate* (in inverse microseconds); 
* names are followed by a capital letter that uniquely identifies each component (e.g. in a *blmlml* fit the asymmetries of the three components would be *asymmetryA*, *asymmetryB*, *asymmetryC*, respectively) 


.. _static:

Static component list
---------------------

A few constants are defined: :math:`\pi`, the muon gyromagnetic ratio, :math:`\gamma_\mu`, the electron gyromagnetic ratio, :math:`\gamma_e`

* **bl**, Lorentz decay: 

  * asymmetry :math:`A`
  * Lor_rate (:math:`\mu s^{-1}`) :math:`\lambda`
    
.. math:: A\exp(-\lambda t)  

* **bg**, Gauss decay: 

  * asymmetry :math:`A`
  * Gau_rate (:math:`\mu s^{-1}`) :math:`\sigma`

.. math:: A\exp\left(-\frac {\sigma^2 t^2} 2\right)

* **bs**, Stretched exponential decay: 
 
  * asymmetry :math:`A`
  * rate (:math:`\mu s^{-1}`) :math:`\lambda`
  * beta :math:`\beta`

.. math:: A \exp \left(-(\lambda t)^\beta \right)

* **da**, Linearized dalpha correction. If :math:`f_0` is the uncorrected, :math:`f` the corrected fitting function and :math:`\alpha` the `alpha`_ ratio:

  * dalpha :math:`d\alpha` the linear correction

.. math:: f = \frac{2f_0(1+\frac \alpha{d\alpha})-1}{1-f_0+2\frac \alpha {d\alpha}}

* **mg**, Gauss decay cosine precession: 

  * asymmetry :math:`A`
  * field (T) :math:`B`
  * phase (degrees) :math:`\phi`
  * Gau_rate (:math:`\mu s^{-1}`) :math:`\sigma`
  

.. math:: A\cos(\gamma_\mu B t + \frac{2\pi}{360}\phi)\,\exp\left(-\frac {\sigma^2 t^2} 2\right)


* **ml**, Lorentz decay cosine precession: 

  * asymmetry :math:`A`
  * field (T) :math:`B`
  * phase (degrees) :math:`\phi`
  * Lor_rate (:math:`\mu s^{-1}`) :math:`\lambda`

.. math:: A\cos(\gamma_\mu B t + \frac{2\pi}{360}\phi)\,\exp(-\lambda t )

* **ms**, Stretched exponential decay cosine precession: 

  * asymmetry :math:`A`
  * field (T) :math:`B`
  * phase (degrees) :math:`\phi`
  * rate (:math:`\mu s^{-1}`) :math:`\lambda`

.. math:: A\cos(\gamma_\mu B t +\frac{2\pi}{360}\phi)\,\exp \left(-(\lambda t)^\beta \right)

* **jg**, Gauss decay Bessel precession 

  * asymmetry :math:`A`
  * field (T) :math:`B`
  * phase (degrees) :math:`\phi`
  * Gau_rate (:math:`\mu s^{-1}`) :math:`\sigma`


.. math:: A j_0 (\gamma_\mu B t  +\frac{2\pi}{360}\phi)\,\exp\left(-\frac {\sigma^2 t^2} 2\right)

* **jl**, Lorentz decay Bessel  precession 

  * asymmetry :math:`A`
  * field (T) :math:`B`
  * phase (degrees) :math:`\phi`
  * Lor_rate (:math:`\mu s^{-1}`) :math:`\lambda`

.. math:: A j_0 (\gamma_\mu B t  +\frac{2\pi}{360}\phi)\,\exp\left(-\lambda t )

* **fm**, FMuF coherent evolution: 

  * asymmetry :math:`A`
  * dipolar field (T) :math:`B_d`
  * Lor_rate (:math:`\mu s^{-1}`) :math:`\lambda`

.. math:: A\,\exp(-\lambda\,t)[\frac 1 2+\frac 1 6 \cos \gamma_\mu B_d \sqrt{3}\, t + \frac{1-\frac 1 {\sqrt{3}}} 6 \cos \gamma_\mu B_d\frac {3-\frac 1\sqrt{3}}2\,t + \frac{1+\frac 1 {\sqrt{3}} 6b\cos\gamma_\mu B_d (3+\sqrt{3})\,t ]

* **kg**, Gauss Kubo-Toyabe: static and dynamic, in zero or longitudinal field by `G. Allodi Phys Scr 89, 115201 <https://arxiv.org/abs/1404.1216>`_


------
output
------
This tab displays iminuit output, warnings, error messages, command execution completions.

---
fft
---
This tab enables FFt analysis.

.. image:: fft.png

* *Do FFT*, execute the Fast Fourier Transform an plot it.
* *Filter* apodization filter width :math:`\lambda`, in inverse microsecond; the filter is hypergaussian, :math:`\exp(-((t-t_0)\lambda)^3)`
* *FFT range*, dplotted frequency interval (in MHz)
* *Real part/Power* dropdown
* *Residues/Asymmetry* dropdown
* *Autophase* checkbox, selects ACME autophase algorithm by `Chen Li et al. Journal of Magnetic Resonance 158 (2002) 164-168 <http://wiki.icmc.usp.br/images/8/8c/Acme.pdf>`_ implemented as in `NMRglue <https://github.com/jjhelmus/nmrglue>`_
* *Animate* checkbox, if checked selects that run suites are displayed as frames in animation, otherwise they are tiledas multiplot, with an offset.
* *Delay* between frames [ms].
* *start/stop* the animation, if selected.

.. _FFT-checkbox:

FFT checkbox
------------
Selects subtracted components for the FFT. E.g. assume best fit model ``blmgmg`` with the first two components checked and the last unchecked. The FFT of Residues will show the Fast Fourier Transform of the data *minus* the model function for the first two components. 


-----
plots
-----
This tab has two rows. The first is for Multiplot of run suites. The second is for Counter inspection.

.. image:: plots.png

Multiplot
---------

* The *Multiplot* button produces the asymmetry plot of a suite of runs.
* The *Animate* checkbox, select to produce one frame per run.
* The *Delay (ms)* Integer Text area, determines the delay between frames (effective after pushing again the *Multiplot* button).
* The *start/stop* button toggles the animation
* The *plot range* Text area is for changing start, stop [,pack] bins; the numbers will be considered as integers. When a new run suite is loaded it automatically offers a range centered around the prompt peak. For zooming, see also the `graphic zoom`_
* The *offset* is a factor that determines the y offset :math:`\Delta y` between run asymmetries, in tile mode, according to the formula :math:`\Delta y = \text{offset}\cdot \max(f)`, where :math:`\max(f)` is the global maximum of the fit function (over all displayed runs)  
* *run T(eT)* is an accordion: click on it and it will display the run temperatures, as recorded in the header (averages over the run duration).


Counter inspection
------------------

* The *Counter* button produces the plot.
* The next label reminds how many are the available counters.
* The *counters* Text area allows the selection of the displayed detectors. The syntax is the same as for `grouping`_. It is advisable not to display more than 16 detetcors at a time
* *bin*, text area to select *start*, *stop*, the same range for all chosen detectors. Zoom also by the the `graphic zoom`_
* *run* dropdown selects one run at a time among the loaded suite.

graphic zoom
------------
All graphic windows display seven icons on the bottom bar

* The |save| icon, far right, opens a dialogue for sabìving the plot.
* The |center| icon, next one to the left, corrects the axes position
* the |zoom| icon, allows zooming in.
* The first icon on the left, |home|, resets the zoom to the orginal ranges

-----
about
-----
A few infos and acknowledgements

.. |save| image:: save-icon.png
.. |center| image:: center-icon.png
.. |zoom| image:: zoom-icon.png
.. |home| image:: home-icon.png
