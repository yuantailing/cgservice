FROM debian:sid

RUN apt-get update && \
	apt-get install --no-install-recommends -y openssh-server && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN echo "DebianBanner no" >/etc/ssh/sshd_config.d/regulations.conf

COPY runscript.sh /runscript.sh

EXPOSE 22
CMD ["/runscript.sh"]
