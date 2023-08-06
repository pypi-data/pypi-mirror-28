#!/usr/bin/env python

import re
import time
import socket
import configs
import logging
import ipaddress
import getmetadata
from parse import *
from command import *

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def configure_transit_vnet(section_dict):
	'''
	WAIT FOR IT

	'''
	role = section_dict['role']

	configure_crypto_policy(section_dict)
	tunnel_network = section_dict['DMVPNTunnelIpCidr']

	if 'hub' in role.lower():
		log.info('[INFO] Configuring router as {}'.format(role))
		hub_dict = {}
		if 'guestshell' in socket.gethostname():
			hub_dict['pip'] = getmetadata.get_pip()
		else:
			hub_dict['pip'] = '255.255.255.254'
		if '1' in role:
			tunn_addr = tunnel_network.network_address + 1
			hub_dict['nbma'] = str(tunn_addr)
			section_dict['hub-1'] = hub_dict
			section_dict['spoke'] = {'count' :  0 }
		else:
			tunn_addr = tunnel_network.network_address + 2
			hub_dict['nbma'] = str(tunn_addr)
			section_dict['hub-2'] = hub_dict
		configure_tunnel(role, tunn_addr, section_dict)
		configure_routing(role)
		#section_dict['dmvpn'] = setup_dmvpn_dict(section_dict)

	elif role.lower() == 'spoke':
		log.info('[INFO] Configuring router as SPOKE')
		try:
			section_dict['spoke']['count'] += 1
			tunn_addr = tunnel_network.network_address + section_dict['spoke']['count'] + 2
		except KeyError:
			log.info('[ERROR] Spoke count is not found in spoke file contents.')
			return None
		configure_tunnel(role, tunn_addr, section_dict)
		configure_routing(role, section_dict['interfaces'])
	else:
		log.info('[ERROR] Unrecognised role is assigned to the router!')


	write_all_files(section_dict)



def configure_crypto_policy(section_dict):	
	output = cmd_configure(configs.crypto_policy_aes256)
	log.info(output)


def configure_tunnel(role, tunn_addr, section_dict):
	cmd = ''
	if 'hub' in role:
		cmd = configs.hub_tunnel_config
		cmd = cmd.format(str(tunn_addr))
	else:
		try:
			hub1_pip = section_dict['hub-1']['pip']
		except KeyError:
			return None
		try:
			hub2_pip = section_dict['hub-2']['pip']
		except (KeyError,TypeError) as e:
			log.info('[ERROR] No HUB-2 dict was found! {}'.format(e))
			hub2_pip = None
		if hub2_pip is not None:
			cmd = configs.spoke_tunnel_config
			cmd = cmd.format(str(tunn_addr), str(hub1_pip), str(hub2_pip))
		else:
			cmd = configs.spoke_tunnel_config_single
			cmd = cmd.format(str(tunn_addr), str(hub1_pip))
	output = cmd_configure(cmd)
	log.info(output)



def configure_routing(role,interface_dict = None):
	cmd = configs.routing_eigrp
	if '2' in role:
		cmd = cmd.format('18.18.18.0','0.0.0.255')
	elif 'spoke' in role:
		try:
			cmd = cmd.format(interface_dict['GigabitEthernet2'].network.network_address,interface_dict['GigabitEthernet2'].hostmask)
		except:
			cmd = cmd.format('10.0.0.0','0.0.0.255')
	else:
		cmd = cmd.format('9.9.9.0','0.0.0.255')
	output = cmd_configure(cmd)
	print(output)


def parse_sh_run():
	'''
	Get running config from CSR.
	'''
	output = cmd_execute('show run')
	print(output)

def get_interfaces():
	output = cmd_execute('sh ip int br')
	print(output)
	regex = r"GigabitEthernet\d+"
	interfaces = re.findall(regex, output)
	return interfaces

def configure_get_interfaces():
	configure_interface_dhcp()
	interface_dict = get_interfaces_ips()
	print(interface_dict)

def get_interfaces_ips():
	interfaces = get_interfaces()
	interface_dict = {}
	for interface in interfaces:
		print('[INFO] Working on {} interface'.format(interface))
		output = cmd_execute('sh int {} | inc Internet address is'.format(interface))
		if '/' not in output:
			time.sleep(10)
			output = cmd_execute('sh int {} | inc Internet address is'.format(interface))
		print(output)
		output = output.replace('Internet address is' , '')
		output = output.replace(' ' , '')
		output = output.replace('\n' , '')
		obj = ipaddress.IPv4Interface(u'{}'.format(output))
		interface_dict[interface]= obj
	return interface_dict

def configure_interface_dhcp():
	interfaces = get_interfaces()
	for interface in interfaces:
		output = cmd_configure('''int {}
no shu
ip addr dhcp'''.format(interface))
		print(output)

def setup_dmvpn_dict(section_dict):
	param_list = ['TunnelKey', 'RoutingProtocol', 'transitvnetname']
	dmvpn_dict = {}
	for param in param_list:
		dmvpn_dict[param] = section_dict[param]
	return dmvpn_dict