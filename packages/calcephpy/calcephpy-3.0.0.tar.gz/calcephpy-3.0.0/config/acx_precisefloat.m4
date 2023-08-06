dnl /*-----------------------------------------------------------------*/
dnl /*! 
dnl   \fileacx_precisefloat.m4
dnl   \brief ACX_C_PRECISEFLOAT
dnl      This macro determines whether the C compiler supports options 
dnl      to respect the IEEE754 norm and precise computations
dnl   \author Mickael Gastineau <Mickael.Gastineau@obspm.fr>
dnl            Astronomie et Systemes Dynamiques, IMCCE, CNRS, Observatoire de Paris. 
dnl 
dnl \version 2017/02/20
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

dnl @synopsis ACX_C_PRECISEFLOAT

AC_DEFUN([ACX_C_PRECISEFLOAT],
[
  AC_MSG_CHECKING(for IEEE754 norm and precise computations flags)
  is_havePRECISEFLOATflags=no

  #intel compiler : add : -fp-model strict
  AC_EGREP_CPP(yes,
   [#if __INTEL_COMPILER>=900
      yes
    #endif
   ], 
   CPPFLAGS="$CPPFLAGS -fp-model strict"
   is_havePRECISEFLOATflags=yes
   AC_MSG_RESULT([-fp-model strict]))


  if test $is_havePRECISEFLOATflags = no;  then
   AC_MSG_RESULT([])
  fi

])

