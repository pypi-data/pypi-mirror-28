#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import logging
import coloredlogs
from tkinter.ttk import *
from tkinter import StringVar
from tkinter import messagebox
from builtins import bytes
from past.builtins import basestring
import os
import sys
import tkinter
import tkinter.filedialog
import re
import base64
import collections
import itertools
from cryptography.x509.base import load_der_x509_certificate
from cryptography.hazmat.backends.openssl.x509 import _Certificate
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.serialization import load_ssh_public_key
LOG_FORMAT = '%(asctime)s [%(process)d] %(levelname)s %(message)s'
logger = logging.getLogger(__name__)
coloredlogs.install(filename='logger.log', level=logging.INFO, fmt=LOG_FORMAT)


class MainGUI(object):
    def __init__(self, master):
        self.TabStrip1 = Notebook()
        self.TabStrip1.place(relx=0.062, rely=0.071, relwidth=0.887, relheight=0.9)
        
        ################
        self.TabStrip1__Tab1 = Frame(self.TabStrip1)
        self.FilePathLabel = tkinter.Label(self.TabStrip1__Tab1, text='Chose the target files :', borderwidth=5, font=('',10,'bold'))
        self.FilePathLabel.place(x=30,y=60)
        
        self.FileName = StringVar()
        self.FileName.set('')
        self.FilePathEntry = tkinter.Entry(self.TabStrip1__Tab1, textvariable=self.FileName, borderwidth=4, width=40);
        self.FilePathEntry.place(x=30,y=120)
        
        self.ChoseBut = tkinter.Button(self.TabStrip1__Tab1, text='...', borderwidth=2, command=self.ChoseFile)
        self.ChoseBut.place(x=380,y=118)
        
        self.DetectBut = tkinter.Button(self.TabStrip1__Tab1, text='Detect', font='bold', borderwidth=3, command=self.Detect_file)
        self.DetectBut.place(x=190,y=200)
        
        self.TabStrip1.add(self.TabStrip1__Tab1, text='Single file')
        #################
        
        self.TabStrip1__Tab2 = Frame(self.TabStrip1)
        self.FilePathLabel2 = tkinter.Label(self.TabStrip1__Tab2, text='Chose the directory :', borderwidth=5, font=('',10,'bold'))
        self.FilePathLabel2.place(x=30,y=60)
        
        self.DirName = StringVar()
        self.DirName.set('')
        self.FilePathEntry = tkinter.Entry(self.TabStrip1__Tab2, textvariable=self.DirName, borderwidth=4, width=40);
        self.FilePathEntry.place(x=30,y=120)
        
        self.ChoseBut = tkinter.Button(self.TabStrip1__Tab2, text='...', borderwidth=2, command=self.ChoseDirectory)
        self.ChoseBut.place(x=380,y=118)
        
        self.DetectBut = tkinter.Button(self.TabStrip1__Tab2, text='Detect', font='bold', borderwidth=3, command=self.Detect_dir)
        self.DetectBut.place(x=190,y=200)
        
        self.TabStrip1.add(self.TabStrip1__Tab2, text='Directory')
        
    def ChoseFile(self):
            
        self.FileName.set(tkinter.filedialog.askopenfilenames())
        
    def ChoseDirectory(self):
        
        self.DirName.set(tkinter.filedialog.askdirectory())
    
    def Detect_file(self):
        start1 = Detector()
        #print self.FileName.get()
        result1 = start1.main(self.FileName.get(),True)
        self.ShowResult(result1)
        return 
        
    def Detect_dir(self):
        start2 = Detector()
        result2 = start2.main(self.DirName.get(),False)
        self.ShowResult(result2)
    
    def ShowResult(self,result):
        #print result
        all_result = []
        if result == None:
            tkinter.messagebox.showinfo(title = 'Result',message = 'it\'s ok!')
        else:
            if (tkinter.messagebox.askyesno(title = 'Result',message = 'find vulnerable keys!\n export to file?') == True):
                
                with open('result.txt','w') as f:
                    f.write('file name\t\t\tidx\n\n')
                    for i,dic in enumerate(result):
                        f.write('%s\t\t\t%d\n'% (dic['fname'],dic['idx']))
                        

