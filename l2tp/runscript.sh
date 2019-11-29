#!/bin/bash -ex

rm -f /var/run/charon.pid /var/run/starter.charon.pid /var/run/xl2tpd.pid

echo -e ": PSK \"${VPN_IPSEC_PSK}\"" >>/etc/ipsec.secrets

mkdir -p /var/run/xl2tpd

# configure firewall
iptables -t nat -A POSTROUTING -s 192.168.46.0/23 ! -d 192.168.46.0/23 -j MASQUERADE
iptables -t mangle -A FORWARD -s 192.168.46.0/23 -p tcp -m tcp --tcp-flags SYN,ACK,FIN,RST SYN -m tcpmss --mss 1361:1536 -j TCPMSS --set-mss 1360

# Tsinghua IP only
iptables -A INPUT -s 166.111.0.0/16 -j ACCEPT
iptables -A INPUT -s 59.66.0.0/16 -j ACCEPT
iptables -A INPUT -s 101.5.0.0/16 -j ACCEPT
iptables -A INPUT -s 101.6.0.0/16 -j ACCEPT
iptables -A INPUT -s 183.172.0.0/15 -j ACCEPT
iptables -A INPUT -s 118.229.0.0/19 -j ACCEPT
iptables -A INPUT -p udp --dport 500 -j DROP
iptables -A INPUT -p udp --dport 4500 -j DROP

# redirect net.tsinghua.edu.cn
netredirect=$(nslookup netredirect | awk -F': ' 'NR==6 {print $2}')
iptables -t nat -A PREROUTING -d 166.111.204.120 -j DNAT --to ${netredirect}
iptables -t nat -A PREROUTING -d 101.6.4.100 -j DNAT --to ${netredirect}

xl2tpd -D -c /etc/xl2tpd/xl2tpd.conf &
ipsec start --nofork 2>&1
