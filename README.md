# Fun with Docker and CIAO

Here are some (well, *two*) experiments in combining
[Docker](https://docs.docker.com/) with
[CIAO](http://cxc.harvard.edu/ciao/). It is:

- very much an experimental set up,
- comes with no warranty,
- is poorly documented,
- is not guaranteed to be kept up to date,
- and is *not* an official product of the Chandra X-ray Center.

I am interested to know if you are interested in using CIAO in some
Docker-related setup, so please get in contact via the issues list if you want
to talk.

You may also be interested in the
[ldouchy/ciao](https://hub.docker.com/r/ldouchy/ciao/) Docker image (which I
have not used, and is also not a CXC product).

# Quick guide

The CIAO 4.9 version is intended to allow use of Jupyter notebooks with
CIAO, and so includes AstroPy and Matplotlib. The Sherpa environment has
been updated to use the Matplotlib for plotting, rather than ChIPS, since
it works better within a Jupyter notebook.

```
% docker run -p 8888:8888 djburke/ciao-build:4.9.0 /home/ciaouser/bin/start_jupyter.bash
```

This starts a Jupyter session which can be accessed as http://localhost:8888/
and the password is ciao. Note that the Jupyter interface claims to be able to
start both Python 2.7 and 3 sessions, but they are both Python 2.7.

# Docker images

- [build/ciao-4.9/Dockerfile](https://hub.docker.com/r/djburke/ciao-build/)
- [build/ciao-4.8/Dockerfile](https://hub.docker.com/r/djburke/ciao-build/)

# Status

Any information provided here is placed in the public domain, although note
that CIAO itself is licensed for use under the GNU General Public License (GPL)
Version 3 (or at your option any later version).