class Detector(object):
    def __init__(self):
        self.PEM_num = 0
        self.DER_num = 0
        self.RSA_key_num = 0
        self.SSH_key_num = 0
        self.PGP_num = 0
        self.APK_num = 0
        self.JSON_num = 0
        self.LDIFF_num = 0
        self.JKS_num = 0
        self.PKCS7_num = 0
        self.FileNames = None
        self.Pohlig_hellman = Pohlig_Hellman()
    def main(self,FileNames, isfile):
        ret = []
        if FileNames is None:
            return ret
        #print FileNames
        #print type(FileNames)
        find_flag = False
        #if FileNames.startswith('(\'') and FileNames.endswith('\')'): #string div by ','
        if isfile:
            if (startswith(FileNames,'(\'') and endswith(FileNames,'\')')) or (startswith(FileNames,'(\'') and endswith(FileNames,',)')): #to test whether the format is right
                FileNames_tuple = tuple(eval(FileNames))
                for file in FileNames_tuple:
                    if file.endswith('.tar') or file.endswith('.tar.gz'):
                        result = self.process_tar(file)
                        if result != None:
                            find_flag = True
                            ret.extend(result)
                        #ret.append(self.process_tar(file))
                    
                    else:
                        fh = open(file, 'rb')
                        with fh:
                            data = fh.read()
                        result = self.process_file(data,file)
                        if result != None:
                            find_flag = True
                            ret.extend(result)
                        #ret.append(self.process_file(data,file))
                            
            else: 
                tkinter.messagebox.showerror("error", 'the format of the filenames you entered is incorrect!')
        else:
            return self.process_dir(FileNames)
        if find_flag == True:
            return ret
        else:
            return None
        #return ret
    def process_tar(self, fname):
        ret = []
        import tarfile
        find_flag = False
        with tarfile.open(fname) as tar:
            members = tar.getmembers()
            for ti in members:
                if not ti.isfile():
                    continue
                fh = tar.extractfile(ti)
                result = self.process_file(fh.read(),ti.name)
                if result != None:
                    find_flag = True
                    ret.extend(result)
                #ret.append(self.process_file(fh.read(),ti.name))
        if find_flag == True:
            return ret
        else:
            return None
    
    def process_dir(self, dirname):
        ret = []
        dir_list = [f for f in os.listdir(dirname)]
        find_flag = False
        for fname in dir_list:
            full_path = os.path.join(dirname, fname)
            if os.path.isfile(full_path):
                with open(full_path, 'rb') as fh:
                    result = self.process_file(fh.read(), fname)
                    if result != None:
                        find_flag = True
                        ret.extend(result)
                    #ret.append(self.process_file(fh.read(), fname))
            elif os.path.isdir(full_path):
                result = self.process_dir(full_path)
                if result != None:
                    ret.extend(result)
                    return ret
                #ret.append(self.process_dir(full_path))
        if find_flag == True:
            return ret
        else:
            return None
        #return ret
    
    def process_file(self, data, fname):
        #print(fname)
        #print('\n')
        #ret = []
        if endswith(fname,'.pem') or startswith(data,'-----BEGIN CER') or startswith(data,'-----BEGIN RSA') or startswith(data,'-----BEGIN PUB') or startswith(data,'-----BEGIN PRI'):
            return self.process_pem(data,fname)
        elif endswith(fname,'.pgp') or endswith(fname,'.gpg') or endswith(fname,'.asc') or startswith(data,'-----BEGIN PGP'):
            return self.process_pgp(data,fname)
        elif endswith(fname,'.der') or endswith(fname,'.crt') or endswith(fname,'.cer') or endswith(fname,'.cert'):
            return self.process_der(data,fname)
        elif endswith(fname,'.pub') and (startswith(data,'ssh-rsa') or ('ssh-rsa' in data)):
            return self.process_ssh(data,fname)
        elif endswith(fname,'.pkcs7') or endswith(fname,'.p7') or endswith(fname,'.p7s'):
            return self.process_pkcs7(data,fname)
        else:
            logger.warning("format not supported for '%s'\n"% fname)
            return None
        #return None
        
    def process_pem(self, data, fname):
        ret = []
        find_flag = False
        data = to_string(data)
        parts = re.split(r'-----BEGIN',data)
        if len(parts) == 0:
            return None
        if len(parts[0]) == 0:
            parts.pop(0)
        data_arr = ['-----BEGIN'+ x for x in parts]
        for idx, data_block in enumerate(data_arr):
            data_block = data_block.strip()
            if startswith(data_block,'-----BEGIN CER'):
                result = self.process_pem_certificate(data_block,fname,idx)
                if result != None:
                    find_flag = True
                    ret.append(result)
                    #ret.append(self.process_pem_certificate(data_block,fname,idx))
            elif startswith(data_block,'-----BEGIN'):
                result = self.process_pem_rsakeys(data_block,fname,idx)
                if result != None:
                    find_flag = True
                    ret.append(result)
                    #ret.append(self.process_pem_rsakeys(data_block,fname,idx))
        if find_flag == True:
            return ret
        else:
            return None
        #return ret
    
    def process_pem_certificate(self, data, fname, idx):
        
        #ret = []
        try:
            
            x509 = load_der_x509_certificate(pem_to_der(data), self.get_backend())
            pub_key = x509.public_key()
            if not isinstance(pub_key, RSAPublicKey):
                return
            pub_value = pub_key.public_numbers()
            #print pub_value
            if self.pohlig_hellman_detect(pub_value.n) == True:
                find = collections.OrderedDict()
                find['fname'] = fname
                find['idx'] = idx
                #ret.append(find)
                #print find
                return find
            return None
        except Exception as e:
            logger.error("error when process the pem_certificate file '%s'\n"% fname)
            return None
            
    def process_pem_rsakeys(self, data, fname, idx):
        try:        
            from cryptography.hazmat.primitives.serialization import load_pem_public_key
            from cryptography.hazmat.primitives.serialization import load_der_public_key
            from cryptography.hazmat.primitives.serialization import load_pem_private_key
            from cryptography.hazmat.primitives.serialization import load_der_private_key
            ret = []
            if startswith(data,r'-----BEGIN RSA PUBLIC KEY') or startswith(data,r'-----BEGIN PUBLIC KEY'):
                pub_key = load_der_public_key(pem_to_der(data),self.get_backend())
                pub_value = pub_key.public_numbers()
            elif startswith(data,r'-----BEGIN RSA PRIVATE KEY') or startswith(data,r'-----BEGIN PRIVATE KEY'):
                priv_key = load_der_private_key(pem_to_der(data),None,self.get_backend())
                pub_value = priv_key.private_numbers().public_numbers
                #print pub_value
            if self.pohlig_hellman_detect(pub_value.n) == True:
                find = collections.OrderedDict()
                find['fname'] = fname
                find['idx'] = idx
                #ret.append(find)
        #print find
                return find
            return None
        except Exception as e:
            logger.error("error when process the pem_rsakeys file '%s'\n"% fname)
            return None
    def process_pgp(self, data, fname):
        try:
        
            from pgpdump.data import AsciiData
            from pgpdump.packet import PublicKeyPacket, PublicSubkeyPacket
            ret = []
            data = to_string(data)
            parts = re.split(r'-----BEGIN',data)
            if len(parts) == 0:
                return None
            if len(parts[0]) == 0:
                parts.pop(0)
            data_arr = ['-----BEGIN'+ x for x in parts]
            find_flag = False
            for idx, data_block in enumerate(data_arr):
                data_block = data_block.strip()
                if len(data_block) == 0:
                    continue
                data_block = data_block.encode()
                pgp_key_data = AsciiData(data_block)
                packets = list(pgp_key_data.packets())
                for idy, packet in enumerate(packets):
                    if isinstance(packet, PublicKeyPacket) or isinstance(packet, PublicSubkeyPacket):
                        pub_value = packet
            #print pub_value.modulus
                if self.pohlig_hellman_detect(pub_value.modulus) == True:
                    find_flag = True
                    find = collections.OrderedDict()
                    find['fname'] = fname
                    find['idx'] = idx
                    ret.append(find)
        #print find
            if find_flag == True:
                return ret
            else:
                return None
        except Exception as e:
            logger.error("error when process the pgp file '%s'\n"% fname)
            return None  
    def process_der(self, data, fname):
        try:  
            ret = []
            x509 = load_der_x509_certificate(data, self.get_backend())
            pub_key = x509.public_key()
            if not isinstance(pub_key, RSAPublicKey):
                return
            pub_value = pub_key.public_numbers()
            #print pub_value
            if self.pohlig_hellman_detect(pub_value.n) == True:
                find = collections.OrderedDict()
                find['fname'] = fname
                find['idx'] = 0
                ret.append(find)
                #print find
                return ret
            return None
        except Exception as e:
            logger.error("error when process the der file '%s'\n"% fname)
            return None
    def process_ssh(self, data, fname):
        try:
            ret = []
            data = [x.strip() for x in data.split(b'\n')]
            if len(data) > 1:
                if data[1] == '':
                    data.pop(1)
                    #print data
            find_flag = False
            for idx, data_block in enumerate(data):
                #print type(data_block)
                data_block = data_block[to_bytes(data_block).find(b'ssh-rsa'):]
                if data_block == b'':
                    continue
                ssh_key = load_ssh_public_key(data_block,self.get_backend())
                if not isinstance(ssh_key,RSAPublicKey):
                    continue
                pub_value = ssh_key.public_numbers()
                #print pub_value
                if self.pohlig_hellman_detect(pub_value.n) == True:
                    find_flag = True
                    find = collections.OrderedDict()
                    find['fname'] = fname
                    find['idx'] = idx
                    ret.append(find)
                    #print find
            if find_flag == True:
            
                return ret
            else:
                return None
        except Exception as e:
            logger.error("error when process the ssh file '%s'\n"% fname)
            return None
    def process_pkcs7(self, data, fname):
        try:
            from cryptography.hazmat.backends.openssl.backend import backend
            ret = []
            if startswith(data,'-----BEGIN'):
                data = data.decode('utf-8')
                data = re.sub(r'\s*-----\s*BEGIN\s+PKCS7\s*-----\s*','',data)
                data = re.sub(r'\s*-----\s*END\s+PKCS7\s*-----\s*','',data)
                der = base64.b64decode(data)
            bio = backend._bytes_to_bio(der)
            pkcs7 = backend._lib.d2i_PKCS7_bio(bio.bio, backend._ffi.NULL)
            backend.openssl_assert(pkcs7 != backend._ffi.NULL)
            signers = backend._lib.PKCS7_get0_signers(pkcs7, backend._ffi.NULL, 0)
            backend.openssl_assert(signers != backend._ffi.NULL)
            backend.openssl_assert(backend._lib.sk_X509_num(signers) > 0)
            x509_ptr = backend._lib.sk_X509_value(signers, 0)
            backend.openssl_assert(x509_ptr != backend._ffi.NULL)
            x509_ptr = backend._ffi.gc(x509_ptr, backend._lib.X509_free)
            x509 = _Certificate(backend, x509_ptr)
            pub_key = x509.public_key()
            if not isinstance(pub_key, RSAPublicKey):
                return
            pub_value = pub_key.public_numbers()
            #print pub_value
            if self.pohlig_hellman_detect(pub_value.n) == True:
                find = collections.OrderedDict()
                find['fname'] = fname
                find['idx'] = 0
                ret.append(find)
                #print find
                return ret
            return None
        except Exception as e:
            logger.error("error when process the pkcs7 file '%s'\n"% fname)
            return None
    def get_backend(self, backend=None):
        from cryptography.hazmat.backends import default_backend
        return default_backend() if backend is None else backend
    
    def pohlig_hellman_detect(self, num):
        return self.Pohlig_hellman.work(num)

