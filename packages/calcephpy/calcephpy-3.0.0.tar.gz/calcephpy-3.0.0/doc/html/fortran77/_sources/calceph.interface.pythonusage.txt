It is designed to work with Python interpreters compliant with the Python 2.6 or later and Python 3.0 or later. 

All declarations needed to use |LIBRARYNAME| are collected in the module :file:`calcephpy`.
You should import this module:

    ::
    
        from calcephpy import *


If you receive the following message ``ImportError: No module named calcephpy`` and if the configuration option *enable-python-package-system* and *enable-python-package-user* was not set, the environment variable *PYTHONPATH* should be set to the right location of the |LIBRARYSHORTNAME| python package  ( e.g., PYTHONPATH=/usr/local/lib64/python3.4/site-packages/:$PYTHONPATH ) in your shell initialization file (e.g.,  ~/.bash_login or  ~/.profile), in order that the python interpreter finds the |LIBRARYSHORTNAME| python package. 

Relative to C or Fortran interface, the prefixes  *calceph_*, *CALCEPH_*, *NAIFID_* are deleted for the naming convention of the functions, constants and NAIF identification numbers.  
