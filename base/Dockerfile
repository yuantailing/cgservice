FROM debian:stretch

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y apt-utils sudo man psmisc net-tools iputils-ping curl wget rsync sshfs build-essential vim git unzip p7zip-full tmux make locate python python-pip python-dev python3 python3-pip python3-dev gcc g++ gdb openssh-server kmod bc && \
	rm -rf /var/lib/apt/lists/*
