FROM yuantailing/sharelatex:2.5.0-scheme-full

RUN cd /var/www/sharelatex/web && \
	git init && \
	git remote add origin https://github.com/overleaf/web.git && \
	git fetch origin master

RUN cd /var/www/sharelatex/clsi && \
	git init && \
	git remote add origin https://github.com/overleaf/clsi.git && \
	git fetch origin master

RUN sed -i s/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y python3-pip python3-setuptools && \
	rm -rf /var/lib/apt/lists/*

RUN pip3 install bibtexparser && \
	rm -rf ~/.cache/pip

RUN cd /var/www/sharelatex/web && \
	git checkout -b master && \
	git reset a3bfa17beecb32ce11f8665a023e43d6930856f5 && \
	git fetch https://github.com/yuantailing/web-sharelatex.git cgservice-subpath-2.5 && \
	git merge --ff-only 434a2c328c464f5f18a199c6951ed2359cef41ae

RUN cd /var/www/sharelatex/clsi && \
	git checkout -b master && \
	git reset a883084bba5491ced188db7b32e64c988ffe73ca && \
	git fetch https://github.com/yuantailing/clsi-sharelatex.git cgservice-2.5 && \
	git merge --ff-only f1368ffce1b82e6cb7414bb6a61860426d2f92cc

ENV SUBPATH=latex

RUN cd /var/www/sharelatex/web && \
	git ls-tree HEAD -r --name-only -z | xargs -I% -P`nproc` --null sed -i "s/\\/SHARELATEX\\/learn/https:\\/\\/overleaf.com\\/learn/g;s/\\/SHARELATEX\\/templates/https:\\/\\/overleaf.com\\/templates/g" % && \
	git ls-tree HEAD -r --name-only -z | xargs -I% -P`nproc` --null sed -i "s/\\/SHARELATEX/\\/${SUBPATH}/g" % && \
	sed -i "s/https:\/\/cg.cs.tsinghua.edu.cn\/serverlist\//http:\/\/cgserver\/serverlist\//g" app/src/Features/Authentication/AuthenticationManager.js && \
	npm install && \
	npm run webpack:production

RUN sed -i "s/\\/project\\//\\/${SUBPATH}\\/project\\//g" /var/www/sharelatex/real-time/app/js/WebApiManager.js /var/www/sharelatex/document-updater/app/js/PersistenceManager.js && \
	sed -i "s/\\/user\\//\\/${SUBPATH}\\/user\\//g" /var/www/sharelatex/track-changes/app/js/WebApiManager.js && \
	sed -i "/project_history/{n;s/enabled: true/enabled: false/}" /var/www/sharelatex/document-updater/config/settings.defaults.js && \
	sed -i "/logger: socketIoLogger/a, resource: '/${SUBPATH}/socket.io'" /var/www/sharelatex/real-time/app.js

RUN sed -i "s/\/socket.io/\/${SUBPATH}\/socket.io/" /etc/nginx/sites-enabled/sharelatex.conf && \
	sed -i "s/expires .*\$/expires 1d;/g" -i /etc/nginx/sites-enabled/sharelatex.conf

RUN sed -i 's/maxRequests: 200,/maxRequests: 10000,/' /var/www/sharelatex/web/app/src/Features/Uploads/UploadsRouter.js

COPY 00_regen_sharelatex_secrets.sh /etc/my_init.d/00_regen_sharelatex_secrets.sh
