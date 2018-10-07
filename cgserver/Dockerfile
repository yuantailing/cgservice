FROM cscg/base

RUN apt-get update && \
	apt-get install --no-install-recommends -y default-libmysqlclient-dev && \
	rm -rf /var/lib/apt/lists/*

RUN pip3 install setuptools && \
	pip3 install mysqlclient && \
	rm -r ~/.cache/pip

RUN git clone https://github.com/yuantailing/cgserver.git /opt/cgserver && \
	cd /opt/cgserver && \
	git checkout 1eb8751859308891b21777601f4e8dcceab35fe0 && \
	pip3 install -r cgserver/requirements.txt && \
	rm -r ~/.cache/pip

COPY conf/settings.py /opt/cgserver/cgserver/cgserver/settings.py

WORKDIR /opt/cgserver/cgserver
EXPOSE 80
CMD ["python3", "manage.py", "runserver", "0.0.0.0:80"]
