#!/bin/bash
export PATH=$PATH:/usr/local/.nvm/versions/node/v7.8.0/bin
#export NEW_RELIC_NO_CONFIG_FILE=True
#export NEW_RELIC_APP_NAME=$NEWRELICAPPNAME
#export NEW_RELIC_LICENSE_KEY=$NEWRELICKEY
CODE_PATH='/var/www/html'
MONITOR='/var/www'
/bin/cp $MONITOR/newrelic.js  $CODE_PATH/newrelic.js
ENV NPM_PATH /usr/local/.nvm/versions/node/v7.8.0/bin/npm
ENV NODE_PATH /usr/local/.nvm/versions/node/v7.8.0/bin/node
cd $CODE_PATH
/bin/sed -i "s/app_name: .*/app_name: [\"$NEWRELICAPPNAME\"],/"   $CODE_PATH/newrelic.js
/bin/sed -i "s/license_key: .*/license_key: \"$NEWRELICKEY\",/"   $CODE_PATH/newrelic.js
if [ -e index.js ]
then
	/bin/sed -ie '/newrelic/d' $CODE_PATH/index.js
	/bin/sed -i '1 irequire("newrelic")' $CODE_PATH/index.js
	cd $CODE_PATH &&  $NPM_PATH  install
	if [ $? -ne 0 ]
	then
	  	$NPM_PATH  install  newrelic && $NODE_PATH  $CODE_PATH/index.js
	else
	  	$NPM_PATH  install  newrelic && $NODE_PATH  $CODE_PATH/index.js
	fi
elif [ -e app.js ]
then
	/bin/sed -ie '/newrelic/d' $CODE_PATH/app.js
	/bin/sed -i '1 irequire("newrelic")' $CODE_PATH/app.js
	cd $CODE_PATH && $NPM_PATH  install && $NPM_PATH  install  newrelic &&  $NODE_PATH  $CODE_PATH/app.js
else
	/bin/sed -ie '/newrelic/d' dist/index.js
	/bin/sed -i '1 irequire("newrelic")' dist/app.js
	cd $CODE_PATH && $NPM_PATH  install && $NPM_PATH  install  newrelic &&  $NODE_PATH  dist/app.js
fi
