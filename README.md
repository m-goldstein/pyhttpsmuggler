# pyhttpsmuggler
Scripts related to web/request smuggling & general web hacking
## Changelog
### 9/2/2021
Implemented a WebRequest class to generate arbitrary web requests with malformed fields and/or fuzz around for TE.CL and CL.TE vulnerabilities in web server configurations.

# Todo:
## pyhttpsuggler-cli
### 1
Improve  CLI for sending arbitrary requests from the command line rather than using driver scripts like smuggle.py. Maybe I will implement this in C++ or scapy depending on the advantages each choice offers...
### 2
Add fuzzing engine script to automate fuzzing websites for various HTTP request desync attacks
