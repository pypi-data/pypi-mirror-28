Release notes
=============
 * Version 3.0.0 
    | Update the license CeCILL v2.0 to CeCILL v2.1.
    | Fix a decode error for SPICE kernels with a big-endian format.
    | Add the function calceph_gettimescale and calceph_gettimespan.
    | Add the function calceph_getpositionrecordcount and calceph_getpositionrecordindex.
    | Add the function calceph_getorientrecordcount and calceph_getorientrecordindex.
    | Add the function calceph_sgettimescale and calceph_sgettimespan.
    | Support INPOP file format 3.0 (add angular momentum due to the rotation in the binary file).
    | Use sphinx-doc to produce the documentation.

 * Version 2.3.2
    | Fix the return value of the function calceph_getconstant if the constant name "AU" or "EMRAT" is not available.
    | Fix the documentation for the fortran interface of the function calceph_prefetch.
    | Fix the return value of the function calceph_orient_unit if the frame SPICE kernel file is missing.

 * Version 2.3.1
    | Fix the compilation warnings with the Pelles compiler.
    | Fix the compilation warnings with the C89 standard.
    | Fix the compilation warnings with the GNU C compilers.
    | Fix the documentation for the constant CALCEPH_VERSION_STRING.

 * Version 2.3.0
    | Add the python interface compliant with python 2.6+ and python 3.
    | Add the preprocessor macro CALCEPH_VERSION_STRING.
    | Add the function calceph_getversion_str.
    | Add the function calceph_compute_order and calceph_orient_order.
    | Fix the return value of the functions calceph_compute_xxx when the reference frame is not available in the spice kernel files.
    | The function should produce an error  and return 0 (before the function performed no computation but it returned 1).

 * Version 2.2.5
    | Fix an incorrect result if CALCEPH_UNIT_DAY is provided to calceph_compute_unit and the target is TCG-TCB or TT-TDB.
    | Support the numerical constants declared without parenthesis in the text kernel files (.tpc).
    | Support the segment 1, 12 and 13 in the SPICE kernel file.

 * Version 2.2.4
    | Update the version number of the dynamic library.


 * Version 2.2.3
    | Add the predefined constants for calceph version in the fortran interface.
    | Fix the build chain if calceph is compiled from another folder.

 * Version 2.2.2
    | Support the compilation in the standard C89.


 * Version 2.2.1
    | Remove debug informations that are printed when errors occur in calceph\_?compute\_???.
    | Support the Portland compilers.
    | Fix the info documentation.
    | Report an error if no asteroid is available in an ephemeris file with the INPOP file format (instead of a crash).

 * Version 2.2.0
    | Support the new segments  20, 102, 103 and 120 in the SPICE kernel file.
    | Support the NAIF identification numbers.
    | Add the functions calceph_orient_unit and calceph_prefetch.

 * Version 2.1.0
    | Fix a bug in calceph_getconstant and calceph_sgetconstant with an invalid name
    | Remove the null character in the name of the constant returned by the function (f90)calceph_(s)getconstantindex when the Fortran interface is used.


 * Version 2.0.0
    | Fix memory leaks in calceph_open when errors occur.
    | Support INPOP file format 2.0 (supports TCB ephemeris file and add asteroids in the binary file).
    | Add the function calceph_open_array and calceph_compute_unit.
    | Add the tools calceph_inspector to show details about ephemeris file.
    | Support SPICE kernel file (SPK with segment 2 or 3, text and binary PCK, meta kernel, basic frame kernel).
    | Improve the performances.
    | Correct the Fortran 2003 interface for calceph_sgetconstantindex.
    | Add the constant 17 to get TCG-TCB from TCB ephemeris file.


 * Version 1.2.0
    |  Change the licensing : triple licenses to support integration in BSD software.
    |  Remove explicit dependencies on the record size for DExxx.


 * Version 1.1.2
    |  Fix a compilation warning with oracle studio compiler 12.
    |  Fix a bug with gcc on solaris in 64 bit mode.
    |  Fix the copyright statements.


 * Version 1.1.1
    |  Fix a compilation error in util.h  and a warning with the sun studio compilers.


 * Version 1.1.0
    |  Add the function calceph_seterrorhandler for the custom error handlers.


 * Version 1.0.3
    |  Support the JPL ephemeris file DE423.


 * Version 1.0.2
    | Fix memory leaks in the fortran-90 interface.

 * Version 1.0.1
    | Support the large ephemeris files (>2GB) on 32-bit operating systems.
    | Fix the documentation of the function f90calceph_sopen.
    | Fix an invalid open mode on Windows operating systems.
    | Report accurately the I/O errors.

 * Version 1.0.0
    | Initial release.


