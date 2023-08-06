#/*-----------------------------------------------------------------*/
#/*! 
#  \file Makefile.am
#  \brief Makefile for automake
#  \author  M. Gastineau 
#           Astronomie et Systemes Dynamiques, IMCCE, CNRS, Observatoire de Paris. 
#
#   Copyright, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, CNRS
#   email of the author : Mickael.Gastineau@obspm.fr
#  
#*/
#/*-----------------------------------------------------------------*/
#
#/*-----------------------------------------------------------------*/
#/* License  of this file :
#  This file is "triple-licensed", you have to choose one  of the three licenses 
#  below to apply on this file.
#  
#     CeCILL-C
#     	The CeCILL-C license is close to the GNU LGPL.
#     	( http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html )
#  
#  or CeCILL-B
#        The CeCILL-B license is close to the BSD.
#        (http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.txt)
#  
#  or CeCILL v2.1
#       The CeCILL license is compatible with the GNU GPL.
#       ( http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html )
#  
# 
# This library is governed by the CeCILL-C, CeCILL-B or the CeCILL license under 
# French law and abiding by the rules of distribution of free software.  
# You can  use, modify and/ or redistribute the software under the terms 
# of the CeCILL-C,CeCILL-B or CeCILL license as circulated by CEA, CNRS and INRIA  
# at the following URL "http://www.cecill.info". 
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability. 
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and,  more generally, to use and operate it in the 
# same conditions as regards security. 
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL-C,CeCILL-B or CeCILL license and that you accept its terms.
# */
# /*-----------------------------------------------------------------*/

## Makefile.am -- Process this file with automake to produce Makefile.in

AUTOMAKE_OPTIONS = serial-tests 

LDADD = libcalcephtest.la $(top_builddir)/src/libcalceph.la  

AM_CPPFLAGS = -I$(top_srcdir)/src 
AM_FCFLAGS =  $(ax_cv_f90_modflag)$(top_builddir)/src/ -I$(top_srcdir)/src/ -I.
AM_FFLAGS =  $(AM_FCFLAGS)
F77 = $(FC)

check_PROGRAMS = cversion csopenfail cmopenfail  csopen cmopen cmgetconstant csgetconstant cscheck cmcheck \
                 csgetconstantindex cmgetconstantindex $(EXTRAFORTRAN2003CHECK)  $(EXTRAFORTRAN77CHECK) \
                 cmgetconstanttxtpck cmgetconstantindextxtpck cmcheckspk cmcomputeunitfail \
                 cmcomputeunit cmcomputeunit_naifid cmcheckspktt cmorientunitfail matrixfail \
                 tfmatrix cmcomputeunitfail2 checktpc_10086 cmcomputeunit_seg12 cmcomputeunit_seg13  cmcomputeunit_frame \
                 cmorientunitfailspk cmcomputeorder01 cmcomputeorder23 checkcst_11015 cmorientunitfail_11025 \
                 crotangmomunitfail crotangmomunitfail2 crotangmomunit crotangmomorder0 crotangmomorder123 \
                 cmtimescale cstimescale cmtimespan cstimespan cgetpositionrecordindex cgetorientrecordindex

TESTS = $(check_PROGRAMS)

check_LTLIBRARIES = libcalcephtest.la

libcalcephtest_la_SOURCES=openfiles.c numericalderivative.c

noinst_HEADERS = openfiles.h numericalderivative.h

cmcomputeunit_seg12_SOURCES = cmcomputeunit_seg12.c cmcomputeunit_hermite.c
cmcomputeunit_seg13_SOURCES = cmcomputeunit_seg13.c cmcomputeunit_hermite.c
cmcomputeunit_frame_SOURCES = cmcomputeunit_frame.c cmcomputeunit_hermite.c

