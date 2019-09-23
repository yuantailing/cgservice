FROM yuantailing/sharelatex:scheme-full

RUN ln -s /var/www/sharelatex/clsi/bin/synctex /opt/synctex

RUN cd /var/www/sharelatex/web && \
	git config user.name "root" && \
	git config user.email "root@localhost" && \
	git checkout package-lock.json && \
	git fetch https://github.com/yuantailing/web-sharelatex.git subpath cgservice && \
	git merge e409c39b31d5383eee6e89bd31b080bc1461e55a 1e9779cce8aa4405c1325d3d5f3f9f54e6aeb1c9 && \
	npm install

RUN cd /var/www/sharelatex/clsi && \
	git pull && \
	git fetch https://github.com/yuantailing/clsi-sharelatex.git fix-synctex && \
	git merge 60fd936798ee73270ad53e1f7cb439b16bfbc85d && \
	npm run compile:app

ENV SUBPATH=latex

RUN cd /var/www/sharelatex/web && \
	git ls-tree HEAD -r --name-only -z | xargs -I% -P`nproc` --null sed -i "s/\\/SHARELATEX/\\/${SUBPATH}/g" % && \
	sed -i "s/SHARELATEX/${SUBPATH}/g" app/src/Features/RealTimeProxy/RealTimeProxyRouter.js && \
	/sbin/setuser www-data make -j`nproc` compile_full && \
	/sbin/setuser www-data make -j`nproc` minify

RUN sed -i "s/\\/project\\//\\/${SUBPATH}\\/project\\//g" /var/www/sharelatex/real-time/app/coffee/WebApiManager.coffee /var/www/sharelatex/document-updater/app/coffee/PersistenceManager.coffee && \
	sed -i "s/\\/user\\//\\/${SUBPATH}\\/user\\//g" /var/www/sharelatex/track-changes/app/coffee/WebApiManager.coffee && \
	sed -i "/project_history/{n;s/enabled: true/enabled: false/}" /var/www/sharelatex/document-updater/config/settings.defaults.coffee && \
	cd /var/www/sharelatex/real-time && npm run compile:app && \
	cd /var/www/sharelatex/document-updater && npm run compile:app && \
	cd /var/www/sharelatex/track-changes && npm run compile:app

COPY 00_regen_sharelatex_secrets.sh /etc/my_init.d/00_regen_sharelatex_secrets.sh
