FROM debian:buster

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y curl default-mysql-client git gnupg2 python3 python3-pip python3-setuptools redis-tools rsync xz-utils && \
	rm -rf /var/lib/apt/lists/*

RUN pip3 install awscli && \
	rm -rf ~/.cache/pip

RUN curl -sSL https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add - && \
	echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.2 main" | tee /etc/apt/sources.list.d/mongodb-org-4.2.list && \
	apt-get update && \
	apt-get install --no-install-recommends -y mongodb-org-tools && \
	rm -rf /var/lib/apt/lists/*

COPY backup.py /backup/backup.py
COPY backup_aws.sh /backup/backup_aws.sh

RUN git config --global user.name root && \
	git config --global user.email root@cgservice

ENTRYPOINT ["python3", "-u", "/backup/backup.py"]
CMD ["nothing"]
