#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Luis Alberto Pérez García <luixal@gmail.com>

import time
from datetime import datetime
import requests

class ServerSender():
    def __init__(self, url, device_id, http_auth, http_auth_username, http_auth_password):
        self.url = url
        self.device_id = device_id
        # if auth data provided, build auth param:
        if (http_auth and (http_auth.lower() == 'basic') and http_auth_username and http_auth_password):
            self.auth = requests.auth.HTTPBasicAuth(http_auth_username, http_auth_password)
        elif (http_auth and (http_auth.lower() == 'digest') and http_auth_username and http_auth_password):
            self.auth = requests.auth.HTTPDigestAuth(http_auth_username, http_auth_password)
        else:
            self.auth = False

    def http_send(self, data):
        try:
            # add read at date:
            data['readAt'] = datetime.now().__str__()
            resp = requests.post(
                self.url,
                auth=self.auth,
                json=data,
                headers={
                    "x-device-id": self.device_id,
                    "Content-Type": "application/json"
                }
            )

            if resp.ok:
                return True
            else:
                return False
        except:
            return False
