FROM cscg/base

RUN echo "deb http://mirrors.tuna.tsinghua.edu.cn/debian stretch-backports main" >>/etc/apt/sources.list && \
	apt-get update && \
	apt-get install --no-install-recommends -y certbot -t stretch-backports && \
	rm -rf /var/lib/apt/lists/*

COPY runscript.py /runscript.py
CMD ["/runscript.py"]
