FROM centos:6

MAINTAINER Douglas Burke <dburke@cfa.harvard.edu>
LABEL description="Test build of CIAO 4.8; this is *not* an official CXC product" \
      version="CIAO 4.8"
      
RUN yum -y update && yum clean all

# This is not guaranteed to be a minimal set of packages needed to
# build and run CIAO.
RUN yum install -y tar wget file \
    gcc-c++ gcc-gfortran flex bison \
    ncurses-devel libICE-devel libSM-devel libX11-devel \
    libXau-devel libXdamage-devel \
    libXext-devel libXfixes-devel libXrender-devel libXt-devel libdrm-devel \
    libXcomposite-devel libXinerama-devel libXrandr-devel libXcursor-devel \
    libxcb-devel mesa-libGLU-devel \
    readline-devel fontconfig-devel \
    libXft

ENV CIAO_BUILD_LOCATION=/opt \
    CIAO_VERSION=ciao-4.8 \
    CIAO_GROUP=ciao \
    CIAO_USER=ciaouser

# Set up a root password for development
RUN echo "root:rootpass" | chpasswd

# It looks like it's safest to use a new ENV line to refer to
# previous settings
ENV CIAO_BASE=${CIAO_BUILD_LOCATION}/${CIAO_VERSION}

RUN groupadd ${CIAO_GROUP} \
    && useradd -r -m -g ${CIAO_GROUP} ${CIAO_USER}

WORKDIR ${CIAO_BUILD_LOCATION}
RUN chown -R ${CIAO_USER}:${CIAO_GROUP} ${CIAO_BUILD_LOCATION}

USER ${CIAO_USER}

COPY ciao-4.8-*gz ${CIAO_BUILD_LOCATION}/

# Start by building and installing the CIAO 4.8 system.
# For now hard-code the list of tar packages
RUN tar xzf ciao-4.8-bin-chips-Linux64.tar.gz \
    && tar xzf ciao-4.8-bin-core-Linux64.tar.gz \
    && tar xzf ciao-4.8-bin-graphics-Linux64.tar.gz \
    && tar xzf ciao-4.8-bin-obsvis-Linux64.tar.gz \
    && tar xzf ciao-4.8-bin-prism-Linux64.tar.gz \
    && tar xzf ciao-4.8-bin-sherpa-Linux64.tar.gz \
    && tar xzf ciao-4.8-bin-tools-Linux64.tar.gz \
    && tar xzf ciao-4.8-contrib-2.tar.gz \
    && tar xzf ciao-4.8-src-chips.tar.gz \
    && tar xzf ciao-4.8-src-core.tar.gz \
    && tar xzf ciao-4.8-src-prism.tar.gz \
    && tar xzf ciao-4.8-src-sherpa.tar.gz \
    && tar xzf ciao-4.8-src-tools.tar.gz

ENV PKG_CONFIG_PATH=${CIAO_BASE}/ots/lib/pkgconfig:/usr/lib64/pkgconfig:/usr/share/pkgconfig

WORKDIR ${CIAO_BASE}

# The following was pieced together following the ciao-install script
# and the "build CIAO" thread at
# http://cxc.harvard.edu/ciao4.8/threads/ciao_build_linux/
# but all mistakes are my own.
#
RUN bash src/config/fixpc.sh ${CIAO_BASE} \
    && mv src src-bak && ./configure && mv src-bak src \
    && bash bin/ciao-python-fix \
    && . bin/ciao.bash \
    && ahelp -r  \
    && rm -rf binexe/* lib/* \
    && ciaorun ./configure --with-fits --with-ascii \
    && ciaorun make install \
    && bash bin/ciao-python-fix \
    && . bin/ciao.bash -o \
    && ahelp -r

WORKDIR /home/${CIAO_USER}

# Autostart CIAO; use ~/.bashrc rather than ~/.bash_profile as easier to
# edit.
RUN echo "# Start up CIAO automatically" >> .bashrc \
    && echo ". ${CIAO_BASE}/bin/ciao.bash" >> .bashrc \
    && echo "echo ''" >> .bashrc \
    && echo "echo '*** CIAO has been started'" >> .bashrc \
    && echo "echo '*** Note: CALDB has not been installed; use download_obsid_caldb'" >> .bashrc \
    && echo "echo '*** The root password is rootpass'" >> .bashrc \
    && echo "echo ''" >> .bashrc

#CMD ["/bin/bash"]
