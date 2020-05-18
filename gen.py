#!/usr/bin/python3.6

import sys
import re
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from random import randrange, uniform

def print_clients(number):
	for i in range(number):
		irand = randrange(0, 150)
		print("<host id=\"torclient"+str(i)+"\" >")
		print("<process plugin=\"tor\" preload=\"tor-preload\" starttime=\""+str(900+irand)+"\" arguments=\"--Address ${NODEID} --Nickname ${NODEID} --DataDirectory shadow.data/hosts/${NODEID} --GeoIPFile ~/.shadow/share/geoip --defaults-torrc conf/tor.common.torrc -f conf/tor.client.torrc --BandwidthRate 1024000 --BandwidthBurst 1024000\" />")
		print("<process plugin=\"torctl\" starttime=\""+str(901+irand)+"\" arguments=\"localhost 9051 STREAM,CIRC,CIRC_MINOR,ORCONN,BW,STREAM_BW,CIRC_BW,CONN_BW\"/>")
		print("<process plugin=\"tgen\" starttime=\""+str(1200+irand)+"\" arguments=\"conf/tgen.torclient.graphml.xml\" />")
		print("</host>")

def print_webclients(number):
	for i in range(number):
		irand = randrange(0, 150)
		print("<host id=\"webclient"+str(i)+"\" >")
		print("<process plugin=\"tor\" preload=\"tor-preload\" starttime=\""+str(500+irand)+"\" arguments=\"--Address ${NODEID} --Nickname ${NODEID} --DataDirectory shadow.data/hosts/${NODEID} --GeoIPFile ~/.shadow/share/geoip --defaults-torrc conf/tor.common.torrc -f conf/tor.client.torrc --BandwidthRate 1024000 --BandwidthBurst 1024000\" />")
		print("<process plugin=\"torctl\" starttime=\""+str(501+irand)+"\" arguments=\"localhost 9051 STREAM,CIRC,CIRC_MINOR,ORCONN,BW,STREAM_BW,CIRC_BW,CONN_BW\"/>")
		print("<process plugin=\"tgen\" starttime=\""+str(700+irand)+"\" arguments=\"conf/tgen.webclient.graphml.xml\" />")
		print("</host>")

def print_victim():

	print("<host id=\"victim\" >")
	print("<process plugin=\"tor\" preload=\"tor-preload\" starttime=\"900\" arguments=\"--Address ${NODEID} --Nickname ${NODEID} --DataDirectory shadow.data/hosts/${NODEID} --GeoIPFile ~/.shadow/share/geoip --defaults-torrc conf/tor.common.torrc -f conf/tor.client.torrc --BandwidthRate 1024000 --BandwidthBurst 1024000\" />")
	print("<process plugin=\"torctl\" starttime=\"901\" arguments=\"localhost 9051 STREAM,CIRC,CIRC_MINOR,ORCONN,BW,STREAM_BW,CIRC_BW,CONN_BW\"/>")
	print("<process plugin=\"tgen\" starttime=\"1200\" arguments=\"conf/tgen.victim.graphml.xml\" />")
	print("</host>")   

def print_bottom():
	print("</shadow>")

def print_relays(number):
	
	print("<host id=\"relay\" quantity=\""+str(number)+"\" bandwidthdown=\"10240\" bandwidthup=\"10240\">")
	print("<process plugin=\"tor\" preload=\"tor-preload\" starttime=\"60\" arguments=\"--Address ${NODEID} --Nickname ${NODEID} --DataDirectory shadow.data/hosts/${NODEID} --GeoIPFile ~/.shadow/share/geoip --defaults-torrc conf/tor.common.torrc -f conf/tor.relay.torrc --BandwidthRate 1024000 --BandwidthBurst 1024000\" />")
	print("<process plugin=\"torctl\" starttime=\"61\" arguments=\"localhost 9051 STREAM,CIRC,CIRC_MINOR,ORCONN,BW,STREAM_BW,CIRC_BW,CONN_BW\"/>")
	print("</host>")

def print_exits(number):
	print("<host id=\"exit\" quantity=\""+str(number)+"\" bandwidthdown=\"10240\" bandwidthup=\"10240\">")
	print("<process plugin=\"tor\" preload=\"tor-preload\" starttime=\"60\" arguments=\"--Address ${NODEID} --Nickname ${NODEID} --DataDirectory shadow.data/hosts/${NODEID} --GeoIPFile ~/.shadow/share/geoip --defaults-torrc conf/tor.common.torrc -f conf/tor.exit.torrc --BandwidthRate 1024000 --BandwidthBurst 1024000\" />")
	print("<process plugin=\"torctl\" starttime=\"61\" arguments=\"localhost 9051 STREAM,CIRC,CIRC_MINOR,ORCONN,BW,STREAM_BW,CIRC_BW,CONN_BW\"/>")
	print("</host>")

