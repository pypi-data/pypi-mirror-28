.. _`Multiple file access functions`:

Multiple file access functions
==============================

The following group of functions should be the preferred method to access to the library. They allow to access to multiple ephemeris files at the same time, even  by multiple threads.  

When an error occurs, these functions execute error handlers according to the behavior defined by the function |calceph_seterrorhandler|. 

.. %----------------------------------------------------------------------------

Thread notes
------------

If the standard I/O functions such as **fread** are not reentrant
then the |LIBRARYSHORTNAME| I/O functions using them will not be reentrant either.
     
.. ifconfig:: calcephapi in ('C')

    It's not safe for two threads to call the functions with the same object of type :c:type:`t_calcephbin`. But it's safe for two threads to access simultaneously to the same ephemeris file with two different objects of type :c:type:`t_calcephbin`.  In this case, each thread must open the same file. 

.. ifconfig:: calcephapi in ('F2003', 'F90')

    It's not safe for two threads to call the functions with the same handle of ephemeris object. But it's safe for two threads to access simultaneously to the same ephemeris file with two different objects.  In this case, each thread must open the same file. 

.. ifconfig:: calcephapi in ('Python')

    It's not safe for two threads to call the functions with the same object of type :py:class:`CalcephBin`. But it's safe for two threads to access simultaneously to the same ephemeris file with two different objects of type :py:class:`CalcephBin`.  In this case, each thread must open the same file. 

Usage
-----

The following examples, that can be found in the directory *examples* of the library sources, show the typical usage of this group of functions.

.. ifconfig:: calcephapi in ('C')

    The example in C language is :file:`cmultiple.c`. 
    
.. ifconfig:: calcephapi in ('F2003')

    The example in Fortran 2003 language is :file:`f2003multiple.f`.
    
.. ifconfig:: calcephapi in ('F90')

    The example in Fortran 77/90/95 language is :file:`f77multiple.f`.

.. ifconfig:: calcephapi in ('Python')

    The example in Python language is :file:`pymultiple.py`.


