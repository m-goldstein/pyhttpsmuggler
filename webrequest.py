import socket
import ssl
import requests
###############################################################################
################# Utility class definitions and scoped constants ##############
###############################################################################
class ColorPallete:
    def __init__(self,color='reset'):
        self.color_modes = {\
        'purple':'\033[1;35;48m',\
        'cyan':'\033[1;36;48m',\
        'bold':'\033[1;37;48m',\
        'blue':'\033[1;34;48m',\
        'green':'\033[1;32;48m',\
        'yellow':'\033[1;33;48m',\
        'red':'\033[1;31;48m',\
        'black':'\033[1;30;48m',\
        'UNDERLINE':'\033[4;37;48m',\
        'reset':'\033[1;37;0m'\
        }
        self.set_color(color)
    
    def set_color(self, color='reset'):
        print(self.color_modes[color],end='')
    
    def log(self, color='reset', msg=''):
        print(self.color_modes[color],end='')
        print(msg,end='')
        print(self.color_modes['reset'])

RN = '\r\n'
PREFIX = '0\r\n\r\n'
TRAILER = '-'*80
padding = ' '

options = {\
        'Transfer-Encoding':'chunked',\
        'Content-Type':'application/x-www-form-urlencoded'\
         }

user_agents = {\
    'Mozilla':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',\
    'Chrome':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',\
    'Edge':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',\
    'Safari':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1',\
    'IE':'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)'\
    }
###############################################################################
###############################################################################

class WebRequest:
    def __init__(self, host='',port=80,ngrok='',method = 'GET',endpoint='/',http_version=1.1,prefix=PREFIX,
            options={'Transfer-Encoding':'chunked','Content-Type':'application/x-www-form-urlencoded'},special_formatting=False,debug=True):
        self.databuf = None
        self.headers = {}
        self.debug = debug
        self.request_string = None
        
        self.host = host
        self.port = port
        self.ngrok = ngrok
        self.endpoint = endpoint
        self.method = method
        self.http_version = http_version

        self.body = prefix
        self.headers['Content-Length'] = str(len(self.body))

        self.request_msg = '{} {} HTTP/{}{}'.format(self.method,self.endpoint,self.http_version,RN)
        self.request_host = 'Host: {}{}'.format(self.host, RN)
        self.key_order = ['Content-Length','Transfer-Encoding','Content-Type']

        for key in options:
            if key not in self.key_order:
                self.key_order.append(key)
            if not special_formatting:
                self.headers[key] = options[key]
            else:
                self.headers[key] = padding*4+options[key] if key == 'Transfer-Encoding' else options[key]

        self.cp = ColorPallete()
    def make_custom_body(self, length=0,data=''):
        self.body = data
        self.headers['Content-Length'] = str(length)
        if self.debug:
            first = self.body[:length] if len(self.body) > int(self.headers['Content-Length']) else self.body
            second = self.body[length:] if len(self.body) > int(self.headers['Content-Length']) else ''
            print('Body:\n',end='')
            self.cp.set_color('purple')
            print('{}'.format(first),end='')
            self.cp.set_color('reset')
            self.cp.set_color('cyan')
            print('{}'.format(second),end='')
            self.cp.set_color('reset')
            print('\n{}'.format(TRAILER))

    def make_body(self, data=PREFIX, options=[],use_body_len=True,length=len(PREFIX),use_custom=False,custom_data=''):
        if use_custom:
            self.make_custom_body(length=length,data=custom_data)
            return
        self.body = data
        for opt in options:
            self.body += opt + RN
        self.headers['Content-Length'] = str(len(self.body)) if use_body_len else str(length)
        if self.debug:
            first = self.body[:length] if len(self.body) > int(self.headers['Content-Length']) else self.body
            second = self.body[length:] if len(self.body) > int(self.headers['Content-Length']) else ''
            print('Body:\n',end='')
            self.cp.set_color('purple')
            print('{}'.format(first),end='')
            self.cp.set_color('reset')
            self.cp.set_color('cyan')
            print('{}'.format(second),end='')
            self.cp.set_color('reset')
            print('\n{}'.format(TRAILER))
    
    def make_request_msg(self):
        self.request_string = ''
        self.request_string = (self.request_msg + self.request_host)
        for key in self.key_order:
            self.request_string += '{}: {}'.format(key,self.headers[key])
            self.request_string += RN
        self.request_string += RN
        self.request_string += self.body
        if self.debug:
            print('Request:\n{}\n{}'.format(self.request_string,TRAILER))
        return self.request_string

    def connect(self,use_ssl=True):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sslsock = ssl.create_default_context().wrap_socket(self.sock, server_hostname=self.host) if use_ssl else self.sock
            self.sslsock.connect((self.host,self.port))
            if self.debug:
                self.cp.log(color='green',msg='Created socket connection to {}:{}'.format(self.host,self.port))

        except Exception as e:
            self.cp.log(color='red',msg='[connect] Exception: {}'.format(e))
    
    def send(self, message):
        try:
            self.sslsock.sendall(message.encode())
            if self.debug:
                self.cp.log(color='green',msg='Sent {} bytes to {}:{}'.format(len(message),self.host,self.port))
        except Exception as e:
            self.cp.log(color='red',msg='[send] Exception: {}'.format(e))
    
    def recv(self):
        try:
            self.databuf = self.sslsock.recv(1024)
            if self.debug:
                self.cp.log(color='green',msg='Received {} bytes from {}:{}'.format(len(self.databuf),self.host,self.port))
            print('{}'.format(self.databuf))
            print('{}'.format(TRAILER))
        except Exception as e:
            self.cp.log(color='red',msg='[recv] Exception: {}'.format(e))
    
    def close(self):
        try:
            self.sslsock.close()
            if self.debug:
                self.cp.log(color='green',msg='Closed socket')
        except Exception as e:
            self.cp.log(color='red',msg='[close] Exception: {}'.format(e))
