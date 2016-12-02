#!/bin/sh
sed -n '
/%!/,/beginpage$/p
/\[ \/Rect/,/pdfmark/p
/^endpage/,/%%EOF/p
'
