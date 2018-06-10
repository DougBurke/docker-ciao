#!/bin/bash

if [[ "${ASCDS_INSTALL}" == "" ]] ; then . /opt/ciao-4.10/bin/ciao.bash; fi

echo "***"
echo "*** Starting jupyter notebook, with Python 3 and bash kernels."
echo "*** The Python kernel includes support for CIAO (e.g. pycrates)"
echo "*** as well as some useful Astronomy packages (astropy, scipy,"
echo "*** and matplotlib)."
echo "***"
echo "*** The password is ciaopass"
echo "***"

ciaorun jupyter notebook --ip 0.0.0.0 --no-browser
