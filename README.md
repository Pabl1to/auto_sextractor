# auto_sextractor
run sextractor by a automatic mode
To run autosex.py you have to add some paths in you .bashrc, These are:
$ AUTOSEXPATH="/home/path/to/autosex"  
$ PYTHONPATH="$AUTOSEXPATH:PYTHONPATH
$ export PYTHONPATH
Also you can create an alias:
$ alias autosex="python $AUTOSEXPATH/autosex.py

In the prog.py file you can notice that it runs sextractor by the command "sex" so, you have to create a simbolic link to this
command if it is necesary. It is:
$ su ....
$ cd /usr/bin
$ ln -sf sextractor sex
And it is all.
This program use sextractor and some python libraries (numpy,matplotlib,os (by defaul) and pyfits)

If you didn't like the default configuration of sextractor, you can modified it. You can find the ".sex" files in 
"/path/to/autosex/conf". In this directory also you can find the ".param" files. But you haven't to modified the following
configurations:
CATALOG_NAME
CATALOG_TYPE (for the firts "run" of sextractor)
WEIGHT_TYPE
WEIGHT_IMAGE
MAG_ZEROPOINT
GAIN
CHECKIMAGE_NAME
ASSOC_NAME (for assoc mode)
PSF_NAME

Enjoy it!
