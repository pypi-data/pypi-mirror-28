It is designed to work with Fortran compilers compliant with the Fortran 77, 90 or 95 standard with wrappers. All declarations are implicit, so you should take care about the types of the arguments. All functions are prefixed by **f90**. This interface is only provided as compatibility layer and have a small overhead due to the wrappers. So if you have a fortran compiler compliant with 2003  standard, you should use the fortran 2003 interface of this library.

All declarations needed to use |LIBRARYNAME| are collected in the header file :file:`f90calceph.h`.  It is designed to work with Fortran compilers compliant with the Fortran 77 , 90 or 95 standard. 

You should include that file in every subroutine or function in any program using the |LIBRARYSHORTNAME| library:

    ::

        include 'f90calceph.h'


.. highlight::  bash

 
Compilation on a Unix-like system
---------------------------------
 
 All programs using  |LIBRARYSHORTNAME| must link against the :file:`libcalceph` library.  On Unix-like system this can be done with *-lcalceph*, for example


    ::
    
        gfortran -I/usr/local/include myprogram.f -o myprogram  -lcalceph 

 If  |LIBRARYNAME| has been installed to a non-standard location then it may be necessary to use *-I* and *-L* compiler options to point to the right directories, and some sort of run-time path for a shared library.

Compilation on a Windows system
---------------------------------
 
 All programs using |LIBRARYSHORTNAME| must link against the :file:`libcalceph.lib`.  On Windows system this can be done with *libcalceph.lib*, for example

    ::
    
        gfortran.exe /out:myprogram.exe myprogram.f libcalceph.lib 

 If  |LIBRARYNAME| has been installed to a non-standard location then it may be necessary to use */I* and */LIBPATH:* compiler options to point to the right directories.

.. highlight::  none

