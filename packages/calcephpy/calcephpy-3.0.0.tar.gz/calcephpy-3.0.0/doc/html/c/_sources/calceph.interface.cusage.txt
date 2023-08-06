All declarations needed to use |LIBRARYNAME| are collected in the include file
:file:`calceph.h`.  It is designed to work with both C and C++ compilers.

You should include that file in any program using the |LIBRARYSHORTNAME| library:

::

    #include <calceph.h>


.. highlight::  bash

Compilation on a Unix-like system
---------------------------------
 
All programs using  |LIBRARYSHORTNAME| must link against the :file:`libcalceph` library.  On Unix-like system this can be done with *-lcalceph*, for example

    
    ::
   
        gcc myprogram.c -o myprogram -lcalceph 
     

If  |LIBRARYNAME| has been installed to a non-standard location then it may be necessary to use *-I* and *-L* compiler options to point to the right directories, and some sort of run-time path for a shared library.

Compilation on a Windows system
-------------------------------
 
* Using the Windows SDK

 All programs using |LIBRARYSHORTNAME| must link against the :file:`libcalceph.lib`.  On Windows system this can be done with *libcalceph.lib*, for example

    ::
    
        cl.exe /out:myprogram myprogram.c libcalceph.lib 


 If  |LIBRARYNAME| has been installed to a non-standard location then it may be necessary to use */I* and */LIBPATH:* compiler options to point to the right directories.

* Using the MinGW
 
 All programs using  |LIBRARYSHORTNAME| must link against the :file:`libcalceph` library.  On the MinGW system, this can be done with *-lcalceph*, for example

    ::
    
        gcc.exe myprogram.c -o myprogram -lcalceph 

 If  |LIBRARYNAME| has been installed to a non-standard location then it may be necessary to use *-I* and *-L* compiler options to point to the right directories, and some sort of run-time path for a shared library.

.. highlight::  none

