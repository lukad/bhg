#!/usr/bin/sh

libreoffice --headless --convert-to pdf *.odt
pdfunite *.pdf out.pdf
