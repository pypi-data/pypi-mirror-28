#!/usr/bin/env python
# -*- coding: utf-8 -*-

hub_tunnel_config = '''
interface Tunnel1 
ip address {} 255.255.255.0 
no ip redirects 
no ip next-hop-self eigrp 1 
no ip split-horizon eigrp 1 
ip nhrp authentication cisco 
ip nhrp network-id 1 
load-interval 30 
tunnel source GigabitEthernet1 
tunnel mode gre multipoint 
tunnel key 0 
tunnel protection ipsec profile vti-1 
ip mtu 1400

'''


crypto_policy_aes256 = '''
crypto isakmp policy 1
encr aes 256
authentication pre-share
crypto isakmp key cisco address 0.0.0.0
crypto ipsec transform-set uni-perf esp-aes 256 esp-sha-hmac
mode transport
crypto ipsec profile vti-1
set security-association lifetime kilobytes disable
set security-association lifetime seconds 86400
set transform-set uni-perf
set pfs group2
'''

routing_eigrp = '''
router eigrp 1 
network 1.1.1.0 0.0.0.255 
network {} {}
passive-interface default 
no passive-interface Tunnel1 
'''

spoke_tunnel_config = '''
interface Tunnel1
ip address {} 255.255.255.0
no ip redirects
ip nhrp authentication cisco
ip nhrp network-id 1
ip nhrp nhs 1.1.1.1 nbma {} multicast
ip nhrp nhs 1.1.1.2 nbma {} multicast
load-interval 30
tunnel source GigabitEthernet1
tunnel mode gre multipoint
tunnel key 0
tunnel protection ipsec profile vti-1
'''

spoke_tunnel_config_single = '''
interface Tunnel1
ip address {} 255.255.255.0
no ip redirects
ip nhrp authentication cisco
ip nhrp network-id 1
ip nhrp nhs 1.1.1.1 nbma {} multicast
load-interval 30
tunnel source GigabitEthernet1
tunnel mode gre multipoint
tunnel key 0
tunnel protection ipsec profile vti-1
'''