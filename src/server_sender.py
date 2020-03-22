#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Luis Alberto Pérez García <luixal@gmail.com>

import time
from datetime import datetime
import requests

class ServerSender():
    def __init__(self, url, device_id):
        self.url = url
        self.device_id = device_id

    def http_send(self, data):
        try:
            # add read at date:
            data['readAt'] = datetime.now().__str__()
            resp = requests.post(
                self.url,
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