.. ifconfig:: calcephapi in ('F2003')

   ::
   
        program f2003multiple
            USE, INTRINSIC :: ISO_C_BINDING
            use calceph
            implicit none
            integer res
            real(8) AU, EMRAT, GM_Mer
            real(8) jd0
            real(8) dt
            real(8) PV(6)
            TYPE(C_PTR) :: peph
            
            jd0 = 2451624
            dt = 0.5E0
            ! open the ephemeris file 
            peph = calceph_open("example1.dat"//C_NULL_CHAR)
            if (C_ASSOCIATED(peph)) then
                write (*,*) "The ephemeris is already opened"
                ! print the values of AU, EMRAT and GM_Mer 
                if (calceph_getconstant(peph, "AU"//C_NULL_CHAR, AU).eq.1) then
                    write (*,*) "AU=", AU
               endif
               if (calceph_getconstant(peph,"EMRAT"//C_NULL_CHAR, EMRAT).eq.1) then
                    write (*,*) "EMRAT=", EMRAT
               endif
               if (calceph_getconstant(peph,"GM_Mer"//C_NULL_CHAR, GM_Mer).eq.1) then
                    write (*,*) "GM_Mer=", GM_Mer
               endif
               
               ! compute and print the coordinates 
               ! the geocentric moon coordinates 
               res = calceph_compute(peph,jd0, dt, 10, 3, PV)
               call printcoord(PV,"geocentric coordinates of the Moon")
               ! the value TT-TDB 
               if (calceph_compute(peph,jd0, dt, 16, 0, PV).eq.1) then
                write (*,*) "TT-TDB = ", PV(1)
               endif
               ! the heliocentric coordinates of Mars 
               res = calceph_compute(peph,jd0, dt, 4, 11, PV)
               call printcoord(PV,"heliocentric coordinates of Mars")
 
               ! close the ephemeris file 
               call calceph_close(peph)
               write (*,*) "The ephemeris is already closed"
           else
               write (*,*) "The ephemeris can't be opened"
           endif
       stop
       end

.. @c %----------------------------------------------------------------------------

Functions
---------

.. @c %----------------------------------------------------------------------------

.. include:: replace.rst

|menu_calceph_open|
~~~~~~~~~~~~~~~~~~~
 
 
.. ifconfig:: calcephapi in ('C')

    .. c:function:: t_calcephbin* calceph_open ( const char *filename )

        :param filename: |arg_filename|
        :return: |arg_eph|. |retfuncfailsNULL|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: function calceph_open (filename) BIND(C)
    
        :p  filename [CHARACTER(len=1,kind=C_CHAR), intent(in)]: |arg_filename|.
        :r calceph_open: |arg_eph|. |retfuncfailsNULL|
        :rtype calceph_open: TYPE(C_PTR)

.. ifconfig:: calcephapi in ('F90')
    
    .. f:function:: function f90calceph_open (eph, filename)

        :p  filename [CHARACTER(len=*), intent(in)]: |arg_filename|.
        :p  eph   [INTEGER(8), intent(out)]: |arg_eph|
        :r f90calceph_open: |retfuncfails0|
        :rtype f90calceph_open: INTEGER


.. ifconfig:: calcephapi in ('Python')

    .. py:function:: calcephpy.CalcephBin.open (filename) -> eph
    
        :param  str filename: |arg_filename|
        :return: |arg_eph|
        :rtype: calcephpy.CalcephBin 


This function opens the file whose pathname is the string pointed to by filename, reads the two header blocks of this file
and returns an ephemeris descriptor associated to it. 
This file must be compliant to the format specified by the 'original JPL binary' , 'INPOP 2.0 binary' or 'SPICE' ephemeris file. 
At the moment, supported SPICE files are the following :

  * text Planetary Constants Kernel (KPL/PCK) files
  * binary PCK  (DAF/PCK) files.
  * binary SPK (DAF/SPK) files containing segments of type |supportedspk|.
  * meta kernel (KPL/MK) files.
  * frame kernel (KPL/FK) files. Only a basic support is provided.

Just after the call of |calceph_open|, the function |calceph_prefetch| should be called to accelerate future computations.

The function |calceph_close| must be called to free allocated memory by this function.

.. ifconfig:: calcephapi in ('C')

    The following example opens the ephemeris file example1.dat and example2.dat
    
    ::

         t_calcephbin *peph1;
         t_calcephbin *peph2;
         peph1 = calceph_open("example1.dat");
         peph2 = calceph_open("example2.dat");
         if (peph1 && peph2)
         {
           calceph_prefetch(peph1);
           calceph_prefetch(peph2);
           /* 
             ...  computation ... 
           */
         }
         /* close the files */
         if (peph1) calceph_close(peph1);
         if (peph2) calceph_close(peph2);

.. ifconfig:: calcephapi in ('Python')

    The following example opens the ephemeris file example1.dat

    ::
    
        from calcephpy import *

        peph = CalcephBin.open("example1.dat")
 
        # ...  computation ...  

        peph.close()
 
.. ifconfig:: calcephapi in ('F2003')

    The following example opens the ephemeris file example1.dat

    ::

           USE, INTRINSIC :: ISO_C_BINDING
           use calceph
           TYPE(C_PTR) :: peph
           
           peph = calceph_open("example1.dat"//C_NULL_CHAR)
           if (C_ASSOCIATED(peph)) then
           
                ! ... computation ... 
           
           endif 
           call calceph_close(peph)    

.. ifconfig:: calcephapi in ('F90')

    The following example opens the ephemeris file example1.dat

    ::

           include 'f90calceph.h'
           integer res

           res = f90calceph_open(peph, "example1.dat")
           if (res.eq.1) then
           
                ! ... computation ... 
           
           endif 
           call f90calceph_close(peph)

.. %----------------------------------------------------------------------------

|menu_calceph_open_array|
~~~~~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: t_calcephbin* calceph_open_array (int n, const char *array_filename[] )

        :param  n: |arg_n|
        :param  array_filename: |arg_array_filename|
        :return: |arg_eph|. |retfuncfailsNULL|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: function calceph_open_array (n, array_filename, len_filename) BIND(C)

        :p  n [INTEGER(C_INT), VALUE, intent(in)]: |arg_n|.
        :p  array_filename [CHARACTER(len=1,kind=C_CHAR), dimension(*), intent(in)]: |arg_array_filename|.
        :p  len_filename [INTEGER(C_INT), VALUE, intent(in)]: |arg_len_filename|.
        :r calceph_open_array: |arg_eph|. |retfuncfailsNULL|
        :rtype calceph_open_array: TYPE(C_PTR)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_open_array (eph, n, array_filename, len_filename)

        :p  eph   [INTEGER(8), intent(out)]: |arg_eph|
        :p  n [INTEGER, intent(in)]: |arg_n|.
        :p  array_filename [CHARACTER(len=*), dimension(*), intent(in)]: |arg_array_filename|
        :p  len_filename [INTEGER, intent(in)]: |arg_len_filename|.
        :r f90calceph_open_array: |retfuncfails0|
        :rtype f90calceph_open_array: INTEGER

.. ifconfig:: calcephapi in ('Python')

    .. py:function:: calcephpy.CalcephBin.open ( array_filename ) -> eph

        :param  list array_filename: |arg_array_filename|
        :return: |arg_eph|
        :rtype: calcephpy.CalcephBin 

This function opens n files whose pathnames are the string pointed to by array_filename, 
reads the header blocks of these files
and returns an ephemeris descriptor associated to them.  

These files must have the same type (e.g., all files are SPICE files or original JPL files). 
This file must be compliant to the format specified by the  'original JPL binary' , 'INPOP 2.0 or 3.0 binary' or 'SPICE' ephemeris file. 
At the moment, supported SPICE files are the following :

 * text Planetary Constants Kernel (KPL/PCK) files
 * binary PCK  (DAF/PCK) files.
 * binary SPK (DAF/SPK) files containing segments of type |supportedspk|.
 * meta kernel (KPL/MK) files.
 * frame kernel (KPL/FK) files. Only a basic support is provided.


Just after the call of |calceph_open_array|, the function |calceph_prefetch| should be called to accelerate future computations.

The function |calceph_close| must be called to free allocated memory by this function.



The following example opens the ephemeris file example1.bsp and example1.tpc

.. include:: examples/multiple_open_array.rst

.. %----------------------------------------------------------------------------

|menu_calceph_prefetch|
~~~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_prefetch ( t_calcephbin* eph )

        :param  eph: |arg_eph|
        :return: |retfuncfails0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_prefetch (eph) BIND(C)

        :p  eph [TYPE(C_PTR), VALUE, intent(in)]: |arg_eph|.
        :r calceph_prefetch: |retfuncfails0|
        :rtype calceph_prefetch: INTEGER(C_INT)


.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_prefetch (eph)

        :p  eph   [INTEGER(8), intent(in)]: |arg_eph|
        :r f90calceph_prefetch: |retfuncfails0|
        :rtype f90calceph_prefetch: INTEGER


.. ifconfig:: calcephapi in ('Python')

    .. py:method:: calcephpy.CalcephBin.prefetch()


This function prefetches to the main memory all files associated to |ephemerisdescriptoreph|. 
This prefetching operation will accelerate the further computations performed with |calceph_compute|, |calceph_compute_unit|,  |calceph_compute_order|, |calceph_orient_unit|, ... . 

It requires that the file is smaller than the main memory.
If multiple threads (e.g. threads of openMP or Posix Pthreads) prefetch the data for the same ephemeris file, 
the used memory will remain the same as if the prefetch operation was done by a single thread if and if the 
endianess of the file is the same as the computer and if the operating system, such as Linux, MacOS X other unix, supports the function mmap.


.. %----------------------------------------------------------------------------

|menu_calceph_compute|
~~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_compute (t_calcephbin* eph, double JD0, double time, int target, int center, double PV[6] )

        :param  eph: |arg_eph|
        :param  JD0: |arg_JD0|
        :param  time: |arg_time|
        :param  target: |arg_target|
        :param  center: |arg_center|
        :param  PV:  .. include:: arg_PV.rst
        :return: |retfuncfails0|


.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_compute (eph, JD0, time, target, center, PV ) BIND(C)
    
        :param eph [TYPE(C_PTR), VALUE, intent(in)]: |arg_eph|
        :param JD0 [REAL(C_DOUBLE), VALUE, intent(in)]: |arg_JD0|
        :param time [REAL(C_DOUBLE), VALUE, intent(in)]: |arg_time|
        :param target [INTEGER(C_INT), VALUE, intent(in)]: |arg_target|
        :param center [INTEGER(C_INT), VALUE, intent(in)]: |arg_center|
        :param PV[REAL(C_DOUBLE), dimension(1\:6), intent(out)]: .. include:: arg_PV.rst
        :r calceph_compute: |retfuncfails0|
        :rtype calceph_compute: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_compute (eph, JD0, time, target, center, PV )
    
        :param eph [INTEGER(8), intent(in)]: |arg_eph|
        :param JD0 [REAL(8), intent(in)]: |arg_JD0|
        :param time [REAL(8), intent(in)]: |arg_time|
        :param target [INTEGER, intent(in)]: |arg_target|
        :param center [INTEGER, intent(in)]: |arg_center|
        :param PV(6) [REAL(8), intent(out)]: .. include:: arg_PV.rst
        :r f90calceph_compute: |retfuncfails0|
        :rtype f90calceph_compute: INTEGER

.. ifconfig:: calcephapi in ('Python')

    .. py:function:: calcephpy.CalcephBin.compute (JD0, time, target, center) -> PV
    
        :param  float JD0: |arg_JD0|
        :param  float time: |arg_time|
        :param  int target: |arg_target|
        :param  int center: |arg_center|
        :return:  .. include:: arg_PV.rst
        :rtype: list

This function reads, if needed, in the ephemeris file |eph| and interpolates a single object, usually the position and velocity of one body (*target*) relative to another (*center*) for the time *JD0+time* and stores the results to *PV*. The ephemeris file |eph| must have been previously opened with the function |calceph_open|.


To get the best precision for the interpolation, the time is splitted in two floating-point numbers. The argument *JD0* should be an integer and *time* should be a fraction of the day. But you may call this function with *time=0* and *JD0*, the desired time, if you don't take care about precision.

The possible values for *target* and *center* are  :

+------------------------------------+------------------------+
| value                              |            meaning     |
+====================================+========================+
| 1                                  | Mercury Barycenter     |
+------------------------------------+------------------------+
| 2                                  | Venus Barycenter       |
+------------------------------------+------------------------+
| 3                                  | Earth                  |
+------------------------------------+------------------------+
| 4                                  | Mars Barycenter        |
+------------------------------------+------------------------+
| 5                                  | Jupiter Barycenter     |
+------------------------------------+------------------------+
| 6                                  | Saturn Barycenter      |
+------------------------------------+------------------------+
| 7                                  | Uranus Barycenter      |
+------------------------------------+------------------------+
| 8                                  | Neptune Barycenter     |
+------------------------------------+------------------------+
| 9                                  | Pluto Barycenter       |
+------------------------------------+------------------------+
| 10                                 | Moon                   |
+------------------------------------+------------------------+
| 11                                 | Sun                    |
+------------------------------------+------------------------+
| 12                                 | Solar Sytem barycenter |
+------------------------------------+------------------------+
| 13                                 | Earth-moon barycenter  |
+------------------------------------+------------------------+
| 15                                 | Librations             |
+------------------------------------+------------------------+
| 16                                 | TT-TDB                 |
+------------------------------------+------------------------+
| 17                                 | TCG-TCB                |
+------------------------------------+------------------------+
| asteroid number + CALCEPH_ASTEROID | asteroid               |
+------------------------------------+------------------------+

These accepted values by this function are the same as the value for the JPL function *PLEPH*, except for the values *TT-TDB*, *TCG-TCB* and asteroids.

For example, the value "CALCEPH_ASTEROID+4" for target or center specifies the asteroid Vesta.


The following example prints the heliocentric coordinates of Mars at time=2451624.5 and at 2451624.9 

.. include:: examples/multiple_compute.rst

   
.. %----------------------------------------------------------------------------

|menu_calceph_compute_unit|
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_compute_unit (t_calcephbin* eph, double JD0, double time, int target, int center, int unit, double PV[6] )

        :param  eph: |arg_eph|
        :param  JD0: |arg_JD0|
        :param  time: |arg_time|
        :param  target: |arg_target_unit|
        :param  center: |arg_center_unit|
        :param  unit: .. include:: arg_unit.rst
        :param  PV:  .. include:: arg_PV_unit.rst
        :return: |retfuncfails0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_compute_unit (eph, JD0, time, target, center, unit, PV ) BIND(C)

        :param eph [TYPE(C_PTR), VALUE, intent(in)]: |arg_eph|
        :param JD0 [REAL(C_DOUBLE), VALUE, intent(in)]: |arg_JD0|
        :param time [REAL(C_DOUBLE), VALUE, intent(in)]: |arg_time|
        :param target [INTEGER(C_INT), VALUE, intent(in)]: |arg_target_unit|
        :param center [INTEGER(C_INT), VALUE, intent(in)]: |arg_center_unit|
        :param unit [INTEGER(C_INT), VALUE, intent(in)]: .. include:: arg_unit.rst
        :param PV[REAL(C_DOUBLE), dimension(1\:6), intent(out)]: .. include:: arg_PV_unit.rst
        :r calceph_compute_unit: |retfuncfails0|
        :rtype calceph_compute_unit: INTEGER(C_INT)
        

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_compute_unit (eph, JD0, time, target, center, unit, PV )
    
        :param eph [INTEGER(8), intent(in)]: |arg_eph|
        :param JD0 [REAL(8), intent(in)]: |arg_JD0|
        :param time [REAL(8), intent(in)]: |arg_time|
        :param target [INTEGER, intent(in)]: |arg_target_unit|
        :param center [INTEGER, intent(in)]: |arg_center_unit|
        :param unit [INTEGER, intent(in)]: .. include:: arg_unit.rst
        :param PV(6) [REAL(8), intent(out)]: .. include:: arg_PV_unit.rst
        :r f90calceph_compute_unit: |retfuncfails0|
        :rtype f90calceph_compute_unit: INTEGER

.. ifconfig:: calcephapi in ('Python')

    .. py:function:: calcephpy.CalcephBin.compute_unit (JD0, time, target, center, unit) -> PV

        :param  float JD0: |arg_JD0|
        :param  float time: |arg_time|
        :param  int target: |arg_target_unit|
        :param  int center: |arg_center_unit|
        :param  int unit: .. include:: arg_unit.rst
        :return:  .. include:: arg_PV_unit.rst
        :rtype: list


This function is similar to the function |calceph_compute|, except that the units of the output are specified. 

This function reads, if needed, in the ephemeris file |eph| and interpolates a single object, usually the position and velocity of one body (*target*) relative to another (*center*) for the time *JD0+time* and stores the results to *PV*. The ephemeris file |eph| must have been previously opened with the function |calceph_open|.
The output values are expressed in the units specified by *unit*.

This function checks the units if invalid combinations of units are given to the function.

The following example prints the heliocentric coordinates of Mars  at time=2451624.5

.. include:: examples/multiple_compute_unit.rst


.. %----------------------------------------------------------------------------

|menu_calceph_orient_unit|
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_orient_unit (t_calcephbin* eph, double JD0, double time, int target, int unit, double PV[6] )

        :param  eph: |arg_eph|
        :param  JD0: |arg_JD0|
        :param  time: |arg_time|
        :param  target: |arg_target_orient_unit|
        :param  unit: .. include:: arg_unit_orient_unit.rst
        :param  PV:  .. include:: arg_PV_orient_unit.rst
        :return: |retfuncfails0|


.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_orient_unit (eph, JD0, time, target, unit, PV) BIND(C)

        :param eph [TYPE(C_PTR), VALUE, intent(in)]: |arg_eph|
        :param JD0 [REAL(C_DOUBLE), VALUE, intent(in)]: |arg_JD0|
        :param time [REAL(C_DOUBLE), VALUE, intent(in)]: |arg_time|
        :param target [INTEGER(C_INT), VALUE, intent(in)]: |arg_target_orient_unit|
        :param unit [INTEGER(C_INT), VALUE, intent(in)]: .. include:: arg_unit_orient_unit.rst
        :param PV[REAL(C_DOUBLE), dimension(1\:6), intent(out)]: .. include:: arg_PV_orient_unit.rst
        :r calceph_orient_unit: |retfuncfails0|
        :rtype calceph_orient_unit: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_orient_unit (eph, JD0, time, target, unit, PV)

        :param eph [INTEGER(8), intent(in)]: |arg_eph|
        :param JD0 [REAL(8), intent(in)]: |arg_JD0|
        :param time [REAL(8), intent(in)]: |arg_time|
        :param target [INTEGER, intent(in)]: |arg_target_orient_unit|
        :param unit [INTEGER, intent(in)]: .. include:: arg_unit_orient_unit.rst
        :param PV(6) [REAL(8), intent(out)]: .. include:: arg_PV_orient_unit.rst
        :r f90calceph_orient_unit: |retfuncfails0|
        :rtype f90calceph_orient_unit: INTEGER

.. ifconfig:: calcephapi in ('Python')

    .. py:function:: calcephpy.CalcephBin.orient_unit (JD0, time, target,  unit) -> PV

        :param  float JD0: |arg_JD0|
        :param  float time: |arg_time|
        :param  int target: |arg_target_orient_unit|
        :param  int unit: .. include:: arg_unit_orient_unit.rst
        :return:  .. include:: arg_PV_orient_unit.rst
        :rtype: list

This function reads, if needed, in the ephemeris file |eph| and interpolates the orientation of a single body (*target*) for the time *JD0+time* and stores the results to *PV*. The ephemeris file |eph| must have been previously opened with the function |calceph_open|.
The output values are expressed in the units specified by *unit*.

This function checks the units if invalid combinations of units are given to the function.


The following example prints the angles of libration of the Moon at time=2451624.5

.. include:: examples/multiple_orient_unit.rst

.. %----------------------------------------------------------------------------

|menu_calceph_rotangmom_unit|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_rotangmom_unit (t_calcephbin* eph, double JD0, double time, int target, int unit, double PV[6] )

        :param  eph: |arg_eph|
        :param  JD0: |arg_JD0|
        :param  time: |arg_time|
        :param  target: |arg_target_orient_unit|
        :param  unit: .. include:: arg_unit_orient_unit.rst
        :param  PV:  .. include:: arg_PV_rotangmom_unit.rst
        :return: |retfuncfails0|


.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_rotangmom_unit (eph, JD0, time, target, unit, PV) BIND(C)

        :param eph [TYPE(C_PTR), VALUE, intent(in)]: |arg_eph|
        :param JD0 [REAL(C_DOUBLE), VALUE, intent(in)]: |arg_JD0|
        :param time [REAL(C_DOUBLE), VALUE, intent(in)]: |arg_time|
        :param target [INTEGER(C_INT), VALUE, intent(in)]: |arg_target_orient_unit|
        :param unit [INTEGER(C_INT), VALUE, intent(in)]: .. include:: arg_unit_orient_unit.rst
        :param PV[REAL(C_DOUBLE), dimension(1\:6), intent(out)]: .. include:: arg_PV_rotangmom_unit.rst
        :r calceph_rotangmom_unit: |retfuncfails0|
        :rtype calceph_rotangmom_unit: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_rotangmom_unit (eph, JD0, time, target, unit, PV)

        :param eph [INTEGER(8), intent(in)]: |arg_eph|
        :param JD0 [REAL(8), intent(in)]: |arg_JD0|
        :param time [REAL(8), intent(in)]: |arg_time|
        :param target [INTEGER, intent(in)]: |arg_target_orient_unit|
        :param unit [INTEGER, intent(in)]: .. include:: arg_unit_orient_unit.rst
        :param PV(6) [REAL(8), intent(out)]: .. include:: arg_PV_rotangmom_unit.rst
        :r f90calceph_rotangmom_unit: |retfuncfails0|
        :rtype f90calceph_rotangmom_unit: INTEGER

.. ifconfig:: calcephapi in ('Python')

    .. py:function:: calcephpy.CalcephBin.rotangmom_unit (JD0, time, target, unit) -> PV

        :param  float JD0: |arg_JD0|
        :param  float time: |arg_time|
        :param  int target: |arg_target_orient_unit|
        :param  int unit: .. include:: arg_unit_orient_unit.rst
        :return:  .. include:: arg_PV_rotangmom_unit.rst
        :rtype: list

This function reads, if needed, in the ephemeris file |eph| and interpolates the angular momentum vector due to the rotation of the body, divided by the product of the mass :math:`m` and of the square of the radius :math:`R`, of a single body (*target*) for the time *JD0+time* and stores the results to *PV*. The ephemeris file |eph| must have been previously opened with the function |calceph_open|. The angular momentum :math:`L` , due to the rotation of the body, is defined as the product of the inertia matrix :math:`I` by the angular velocity vector :math:`{\omega}`. So the returned value is :math:`L/(mR^2)=(I\omega)/(mR^2)`
The output values are expressed in the units specified by *unit*.

This function checks the units if invalid combinations of units are given to the function.


The following example prints the angular momentum, due to its rotation, for the Earth at time=2451624.5

.. include:: examples/multiple_rotangmom_unit.rst


.. %----------------------------------------------------------------------------

|menu_calceph_compute_order|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_compute_order (t_calcephbin* eph, double JD0, double time, int target, int center, int unit, int order, double *PVAJ )

        :param  eph: |arg_eph|
        :param  JD0: |arg_JD0|
        :param  time: |arg_time|
        :param  target: |arg_target_unit|
        :param  center: |arg_center_unit|
        :param  unit: .. include:: arg_unit.rst
        :param  order: .. include:: arg_order.rst
        :param  PVAJ: 
                   | An array to receive the cartesian position (x,y,z) and the derivatives. 
                   | This array must be large enough to store the results. For the C interface, the size of this array must be equal to 3*(order+1).
                   |  - PVAJ[0..2] contain the position (x,y,z) and is always valid.
                   |  - PVAJ[3..5] contain the velocity  (dx/dt,dy/dt,dz/dt) and is only valid if *order* is greater or equal to 1.
                   |  - PVAJ[6..8] contain the acceleration (d^2x/dt^2,d^2y/dt^2,d^2z/dt^2) and is only valid if *order* is greater or equal to 2.
                   |  - PVAJ[9..11] contain the jerk (d^3x/dt^3,d^3y/dt^3,d^3z/dt^3) and is only valid if *order* is equal to 3.
                   | The position, velocity, acceleration and jerk are expressed in Astronomical Unit (au) if unit contains |CALCEPH_UNIT_AU|.
                   | The position, velocity, acceleration and jerk are expressed in kilometers if unit contains |CALCEPH_UNIT_KM|.
                   | The velocity, acceleration, jerk, TT-TDB, TCG-TCB or the derivatives of the angles of the librations of the Moon are expressed in days if unit contains |CALCEPH_UNIT_DAY|.
                   | The velocity, acceleration, jerk, TT-TDB, TCG-TCB or the derivatives of the angles of the librations of the Moon are expressed in seconds if unit contains |CALCEPH_UNIT_SEC|.
                   | The angles of the librations of the Moon are expressed in radians if unit contains |CALCEPH_UNIT_RAD|.
                   | For example, to get the positions, velocities, accelerations and jerks expressed in kilometers and kilometers/seconds, the unit must be set to |CALCEPH_UNIT_KM| + |CALCEPH_UNIT_SEC|. 

        :return: |retfuncfails0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_compute_order (eph, JD0, time, target, center, unit, order, PVAJ ) BIND(C)

        :param eph [TYPE(C_PTR), VALUE, intent(in)]: |arg_eph|
        :param JD0 [REAL(C_DOUBLE), VALUE, intent(in)]: |arg_JD0|
        :param time [REAL(C_DOUBLE), VALUE, intent(in)]: |arg_time|
        :param target [INTEGER(C_INT), VALUE, intent(in)]: |arg_target|
        :param center [INTEGER(C_INT), VALUE, intent(in)]: |arg_center|
        :param unit [INTEGER(C_INT), VALUE, intent(in)]: .. include:: arg_unit_order.rst
        :param order [INTEGER(C_INT), VALUE, intent(in)]: .. include:: arg_order.rst
        :param PVAJ[REAL(C_DOUBLE), dimension(1\:12), intent(out)]: .. include:: arg_PVAJ_order.rst
        :r calceph_compute_order: |retfuncfails0|
        :rtype calceph_compute_order: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_compute_order (eph, JD0, time, target, center, unit, order, PVAJ )

        :param eph [INTEGER(8), intent(in)]: |arg_eph|
        :param JD0 [REAL(8), intent(in)]: |arg_JD0|
        :param time [REAL(8), intent(in)]: |arg_time|
        :param target [INTEGER, intent(in)]: |arg_target_unit|
        :param center [INTEGER, intent(in)]: |arg_center_unit|
        :param unit [INTEGER, intent(in)]: .. include:: arg_unit_order.rst
        :param order [INTEGER, intent(in)]: .. include:: arg_order.rst
        :param PVAJ(12) [REAL(8), intent(out)]: .. include:: arg_PVAJ_order.rst
        :r f90calceph_compute_order: |retfuncfails0|
        :rtype f90calceph_compute_order: INTEGER

.. ifconfig:: calcephapi in ('Python')

    .. py:function:: calcephpy.CalcephBin.compute_order(JD0, time, target, center, unit, order) -> PVAJ
    
        :param  float JD0: |arg_JD0|
        :param  float time: |arg_time|
        :param  int target: |arg_target_unit|
        :param  int center: |arg_center_unit|
        :param  int unit: .. include:: arg_unit_order.rst
        :param  int order: .. include:: arg_order.rst
        :return:  .. include:: arg_PVAJ_order.rst
        :rtype: list

This function is similar to the function |calceph_compute_unit|, except that the order of the computed derivatives is specified. 

This function reads, if needed, in the ephemeris file |eph| and interpolates a single object, usually the position and their derivatives of one body (*target*) relative to another (*center*) for the time *JD0+time* and stores the results to *PVAJ*. The ephemeris file |eph| must have been previously opened with the function |calceph_open|.
The order of the derivatives are specified by *order*. The output values are expressed in the units specified by *unit*.

This function checks the units if invalid combinations of units are given to the function.



The following example prints the heliocentric coordinates of Mars at time=2451624.5

.. include:: examples/multiple_compute_order.rst


.. %----------------------------------------------------------------------------

|menu_calceph_orient_order|
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_orient_order (t_calcephbin* eph, double JD0, double time, int target, int unit, int order, double *PVAJ )

        :param  eph: |arg_eph|
        :param  JD0: |arg_JD0|
        :param  time: |arg_time|
        :param  target: |arg_target_orient_unit|
        :param  unit: .. include:: arg_unit_orient_unit.rst
        :param  order: .. include:: arg_order_orient.rst
        :param  PVAJ:  
                | An array to receive the euler angles and their different order of the derivatives for the orientation of the body. 
                | This array must be large enough to store the results. The size of this array must be equal to 3*(order+1).
                |  - PVAJ[0..2] contain the angles  and is always valid.
                |  - PVAJ[3..5] contain the first derivative and is only valid if *order* is greater or equal to 1.
                |  - PVAJ[6..8] contain the second derivative and is only valid if *order* is greater or equal to 2.
                |  - PVAJ[9..11] contain the third derivative and is only valid if *order* is equal to 3.
                | The derivatives of the angles are expressed in days if unit contains |CALCEPH_UNIT_DAY|.
                | The derivatives of the angles are expressed in seconds if unit contains |CALCEPH_UNIT_SEC|.
                | The angles of the orientation are expressed in radians if unit contains |CALCEPH_UNIT_RAD|.

        :return: |retfuncfails0|


.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_orient_order (eph, JD0, time, target, unit, order, PVAJ ) BIND(C)

        :param eph [TYPE(C_PTR), VALUE, intent(in)]: |arg_eph|
        :param JD0 [REAL(C_DOUBLE), VALUE, intent(in)]: |arg_JD0|
        :param time [REAL(C_DOUBLE), VALUE, intent(in)]: |arg_time|
        :param target [INTEGER(C_INT), VALUE, intent(in)]: |arg_target_orient_unit|
        :param unit [INTEGER(C_INT), VALUE, intent(in)]: .. include:: arg_unit_order.rst
        :param order [INTEGER(C_INT), VALUE, intent(in)]: .. include:: arg_order_orient.rst
        :param PVAJ[REAL(C_DOUBLE), dimension(1\:12), intent(out)]: .. include:: arg_PVAJ_orient_order.rst
        :r calceph_compute_order: |retfuncfails0|
        :rtype calceph_compute_order: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_orient_order (eph, JD0, time, target,  unit, order, PVAJ )

        :param eph [INTEGER(8), intent(in)]: |arg_eph|
        :param JD0 [REAL(8), intent(in)]: |arg_JD0|
        :param time [REAL(8), intent(in)]: |arg_time|
        :param target [INTEGER, intent(in)]: |arg_target_orient_unit|
        :param unit [INTEGER, intent(in)]: .. include:: arg_unit_orient_unit.rst
        :param order [INTEGER, intent(in)]: .. include:: arg_order_orient.rst
        :param PVAJ(12) [REAL(8), intent(out)]: .. include:: arg_PVAJ_orient_order.rst
        :r f90calceph_orient_order: |retfuncfails0|
        :rtype f90calceph_orient_order: INTEGER


.. ifconfig:: calcephapi in ('Python')

    .. py:function:: calcephpy.CalcephBin.orient_order(JD0, time, target, unit, order) -> PVAJ
    
        :param  float JD0: |arg_JD0|
        :param  float time: |arg_time|
        :param  int target: |arg_target_orient_unit|
        :param  int unit: .. include:: arg_unit_orient_unit.rst
        :param  int order: .. include:: arg_order_orient.rst
        :return: .. include:: arg_PVAJ_orient_order.rst
        :rtype: list

This function is similar to the function |calceph_orient_unit|, except that the order of the computed derivatives is specified. 


This function reads, if needed, in the ephemeris file |eph| and interpolates the orientation of a single body (*target*) for the time *JD0+time* and stores the results to *PVAJ*. 
The order of the derivatives are specified by *order*. The ephemeris file |eph| must have been previously opened with the function |calceph_open|. 
The output values are expressed in the units specified by *unit*.

This function checks the units if invalid combinations of units are given to the function.


The following example prints only the angles of libration of the Moon at time=2451624.5

.. include:: examples/multiple_orient_order.rst

.. %----------------------------------------------------------------------------

|menu_calceph_rotangmom_order|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_rotangmom_order (t_calcephbin* eph, double JD0, double time, int target, int unit, int order, double *PVAJ )

        :param  eph: |arg_eph|
        :param  JD0: |arg_JD0|
        :param  time: |arg_time|
        :param  target: |arg_target_orient_unit|
        :param  unit: .. include:: arg_unit_orient_unit.rst
        :param  order: .. include:: arg_order_rotangmom.rst
        :param  PVAJ:  
                | An array to receive the angular momentum due to its rotation, divided by the product of the mass and of the square of the radius, and their different order of the derivatives, of the body. 
                | This array must be large enough to store the results. The size of this array must be equal to 3*(order+1).
                |  - PVAJ[0..2] contain the angular momentum  and is always valid.
                |  - PVAJ[3..5] contain the first derivative and is only valid if *order* is greater or equal to 1.
                |  - PVAJ[6..8] contain the second derivative and is only valid if *order* is greater or equal to 2.
                |  - PVAJ[9..11] contain the third derivative and is only valid if *order* is equal to 3.
                | The angular momentum and its derivatives are expressed in days if unit contains |CALCEPH_UNIT_DAY|.
                | The angular momentum and its derivatives are expressed in seconds if unit contains |CALCEPH_UNIT_SEC|.

        :return: |retfuncfails0|


.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_rotangmom_order (eph, JD0, time, target, unit, order, PVAJ ) BIND(C)

        :param eph [TYPE(C_PTR), VALUE, intent(in)]: |arg_eph|
        :param JD0 [REAL(C_DOUBLE), VALUE, intent(in)]: |arg_JD0|
        :param time [REAL(C_DOUBLE), VALUE, intent(in)]: |arg_time|
        :param target [INTEGER(C_INT), VALUE, intent(in)]: |arg_target_orient_unit|
        :param unit [INTEGER(C_INT), VALUE, intent(in)]: .. include:: arg_unit_order.rst
        :param order [INTEGER(C_INT), VALUE, intent(in)]: .. include:: arg_order_rotangmom.rst
        :param PVAJ[REAL(C_DOUBLE), dimension(1\:12), intent(out)]: .. include:: arg_PVAJ_rotangmom_order.rst
        :r calceph_rotangmom_order: |retfuncfails0|
        :rtype calceph_rotangmom_order: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_rotangmom_order (eph, JD0, time, target,  unit, order, PVAJ )

        :param eph [INTEGER(8), intent(in)]: |arg_eph|
        :param JD0 [REAL(8), intent(in)]: |arg_JD0|
        :param time [REAL(8), intent(in)]: |arg_time|
        :param target [INTEGER, intent(in)]: |arg_target_orient_unit|
        :param unit [INTEGER, intent(in)]: .. include:: arg_unit_orient_unit.rst
        :param order [INTEGER, intent(in)]: .. include:: arg_order_rotangmom.rst
        :param PVAJ(12) [REAL(8), intent(out)]: .. include:: arg_PVAJ_rotangmom_order.rst
        :r f90calceph_rotangmom_order: |retfuncfails0|
        :rtype f90calceph_rotangmom_order: INTEGER


.. ifconfig:: calcephapi in ('Python')

    .. py:function:: calcephpy.CalcephBin.rotangmom_order(JD0, time, target, unit, order) -> PVAJ
    
        :param  float JD0: |arg_JD0|
        :param  float time: |arg_time|
        :param  int target: |arg_target_orient_unit|
        :param  int unit: .. include:: arg_unit_orient_unit.rst
        :param  int order: .. include:: arg_order_rotangmom.rst
        :return: .. include:: arg_PVAJ_rotangmom_order.rst
        :rtype: list

This function is similar to the function |calceph_orient_unit|, except that the order of the computed derivatives is specified. 


This function reads, if needed, in the ephemeris file |eph| and interpolates the angular momentum vector due to the rotation of the body, divided by the product of the mass :math:`m` and of the square of the radius :math:`R`, of a single body (*target*) for the time *JD0+time* and stores the results to *PVAJ*. The angular momentum :math:`L` , due to the rotation of the body, is defined as the product of the inertia matrix :math:`I` by the angular velocity vector :math:`{\omega}`. So the returned value is :math:`L/(mR^2)=(I\omega)/(mR^2)`
The order of the derivatives are specified by *order*. The ephemeris file |eph| must have been previously opened with the function |calceph_open|. 
The output values are expressed in the units specified by *unit*.

This function checks the units if invalid combinations of units are given to the function.


The following example prints only the angular momentum, due to its rotation, of the Earth at time=2451624.5

.. include:: examples/multiple_rotangmom_order.rst




.. %----------------------------------------------------------------------------

|menu_calceph_getconstant|
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_getconstant (t_calcephbin*  eph, const char* name, double *value )

        :param  eph: |arg_eph|
        :param  name: |arg_constant_name|
        :param  value: |arg_constant_value|
        :return: |retfuncfails0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_getconstant (eph, name, value) BIND(C)

        :p  eph [TYPE(C_PTR), VALUE, intent(in)]: |arg_eph|.
        :p  name [CHARACTER(len=1,kind=C_CHAR), intent(in)]: |arg_constant_name|.
        :p  value [REAL(C_DOUBLE), intent(out)]: |arg_constant_value|.
        :r calceph_getconstant: |retfuncfails0|
        :rtype calceph_getconstant: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_getconstant (eph, name, value) 

        :p  eph  [INTEGER(8), intent(in)]: |arg_eph|
        :p  name  [CHARACTER(len=*), intent(in)]: |arg_constant_name|
        :p  value [REAL(8), intent(out)]: |arg_constant_value|
        :r f90calceph_getconstant: |retfuncfails0|
        :rtype f90calceph_getconstant: INTEGER

.. ifconfig:: calcephapi in ('Python')

    .. py:function:: calcephpy.CalcephBin.getconstant(name) -> value
    
        :param  str name: |arg_constant_name|
        :return: |arg_constant_value|
        :rtype: float

This function returns the value associated to the constant *name* in the header of the ephemeris file |eph|.


The following example prints the value of the astronomical unit stored in the ephemeris file

.. include:: examples/multiple_getconstant.rst


.. %------------------------------------------------

|menu_calceph_getconstantcount|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_getconstantcount (t_calcephbin* eph )

        :param  eph: |arg_eph|
        :return: |arg_constant_number|. |retfuncfails0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_getconstantcount (eph) BIND(C)

        :param eph [TYPE(C_PTR), VALUE, intent(in)]: |arg_eph|
        :r calceph_getconstantcount: |arg_constant_number|. |retfuncfails0|
        :rtype calceph_getconstantcount: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_getconstantcount (eph) 

        :param eph [INTEGER(8), intent(in)]: |arg_eph|
        :r f90calceph_getconstantcount: |arg_constant_number|. |retfuncfails0|
        :rtype f90calceph_getconstantcount: INTEGER

.. ifconfig:: calcephapi in ('Python')

    .. py:function:: calcephpy.CalcephBin.getconstantcount ()

        :return:  |arg_constant_number|
        :rtype: int

This function returns the number of constants available in the header of the ephemeris file |eph|.

The following example prints the number of available constants stored in the ephemeris file

.. include:: examples/multiple_getconstantcount.rst

.. %------------------------------------------------

|menu_calceph_getconstantindex|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_getconstantindex (t_calcephbin* eph, int index, char name[CALCEPH_MAX_CONSTANTNAME], double *value)

        :param  eph: |arg_eph|
        :param  index: |arg_constant_index|
        :param  name: |arg_constant_name|
        :param  value: |arg_constant_value|
        :return: |retfuncfails0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_getconstantindex (eph, index, name, value) BIND(C)

        :p  eph [TYPE(C_PTR), VALUE, intent(in)]: |arg_eph|
        :p  index [INTEGER(C_INT), VALUE, intent(in)]: |arg_constant_index|
        :p  name [CHARACTER(len=1,kind=C_CHAR),  dimension(CALCEPH_MAX_CONSTANTNAME), intent(out)]: |arg_constant_name|.
        :p  value [REAL(C_DOUBLE), intent(out)]: |arg_constant_value|
        :r calceph_getconstantindex: |retfuncfails0|
        :rtype calceph_getconstantindex: INTEGER(C_INT)


.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_getconstantindex (eph, index, name, value) 

        :p  eph  [INTEGER(8), intent(in)]: |arg_eph|
        :p  index [INTEGER, intent(in)]: |arg_constant_index|
        :p  name  [CHARACTER(len=CALCEPH_MAX_CONSTANTNAME), intent(out)]: |arg_constant_name|
        :p  value [REAL(8), intent(out)]: |arg_constant_value|
        :r f90calceph_getconstantindex: |retfuncfails0|
        :rtype f90calceph_getconstantindex: INTEGER

.. ifconfig:: calcephapi in ('Python')

    .. py:function:: calcephpy.CalcephBin.getconstantindex (index) ->name, value

        :param  int index: |arg_constant_index|
        :return: |arg_constant_name|, |arg_constant_value|
        :rtype: str, float

This function returns the name and its value of the constant available at the specified index in the header of the ephemeris file |eph|. The value of *index* must be between 1 and |calceph_getconstantcount|.

.. ifconfig:: calcephapi in ('F90')

    Trailing blanks are added to the name of the constant.

The following example displays the name of the constants, stored in the ephemeris file, and their values 

.. include:: examples/multiple_getconstantindex.rst

.. %------------------------------------------------

|menu_calceph_gettimescale|
~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_gettimescale (t_calcephbin* eph)

        :param  eph: |arg_eph|
        :return: |retfuncfails0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_gettimescale (eph) BIND(C)

        :param eph [TYPE(C_PTR), VALUE, intent(in)]: |arg_eph|
        :r calceph_gettimescale: |retfuncfails0|
        :rtype calceph_gettimescale: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_gettimescale (eph) 

        :param eph [INTEGER(8), intent(in)]: |arg_eph|
        :r f90calceph_gettimescale: |retfuncfails0|
        :rtype f90calceph_gettimescale: INTEGER

.. ifconfig:: calcephapi in ('Python')

    .. py:function:: calcephpy.CalcephBin.gettimescale ()

        :return:  time scale of the ephemeris file
        :rtype: int

This function returns the timescale of the ephemeris file |eph| : 
  * 1 if the quantities of all bodies are expressed in the TDB time scale. 
  * 2 if the quantities of all bodies are expressed in the TCB time scale. 
  

The following example prints the time scale available in the ephemeris file

.. include:: examples/multiple_gettimescale.rst

.. %------------------------------------------------

|menu_calceph_gettimespan|
~~~~~~~~~~~~~~~~~~~~~~~~~~ 

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_gettimespan (t_calcephbin* eph, double* firsttime, double* lasttime, int* continuous )

        :param  eph: |arg_eph|
        :param  firsttime: |arg_firsttime|
        :param  lasttime: |arg_lasttime|
        :param  continuous: |arg_continuous|
        :return: |retfuncfails0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_gettimespan (eph, firsttime, lasttime, continuous) BIND(C)

        :param eph [TYPE(C_PTR), VALUE, intent(in)]: |arg_eph|
        :p  firsttime [REAL(C_DOUBLE), intent(out)]: |arg_firsttime|
        :p  lasttime [REAL(C_DOUBLE), intent(out)]: |arg_lasttime|
        :p  continuous [INTEGER(C_INT), intent(out)]: |arg_continuous|
        :r calceph_gettimespan: |retfuncfails0|
        :rtype calceph_gettimespan: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_gettimespan (eph, firsttime, lasttime, continuous) 

        :param eph [INTEGER(8), intent(in)]: |arg_eph|
        :p  firsttime [REAL(8), intent(out)]: |arg_firsttime|
        :p  lasttime [REAL(8), intent(out)]: |arg_lasttime|
        :p  continuous [INTEGER, intent(out)]: |arg_continuous|
        :r f90calceph_gettimespan: |retfuncfails0|
        :rtype f90calceph_gettimespan: INTEGER

.. ifconfig:: calcephapi in ('Python')

    .. py:function:: calcephpy.CalcephBin.gettimespan () -> firsttime, lasttime, continuous

        :return:  first and last available time, availability of the quantities of the bodies over the time span
        :rtype: float, float, int

This function returns the first and last time available in the ephemeris file |eph|. The Julian date for the first and last time are expressed in the time scale returned by  |calceph_gettimescale|
. 

It returns the following value in the parameter *continuous* :

  * 1 if the quantities of all bodies are available for any time between the first and last time. 
  * 2 if the quantities of some bodies are available on discontinuous time intervals between the first and last time. 
  * 3 if the quantities of each body are available on a continuous time interval between the first and last time, but not available for any time between the first and last time. 
  

The following example prints the first and last time available in the ephemeris file

.. include:: examples/multiple_gettimespan.rst

.. %------------------------------------------------

|menu_calceph_getpositionrecordcount|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_getpositionrecordcount (t_calcephbin* eph)

        :param  eph: |arg_eph|
        :return: |arg_positionrecordcount|. |retfuncfails0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_getpositionrecordcount (eph) BIND(C)

        :param eph [TYPE(C_PTR), VALUE, intent(in)]: |arg_eph|
        :r calceph_getpositionrecordcount: |arg_positionrecordcount|. |retfuncfails0|
        :rtype calceph_getpositionrecordcount: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_getpositionrecordcount (eph) 

        :param eph [INTEGER(8), intent(in)]: |arg_eph|
        :r f90calceph_getpositionrecordcount: |arg_positionrecordcount|. |retfuncfails0|
        :rtype f90calceph_getpositionrecordcount: INTEGER

.. ifconfig:: calcephapi in ('Python')

    .. py:function:: calcephpy.CalcephBin.getpositionrecordcount ()

        :return:  |arg_positionrecordcount|
        :rtype: int

This function returns the number of position's records available in the ephemeris file |eph|. 
Usually, the number of records is equal to the number of bodies in the ephemeris file if the timespan is continuous. 
If the timespan is discontinuous for the target and center bodies, 
then each different timespan is counted as a different record.
If the ephemeris file contain timescale transformations' records, such as *TT-TDB* or *TCG-TCB*, then these records are included in the returned value.


The following example prints the number of position's records available in the ephemeris file

.. include:: examples/multiple_getpositionrecordcount.rst


.. %------------------------------------------------

|menu_calceph_getpositionrecordindex|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_getpositionrecordindex (t_calcephbin* eph, int index, int* target, int* center, double* firsttime, double* lasttime, int* frame)

        :param  eph: |arg_eph|
        :param  index: |arg_positionrecord_index|
        :param  target: |arg_positionrecord_target|
        :param  center: |arg_positionrecord_center|
        :param  firsttime: |arg_firsttime|
        :param  lasttime: |arg_lasttime|
        :param  frame: |arg_frame|
        :return: |retfuncfails0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_getpositionrecordindex (eph, index, target, center, firsttime, lasttime, frame) BIND(C)

        :param eph [TYPE(C_PTR), VALUE, intent(in)]: |arg_eph|
        :p  index [INTEGER(C_INT), intent(int)]: |arg_positionrecord_index|
        :p  target [INTEGER(C_INT), intent(out)]: |arg_positionrecord_target|
        :p  center [INTEGER(C_INT), intent(out)]: |arg_positionrecord_center|
        :p  firsttime [REAL(C_DOUBLE), intent(out)]: |arg_firsttime|
        :p  lasttime [REAL(C_DOUBLE), intent(out)]: |arg_lasttime|
        :p  frame [INTEGER(C_INT), intent(out)]: |arg_frame|
        :r calceph_getpositionrecordindex: |retfuncfails0|
        :rtype calceph_getpositionrecordindex: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_getpositionrecordindex (eph, index, target, center, firsttime, lasttime, frame) 

        :param eph [INTEGER(8), intent(in)]: |arg_eph|
        :p  index [INTEGER, intent(int)]: |arg_positionrecord_index|
        :p  target [INTEGER, intent(out)]: |arg_positionrecord_target|
        :p  center [INTEGER, intent(out)]: |arg_positionrecord_center|
        :p  firsttime [REAL(8), intent(out)]: |arg_firsttime|
        :p  lasttime [REAL(8), intent(out)]: |arg_lasttime|
        :p  frame [INTEGER, intent(out)]: |arg_frame|
        :r f90calceph_getpositionrecordindex: |retfuncfails0|
        :rtype f90calceph_getpositionrecordindex: INTEGER

.. ifconfig:: calcephapi in ('Python')

    .. py:function:: calcephpy.CalcephBin.getpositionrecordindex (index) -> target, center, firsttime, lasttime, frame

        :param  int index: |arg_positionrecord_index|
        :return:  .. include:: arg_positionrecordindex.rst
        :rtype: int, int, float, float, int

This function returns the target and origin bodies, the first and last time, and the reference frame available at the specified index for the position's records of the ephemeris file |eph|. 
The NAIF identification numbering system is used for the target and center integers (:ref:`NAIF identification numbers` for the list).
The Julian date for the first and last time are expressed in the time scale returned by |calceph_gettimescale|. 

It returns the following value in the parameter *frame* :

+--------+-----------+
| value  | Name      |
+========+===========+
|  1     | ICRF      | 
+--------+-----------+
  

The following example displays the position's records stored in the ephemeris file.

.. include:: examples/multiple_getpositionrecordindex.rst

.. %------------------------------------------------

|menu_calceph_getorientrecordcount|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_getorientrecordcount (t_calcephbin* eph)

        :param  eph: |arg_eph|
        :return: |arg_orientrecordcount|. |retfuncfails0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_getorientrecordcount (eph) BIND(C)

        :param eph [TYPE(C_PTR), VALUE, intent(in)]: |arg_eph|
        :r calceph_getorientrecordcount: |arg_orientrecordcount|. |retfuncfails0|
        :rtype calceph_getorientrecordcount: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_getorientrecordcount (eph) 

        :param eph [INTEGER(8), intent(in)]: |arg_eph|
        :r f90calceph_getorientrecordcount: |arg_orientrecordcount|. |retfuncfails0|
        :rtype f90calceph_getorientrecordcount: INTEGER

.. ifconfig:: calcephapi in ('Python')

    .. py:function:: calcephpy.CalcephBin.getorientrecordcount ()

        :return:  |arg_orientrecordcount|
        :rtype: int

This function returns the number of orientation's records available in the ephemeris file |eph|. 
Usually, the number of records is equal to the number of bodies in the ephemeris file if the timespan is continuous. 
If the timespan is discontinuous for the target body, 
then each different timespan is counted as a different record.


The following example prints the number of orientation's records available in the ephemeris file

.. include:: examples/multiple_getorientrecordcount.rst


.. %------------------------------------------------

|menu_calceph_getorientrecordindex|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    .. c:function:: int calceph_getorientrecordindex (t_calcephbin* eph, int index, int* target, double* firsttime, double* lasttime, int* frame)

        :param  eph: |arg_eph|
        :param  index: |arg_orientrecord_index|
        :param  target: |arg_positionrecord_target|
        :param  firsttime: |arg_firsttime|
        :param  lasttime: |arg_lasttime|
        :param  frame: |arg_frame|
        :return: |retfuncfails0|

.. ifconfig:: calcephapi in ('F2003')

    .. f:function:: calceph_getorientrecordindex (eph, index, target, firsttime, lasttime, frame) BIND(C)

        :param eph [TYPE(C_PTR), VALUE, intent(in)]: |arg_eph|
        :p  index [INTEGER(C_INT), intent(int)]: |arg_orientrecord_index|
        :p  target [INTEGER(C_INT), intent(out)]: |arg_positionrecord_target|
        :p  firsttime [REAL(C_DOUBLE), intent(out)]: |arg_firsttime|
        :p  lasttime [REAL(C_DOUBLE), intent(out)]: |arg_lasttime|
        :p  frame [INTEGER(C_INT), intent(out)]: |arg_frame|
        :r calceph_getorientrecordindex: |retfuncfails0|
        :rtype calceph_getorientrecordindex: INTEGER(C_INT)

.. ifconfig:: calcephapi in ('F90')

    .. f:function:: f90calceph_getpositionrecordindex (eph, index, target, firsttime, lasttime, frame) 

        :param eph [INTEGER(8), intent(in)]: |arg_eph|
        :p  index [INTEGER, intent(int)]: |arg_orientrecord_index|
        :p  target [INTEGER, intent(out)]: |arg_positionrecord_target|
        :p  firsttime [REAL(8), intent(out)]: |arg_firsttime|
        :p  lasttime [REAL(8), intent(out)]: |arg_lasttime|
        :p  frame [INTEGER, intent(out)]: |arg_frame|
        :r f90calceph_getorientrecordindex: |retfuncfails0|
        :rtype f90calceph_getorientrecordindex: INTEGER

.. ifconfig:: calcephapi in ('Python')

    .. py:function:: calcephpy.CalcephBin.getorientrecordindex (index) -> target, firsttime, lasttime, frame

        :param  int index: |arg_orientrecord_index|
        :return:  .. include:: arg_positionrecordindex.rst
        :rtype: int, float, float, int

This function returns the target body, the first and last time, and the reference frame available at the specified index for the orientation's records of the ephemeris file |eph|. 
The NAIF identification numbering system is used for the target body (:ref:`NAIF identification numbers` for the list).
The Julian date for the first and last time are expressed in the time scale returned by |calceph_gettimescale|. 

It returns the following value in the parameter *frame* :

+--------+-----------+
| value  | Name      |
+========+===========+
|  1     | ICRF      | 
+--------+-----------+
  

The following example displays the orientation's records stored in the ephemeris file.

.. include:: examples/multiple_getorientrecordindex.rst

.. %----------------------------------------------------------------------------

|menu_calceph_close|
~~~~~~~~~~~~~~~~~~~~

.. ifconfig:: calcephapi in ('C')

    
    .. c:function:: void calceph_close (t_calcephbin* eph )

        :param  eph: |arg_eph|

.. ifconfig:: calcephapi in ('F2003')

    .. f:subroutine:: calceph_close (eph) BIND(C)

        :param eph [TYPE(C_PTR), VALUE, intent(in)]: |arg_eph|

.. ifconfig:: calcephapi in ('F90')

    .. f:subroutine:: f90calceph_close (eph)

        :param eph [INTEGER(8), intent(in)]: |arg_eph|

.. ifconfig:: calcephapi in ('Python')

    .. py:method:: calcephpy.CalcephBin.close ()

This function closes the access associated to |ephemerisdescriptoreph| and frees allocated memory for it.



