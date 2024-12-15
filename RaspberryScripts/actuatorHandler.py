# -*- coding: utf-8 -*-
#!/usr/bin/env python
import requests, json, hashlib, uuid, time   

class ActuatorHandler:

    actuator_is_on = False

    def __init__(self):
        # This is where to insert your generated API keys (http://api.telldus.com/keys)
        self.pubkey = "FEHUVEW84RAFR5SP22RABURUPHAFRUNU"  # Public Key
        self.privkey = "ZUXEVEGA9USTAZEWRETHAQUBUR69U6EF" # Private Key
        self.token = "8aba8385b6f65e0f7bf274e5e673f04b05d541a1e" # Token
        self.secret = "ecd6a7203c64ec98469df1da577eeff3" # Token Secret 

        self.turnOnActuator()

        

    def turnOnActuator(self):

        localtime = time.localtime(time.time())
        timestamp = str(time.mktime(localtime))
        nonce = uuid.uuid4().hex
        oauthSignature = (self.privkey + "%26" + self.secret)

        # GET-request
        response = requests.get(
            url="https://pa-api.telldus.com/json/device/turnOn",
            params={
                "id": "SET-ID-HERE",    #!!!
            },
            headers={
                "Authorization": 'OAuth oauth_consumer_key="{pubkey}", oauth_nonce="{nonce}", oauth_signature="{oauthSignature}", oauth_signature_method="PLAINTEXT", oauth_timestamp="{timestamp}", oauth_token="{token}", oauth_version="1.0"'.format(pubkey=self.pubkey, nonce=nonce, oauthSignature=oauthSignature, timestamp=timestamp, token=self.token),
                },
            )
            # Output/response from GET-request	
        
        self.actuator_is_on = True
        return response.json()

    def turnOffActuator(self):

        localtime = time.localtime(time.time())
        timestamp = str(time.mktime(localtime))
        nonce = uuid.uuid4().hex
        oauthSignature = (self.privkey + "%26" + self.secret)

        # GET-request
        response = requests.get(
            url="https://pa-api.telldus.com/json/device/turnOff",
            params={
                "id": "SET-ID-HERE",    #!!!
            },
            headers={
                "Authorization": 'OAuth oauth_consumer_key="{pubkey}", oauth_nonce="{nonce}", oauth_signature="{oauthSignature}", oauth_signature_method="PLAINTEXT", oauth_timestamp="{timestamp}", oauth_token="{token}", oauth_version="1.0"'.format(pubkey=self.pubkey, nonce=nonce, oauthSignature=oauthSignature, timestamp=timestamp, token=self.token),
                },
            )
            # Output/response from GET-request	

        self.actuator_is_on = False

        return response.json()
    

actuator_handler = ActuatorHandler()