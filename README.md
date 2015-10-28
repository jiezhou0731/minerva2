
Minerva2 is a MEAN (MongoDB, Express.js, Angular.js, Node.js) Project.

##Setup On Ubuntu:
sudo apt-get install nodejs

sudo apt-get install npm

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list

sudo apt-get update

sudo apt-get install -y mongodb-org

sudo service mongod start


In server folder, run:

npm install --save express

npm install --save mongoose

npm install --save node-restful

npm install --save method-override

npm install --save body-parser

npm install --save lodash

node index.js

check nodejs processes:

lsof -Pi | grep LISTEN


In client folder, run:

sudo npm install -g yo

sudo npm install yo

sudo npm install -g generator-angular

yo angular

sudo bower install --allow-root

sudo apt-get install ruby-compass

sudo apt-get install ruby

sudo npm install -g grunt-cli

sudo apt-get install ruby-dev

sudo gem install compass

npm install grunt-contrib-compass --save-dev

sudo grunt serve

##Trouble Shooting:
Upgrade npm:

curl https://raw.githubusercontent.com/creationix/nvm/v0.13.1/install.sh | sh

npm not found (/usr/bin/env: node: No such file or directory)

sudo ln -s /usr/bin/nodejs /usr/bin/node
