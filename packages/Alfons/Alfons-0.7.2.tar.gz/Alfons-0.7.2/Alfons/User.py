#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import json
import Alfons
import time
import string
import random

TOKEN_TIME_LENGTH = 3600

def verify(token, sender):
	(head, body, signature) = token.split(".")

	payload = json.loads(base64.b64decode(body))

	# Verify the sender
	if payload["device"] != sender:
		return False

	# Verify expired
	if payload["exp"] <= time.time():
		return False

	# Verify the signature
	signValid = Alfons.AlfonsRSA.verify(head + "." + body, signature, Alfons.info["alfons_key"])

	if not signValid:
		return False

	return payload

def verifyAuth(auth, sender):
	auth = auth.split(" ")
	if not auth[0] == "Bearer":
		return False
	else:
		return verify(auth[1], sender)

def generateTokens(username, deviceId):
	# Set up data
	head = {}
	body = {}

	head["typ"] = "JWT"
	head["alg"] = "RS256"

	body["sub"] = username
	body["username"] = username
	body["device"] = deviceId
	
	body["iat"] = time.time()
	body["exp"] = time.time() + TOKEN_TIME_LENGTH
	body["iss"] = Alfons.info["device_id"]

	# Encode the data
	headEncoded = base64.b64encode(json.dumps(head))
	bodyEncoded = base64.b64encode(json.dumps(body))

	# Sign encoded data
	sign = Alfons.AlfonsRSA.sign(headEncoded  + "." + bodyEncoded)

	# Combine the encoded data and signature
	accessToken = headEncoded + "." + bodyEncoded + "." + sign
	# Create a random string to be used as refresh token
	refreshToken =  "".join(random.choice(string.letters + string.digits) for _ in range(20))

	return {"access": accessToken, "refresh": refreshToken}

def requirePermissions(permissions, request):
	if "permissions" in request.headers:
		namespace = request.headers["destination"] + ":"
		userPermissions = request.headers["permissions"].replace(namespace, "").split(" ")
		
		for p in permissions:
			if not p in userPermissions:
				return False
		return True
	else:
		return False