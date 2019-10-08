FROM yuantailing/sharelatex:2.0-beta-2-scheme-full

RUN sed -i s/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list && \
	sed -i s/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g /etc/apt/sources.list

RUN apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y python3-pip python3-setuptools && \
	rm -rf /var/lib/apt/lists/*

RUN pip3 install bibtexparser && \
	rm -rf ~/.cache/pip

RUN ln -s /var/www/sharelatex/clsi/bin/synctex /opt/synctex

RUN sed -i "s/expires .*\$/expires 1d;/g" -i /etc/nginx/sites-enabled/sharelatex.conf

RUN cd /var/www/sharelatex/web && \
	git config --global user.name "root" && \
	git config --global user.email "root@localhost" && \
	git checkout package-lock.json && \
	git fetch https://github.com/yuantailing/web-sharelatex.git subpath cgservice cgservice-subpath && \
	git merge e2b6efcd49daa50311446f0d73666f5be6ef8c6d cb33e9864069f0cc93bde5637f54e793a361e1b3 9d2ca5ac8dc3b616aacd64f2029319df6bc4cfc4 && \
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

COPY 00_regen_sharelatex_secrets.sh /etc/my_init.d/00_regen_sharelatex_secrets.sh
