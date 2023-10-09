# Network Suit
A set of network tools with real world application, that I wrote either as student project or my personal hobby. These Include traceroute, subnetter, etc.

## subnetter
`python subnetter.py`<br />
This is a subnetting tool for IPv4 CIDR. Script is highly reliable and supports both doted decimal notation as well as slash notation. Upon execution asks for network address and netmask, then it assists user by suggesting all combinations of number of network/hosts available, when users selects a plan the scripts lists all the new networks with their range of hosts, and special addresses i.e. network address, broadcast address.

## ip validate
This directory includes seven python scripts that validate IPv4 format using different modules as well as manually.

## proxy
This is a simple web proxy that binds on the port 8000. By default it just forwards http traffic but the program can be extended to further process the request before sending it to the server. This is done in the **process_request** handler function which is called upon receiving any new request with the request being forwarded to it as an argument.
