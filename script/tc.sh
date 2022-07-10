#!/bin/sh

DEV=eth0
CEIL=20

start_tc(){
echo "start TC"
tc qdisc add dev $DEV root handle 1: htb default 14
tc class add dev $DEV parent 1: classid 1:1 htb rate ${CEIL}mbit ceil ${CEIL}mbit
tc qdisc add dev $DEV handle ffff: ingress
tc filter add dev $DEV parent ffff: protocol ip prio 2 u32 match ip src 0.0.0.0/0 police rate ${CEIL}mbit burst 20mbit drop flowid ffff
echo "Done"
}

stop_tc() {
echo  "Stop TC......"
(tc qdisc del dev $DEV root && echo "ok." ) || echo "error."
tc filter del dev $DEV parent ffff: protocol ip prio 2 u32 match ip src 0.0.0.0/0 police rate ${CEIL}mbit burst 20mbit drop flowid ffff
tc qdisc del dev $DEV handle ffff: ingress
}

status() {
tc -s class show dev $DEV
}

usage() {
 echo "Usage: `basename $0` [start | stop | restart | status | mangle ]"
}

###################
case "$1" in

start)

( #start_tc && start_mangle && echo "TC started!" ) || echo "error."
start_tc && echo "TC started!" ) || echo "error."
exit 0
;;

stop)

( #stop_tc && stop_mangle && echo "TC stopped!" ) || echo "error."
stop_tc && echo "TC stopped!" ) || echo "error."
exit 0
;;

restart)

stop_tc
stop_mangle
sleep 1
start_tc
start_mangle
echo "TC restart"
;;

status)

status
;;

mangle)

iptables -t mangle -nL
;;

*) usage
exit 1
;;
esac
