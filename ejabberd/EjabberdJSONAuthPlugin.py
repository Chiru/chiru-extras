#!/usr/bin/python

# Ejabberd plugin for querying user authentication from 
# custom auth server over json.

import json
import ssl
import sys
import logging
import httplib
from struct import *
import struct

# Requests for usernames outside this domain will be denied
# e.g. "chiru.cie.fi"
# Must Be set!
EJABBERD_SERVER_HOSTNAME = ""

CERTFILE = "/etc/ejabberd/localhost.crt"
KEYFILE = "/etc/ejabberd/localhost.key"
ADDRESS = "localhost"
PORT = "4443"

LOG_FILENAME = "/var/log/ejabberd/json_auth.log"
LOG_FORMAT = "%(asctime)-15s %(message)s"

logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILENAME, level=logging.DEBUG)
logger = logging.getLogger("jsonauth")

class EjabberdInputError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# Write response for ejabberd in stdout
def generate_response(success = False):
    result = 0
    if success:
        result = 1
    sys.stdout.write(struct.pack(">hh", 2, result))
    sys.stdout.flush()

# Read ejabberd messages from stdin
def ejabberd_in():
    try:
        input_len = sys.stdin.read(2)
    except IOError:
        logging.debug("IOError")
    if len(input_len) != 2:
        logging.debug("Malformed input from Ejabberd")
        raise EjabberdInputError("Malformed input from Ejabberd")
        
    (size,) = unpack(">h", input_len)
    return sys.stdin.read(size).split(":")

# Query the auth server
def send_json_query(data):
    try:
        conn = httplib.HTTPSConnection( ADDRESS,
                                        port = PORT,
                                        key_file = KEYFILE,
                                        cert_file = CERTFILE )
    except Exception, ex:
        logger.warning("Exception raised while connecting to remote host: {0}".format(ex))
        return {}
    
    json_data = json.dumps(data)
    headers = {"Content-type": "application/json",
               "Content-length": str(len(json_data)) }
    
    try:
        conn.request("POST", "/authenticate", json_data, headers)
    except Exception, ex:
        logger.warning("Exception raised in POST: {0}".format(ex))
        return {}
    
    httpresponse = conn.getresponse()
    conn.close()
    
    if httpresponse.status != 200:
        logger.warning("Remote server returned error code: {0}".format(httpresponse.status))
        return {}
      
    try:
        response = json.loads(httpresponse.read())
    except ValueError, msg:
        logger.warning("Malformed JSON data returned from remote server")
        return {}
        
    return response

# Get authentication response from the auth server
def handle_auth(username, password):
    logger.debug("Sending authentication request for user: {0}".format(username))
    
    request = { "req-type":"user-authentication-request",
                  "username":username,
                  "password":password }
    response = send_json_query(request)
    
    if response.get("status") == "allow":
        logger.info("Access allowed for user: {0}".format(username))
        return True
    else:
        logger.info("Access denied for user: {0}".format(username))
        return False


logger.info("Ejabberd JSON authenticator process started")
while True:
    try:
        std_input = ejabberd_in()
    except EjabberdInputError, ex:
        logging.info("Exception raised: {0}".format(ex))
        break

    operation = std_input[0]
    
    if std_input[2] != EJABBERD_SERVER_HOSTNAME:
        logger.warning("Authentication requested for invalid user domain, denying.")
        generate_response(False)
        continue
        
    if operation == "auth":
        generate_response(handle_auth(std_input[1], std_input[3]))
        
    elif operation == "isuser":
        # no-op at the moment, could be usable in the future?
        logging.debug("Unsupported operation from Ejabberd: {0}".format("isuser"))
        generate_response(False)
        
    elif operation == "setpass":
        logging.debug("Unsupported operation from Ejabberd: {0}".format("setpass"))
        generate_response(False)
        
    elif operation == "tryregister":
        # Do we wan"t to register here?
        logging.debug("Unsupported operation from Ejabberd: {0}".format("tryregister"))
        generate_response(False)
        
    elif operation == "removeuser":
        logging.debug("Unsupported operation from Ejabberd: {0}".format("removeuser"))
        generate_response(False)
        
    elif operation == "removeuser3":
        logging.warning("Unsupported operation from Ejabberd: {0}".format("removeuser3"))
        generate_debug(False)
        
logger.info("Ejabberd JSON authenticator terminated")
