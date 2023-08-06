.. include:: replace.rst

Error functions
===============

The following group of functions defines the behavior of the library when errors occur during the execution. 


.. %----------------------------------------------------------------------------

Usage
-----

The following examples, that can be found in the directory *examples* of the library sources, show the typical usage of this group of functions. 

.. ifconfig:: calcephapi in ('C')

    The example in C language is :file:`cerror.c`. 
    
.. ifconfig:: calcephapi in ('F2003')

    The example in Fortran 2003 language is :file:`f2003error.f`.
    
.. ifconfig:: calcephapi in ('F90')

    The example in Fortran 77/90/95 language is :file:`f77error.f`.

.. ifconfig:: calcephapi in ('Python')

    The example in Python language is :file:`pyerror.py`.

.. include:: examples/error_usage.rst


.. %----------------------------------------------------------------------------

|menu_calceph_seterrorhandler|
------------------------------

.. ifconfig:: calcephapi in ('C')

    .. c:function:: void calceph_seterrorhandler (int typehandler, void (*userfunc)(const char*) )

        :param  typehandler: |arg_typehandler|
        :param  userfunc: |arg_userfunc|

.. ifconfig:: calcephapi in ('F2003')

    .. f:subroutine:: calceph_seterrorhandler (typehandler, userfunc ) BIND(C)

        :param  typehandler [TYPE(C_INT), VALUE, intent(in)]: |arg_typehandler|
        :param  userfunc [TYPE(C_FUNPTR), VALUE, intent(in)]: |arg_userfunc|

.. ifconfig:: calcephapi in ('F90')

    .. f:subroutine:: f90calceph_seterrorhandler (typehandler, userfunc)

        :param  typehandler [INTEGER, intent(in)]: |arg_typehandler|
        :param  userfunc [EXTERNAL, intent(in)]: |arg_userfunc|


.. ifconfig:: calcephapi in ('Python')

    .. py:method:: calcephpy.seterrorhandler (typehandler, userfunc) 

        :param  int typehandler: |arg_typehandler|
        :param  function userfunc: |arg_userfunc|

This function defines the behavior of the library when an error occurs during the execution of the library's functions. This function should be (not mandatory) called before any other functions of the library. The behavior depends on the value of *typehandler*. 

The possible values for *typehandler* are  :

+-------+---------------------------------------------------------------------------------------+
| value | meaning                                                                               |
+=======+=======================================================================================+
| 1     | | The library displays a message and continues the execution.                         |
|       | | The functions return an error code. The python interface raises an exception.       |
|       | | This is the default behavior of the library.                                        |
+-------+---------------------------------------------------------------------------------------+
| 2     | | The library displays a message                                                      |
|       | | and terminates the execution with a system call to thefunction *exit*.              |
+-------+---------------------------------------------------------------------------------------+
| 3     | | The library calls the user function *userfunc* with the message.                    |
+-------+---------------------------------------------------------------------------------------+

.. ifconfig:: calcephapi in ('C')

    If the function is called with 1 or 2 for *typehandler*, the parameter *userfunc* must be set to *NULL*.

.. ifconfig:: calcephapi in ('F2003')

    If the function is called with 1 or 2 for *typehandler*, the parameter *userfunc* must be set to *C_NULL_FUNPTR*.
    
    The function *userfunc* must be defined as 
    
    ::

        subroutine userfunc (msg, msglen)  BIND(C)
        USE, INTRINSIC :: ISO_C_BINDING
        implicit none
        CHARACTER(kind=C_CHAR), dimension(msglen), intent(in) :: msg
        INTEGER(C_INT), VALUE, intent(in) :: msglen

    This function must have an explicit interface. 

.. ifconfig:: calcephapi in ('F90')

    If the function is called with 1 or 2 for *typehandler*, the parameter *userfunc* must be set to *0*.

    The function *userfunc* must be defined as 

    ::

        subroutine userfunc (msg) 
        implicit none
        CHARACTER(len=*), intent(in) :: msg

    This function must be declared as **EXTERNAL**

.. ifconfig:: calcephapi in ('Python')

    If the function is called with 1 or 2 for *typehandler*, the parameter *userfunc* must be set to *0*.


    The function *userfunc* must be defined as 
    
    ::
    
        def userfunc (msg)
        # parameter msg is of type str

