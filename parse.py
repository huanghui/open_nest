#!/usr/bin/env python3

import re
import sys
import datetime
import subprocess
from Crypto.Cipher import AES
from binascii import a2b_hex

import uuid

class check_license_file():

    def license_check(self):
        license_dic = self.parse_license_file()
        print(license_dic)
        sign = self.decrypt(license_dic['Sign'])
        sign_list = sign.split('#')
        #print(sign_list)
        mac = sign_list[0].strip()
        date = sign_list[1].strip()
        if (mac != license_dic['MAC']) or (date != license_dic['Date']):
            print('*Error*: License file is modified!')
            sys.exit(1)
        # Check MAC and effective date invalid or not.
        if len(sign_list) == 2:
            #mac = self.get_mac()
            #mac="02:42:8f:92:4a:9d"
            mac=self.get_mac_address()
            current_date = datetime.datetime.now().strftime('%Y%m%d')
            if sign_list[0] != mac:
                print("mac=",mac)
                print(sign_list[0])
                print('*Error*: Invalid host!')
                sys.exit(1)
            # Current time must be before effective date.

            if sign_list[1] < current_date:
                print('*Error*: License is expired!')
                sys.exit(1)

            print("恭喜您，产品还在有效期内")
            #print(sign_list)
            return sign_list
        else:
            print('*Error*: Wrong Sign setting on license file.')
            sys.exit(1)

    def parse_license_file(self):
        license_dic = {}
        license_file = 'License.dat'
        #print("help")
        #print(license_file)
        with open(license_file, 'r') as LF:
            for line in LF.readlines():
                if re.match('^\s*(\S+)\s*:\s*(\S+)\s*$', line):
                    my_match = re.match('^\s*(\S+)\s*:\s*(\S+)\s*$', line)
                    license_dic[my_match.group(1)] = my_match.group(2)
    
        return (license_dic)

    def decrypt(self, content):
        aes = AES.new(b'2021052020210520', AES.MODE_CBC, b'2021052020210520')
        decrypted_content = aes.decrypt(a2b_hex(content.encode('utf-8')))
        return (decrypted_content.decode('utf-8'))

    def get_mac(self):
        mac = ''
        SP = subprocess.Popen('/sbin/ifconfig', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        (stdout, stderr) = SP.communicate()
        for line in str(stdout, 'utf-8').split('\n'):
            if re.match('^\s*ether\s+(\S+)\s+.*$', line):
                my_match = re.match('^\s*ether\s+(\S+)\s+.*$', line)
                mac = my_match.group(1)
                break
        return mac
    import uuid

    def get_mac_address(self):
        mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e+2] for e in range(0,11,2)])



if __name__ == '__main__':
    # check license file
    check_license_file().license_check()