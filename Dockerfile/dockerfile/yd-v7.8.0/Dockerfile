FROM docker.io/joshfinnie/nvm:latest
ENV NVM_DIR /usr/local/.nvm
ENV NODE_VERSION v7.8.0
RUN rm -rf $NVM_DIR
RUN /bin/bash -c "git clone https://github.com/cnpm/nvm.git $NVM_DIR && cd $NVM_DIR && git checkout `git describe --abbrev=0 --tags`"
RUN /bin/bash -c "source $NVM_DIR/nvm.sh && nvm install $NODE_VERSION && nvm install $NODE_VERSION && nvm use $NODE_VERSION"
ENV NODE_PATH $NVM_DIR/versions/node/$NODE_VERSION/lib/node_modules
ENV PATH      $NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH
RUN mkdir -p /var/www/html
COPY  newrelic.js    /var/www/newrelic.js
COPY docker-entrypoint.sh /var/www/docker-entrypoint.sh
RUN chmod a+x /var/www/docker-entrypoint.sh

ENTRYPOINT ["/var/www/docker-entrypoint.sh", "> /dev/stdout"]

WORKDIR  /var/www/html
