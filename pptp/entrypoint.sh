#!/bin/bash

set -ex

echo "${CLIENT} *   ${SECRET}   *" >/etc/ppp/chap-secrets
chmod 600 /etc/ppp/chap-secrets

# configure firewall
iptables -t nat -A POSTROUTING -s 192.168.61.0/24 ! -d 192.168.61.0/24 -j MASQUERADE
iptables -A FORWARD -s 192.168.61.0/24 -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -j TCPMSS --set-mss 1356

# redirect net.tsinghua.edu.cn
netredirect=$(nslookup netredirect | awk -F': ' 'NR==6 {print $2}')
iptables -t nat -A PREROUTING -d 166.111.4.0/24 -j DNAT --to ${netredirect}
iptables -t nat -A PREROUTING -d 166.111.120.0/24 -j DNAT --to ${netredirect}
iptables -t nat -A PREROUTING -d 166.111.204.0/24 -j DNAT --to ${netredirect}
iptables -t nat -A PREROUTING -d 59.66.0.0/16 -j DNAT --to ${netredirect}
iptables -t nat -A PREROUTING -d 101.6.0.0/16 -j DNAT --to ${netredirect}

exec "$@"