class Pohlig_Hellman(object):
    def __init__(self):
        self.primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 
                       97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167]
        self.generator = 65537
        self.m,self.phi_m = self.get_phi_m()
        self.largest_prime = 83
        self.phi_m_factorization = self.factorization(self.phi_m,self.largest_prime)
        self.generator_order = self.get_element_order(self.generator,self.m,self.phi_m,self.phi_m_factorization)
        self.generator_order_factorization = self.factorization(self.generator_order,self.largest_prime)
    def work(self, N):
        result = self.discrete_log(N, self.generator, self.generator_order, self.generator_order_factorization, self.m)
        return result 
        
    def get_phi_m(self):
        m = 1
        phi_m = 1
        for i in self.primes:
            m = m*i
            phi_m = phi_m*(i-1)
        return m,phi_m
        
    def factorization(self, num, lim = None):
        ret = []
        while num % 2 == 0:
            num = num // 2
            ret.append(2)
        while num % 3 == 0:
            num = num // 3
            ret.append(3)
        prime = 5
        i = 2
        while prime <= lim:
            while (num % prime) == 0:
                num = num // prime
                ret.append(prime)
            prime += i
            i = 6-i
        if  num != 1:
            ret.append(num)
        return self.list_to_map(ret)
          
    def list_to_map(self, l):
        ret = {}
        for k,group in itertools.groupby(l):
            ret[k] = len(list(group))
            
        return ret
        
    def get_element_order(self, element, modulus, phi_m, phi_m_factorization):
        if pow(element,phi_m,modulus) != 1:
            return None
        order = phi_m
        for (k,power) in phi_m_factorization.items():
            for i in range(1,power+1):
                n_order = order // k
                if pow(element,n_order,modulus) == 1:
                    order = n_order
                else:
                    break
        return order
        
    def discrete_log(self, N, generator, generator_order, generator_order_factorization, modulus):
        for prime,power in generator_order_factorization.items():
            find = 0
            pri_to_power = prime ** power
            order_div_primepower = generator_order // pri_to_power
            temp_1 = pow(N,order_div_primepower,modulus)
            temp_2 = pow(generator,order_div_primepower,modulus)
            for i in range(0,pri_to_power):
                if pow(temp_2,i,modulus) == temp_1:
                    find = 1
                    break
            if find == 0:
                return False
        return True
        
def to_string(data):
    if isinstance(data,bytes):
        return data.decode('utf-8')
    if isinstance(data,basestring):
        return data

def to_bytes(data):
    if isinstance(data,bytes):
        return data
    if isinstance(data,basestring):
        return data.encode('utf-8')
        
def startswith(data, string):

    if data is None:
        return False

    if sys.version_info[0] < 3:
        return data.startswith(string)

    return to_bytes(data).startswith(to_bytes(string))

def endswith(data, string):

    if data is None:
        return False

    if sys.version_info[0] < 3:
        return data.endswith(string)

    return to_bytes(data).endswith(to_bytes(string))

def pem_to_der(data):
    data = re.sub(r'-----BEGIN .+-----','',data)
    data = re.sub(r'-----END .+-----','',data)
    data = data.replace(' ','')
    data = data.replace('\n','')
    data = data.replace('\t','')
    data = data.replace('\r','')
    return base64.b64decode(data)
    
    
if __name__ == '__main__':
    main = tkinter.Tk()
    main.title('Vulnerable keys detector')
    main.geometry('500x320')
    mypro = MainGUI(main)
    tkinter.mainloop()
    