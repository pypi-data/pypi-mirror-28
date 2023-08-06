Installation
************

Quick instructions for installing on a Unix-like system (Linux, Mac OS X, BSD, cygwin, ...)
==============================================================================================

Here are the quick steps needed to install the library on Unix systems. 
In the following instructions, you must replace */home/mylogin/mydir* by the directory location where you want to install calceph.


.. highlight::  bash

.. ifconfig:: calcephapi in ('Python')

    If you use the python interface of the library and the **pip** package management system, the steps are :

        ::

            pip install calcephpy
        

    If you use the python interface of the library, the steps are :

        .. parsed-literal::

            tar xzf calceph-|version|.tar.gz
            cd calceph-|version|
            ./configure --enable-python=yes --enable-python-package-user=yes --prefix=/home/mylogin/mydir
            make check && make install


If you use the gcc and gfortran compilers, the steps are :

    .. parsed-literal::

        tar xzf calceph-|version|.tar.gz
        cd calceph-|version|
        ./configure --disable-shared CC=gcc FC=gfortran --prefix=/home/mylogin/mydir
        make check && make install
    


If you use the Intel c++ and fortran compilers, the steps are :

    .. parsed-literal::

        tar xzf calceph-|version|.tar.gz
        cd calceph-|version|
        ./configure --disable-shared CC=icc FC=ifort --prefix=/home/mylogin/mydir
        make check && make install


.. ifconfig:: calcephapi in ('C','F90','F2003')

    If you use the python interface of the library and the **pip** package management system, the steps are :

        ::

            pip install calcephpy
        

    If you use the python interface of the library, the steps are :

        .. parsed-literal::

            tar xzf calceph-|version|.tar.gz
            cd calceph-|version|
            ./configure --enable-python=yes --enable-python-package-user=yes --prefix=/home/mylogin/mydir
            make check && make install



.. highlight::  none


Detailed instructions for installing on a Unix-like system (Linux, Mac OS X, BSD, cygwin, ...)
==============================================================================================

You need a C compiler, such as gcc. A fortran compiler, compliant with the ANSI Fortran 77 specifications, is required to compile the fortran-77/90/95 interface of the library. A fortran compiler, compliant with the Fortran 2003 specifications, is required to compile the fortran-2003 interface of the library. A python interpreter, compliant at least with with the Python 2.6 or Python 3.0  specifications, is required to compile the python interface of the library.
And you need a standard Unix *make* program, plus some other standard Unix utility
programs.

Here are the detailed steps needed to install the library on Unix systems:

* tar xzf calceph-|version|.tar.gz
* cd calceph-|version|
* ./configure

    Running *configure* might take a while.  While running, it prints some
    messages telling which features it is checking for.

    *configure* recognizes the following options to control how it
    operates.

     * | --enable-fortran={yes|no}
       | Enable or disable the fortran-77 and fortran-2003 interface. The default is *yes*. 
     * | --enable-python={yes|no}
       | Enable or disable the python interface. The default is *no*.
     * | --enable-python-package-system={yes|no}
       | Enable or disable the installation of the python package to the system site-packages directory (e.g., /usr/lib/python3.4/sites-packages/) . The default is *no*.
     * | --enable-python-package-user={yes|no}
       | Enable or disable the installation of the python package to the user site-packages directory (e.g.,  ~/.local/lib/python3.4/site-packages/) . The default is *no*.
     * | --enable-thread={yes|no}
       | Enable or disable the thread-safe version of the functions |calceph_sopen| and |calceph_scompute|.  The default is *no*.
     * | --disable-shared
       | Disable shared library.
     * | --disable-static
       | Disable static library.
     * | --help
       | Print a summary of all of the options to *configure*, and exit.
     * | --prefix= *dir*
       | Use *dir* as the installation prefix.  See the command *make install* for the installation names.

    The default compilers could be changed using the variable CC for C compiler, FC for the Fortran compiler and PYTHON for the python interpreter. The default compiler flags could be changed using the variable CFLAGS for C compiler and FCFLAGS for the Fortran compiler.

    If *--enable-python=yes*, we recommend to set *--enable-python-package-user=yes* ( or *--enable-python-package-system=yes* if you have administrative right on the system directory) in order to that the python interpreter finds the |LIBRARYSHORTNAME| python package.

 * make
 
    This compiles the |LIBRARYNAME| in the working directory.

 * make check

    This will make sure that the |LIBRARYNAME| was built correctly.

    If you get error messages, please report them to |EMAIL| (see :ref:`Reporting bugs`, for information on what to include in useful bug reports).

 * make install

    This will copy the files :file:`calceph.h`, :file:`calceph.mod` and  :file:`f90calceph.h` to the directory **/usr/local/include**, the file  :file:`libcalceph.a`,  :file:`libcalceph.so` to the directory **/usr/local/lib**, and the documentations files to the directory **/usr/local/doc/calceph/** (or if you passed the *--prefix* option to *configure*, using the prefix directory given as argument to *--prefix* instead of  **/usr/local**). Note: you need write permissions on these directories.

    If the python interface is enabled and *enable-python-package-system=yes* or *enable-python-package-user=yes*, the python package will be copied to system or user python site-package.



