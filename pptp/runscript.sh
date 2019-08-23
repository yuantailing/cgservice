#!/bin/bash

set -ex

# configure firewall
iptables -t nat -A POSTROUTING -s 192.168.61.0/24 ! -d 192.168.61.0/24 -j MASQUERADE
iptables -A FORWARD -s 192.168.61.0/24 -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -j TCPMSS --set-mss 1356

# redirect net.tsinghua.edu.cn
netredirect=$(nslookup netredirect | awk -F': ' 'NR==6 {print $2}')
iptables -t nat -A PREROUTING -d 166.111.204.120 -j DNAT --to ${netredirect}
iptables -t nat -A PREROUTING -d 101.6.4.100 -j DNAT --to ${netredirect}
iptables -t nat -A PREROUTING -d 101.6.6.219 -j DNAT --to ${netredirect}

pptpd --fg
