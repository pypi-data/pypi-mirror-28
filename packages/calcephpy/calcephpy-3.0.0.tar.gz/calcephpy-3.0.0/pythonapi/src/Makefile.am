# /*-----------------------------------------------------------------*/
#/*!
#  \file Makefile.am
#  \brief Makefile for automake
#  \author  M. Gastineau
#           Astronomie et Systemes Dynamiques, IMCCE, CNRS, Observatoire de Paris.
#
#   Copyright, 2016, 2017, CNRS
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

pyexec_LTLIBRARIES = calcephpy.la

calcephpy_la_SOURCES = calcephpy.c
calcephpy_la_LDFLAGS = -avoid-version -module $(PYTHON_LIBS)  -shared
calcephpy_la_LIBADD = $(top_builddir)/src/libcalcephnoinst.la
calcephpy_la_CPPFLAGS = $(PYTHON_CPPFLAGS) -I$(top_srcdir)/src
EXTRA_DIST = calcephpy.pyx calcephpy.pxd calcephpy.c Makefile.mingw


#specific rules to generate the file calcephpy.c
#the developer must call: make pythonapi

pythonapi:
	CC="$(CC) $(CFLAGS)" $(PYTHON) setup.py build_ext -i


# /*-----------------------------------------------------------------*/
# installation to system and/or user site-package directory
# /*-----------------------------------------------------------------*/
if COND_PYTHON_PACKAGE_SYSTEM
   MAYBE_PYTHONAPI_INSTALL_SYSTEM = install_pythonapi_system
   MAYBE_PYTHONAPI_UNINSTALL_SYSTEM = uninstall_pythonapi_system
else
   MAYBE_PYTHONAPI_INSTALL_SYSTEM =
   MAYBE_PYTHONAPI_UNINSTALL_SYSTEM =
endif

if COND_PYTHON_PACKAGE_USER
   MAYBE_PYTHONAPI_INSTALL_USER = install_pythonapi_user
   MAYBE_PYTHONAPI_UNINSTALL_USER = uninstall_pythonapi_user
   PYTHON_USER_SITE_PKG = `$(PYTHON) -m site --user-site`
else
   MAYBE_PYTHONAPI_INSTALL_USER =
   MAYBE_PYTHONAPI_UNINSTALL_USER =
   PYTHON_USER_SITE_PKG =
endif

install-exec-hook: $(MAYBE_PYTHONAPI_INSTALL_SYSTEM)  $(MAYBE_PYTHONAPI_INSTALL_USER)

#uninstall-hook: $(MAYBE_PYTHONAPI_UNINSTALL_SYSTEM)  $(MAYBE_PYTHONAPI_UNINSTALL_USER)


install_pythonapi_system:
	test -n "$(PYTHON_SITE_PKG)" && test -d "$(PYTHON_SITE_PKG)" && for c in `ls $(DESTDIR)$(pyexecdir)` ; do echo $$c ; $(LN_S) -f $(DESTDIR)$(pyexecdir)/$$c $(PYTHON_SITE_PKG)/$$c; done

install_pythonapi_user:
	echo installing in $(PYTHON_USER_SITE_PKG)
	$(INSTALL) -d  $(PYTHON_USER_SITE_PKG)
	test -n "$(PYTHON_USER_SITE_PKG)" && for c in `ls $(DESTDIR)$(pyexecdir)` ; do echo $$c ; $(LN_S) -f $(DESTDIR)$(pyexecdir)/$$c $(PYTHON_USER_SITE_PKG)/$$c; done


#uninstall_pythonapi_system:
#	for c in `ls $(DESTDIR)$(pyexecdir)` ; do echo $$c ; rm -f $(PYTHON_SITE_PKG)/$$c; done

#uninstall_pythonapi_user:
#	for c in `ls $(DESTDIR)$(pyexecdir)` ; do echo $$c ; rm -f $(PYTHON_USER_SITE_PKG)/$$c; done


#install_pythonapi_system:
#	CC="$(CC) $(CFLAGS)" $(PYTHON) setup.py build_ext install

#install_pythonapi_user:
#	CC="$(CC) $(CFLAGS)" $(PYTHON) setup.py build_ext install --user

clean-local:
	rm -r -f build
