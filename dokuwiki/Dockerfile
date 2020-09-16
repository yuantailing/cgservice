FROM debian:buster

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y apache2 curl git libapache2-mod-php php-xml python3 python3-requests unzip && \
	rm -rf /var/lib/apt/lists/*

RUN cd /root && \
	curl https://open-access.oss-cn-beijing.aliyuncs.com/Downloads/dokuwiki-24117f7f9e0362c4b1782ff29220b0ab.tgz -o dokuwiki.tgz && \
	tar xzf dokuwiki.tgz -C /srv && \
	rm dokuwiki.tgz && \
    chown -R www-data:www-data /srv/dokuwiki/data

RUN git clone https://github.com/dwp-forge/tablewidth.git /srv/dokuwiki/lib/plugins/tablewidth && \
	cd /srv/dokuwiki/lib/plugins/tablewidth && \
	git checkout 0cdc3206b9b0ce865f7d7424b21f4a5ca6d5ab8e

COPY conf/* /srv/dokuwiki/conf/

COPY 000-default.conf /etc/apache2/sites-available/000-default.conf

COPY scripts/ /root/scripts/

EXPOSE 80
CMD ["/root/scripts/cmd.sh"]
