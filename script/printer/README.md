## kitchen

This git is built by Wupeijin@Sparkpad to run network printer by docker packages

## Installation steps 

1. change directory to root of this repo
2. run "docker build -t kitchen ."
3. wait until it complete

## Running of package 

docker run  -v <PATH of your python config file>/config.py:/usr/local/proxy/printer/config.py -v <PATH of your printer python file>/printer.py::/usr/local/proxy/printer/printer.py  --name tangshi kitchen

## License

A short snippet describing the license (MIT, Apache, etc.)
