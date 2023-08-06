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
# to generate the documentation : run the script makedoc.sh
 
AUTOMAKE_OPTIONS = no-texinfo.tex
AM_MAKEINFOFLAGS= --no-split

include Makefile_listdoc.am

#$(PACKAGE)/

calcephpdfdir = $(docdir)
calcephpdf_DATA = calceph_c.pdf calceph_fortran2003.pdf calceph_fortran77.pdf  calceph_python.pdf

calcephhtmldir = $(htmldir)
nobase_calcephhtml_DATA =   $(LISTFILEHTML)

EXTRA_DIST =   $(calcephpdf_DATA) $(nobase_calcephhtml_DATA) makedoc.sh Makefile.vc Makefile.mingw Makefile.sphinx \
  source/confcommon.py	source_c/conf.py	source_f2003/conf.py	source_f9x/conf.py	source_python/conf.py \
  source/_templates/layout.html \
source/arg_PV.rst				source/calceph.interface.cusage.rst \
source/arg_PVAJ_order.rst			source/calceph.interface.f2003usage.rst \
source/arg_PVAJ_orient_order.rst		source/calceph.interface.f9xusage.rst \
source/arg_PV_orient_unit.rst			source/calceph.interface.pythonusage.rst \
source/arg_PV_unit.rst				source/calceph.interface.rst \
source/arg_order.rst				source/calceph.intro.rst \
source/arg_order_orient.rst			source/calceph.misc.rst \
source/arg_unit.rst				source/calceph.multiple.rst \
source/arg_unit_order.rst			source/calceph.naifid.rst \
source/arg_unit_orient_unit.rst			source/calceph.reportbugs.rst \
source/calceph.copying.rst			source/index.rst \
source/calceph.error.rst			source/confcommon.py \
source/calceph.final.rst			source/confcommon.py.in \
source/calceph.install.rst			source/replace.rst \
source/condsingle/calceph.single.rst		source/condsingle/single_sgetconstant.rst \
source/condsingle/single_prog.rst		source/condsingle/single_sgetconstantcount.rst \
source/condsingle/single_scompute.rst		source/condsingle/single_sgetconstantindex.rst \
source/condsingle/single_sgettimescale.rst  source/condsingle/single_sgettimespan.rst \
source/examples/error_usage.rst			source/examples/multiple_getconstantcount.rst \
source/examples/multiple_compute.rst		source/examples/multiple_getconstantindex.rst \
source/examples/multiple_compute_order.rst	source/examples/multiple_open_array.rst \
source/examples/multiple_compute_unit.rst	source/examples/multiple_orient_order.rst \
source/examples/multiple_getconstant.rst	source/examples/multiple_orient_unit.rst \
  source/examples/simple_program.rst    source/examples/multiple_gettimespan.rst \
  source/examples/multiple_gettimescale.rst source/arg_positionrecordindex.rst
  

  

