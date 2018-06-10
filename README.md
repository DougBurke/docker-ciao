# Fun with Docker and CIAO

Here are some experiments in combining
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

# Quick guide: CIAO 4.10/Python 3.5

The CIAO 4.10 version is intended to allow use of Jupyter notebooks with
CIAO, and so includes AstroPy, Matplotlib, AplPy, and SciPy. The Sherpa
environment has been updated to use the Matplotlib for plotting, rather
than ChIPS, since it works better within a Jupyter notebook (in fact
the CIAO graphical packages, including ChIPS and prism, have not been
installed, and neither has X11).

The Jupyter notebook can be started up with the `run_ciao_notebooks.sh`
script; for example

```
% sudo docker run -it -p 8888:8888 djburke/ciao-build:4.10.0-ubuntu-1804 \
       /home/ciaouser/run_ciao_notebooks.sh 
```

or

```
% sudo docker run -it -p 8888:8888 djburke/ciao-build:4.10.0-centos-7 \
       /home/ciaouser/run_ciao_notebooks.sh 
```

The password for the notebook server is `ciaopass` and there is an example
notebook available at `notebooks/Example CIAO notebook.ipynb`.

# Quick guide: CIAO 4.9/Python 2.7

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

- build/ciao-4.10/Dockerfile.ubuntu - CIAO 4.10, Python 3.5, Ubuntu 18.04
- build/ciao-4.10/Dockerfile.centos - CIAO 4.10, Python 3.5, Centos 7
- [build/ciao-4.9/Dockerfile](https://hub.docker.com/r/djburke/ciao-build/)
- [build/ciao-4.8/Dockerfile](https://hub.docker.com/r/djburke/ciao-build/)

For CIAO 4.10, you first need to download the tar files into the directory
`store.ubuntu` or `store.centos`, using the supplied `ciao-install`
script (changing `ubuntu` to `centos` as desired):

    % cd build/ciao-4.10
    % system=ubuntu
    % mkdir store.$system
    % bash ciao-install --download-only --batch --remove chips \
           --remove prism --system $system --download store.$system

At this point the Docker image can be built
the tar files should be downloaded and placed within a
sub-directory of `build/ciao-4.10/` - `store.ubuntu` or `store.centos` -
as is - i.e. leave as compressed tar files - and then build with

    % sudo docker build -f Dockerfile.$system -t ciao410.$system .

(hopefully picking a more-suitable name than `ciao410.ubuntu`).

Note that I have not installed some of the graphical packages of
CIAO - namely `prism`, `obsvis`, and `chips` - since they are tricker
to use effectively from within a Docker container.

The builds *do* contain several additional Python packages: `astropy`,
`scipy`, `matplotlib`, `aplpy`, and Jupyter notebooks for both Python 3.5
and bash.

# Status

Any information provided here is placed in the public domain, although note
that CIAO itself is licensed for use under the GNU General Public License (GPL)
Version 3 (or at your option any later version).

