specguiutils is a python library that provides gui elements that display scan information from a SPEC file, and allows the user
to pick a particular scan or scans and then display/process information about that scan.  Note that this library uses spec2nexus
 reader (https://pypi.python.org/pypi/spec2nexus) to read and parse the spec file.

Version 0.0.1 
	Started 5/12/2017
	
Version 0.1    10/2/2017
More work to get this up and running for the first distribution.

Version 0.2   2017-10-02
  - Change comments saying pyqt4 to pyqt5 
  
Version 0.3   2017-10-02
  - Change requirement for pyqt from pyqt5 to pyqt
  
Version 0.4   2017-10-02
  - Remove requirement for pyqt from setup.py.  It is not available through pip.
    If using anaconda, user will need to do conda install.  Still cannot leave 
    this as a requirement.  Not finding it.
    
Version 0.5 2017-10-02
   - Set ScanBrowser Table so that it is not editable
   
Version 0.6.3 
    - Add positioner selector and adding the values of positioners to 
    the ScanBrowser so that users can see more details about the scans.
    
    
Version 0.6.4
    - Code cleanup removing unused variables and imports
    - Remove Empty item when the ScanBrowser is initialized.
    - Remove the row number from the scan browser.  This is confusing 
    when combined with the scan number.
    
Version 0.6.5  2018-01-08
    - Add code to PositionSelector and ScanBrowser to allow selecting 
    user parameters and showing them in the scanBrowser
    
Version 0.7 2018-01-14
    - combine all the 0.6.x to make final 0.7 rev.
    - Also removed a catch of the error in a place that it is not used.