## if we add programs to EXTRA_PROGRAMS, update the file configure.ac !
EXTRA_PROGRAMS = f2003sopenfail f2003mopenfail f2003sopen  f2003mopen f2003sgetconstant \
                 f2003mgetconstant f2003mcheck f2003sgetconstantindex f2003mgetconstantindex \
                 f2003mcomputeunit f2003mcomputeunit_naifid f2003version \
                 f2003mcomputeorder f2003rotangmomunit f2003rotangmomorder \
                 f2003mtimescale f2003mtimespan f2003stimescale f2003stimespan  \
                 f2003getpositionrecordindex f2003getorientrecordindex \
                 f77sopenfail f77mopenfail f77sopen  f77mopen f77sgetconstant \
                 f77mgetconstant f77mcheck f77sgetconstantindex f77mgetconstantindex \
                 f77mcomputeunit  f77mcomputeunit_naifid f77version \
                 f77mcomputeorder f77rotangmomunit f77rotangmomorder \
                 f77mtimescale f77mtimespan f77stimescale f77stimespan  \
                 f77getpositionrecordindex f77getorientrecordindex

f2003sopenfail_SOURCES = f2003sopenfail.f
f2003mopenfail_SOURCES = f2003mopenfail.f
f2003sopen_SOURCES = f2003sopen.f
f2003mopen_SOURCES = f2003mopen.f
f2003sgetconstant_SOURCES = f2003sgetconstant.f
f2003mgetconstant_SOURCES = f2003mgetconstant.f
f2003mcheck_SOURCES = f2003mcheck.f
f2003sgetconstantindex_SOURCES = f2003sgetconstantindex.f
f2003mgetconstantindex_SOURCES = f2003mgetconstantindex.f
f2003mcomputeunit_SOURCES = f2003mcomputeunit.f
f2003mcomputeunit_naifid_SOURCES = f2003mcomputeunit_naifid.f
f2003version_SOURCES = f2003version.f
f2003mcomputeorder_SOURCES = f2003mcomputeorder.f
f2003rotangmomunit_SOURCES = f2003rotangmomunit.f
f2003rotangmomorder_SOURCES = f2003rotangmomorder.f
f2003mtimescale_SOURCES = f2003mtimescale.f
f2003stimescale_SOURCES = f2003stimescale.f
f2003mtimespan_SOURCES = f2003mtimespan.f
f2003stimespan_SOURCES = f2003stimespan.f
f2003getpositionrecordindex_SOURCES = f2003getpositionrecordindex.f
f2003getorientrecordindex_SOURCES = f2003getorientrecordindex.f
f77sopenfail_SOURCES = f77sopenfail.f
f77mopenfail_SOURCES = f77mopenfail.f
f77sopen_SOURCES = f77sopen.f
f77mopen_SOURCES = f77mopen.f
f77sgetconstant_SOURCES = f77sgetconstant.f
f77mgetconstant_SOURCES = f77mgetconstant.f
f77mcheck_SOURCES = f77mcheck.f
f77sgetconstantindex_SOURCES = f77sgetconstantindex.f
f77mgetconstantindex_SOURCES = f77mgetconstantindex.f
f77mcomputeunit_SOURCES = f77mcomputeunit.f
f77mcomputeunit_naifid_SOURCES = f77mcomputeunit_naifid.f
f77version_SOURCES = f77version.f
f77mcomputeorder_SOURCES = f77mcomputeorder.f
f77rotangmomunit_SOURCES = f77rotangmomunit.f
f77rotangmomorder_SOURCES = f77rotangmomorder.f
f77mtimescale_SOURCES = f77mtimescale.f
f77stimescale_SOURCES = f77stimescale.f
f77mtimespan_SOURCES = f77mtimespan.f
f77stimespan_SOURCES = f77stimespan.f
f77getpositionrecordindex_SOURCES = f77getpositionrecordindex.f
f77getorientrecordindex_SOURCES = f77getorientrecordindex.f

EXTRA_DIST = Makefile.vc Makefile.mingw example1_tests.dat  example1_tt.dat example1_tests_naifid.dat \
 invalidmatrix1.tf invalidmatrix2.tf matrix3.tf checktpc_10086.tpc example1spk_seg12.bsp example1spk_seg12.txt \
 example1spk_seg13.bsp example1spk_seg13.txt example1spk_frame.bsp example1spk_frame.tf example1spk_frame.txt \
 fopenfiles.vc example2_rotangmom_tests.dat
 
clean-local:
	@rm -f example1_tests_23_derivative.dat

distclean-local:
	@rm -f example1_tests_23_derivative.dat


