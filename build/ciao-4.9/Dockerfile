FROM ubuntu:18.04

MAINTAINER Douglas Burke <dburke@cfa.harvard.edu>
LABEL description="Can we use CIAO 4.9 and Jupyter notebooks?; this is *not* an official CXC product" \
      version="CIAO 4.9"

RUN apt-get update \
    && apt-get install -y --assume-yes \
    gcc \
    curl \
    pandoc \
    libzmq3-dev

ENV CIAO_INSTALL_LOCATION=/opt \
    CIAO_VERSION=ciao-4.9 \
    CIAO_GROUP=ciao \
    CIAO_USER=ciaouser

# Set up a root password for development
RUN echo "root:rootpass" | chpasswd

ENV CIAO_BASE=${CIAO_INSTALL_LOCATION}/${CIAO_VERSION}

RUN groupadd ${CIAO_GROUP} \
    && useradd -r -m -g ${CIAO_GROUP} ${CIAO_USER}

WORKDIR ${CIAO_INSTALL_LOCATION}
RUN chown -R ${CIAO_USER}:${CIAO_GROUP} ${CIAO_INSTALL_LOCATION}

USER ${CIAO_USER}

# openssl.tar.gz is the tarred-up output of
#
# wget https://rpmfind.net/linux/fedora/linux/releases/25/Everything/x86_64/os/Packages/o/openssl-libs-1.0.2j-1.fc25.x86_64.rpm
# rpm2cpio openssl-libs-1.0.2j-1.fc25.x86_64.rpm | cpio -i --make-directories
# 
COPY install/ciao-4.9-bin-core-Linux64.tar.gz \
     install/ciao-4.9-bin-tools-Linux64.tar.gz \
     install/ciao-4.9-bin-graphics-Linux64.tar.gz \
     install/ciao-4.9-bin-chips-Linux64.tar.gz \
     install/ciao-4.9-bin-sherpa-Linux64.tar.gz \
     install/ciao-4.9-contrib-4.tar.gz \
     install/openssl.tar.gz \
     install/ciao-remove-proj \
     ${CIAO_INSTALL_LOCATION}/

# Unpack and install CIAO, then tweak it so that it can play nicely with
# other installation systems, such as pip.
#
# Note that the prism and obsvis packages are not installed, and
# neither is CALDB.
#
RUN tar xzf ciao-4.9-bin-core-Linux64.tar.gz \
    && tar xzf ciao-4.9-bin-tools-Linux64.tar.gz \
    && tar xzf ciao-4.9-bin-graphics-Linux64.tar.gz \
    && tar xzf ciao-4.9-bin-chips-Linux64.tar.gz \
    && tar xzf ciao-4.9-bin-sherpa-Linux64.tar.gz \
    && tar xzf ciao-4.9-contrib-4.tar.gz \
    && tar xzf openssl.tar.gz \
    && cd ciao-4.9 \
    && ./configure \
    && bash bin/ciao-python-fix \
    && cd ots/lib \
    && ln -s ${CIAO_INSTALL_LOCATION}/usr/lib64/libssl.so.10 libssl.so.10 \
    && ln -s ${CIAO_INSTALL_LOCATION}/usr/lib64/libcrypto.so.10 libcrypto.so.10 \
    && . ${CIAO_BASE}/bin/ciao.bash \
    && python ${CIAO_INSTALL_LOCATION}/ciao-remove-proj

# Set up pip
RUN curl -O https://bootstrap.pypa.io/get-pip.py \
    && . ${CIAO_BASE}/bin/ciao.bash \
    && ciaorun python get-pip.py

# Install useful packages. The backports.shutil_get_terminal_size
# package needs to be removed before jupyter can be properly installed.
#
RUN . ${CIAO_BASE}/bin/ciao.bash \
    && ciaorun pip uninstall --yes backports.shutil_get_terminal_size \
    && ciaorun pip install jupyter astropy matplotlib scipy backports.shutil_get_terminal_size

WORKDIR /home/${CIAO_USER}/bin
COPY install/start_jupyter.bash start_jupyter.bash
USER root
RUN chown -R ${CIAO_USER}:${CIAO_GROUP} start_jupyter.bash
USER ${CIAO_USER}
RUN chmod u+x start_jupyter.bash

WORKDIR /home/${CIAO_USER}

# Use ~/.bashrc rather than ~/.bash_profile as easier for me to edit.
#
# Tweak Sherpa so that it uses matplotlib for the plotting backend,
# as that has better support for running in Jupyter notebooks than ChIPS.
#
# Set up the password "ciao" for the Jupyter notebook session. At present
# I am not attempting to make this secure.
#
RUN echo "# Set up CIAO alias" >> .bashrc \
    && echo "alias ciao='. ${CIAO_BASE}/bin/ciao.bash'" >> .bashrc \
    && echo "export PATH=/home/${CIAO_USER}/bin:$PATH" >> .bashrc \
    && echo "echo ''" >> .bashrc \
    && echo "echo '***'" >> .bashrc \
    && echo "echo '*** Start CIAO with ciao'" >> .bashrc \
    && echo "echo '*** Start the jupyter notebook server with:'" >> .bashrc \
    && echo "echo '***   /home/ciaouser/bin/start_jupyter.bash'" >> .bashrc \
    && echo "echo '***'" >> .bashrc \
    && echo "echo '*** Note: CALDB has not been installed; use download_obsid_caldb'" >> .bashrc \
    && echo "echo '***'" >> .bashrc \
    && echo "echo '*** The root password is rootpass'" >> .bashrc \
    && echo "echo ''" >> .bashrc \
    && sed -e s/chips/pylab/ ${CIAO_BASE}/config/sherpa/.sherpa.rc > .sherpa.rc \
    && mkdir notebooks \
    && . ${CIAO_BASE}/bin/ciao.bash \
    && ciaorun jupyter notebook --generate-config \
    && echo 'c.NotebookApp.password = u"sha1:e88785a5128b:ce643d906a222048fdcfef36980f518e7546fee4"' >> .jupyter/jupyter_notebook_config.py

# CMD ["/home/ciaouser/bin/start_jupyter.bash"]
