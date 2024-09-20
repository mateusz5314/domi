FROM ubuntu:24.04

# Create user
ARG USR_NAME
RUN echo "Creating user: ${USR_NAME}" && \
    apt-get update && apt-get -y install sudo && \
    useradd -rm -d /home/${USR_NAME} -s /bin/bash -g root -G sudo -u 1001 ${USR_NAME} && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
    chown ${USR_NAME} -R /home/${USR_NAME}

# Switch user
USER ${USR_NAME}
ENV HOME=/home/${USR_NAME}
WORKDIR $HOME

# Install required packages
RUN echo "Installing packages" && \
    sudo apt-get update && \
    sudo apt-get -y install bash-completion build-essential git python3.12 wget nano

# Install & setup anaconda
RUN echo "Setting up anaconda environment" && \
    wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh && \
    bash Anaconda3-2022.05-Linux-x86_64.sh -b

RUN /home/${USR_NAME}/anaconda3/bin/conda init bash && \
    /home/${USR_NAME}/anaconda3/bin/conda config --set auto_activate_base false && \
    /home/${USR_NAME}/anaconda3/bin/conda create -n domi python=3.12 -y && \
    echo "conda activate domi" >> /home/${USR_NAME}/.bashrc

# Install python packages
RUN echo "Install python packages" && \
    /home/${USR_NAME}/anaconda3/bin/conda run -n domi pip install adafruit-ampy && \
    /home/${USR_NAME}/anaconda3/bin/conda run -n domi pip install -U micropython-rp2-pico_w-stubs && \
    /home/${USR_NAME}/anaconda3/bin/conda run -n domi conda install conda-forge::micropython

# Add console history search on arrows
RUN echo "" >> /home/${USR_NAME}/.bashrc  && \
    echo "bind '\"\e[A\": history-search-backward'" >> /home/${USR_NAME}/.bashrc && \
    echo "bind '\"\e[B\": history-search-forward'" >> /home/${USR_NAME}/.bashrc && \
    echo "" >> /home/${USR_NAME}/.bashrc
