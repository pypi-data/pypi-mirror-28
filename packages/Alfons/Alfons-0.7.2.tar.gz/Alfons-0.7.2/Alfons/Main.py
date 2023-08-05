#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string
import json
import socket
import time
import Alfons.Crypt
import traceback
import threading
import logging
import os
import sys

HEADERS_IN_DATA = ["success", "message"]
ACP_VERSION = "0.6"

deviceSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

info = {}
requests = {}

path = os.path.dirname(os.path.abspath(sys.argv[0]))

log = logging.getLogger("alfons")

logging.basicConfig(filename=path + "/" + os.path.splitext(os.path.basename(os.path.abspath(sys.argv[0])))[0] + ".log",level=logging.DEBUG, format="%(asctime)s %(name)s %(levelname)s %(filename)s line %(lineno)d %(funcName)s \t %(message)s", datefmt="%Y-%m-%d %H:%M:%S %z")

def request(command, dest, data, headers={}, **kwargs):
	"Send a request with the command, data and headers to the destination"
	headers["sender"] = info["device_id"]
	headers["destination"] = dest

	request = AlfonsRequest().setFromComponents(command, headers, data, AlfonsRequest.createRequestId())
	requestId = request.requestId
	requestString = request.export()
	
	sendToServer(requestString)

	if not kwargs.get("callback", None) is None:
		requests[requestId] = {}
		requests[requestId]["callback"] = kwargs.get("callback")
		requests[requestId]["timestamp"] = int(time.time())
		
		return listen(None, forId=requestId)

	return request

def sendToServer(s):
	"Encrypt a string with the server public key and send it to the server"
	s = Alfons.Crypt.encrypt(s, info["alfons_key"])
	deviceSocket.sendall(s)

def findServer(ip = "255.255.255.255"):
	"Find the server and register"
	global info
	
	discoverRequestString = AlfonsRequest().setFromComponents("discover", {"destination": "alfons"}, {}, AlfonsRequest.createRequestId()).export()

	broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	def broadcast():
		while True:
			try:
				broadcastSocket.sendto(discoverRequestString, (ip, 27373))
			except:
				break
			time.sleep(3)

	thread = threading.Thread(target=broadcast)
	thread.daemon = True
	thread.start()
	
	try:
		data, addr = broadcastSocket.recvfrom(2028)
	except KeyboardInterrupt as e:
		broadcastSocket.close()
		exit()

	broadcastSocket.close()

	response = AlfonsResponse().setFromString(data)

	if not response.headers["success"]:
		return False
	
	info["ip"] = addr[0]
	info["alfons_key"] = Alfons.Crypt.AlfonsRSA.importKey(response.body["public_key"])
	connect(addr[0])

	def registered(response):
		if response.headers["success"]:
			return True
		else:
			return False

	body = {"id": info["device_id"], "name": info["name"], "description": info["description"], "public_key": info["public_key"].exportKey()}
	return request("register", "alfons", body, callback=registered)

def connect(ip):
	"Connect to the ip"
	global info
	info["ip"] = ip
	deviceSocket.connect((ip, 27373))

def close():
	"Close the connection to the server"
	deviceSocket.close()

def createErrorResponse(message, requestId):
	"Create a response string with an error message"
	return AlfonsResponse().setFromComponents({"destination": info["device_id"], "sender": "alfons", "success": False, "message": message}, {}, requestId)

def listen(run, **kwargs):
	"Listen for a message from the server"
	if kwargs.get("forId", False):
		deviceSocket.settimeout(kwargs.get("timeout", 7))
	else:
		deviceSocket.settimeout(None)

	while True:
		try:
			data, addr = deviceSocket.recvfrom(2028)
		except socket.timeout: # Timeout will only occur if 'forId' is set due to 'deviceSocket.settimeout(kwargs.get("timeout", 7))'
			requestId = kwargs.get("forId")
			response = createErrorResponse("Timed out", requestId)
			requests[requestId]["callback"](response)
			return response

		if not data.startswith("ACP/" + ACP_VERSION):
			(data, signature) = Alfons.Crypt.decrypt(data)
			if not Alfons.Crypt.AlfonsRSA.verify(data, signature, info["alfons_key"]):
				print "Not valid"
				continue

		r = decodeR(data)
		
		if not r:
			continue

		if r["type"] == "request":
			if not run is None:
				request = AlfonsRequest().setFromComponents(r["command"], r["headers"], r["body"], r["request_id"])

				try:
					d = run(request)
					if d is None:
						log.error("Didn't get any data from command (%s)" % request.command)
					data = d if d is not None else {"success": False, "message": "Didn't get any data from command"}
				except:
					log.error("Error executing command (%s) on IoT" % request.command)
					data = {"success": False, "message": "Error executing command on IoT"}
				
				response = AlfonsResponse().setFromDataAndRequest(data, request).export()
				deviceSocket.sendall(response)
			else:
				response = AlfonsResponse().setFromComponents({"sender": info["device_id"], "destination": r["headers"]["sender"], "success": False, "message": "This device does not take any commands (right now)"}, {}, r["request_id"])
				deviceSocket.sendall(response.export())
		else:
			response = AlfonsResponse().setFromComponents(r["headers"], r["body"], r["request_id"])
			forId = kwargs.get("forId", False)
			if forId == response.requestId:
				if response.requestId in requests:
					requests[response.requestId]["callback"](response)

				return response

