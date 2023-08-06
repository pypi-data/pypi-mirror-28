CALCEPH library
===============           

Description
-----------

This  is  a  release  of the  CALCEPH library.  This library  is
developed  in the "Astronomy and Dynamical System" team
at  Observatoire de Paris-IMCCE-CNRS-UPMC (PARIS).  The contact
email is inpop.imcce@obspm.fr .

This library is available at :  http://www.imcce.fr/inpop/calceph

This library is designed to access and interpolate INPOP and JPL Ephemeris data.
The sources needed to build the CALCPEPH library are in the directory src.


The library is "triple-licensed" (CeCILL-C,CeCILL-B or CeCILL),
you have to choose one of the three licenses  below to apply on the library.
  
  CeCILL-C

	The CeCILL-C license is close to the GNU LGPL.
    ( http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html or COPYING_CECILL_C.LIB)
 
or  
   CeCILL-B
    The CeCILL-B license is close to the BSD.
    (http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.txt)

or  
   CeCILL v2.1
    The CeCILL license is compatible with the GNU GPL.
    ( http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html or COPYING_CECILL_V2.1.LIB)
    
Installation
------------
To compile and use this library, 
please refer to the detailed documentation calceph.pdf in the directory "doc" 
or to the section "Installation" of the website http://www.imcce.fr/inpop/calceph

Simplified installation notes :
 On a Unix-like system (Linux, Mac OS X, BSD, cygwin, ...), 
 execute the following statements to install your library in the default directory  /usr/local 
         ./configure --disable-shared --enable-python=yes
         make 
         make check
         make install

 On a Windows system with the Windows SDK, 
 execute the following statements to install your library in the  directory C:\CALCEPH
        nmake /f Makefile.vc
        nmake /f Makefile.vc check
        nmake /f Makefile.vc install DESTDIR=C:\CALCEPH

 Source installation with Pip for python developers,
 it is possible to build and install the latest CALCPEPH library with pip

    pip install --user calcephpy
    
 if you have administrative rights on the computer, you can do
    pip install  calcephpy
    
 if you have installed with pip, you can keep your installation up to date by upgrading :
    pip install --user --upgrade calcephpy