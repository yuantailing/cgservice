FROM debian:buster

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y curl default-mysql-client git python3 python3-pip python3-setuptools rsync xz-utils && \
	rm -rf /var/lib/apt/lists/*

RUN pip3 install awscli && \
	rm -rf ~/.cache/pip

RUN cd /opt/ && \
	curl -sSL https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-debian92-4.2.0.tgz | tar xzvf - mongodb-linux-x86_64-debian92-4.2.0/bin/mongodump && \
	ln -s /opt/mongodb-linux-x86_64-debian92-4.2.0/bin/mongodump /usr/local/bin/

COPY backup.py /backup/backup.py
COPY backup_aws.sh /backup/backup_aws.sh

RUN git config --global user.name root && \
	git config --global user.email root@cgservice

ENTRYPOINT ["python3", "-u", "/backup/backup.py"]
CMD ["nothing"]