def print_header(time):
	print("<!-- stoptime is the length of our experiment in seconds -->")
	print("<shadow stoptime=\""+str(time)+"\" preload=\"~/.shadow/lib/libshadow-interpose.so\" environment=\"OPENSSL_ia32cap=~0x200000200000000;EVENT_NOSELECT=1;EVENT_NOPOLL=1;EVENT_NOKQUEUE=1;EVENT_NODEVPOLL=1;EVENT_NOEVPORT=1;EVENT_NOWIN32=1\">")
	print("<!-- our network -->")
	print("<topology>")
	print("<![CDATA[<?xml version=\"1.0\" encoding=\"utf-8\"?><graphml xmlns=\"http://graphml.graphdrawing.org/xmlns\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd\">")
	print("<key attr.name=\"packetloss\" attr.type=\"double\" for=\"edge\" id=\"d9\" />")
	print("<key attr.name=\"jitter\" attr.type=\"double\" for=\"edge\" id=\"d8\" />")
	print("<key attr.name=\"latency\" attr.type=\"double\" for=\"edge\" id=\"d7\" />")
	print("<key attr.name=\"type\" attr.type=\"string\" for=\"node\" id=\"d5\" />")
	print("<key attr.name=\"bandwidthup\" attr.type=\"int\" for=\"node\" id=\"d4\" />")
	print("<key attr.name=\"bandwidthdown\" attr.type=\"int\" for=\"node\" id=\"d3\" />")
	print("<key attr.name=\"countrycode\" attr.type=\"string\" for=\"node\" id=\"d2\" />")
	print("<key attr.name=\"ip\" attr.type=\"string\" for=\"node\" id=\"d1\" />")
	print("<key attr.name=\"packetloss\" attr.type=\"double\" for=\"node\" id=\"d0\" />")
	print("<graph edgedefault=\"undirected\">")
	print("<node id=\"poi-1\">")
	print("<data key=\"d0\">0.0</data>")
	print("<data key=\"d1\">0.0.0.0</data>")
	print("<data key=\"d2\">US</data>")
	print("<data key=\"d3\">10240</data>")
	print("<data key=\"d4\">10240</data>")
	print("<data key=\"d5\">net</data>")
	print("</node>")
	print("<edge source=\"poi-1\" target=\"poi-1\">")
	print("<data key=\"d7\">50.0</data>")
	print("<data key=\"d8\">0.0</data>")
	print("<data key=\"d9\">0.0</data>")
	print("</edge>")
	print("</graph>")
	print("</graphml>]]>")
	print("</topology>")
	print("<!-- the plug-ins we will be using -->")
	print("<plugin id=\"tgen\" path=\"~/.shadow/bin/tgen\" />")
	print("<plugin id=\"tor\" path=\"~/.shadow/lib/libshadow-plugin-tor.so\" />")
	print("<plugin id=\"tor-preload\" path=\"~/.shadow/lib/libshadow-preload-tor.so\" />")
	print("<plugin id=\"torctl\" path=\"~/.shadow/lib/libshadow-plugin-torctl.so\" />")
	print("<!-- our services -->")
	print("<host id=\"fileserver\" bandwidthdown=\"102400\" bandwidthup=\"102400\" >")
	print("<process plugin=\"tgen\" starttime=\"1\" arguments=\"conf/tgen.server.graphml.xml\" />")
	print("</host>")
	print("<host id=\"webserver\" bandwidthdown=\"102400\" bandwidthup=\"102400\" >")
	print("<process plugin=\"tgen\" starttime=\"1\" arguments=\"conf/tgen.webserver.graphml.xml\" />")
	print("</host>")
	print("<host id=\"hiddenserver\" bandwidthdown=\"102400\" bandwidthup=\"102400\" >")
	print("<process plugin=\"tgen\" starttime=\"1\" arguments=\"conf/tgen.hiddenserver.graphml.xml\" />")
	print("<process plugin=\"tor\" preload=\"tor-preload\" starttime=\"900\" arguments=\"--Address ${NODEID} --Nickname ${NODEID} --DataDirectory shadow.data/hosts/${NODEID} --GeoIPFile ~/.shadow/share/geoip --defaults-torrc conf/tor.common.torrc -f conf/tor.hiddenserver.torrc --BandwidthRate 1024000 --BandwidthBurst 1024000\" />")
	print("<process plugin=\"torctl\" starttime=\"901\" arguments=\"localhost 9051 STREAM,CIRC,CIRC_MINOR,ORCONN,BW,STREAM_BW,CIRC_BW,CONN_BW\"/>")
	print("</host>")
	print("<!-- our Tor network infrastructure -->")
	print("<host id=\"4uthority\" bandwidthdown=\"10240\" bandwidthup=\"10240\" iphint=\"100.0.0.1\" >")
	print("<process plugin=\"tor\" preload=\"tor-preload\" starttime=\"1\" arguments=\"--Address ${NODEID} --Nickname ${NODEID} --DataDirectory shadow.data/hosts/${NODEID} --GeoIPFile ~/.shadow/share/geoip --defaults-torrc conf/tor.common.torrc -f conf/tor.authority.torrc --BandwidthRate 1024000 --BandwidthBurst 1024000\" />")
	print("<process plugin=\"torctl\" starttime=\"2\" arguments=\"localhost 9051 STREAM,CIRC,CIRC_MINOR,ORCONN,BW,STREAM_BW,CIRC_BW,CONN_BW\"/>")
	print("</host>")
	print("<host id=\"bridge\" iphint=\"100.0.0.1\" bandwidthdown=\"10240\" bandwidthup=\"10240\">")
	print("<process plugin=\"tor\" preload=\"tor-preload\" starttime=\"60\" arguments=\"--Address ${NODEID} --Nickname ${NODEID} --DataDirectory shadow.data/hosts/${NODEID} --GeoIPFile ~/.shadow/share/geoip --defaults-torrc conf/tor.common.torrc -f conf/tor.relay.torrc --BandwidthRate 1024000 --BandwidthBurst 1024000 --BridgeRelay 1\" />")
	print("<process plugin=\"torctl\" starttime=\"61\" arguments=\"localhost 9051 STREAM,CIRC,CIRC_MINOR,ORCONN,BW,STREAM_BW,CIRC_BW,CONN_BW\"/>")
	print("</host>")
    

print_header(12500)
print_relays(10)
print_exits(5)
print_victim()
print_clients(10)
print_webclients(40)
print_bottom()
