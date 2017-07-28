#!/usr/bin/env python

import requests
from lxml import html,etree

LOGIN_URL = "https://account.mojang.com/login"


# Issue a get request to the website to get the csrf_token
def getAuthToken():
	headers = {
		"Host": "account.mojang.com",
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Encoding":"gzip, deflate, sdch, br",
		"Accept-Language":"it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4",
		"Connection":"keep-alive",
 		"Upgrade-Insecure-Requests":"1",
		"Referer": "https://account.mojang.com/login",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
	}

	result = requests.get(LOGIN_URL, headers=headers)		# Get request to the login page

	tree = html.fromstring(result.text)
	return list(set(tree.xpath("//input[@name='authenticityToken']/@value")))[0]# Returning csfr_token needed for authentication

# Returns the dict with the data
def buildPayload(auth,email,password):
	return {
  		'email': email,
  		'password': password,
		'rememberMe': 'true',
		'authenticityToken': auth,
	}


# Performs the login and checks for account subscription
def login(email,password):
	token = getAuthToken()
	payload = buildPayload(token,email,password)

	headers = {
		"Host": "account.mojang.com",
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Encoding":"gzip, deflate, sdch, br",
		"Accept-Language":"it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4",
		"Connection":"keep-alive",
 		"Upgrade-Insecure-Requests":"1",
		"Referer": "https://account.mojang.com/login",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
	}

	login = requests.post(LOGIN_URL, headers=headers, data=payload)	# Perform the login

	print login.text

	if "Error" or "error" in login.text:
		return [False,"Dead"]
	elif "Confirm" in login.text:
		return [True,"Working, non-full access"]
	elif "My Games" in login.text:
		return [True,"Working, full access"]
