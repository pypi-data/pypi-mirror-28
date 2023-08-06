.. include:: replace.rst

Miscellaneous functions
=======================

|menu_calceph_getversion_str|
-----------------------------

.. ifconfig:: calcephapi in ('C')

    .. c:function:: void calceph_getversion_str ( char version[CALCEPH_MAX_CONSTANTNAME])

        :param  version: |arg_version|

.. ifconfig:: calcephapi in ('F2003')

    .. f:subroutine:: calceph_getversion_str (version) BIND(C)
    
        :param  version [CHARACTER(len=1,kind=C_CHAR), dimension(CALCEPH_MAX_CONSTANTNAME), intent(out)]: |arg_version|

.. ifconfig:: calcephapi in ('F90')

     .. f:subroutine:: f90calceph_getversion_str (version) 
     
        :param  version [CHARACTER(len=CALCEPH_MAX_CONSTANTNAME), intent(out)]: |arg_version|

.. ifconfig:: calcephapi in ('Python')

    .. py:method:: calcephpy.getversion_str () 
    
        :return: |arg_version|
        :rtype: str 


.. ifconfig:: calcephapi in ('C')

    This function returns the version of the |LIBRARYNAME|, as a null-terminated string.

.. ifconfig:: calcephapi in ('F2003', 'F90', 'Python')

    This function returns the version of the |LIBRARYNAME|, as a string.

.. ifconfig:: calcephapi in ('F90', 'F2003')

    Trailing blanks are added to the name version.


.. ifconfig:: calcephapi in ('C')

    ::
              
        char cversion[CALCEPH_MAX_CONSTANTNAME];
        calceph_getversion_str(cversion);
        printf ("library version is '%s'\n", cversion);


.. ifconfig:: calcephapi in ('F2003')

    ::
              
           character(len=CALCEPH_MAX_CONSTANTNAME) version
           
           call calceph_getversion_str(version)
           write(*,*) 'library version is ', version


.. ifconfig:: calcephapi in ('F90')

    ::

           character(len=CALCEPH_MAX_CONSTANTNAME) version
           
           call f90calceph_getversion_str(version)
           write(*,*) 'library version is ', version


.. ifconfig:: calcephapi in ('Python')

    ::

        from calcephpy import *
        print('version=', getversion_str())



