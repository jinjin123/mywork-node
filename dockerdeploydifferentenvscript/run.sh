#!/bin/bash
/etc/init.d/nginx start && \
sed -i "s|/project/env/|/${PROJ}/${ENVT}/|g" /etc/confd/conf.d/conf.toml && \
sed -i "s|/project/env/|/${PROJ}/${ENVT}/|g" /etc/confd/templates/conf.tmpl && \
confd -watch -backend etcd -node=http://192.168.107.101:2379 -node=http://192.168.107.102:2379 || \
exit 1
