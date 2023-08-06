#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Alfons
import traceback
import time
import logging
import json

log = logging.getLogger("IoT")

def start(name, description):
	"Start an IoT service"
	Alfons.info["name"] = name
	Alfons.info["description"] = description
	Alfons.Crypt.AlfonsRSA.getKey()

	ip, Alfons.info["alfons_key"] = Alfons.findServer()

	Alfons.connect(ip)

	# Retry until the device have been allowed
	while not Alfons.register().headers["success"]:
		time.sleep(30)
	
	Alfons.IoT.addCommand("list", "List commands on the IoT", _commandList)

	def handler(request):
		if request.command in Alfons.info["iot_commands"]:
			try:
				return Alfons.info["iot_commands"][request.command]["function"](request)
			except:
				log.critical("Request crashed on the IoT device", exc_info=1)
				return ({"success": False, "message": "Request crashed on the IoT device"}, {})

		return ({"success": False, "message": "Command not found"}, {})

	while True:
		try:
			Alfons.listen(handler)
		except KeyboardInterrupt:
			Alfons.eradicate()
			break
		except:
			log.critical("Crashed", exc_info=1)

def addCommand(command, description, function):
	if not "iot_commands" in Alfons.info:
		Alfons.info["iot_commands"] = {}
	Alfons.info["iot_commands"][command] = {"command": command, "description": description, "function": function}

def _commandList(request):
	if not "data-transfer" in request.headers or request.headers["data-transfer"] != "expected":
		return {"data-transfer": "required", "success": False}
	
	commands = []

	for c in Alfons.info["iot_commands"]:
		command = Alfons.info["iot_commands"][c]
		commands.append({"command": command["command"], "description": command["description"]})

	Alfons.transportString(json.dumps({"items": commands}), request)

	return {"success": True}