Other *make* Targets
--------------------

    There are some other useful make targets:


    * *clean*

        Delete all object files and archive files, but not the configuration files.

    * *distclean*

        Delete all files not included in the distribution.

    * *uninstall*

        Delete all files copied by ``make install``.


Installation on Windows system
==============================

Using the Windows SDK
---------------------

You need a C compiler, such as cl.exe, and a Windows SDK. A fortran compiler, compliant with the ANSI Fortran 77 specifications, is required to compile the fortran-77/90/95 interface of the library. A fortran compiler, compliant with the Fortran 2003 specifications, is required to compile the fortran-2003 interface of the library. It has been successfully compiled with  the Windows Server 2003 R2 Platform SDK, the Windows SDK of Vista, and the Windows Server 2008 Platform SDK. 

Here are the steps needed to install the library on Windows systems:

* Expand the file calceph-|version|.tar.gz

* Execute the command ::command:`cmd.exe` from the menu *Start / Execute...*

    This will open a console window

* cd *dir*\\calceph-|version|

    Go to the directory *dir* where |LIBRARYNAME| has been expanded.

* nmake /f Makefile.vc 

    This compiles |LIBRARYNAME| in the working directory.
    This command line accepts several options :

    * CC= ``xx``

        specifies the name of the C compiler. The defaut value is *cl.exe*

    * FC= ``xx``

        specifies the name of the Fortran compiler. The defaut value is *gfortran.exe*

    * F77FUNC= ``naming``

        specifies the naming convention of the fortran 77 compiler.
        
        The possible value are: x, X, x##_ , X##_.

    * ENABLEF2003={0|1} 

        specifies if it must compile the fortran 2003 interface. The defaut value is 0.

    * ENABLEF77={0|1} 
    
        specifies if it must compile the fortran 77/90/95 interface. The defaut value is 0.

* nmake /f Makefile.vc check

    This will make sure that the |LIBRARYNAME| was built correctly.

    If you get error messages, please report them to |EMAIL| (see :ref:`Reporting bugs`, for information on what to include in useful bug reports).

    This command line accepts several options :

    * CC= ``xx``

        specifies the name of the C compiler. The defaut value is *cl.exe*

    * FC= ``xx``

        specifies the name of the Fortran compiler. The defaut value is *gfortran.exe*

    * F77FUNC= ``naming``

        specifies the naming convention of the fortran 77 compiler.
        
        The possible value are: x, X, x##_ , X##_.

    * ENABLEF2003={0|1} 

        specifies if it must compile the fortran 2003 interface. The defaut value is 0.

    * ENABLEF77={0|1} 
    
        specifies if it must compile the fortran 77/90/95 interface. The defaut value is 0.

 * nmake /f Makefile.vc  install DESTDIR= *dir*

    This will copy the file :file:`calceph.h`, :file:`calceph.mod` and :file:`f90calceph.h` to the directory **/usr/local/include**, the file :file:`libcalceph.lib` to the directory *dir* **\\lib**, the documentation files to the directory *dir* **\\doc**. Note: you need write permissions on these directories.

This command line accepts several options :

    * CC= ``xx``

        specifies the name of the C compiler. The defaut value is *cl.exe*

    * FC= ``xx``

        specifies the name of the Fortran compiler. The defaut value is *gfortran.exe*

    * F77FUNC= ``naming``

        specifies the naming convention of the fortran 77 compiler.
        
        The possible value are: x, X, x##_ , X##_.

    * ENABLEF2003={0|1} 

        specifies if it must compile the fortran 2003 interface. The defaut value is 0.

    * ENABLEF77={0|1} 
    
        specifies if it must compile the fortran 77/90/95 interface. The defaut value is 0.

