#! /bin/bash

CMD_MAKE_SPHINX="make -f Makefile.sphinx"
SPHINX_BUILD_HTML="sphinx-build -b html -d build/doctrees"

find html -not -path '*.svn*' -exec rm -f {} \;
rm -r -f  calceph_*.pdf

$CMD_MAKE_SPHINX clean
$SPHINX_BUILD_HTML -c source_c source html/c || exit 1

$CMD_MAKE_SPHINX clean
$SPHINX_BUILD_HTML -c source_f2003 source html/fortran2003|| exit 1

$CMD_MAKE_SPHINX clean
$SPHINX_BUILD_HTML -c source_f9x source html/fortran77 || exit 1
 
$CMD_MAKE_SPHINX clean
$SPHINX_BUILD_HTML -c source_python source html/python || exit 1

$CMD_MAKE_SPHINX clean
$CMD_MAKE_SPHINX latexpdf SPHINXOPTS="-c source_c" && mv build/latex/calceph.pdf calceph_c.pdf || exit 1

$CMD_MAKE_SPHINX clean
$CMD_MAKE_SPHINX latexpdf SPHINXOPTS="-c source_f2003" && mv build/latex/calceph.pdf calceph_fortran2003.pdf || exit 1

$CMD_MAKE_SPHINX clean
$CMD_MAKE_SPHINX latexpdf SPHINXOPTS="-c source_f9x" && mv build/latex/calceph.pdf calceph_fortran77.pdf || exit 1
 
$CMD_MAKE_SPHINX clean
$CMD_MAKE_SPHINX latexpdf SPHINXOPTS="-c source_python" && mv build/latex/calceph.pdf calceph_python.pdf || exit 1


$CMD_MAKE_SPHINX clean

FILELIST=`find html -name \*.\* -print` 
echo 'LISTFILEHTML='$FILELIST >Makefile_listdoc.am

# suppression des index inutiles en html : 
#pour le C
HTMLSRC=html/c/genindex.html
SEARCHSRC=html/c/searchindex.js 
perl -p -i -e 's/a>\n/a>/' $HTMLSRC
grep -v fortran $HTMLSRC | grep -v 'built-in' | grep -v calcephpy >tmpfile && mv tmpfile $HTMLSRC
perl -p -i -e 's/"f\/_\/([^]])*]\,//g' $SEARCHSRC

#pour le fortran 2003
HTMLSRC=html/fortran2003/genindex.html
SEARCHSRC=html/fortran2003/searchindex.js 
perl -p -i -e 's/a>\n/a>/' $HTMLSRC
grep -v '(C ' $HTMLSRC | grep -v 'built-in' |  grep -v 'f90' |grep -v calcephpy >tmpfile && mv tmpfile $HTMLSRC
sed -i  -e 's/<a\(.*\)\_\/\(.*\)"><strong>(fortran variable)/<a\1\_\/\2"><strong>\2 \(fortran variable\)/g'  $HTMLSRC
perl -p -i -e 's/"f\/_\/f90([^]])*]\,//g' $SEARCHSRC

#pour le fortran 77
HTMLSRC=html/fortran77/genindex.html
SEARCHSRC=html/fortran77/searchindex.js 
perl -p -i -e 's/a>\n/a>/' $HTMLSRC
grep -v '(C ' $HTMLSRC | grep -v 'built-in' | grep -v calcephpy | grep -v '#f/_/calceph_' >tmpfile && mv tmpfile $HTMLSRC
sed -i  -e 's/<a\(.*\)\_\/\(.*\)"><strong>(fortran variable)/<a\1\_\/\2"><strong>\2 \(fortran variable\)/g'  $HTMLSRC

#pour le python
HTMLSRC=html/python/genindex.html
SEARCHSRC=html/python/searchindex.js 
perl -p -i -e 's/a>\n/a>/' $HTMLSRC
grep -v fortran $HTMLSRC | grep -v '(C '  >tmpfile && mv tmpfile $HTMLSRC
perl -p -i -e 's/"f\/_\/([^]])*]\,//g' $SEARCHSRC

echo 'Generating the documentation.....ok'

exit  0

#unused code
perl -p -i -e 's/<li.*fortran.*\n/FORTRAN/g' $HTMLSRC 
perl -p -i -e 's/FORTRAN<\/li>//g'    $HTMLSRC  
perl -p  -i -e 's/<dt.*fortran subroutine([^d])*dt>//g' $HTMLSRC 
perl -p -i -e 's/FORTRAN<\/li>//g'    $HTMLSRC  
perl -p -i -e 's/<li.*built-in.*\n/PYTHON/g'   $HTMLSRC 
perl -p -i -e 's/PYTHON<\/li>//g'   $HTMLSRC  
perl -p -i -e 's/<li.*calcephpy.*\n/PYTHON/g'  $HTMLSRC 
perl -p -i -e 's/PYTHON<\/li>//g'  $HTMLSRC  

perl -p -i -e 's/<a.*C macro.*a>//g' $HTMLSRC 
perl -p -i -e 's/<li.*\(C .*\n/LANGUAGEC/g' $HTMLSRC 
perl -p -i -e 's/LANGUAGEC<\/li>//g'    $HTMLSRC
perl -p -i -e 's/<li.*built-in.*\n/PYTHON/g'   $HTMLSRC 
perl -p -i -e 's/PYTHON<\/li>//g'   $HTMLSRC  
perl -p -i -e 's/<li.*calcephpy.*\n/PYTHON/g'  $HTMLSRC 
perl -p -i -e 's/PYTHON<\/li>//g'  $HTMLSRC  

perl -p -i -e 's/<a.*C macro.*a>//g' $HTMLSRC 
perl -p -i -e 's/<li.*\(C .*\n/LANGUAGEC/g' $HTMLSRC 
perl -p -i -e 's/LANGUAGEC<\/li>//g'    $HTMLSRC
perl -p -i -e 's/<li.*fortran.*\n/FORTRAN/g' $HTMLSRC 
perl -p -i -e 's/FORTRAN<\/li>//g'    $HTMLSRC  
