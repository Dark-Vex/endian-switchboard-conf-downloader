#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (C) 2018  Daniele De Lorenzi - d.delorenzi@fastnetserv.net
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.

import urllib2
import base64
import json
import ssl

__author__ = "Daniele De Lorenzi <d.delorenzi@fastnetserv.net>"
__date__ = "2018-01-05"
__version__ = "1.0"

url = 'https://<switchboard-url>/manage/status/status.access.config/'

username = '<email>'
password = '<mysuperpassword>'

request = urllib2.Request(url)
skipssl = ssl._create_unverified_context()
base64string = base64.b64encode('%s:%s' % (username, password))
request.add_header("Authorization", "Basic %s" % base64string)
result = urllib2.urlopen(request, context=skipssl)

data = json.load(result)

credentials_file = open("credentials","w")
credentials_file.write(username)
credentials_file.write("\n")
credentials_file.write(password)
credentials_file.close()

openvpn_file = open("openvpn_conf.ovpn","w")
openvpn_file.write(data['openvpn_conf'])
openvpn_file.write("\nauth-user-pass /root/credentials")
openvpn_file.write("\n<ca>\n")
openvpn_file.write(data['openvpn_cert'])
openvpn_file.write("\n</ca>")
openvpn_file.close()

openvpn_fallback_file = open("openvpn_fallback_conf.ovpn","w")
openvpn_fallback_file.write(data['fallback_openvpn_conf'])
openvpn_fallback_file.write("\nauth-user-pass /root/credentials")
openvpn_fallback_file.write("\n<ca>\n")
openvpn_fallback_file.write(data['openvpn_cert'])
openvpn_fallback_file.write("\n</ca>")
openvpn_fallback_file.close()
