# aws_check_for_domain_hijacking.py
===================================

Description:
============
	Script has been written in python 2.7
	This script fetches domains from AWS
	For each domain on AWS, it fetches corresponding subdomains
	It checks all these subdomains if they are vulnerable to subdomain hijacking
	Writes output to multiple files

Usage:
======
	1. Configure aws credentials on your system
	2. run this "sudo python2 aws_check_for_domain_hijacking.py"

Future Prospects:
=================
	1. Script will include a known endpoint check against subdomain list
	2. Script can gatehr more subdomains from publicly accessible resources like shodan, google etc

