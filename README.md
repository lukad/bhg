# bhg

## Prerequisites

* python2
* [pod](http://appyframework.org/pod.html)
* [LibreOffice](https://www.libreoffice.org/) (for converting the generated odt files to pdfs)
* poppler (for merging the pdfs with pdfunite)

## How-To

1. Define some activities (see `example-input` for reference)
2. Let's do it!

        $ mkdir build && cd build
        $ ../bhg.py -n Luka -l Dornhecker -dFoo -i ../example-input -b 01.08.2011 -e 31.07.2014
		$ ../make-pdf

3. You should now have a file called `out.pdf`
4. Profit