def eradicate():
	"Send an eradicate request to the server and listen for the response"
	log.info("Eradicating")
	r = request("eradicate", "alfons", {"id": info["device_id"]})
	return listen(None, forId=r.requestId)

class AlfonsRequest:
	"An object holding all information about a request"
	address = ("", 0)

	@staticmethod
	def createRequestId():
		"Generate a request id"
		return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))

	def setFromComponents(self, command, headers, body, requestId):
		"Set the response info from components"
		self.command = command
		self.headers = headers
		self.body = body
		self.requestId = requestId

		return self

	def setFromString(self, s):
		"Set the response info from a strign"
		r = decodeR(s)
		self.setFromComponents(r["command"], r["headers"], r["body"], r["request_id"])

		return self

	def export(self):
		"Export the object to a string"
		body = json.dumps(self.body)
		
		requestString = "ACP/" + ACP_VERSION + " " + self.command + " " + self.requestId

		if not "sender" in self.headers:
			self.headers["sender"] = Alfons.info["device_id"]

		for h in self.headers:
			requestString += "\n" + h.capitalize() + ": " + self.headers[h]

		requestString += "\n\n" + body
		
		return requestString

class AlfonsResponse:
	"An object holding all info about a response"
	
	def __init__(self):
		self.headers = {}
		self.body = {}
		self.requestId = ""

	def setFromDataAndRequest(self, data, request):
		"Set info from data and request"

		# If a header is set in the data, move it to the 
		for header in HEADERS_IN_DATA:
			if header in data:
				self.headers[header] = data[header]
				data.pop(header)
		
		return self.setFromBodyAndRequest(data, request)

	def setFromComponents(self, headers, body, requestId):
		"Set info from components"
		self.headers = headers
		self.body = body
		self.requestId = requestId

		return self

	def setFromString(self, s):
		"Set info from a string"
		r = decodeR(s)
		self.setFromComponents(r["headers"], r["body"], r["request_id"])

		return self

	def setFromBodyAndRequest(self, body, request):
		"Set info from body and a request"
		# Copy data from request
		self.headers["sender"] = request.headers["destination"]
		self.headers["destination"] = request.headers["sender"]
		self.requestId = request.requestId
		self.body = body
		return self

	def export(self):
		"Export the object to a string"
		response = "ACP/" + ACP_VERSION + " " + self.requestId

		for h in self.headers:
			response += "\n" + h.capitalize() + ": " + str(self.headers[h])

		response += "\n\n" + json.dumps(self.body)

		return response

def decodeR(r, sender = None):
	"Decode a request or response to a dict"
	requestId = ""
	headers = {}
	body = {}

	response = {}
	
	try:
		parts = r.split("\n\n", 1)
		sHeaders = parts[0].split("\n")
		sBody = parts[1]
		topRow = sHeaders.pop(0).split(" ")
		
		# Remove the first object (protocol), and get the last (id)
		topRow.pop(0)
		requestId = topRow.pop()
		
		response["request_id"] = requestId

		# If it's a request there will be a command
		if len(topRow) == 1:
			response["type"] = "request"
			response["command"] = topRow.pop()
		else:
			response["type"] = "response"

		# Convert the headers to a dict
		for h in sHeaders:
			parts = h.split(": ")
			key = parts[0].lower()
			value = parts[1]

			if value == "True":
				value = True
			elif value == "False":
				value = False

			headers[key] = value
		
		response["headers"] = headers
		
		body = json.loads(sBody)
		
		response["body"] = body
	except:
		print "Not valid ACP/" + ACP_VERSION
		return {}

	return response