Using the MinGW
---------------

You need a C compiler, such as gcc.exe. A fortran compiler, compliant with the ANSI Fortran 77 specifications, is required to compile the fortran-77/90/95 interface of the library. A fortran compiler, such as gfortran.exe, compliant with the Fortran 2003 specifications, is required to compile the fortran-2003 interface of the library.  
A python interpreter, compliant at least with with the Python 2.6 or Python 3.0  specifications, is required to compile the python interface of the library.

Here are the steps needed to install the library on MinGW :

* Expand the file calceph-|version|.tar.gz

* Execute the command *MinGW Shell* from the menu *Start*.

    This will open a MinGW Shell console window.

* cd *dir*\\calceph-|version|

    Go to the directory *dir* where |LIBRARYNAME| has been expanded.

* make -f Makefile.mingw

    This compiles |LIBRARYNAME| in the working directory.

    This command line accepts several options :

    * CC= ``xx``

        specifies the name of the C compiler. The defaut value is *gcc.exe*

    * FC= ``xx``

        specifies the name of the Fortran compiler. The defaut value is *gfortran.exe*

    * PYTHON= ``xx``
    
    specifies the name of the Python interpreter. The defaut value is *python.exe*

    * F77FUNC= ``naming``

        specifies the naming convention of the fortran 77 compiler.
        
        The possible value are: x, X, x##_ , X##_.

    * ENABLEF2003={0|1} 

        specifies if it must compile the fortran 2003 interface. The defaut value is 0.

    * ENABLEF77={0|1} 
    
        specifies if it must compile the fortran 77/90/95 interface. The defaut value is 0.

    * ENABLEPYTHON={0|1} 

    specifies if it must compile the python interface. The defaut value is 0.

* make -f Makefile.mingw check

    This will make sure that the |LIBRARYNAME| was built correctly.

    If you get error messages, please report them to |EMAIL| (see :ref:`Reporting bugs` ,  for information on what to include in useful bug reports).

    This command line accepts several options :

    * CC= ``xx``

        specifies the name of the C compiler. The defaut value is *gcc.exe*

    * FC= ``xx``

        specifies the name of the Fortran compiler. The defaut value is *gfortran.exe*

    * PYTHON= ``xx``
    
    specifies the name of the Python interpreter. The defaut value is *python.exe*

    * F77FUNC= ``naming``

        specifies the naming convention of the fortran 77 compiler.
        
        The possible value are: x, X, x##_ , X##_.

    * ENABLEF2003={0|1} 

        specifies if it must compile the fortran 2003 interface. The defaut value is 0.

    * ENABLEF77={0|1} 
    
        specifies if it must compile the fortran 77/90/95 interface. The defaut value is 0.

    * ENABLEPYTHON={0|1} 

    specifies if it must compile the python interface. The defaut value is 0.

* make -f Makefile.mingw install DESTDIR= *dir*

    This will copy the file  :file:`calceph.h`, :file:`calceph.mod` and :file:`f90calceph.h`  to the directory *dir*, the file :file:`libcalceph.lib` to the directory *dir* **\\lib**, the documentation files to the directory *dir* **\\doc**. 

If *ENABLEPYTHON=1*, the installation will copy the of the |LIBRARYSHORTNAME| python package to the system python site package (e.g., C:\\Python27\\Lib\\sites-packages\\) in order to that the python interpreter finds the |LIBRARYSHORTNAME| module.

Note: you need write permissions on these directories.

This command line accepts several options :

    * CC= ``xx``

        specifies the name of the C compiler. The defaut value is *gcc.exe*

    * FC= ``xx``

        specifies the name of the Fortran compiler. The defaut value is *gfortran.exe*

    * PYTHON= ``xx``
    
    specifies the name of the Python interpreter. The defaut value is *python.exe*

    * F77FUNC= ``naming``

        specifies the naming convention of the fortran 77 compiler.
        
        The possible value are: x, X, x##_ , X##_.

    * ENABLEF2003={0|1} 

        specifies if it must compile the fortran 2003 interface. The defaut value is 0.

    * ENABLEF77={0|1} 
    
        specifies if it must compile the fortran 77/90/95 interface. The defaut value is 0.

    * ENABLEPYTHON={0|1} 

    specifies if it must compile the python interface. The defaut value is 0.

