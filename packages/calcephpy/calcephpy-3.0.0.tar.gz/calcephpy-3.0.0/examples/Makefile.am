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
LDADD = $(top_builddir)/src/libcalceph.la


AM_CPPFLAGS = -I$(top_srcdir)/src
AM_FCFLAGS =  $(ax_cv_f90_modflag)$(top_builddir)/src/ -I$(top_srcdir)/src/
AM_FFLAGS =  $(AM_FCFLAGS)
F77 = $(FC)

noinst_PROGRAMS = csingle cmultiple cscompute cerror corder corient $(EXTRAFORTRAN2003EXAMPLES) $(EXTRAFORTRAN77EXAMPLES)

EXTRA_PROGRAMS = f2003single f2003multiple f2003scompute f2003error f2003orient f77single f77multiple f77error f77orient

f2003single_SOURCES = f2003single.f
f2003multiple_SOURCES = f2003multiple.f
f2003scompute_SOURCES = f2003scompute.f
f2003error_SOURCES = f2003error.f
f2003orient_SOURCES = f2003orient.f
f77single_SOURCES = f77single.f
f77multiple_SOURCES = f77multiple.f
f77error_SOURCES = f77error.f
f77orient_SOURCES = f77orient.f

EXTRA_DIST = Makefile.vc Makefile.mingw readme.txt example1.dat example1.bsp example1.tpc example1.mk \
 example1.bpc example1.tf example1spk_time.bsp pycompute.py pymultiple.py pyerror.py \
 example2_rotangmom.dat pyorient.py
 
