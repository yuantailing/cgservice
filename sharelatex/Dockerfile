FROM yuantailing/sharelatex:2.0.0-scheme-full

RUN sed -i s/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y python3-pip python3-setuptools && \
	rm -rf /var/lib/apt/lists/*

RUN pip3 install bibtexparser && \
	rm -rf ~/.cache/pip

RUN sed -i "s/expires .*\$/expires 1d;/g" -i /etc/nginx/sites-enabled/sharelatex.conf

RUN cd /var/www/sharelatex/web && \
	git config --global user.name "root" && \
	git config --global user.email "root@localhost" && \
	git checkout package-lock.json && \
	git remote add cgservice https://github.com/yuantailing/web-sharelatex.git && \
	git fetch cgservice cgservice-subpath subpath cgservice && \
	git checkout cgservice-subpath && git reset --hard 649b6410490636eba2210d70ce84b2ce2f6948bd && \
	git merge efd96ca939535d14baa90f25c252919832def40b 42c4a5ee0093dd0bd95906f0426aa7a8b9f84316 && \
	npm install

RUN cd /var/www/sharelatex/clsi && \
	git fetch https://github.com/yuantailing/clsi-sharelatex.git cgservice && \
	git merge d9a92121c7b73b66528612a07a6bc438308c7648 && \
	npm run compile:app

ENV SUBPATH=latex

RUN cd /var/www/sharelatex/web && \
	git ls-tree HEAD -r --name-only -z | xargs -I% -P`nproc` --null sed -i "s/\\/SHARELATEX\\/learn/https:\\/\\/overleaf.com\\/learn/g;s/\\/SHARELATEX\\/templates/https:\\/\\/overleaf.com\\/templates/g" % && \
	git ls-tree HEAD -r --name-only -z | xargs -I% -P`nproc` --null sed -i "s/\\/SHARELATEX/\\/${SUBPATH}/g" % && \
	sed -i "s/SHARELATEX/${SUBPATH}/g" app/src/Features/RealTimeProxy/RealTimeProxyRouter.js && \
	sed -i "s/https:\/\/cg.cs.tsinghua.edu.cn\/serverlist\//http:\/\/cgserver\/serverlist\//g" app/src/Features/Authentication/AuthenticationManager.js && \
	/sbin/setuser www-data make -j`nproc` compile_full && \
	/sbin/setuser www-data make -j`nproc` minify

RUN sed -i "s/\\/project\\//\\/${SUBPATH}\\/project\\//g" /var/www/sharelatex/real-time/app/coffee/WebApiManager.coffee /var/www/sharelatex/document-updater/app/coffee/PersistenceManager.coffee && \
	sed -i "s/\\/user\\//\\/${SUBPATH}\\/user\\//g" /var/www/sharelatex/track-changes/app/coffee/WebApiManager.coffee && \
	sed -i "/project_history/{n;s/enabled: true/enabled: false/}" /var/www/sharelatex/document-updater/config/settings.defaults.coffee && \
	cd /var/www/sharelatex/real-time && npm run compile:app && \
	cd /var/www/sharelatex/document-updater && npm run compile:app && \
	cd /var/www/sharelatex/track-changes && npm run compile:app

RUN cd /var/www/sharelatex && \
	git fetch origin master && \
	git checkout d7a05d3bf7bed425e7270dcf62de57e82aaa6d26 hotfix/2.0.2/1-anon-upload.patch && \
	/usr/bin/patch -i hotfix/2.0.2/1-anon-upload.patch -u web/app/src/Features/Uploads/UploadsRouter.js

RUN sed -i 's/maxRequests: 200,/maxRequests: 10000,/' /var/www/sharelatex/web/app/src/Features/Uploads/UploadsRouter.js

COPY 00_regen_sharelatex_secrets.sh /etc/my_init.d/00_regen_sharelatex_secrets.sh
