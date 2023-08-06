dnl /*-----------------------------------------------------------------*/
dnl /*! 
dnl   @synopsis ax_f2003_iso_c_binding.m4
dnl @category Fortran
dnl   \brief ACX_C_PRECISEFLOAT
dnl Check if the fortran compiler supports the ISO_C_BINDING module defiend by the fortran 2003 standard.
dnl The cache variable ax_f2003_iso_c_binding is defined to yes or no.
dnl extension cannot be found.
dnl
dnl   @author Mickael Gastineau <Mickael.Gastineau@obspm.fr>
dnl            Astronomie et Systemes Dynamiques, IMCCE, CNRS, Observatoire de Paris. 
dnl 
dnl @version 2017/02/20
dnl    Copyright, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, CNRS
dnl    email of the author : Mickael.Gastineau@obspm.fr
dnl   
dnl */
dnl /*-----------------------------------------------------------------*/
dnl 
dnl /*-----------------------------------------------------------------*/
dnl /* License  of this file :
dnl This file is "triple-licensed", you have to choose one  of the three licenses
dnl below to apply on this file.
dnl
dnl     CeCILL-C
dnl      The CeCILL-C license is close to the GNU LGPL.
dnl      ( http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html )
dnl
dnl  or CeCILL-B
dnl      The CeCILL-B license is close to the BSD.
dnl      (http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.txt)
dnl
dnl  or CeCILL v2.1
dnl      The CeCILL license is compatible with the GNU GPL.
dnl      ( http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html )
dnl
dnl
dnl  This library is governed by the CeCILL-C, CeCILL-B or the CeCILL license under
dnl  French law and abiding by the rules of distribution of free software.
dnl  You can  use, modify and/ or redistribute the software under the terms
dnl  of the CeCILL-C or CeCILL license as circulated by CEA, CNRS and INRIA
dnl  at the following URL "http://www.cecill.info".
dnl
dnl  As a counterpart to the access to the source code and  rights to copy,
dnl  modify and redistribute granted by the license, users are provided only
dnl  with a limited warranty  and the software's author,  the holder of the
dnl  economic rights,  and the successive licensors  have only  limited
dnl  liability.
dnl
dnl  In this respect, the user's attention is drawn to the risks associated
dnl  with loading,  using,  modifying and/or developing or reproducing the
dnl  software by the user in light of its specific status of free software,
dnl  that may mean  that it is complicated to manipulate,  and  that  also
dnl  therefore means  that it is reserved for developers  and  experienced
dnl  professionals having in-depth computer knowledge. Users are therefore
dnl  encouraged to load and test the software's suitability as regards their
dnl  requirements in conditions enabling the security of their systems and/or
dnl  data to be ensured and,  more generally, to use and operate it in the
dnl  same conditions as regards security.
dnl
dnl  The fact that you are presently reading this means that you have had
dnl  knowledge of the CeCILL-C, CeCILL-B or CeCILL license and that you accept its terms.
dnl  */
dnl /*-----------------------------------------------------------------*/


AC_DEFUN([AX_F2003_ISO_C_BINDING],[
AC_CACHE_CHECK([fortran 2003 ISO_C_BINDING module],
ax_cv_f2003_iso_c_binding,
[AC_LANG_PUSH(Fortran)
i=0
while test \( -f tmpdir_$i \) -o \( -d tmpdir_$i \) ; do
  i=`expr $i + 1`
done
mkdir tmpdir_$i
cd tmpdir_$i
AC_COMPILE_IFELSE([          module modtestisoc
          interface
          FUNCTION testisoc(eph,time) BIND(C)
          USE, INTRINSIC :: ISO_C_BINDING
          IMPLICIT NONE
          INTEGER(C_INT), VALUE, intent(in) :: eph
          TYPE(C_PTR), VALUE, intent(in) :: time
          REAL(C_DOUBLE) :: testisoc
       END FUNCTION testisoc
       end interface
       end module modtestisoc
],
  [ax_cv_f2003_iso_c_binding=yes],
  [ax_cv_f2003_iso_c_binding=no])
cd ..
rm -fr tmpdir_$i
AC_LANG_POP(Fortran)
])])