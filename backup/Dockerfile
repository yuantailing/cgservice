FROM debian:stretch

RUN sed -i s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	apt-get install --no-install-recommends -y rsync python3 git && \
	rm -rf /var/lib/apt/lists/*

RUN git config --global user.name root && \
	git config --global user.email root@cgservice

ENTRYPOINT ["python3", "-u", "/backup.py"]
CMD ["nothing"]
