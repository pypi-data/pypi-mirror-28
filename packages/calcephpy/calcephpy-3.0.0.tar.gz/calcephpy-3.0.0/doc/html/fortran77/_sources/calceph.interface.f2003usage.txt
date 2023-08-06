All declarations needed to use |LIBRARYNAME| are collected in the module files :file:`calceph.mod`.  The library is designed to work with Fortran compilers compliant with the Fortran 2003 standard. All declarations use the standard **ISO_C_BINDING** module.

You should include that module in any program using the |LIBRARYSHORTNAME| library:

::

    use calceph


When a fortran string is given as a parameter to a function of this library, you should append this string with **//C_NULL_CHAR** because the C library works only with C string.
   
.. highlight::  bash

Compilation on a Unix-like system
---------------------------------
 
 
 All programs using  |LIBRARYSHORTNAME| must link against the :file:`libcalceph` library.  On Unix-like system this can be done with *-lcalceph*, for example

    ::
  
        gfortran -I/usr/local/include myprogram.f -o myprogram -lcalceph 


 If  |LIBRARYNAME| has been installed to a non-standard location then it may be necessary to use *-I* and *-L* compiler options to point to the right directories, and some sort of run-time path for a shared library.

Compilation on a Windows system
-------------------------------

 All programs using |LIBRARYSHORTNAME| must link against the :file:`libcalceph.lib`.  On Windows system this can be done with *libcalceph.lib*, for example

    ::

        gfortran.exe /out:myprogram.exe myprogram.f libcalceph.lib 

 If  |LIBRARYNAME| has been installed to a non-standard location then it may be necessary to use */I* and */LIBPATH:* compiler options to point to the right directories.

.. highlight::  none

