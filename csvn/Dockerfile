FROM debian:stretch

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y curl default-jre gettext procps libmagic1 python-svn python-subversion && \
	rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/jre

RUN curl https://downloads-guests.open.collab.net/files/documents/61/18759/CollabNetSubversionEdge-5.2.2_linux-x86_64.tar.gz -o csvn.tar.gz && \
	tar xzvf csvn.tar.gz -C /opt/ && \
	rm csvn.tar.gz

RUN useradd csvn && \
	usermod -u13690 csvn && \
	groupmod -g13690 csvn

WORKDIR /opt/csvn

COPY runscript.sh /runscript.sh

EXPOSE 3343
EXPOSE 4434
EXPOSE 18080

CMD ["/runscript.sh"]
