# -*- coding: utf-8 -*-
import json
import os
import sys

import requests

from flask import Flask, make_response, request


class Handler:
    app = Flask(__name__)

    def __init__(self) -> None:
        super().__init__()
        self.account_id = os.getenv('ACCOUNT_ID')
        self.passcode = os.getenv('ACCOUNT_PASSCODE')

    @staticmethod
    def _get_event(identity, event_name, event_props):
        return {
            'identity': identity,
            'type': 'event',
            'evtName': event_name,
            'evtData': event_props or {}
        }

    @staticmethod
    def _get_profile(identity, profile):
        return {
            'identity': identity,
            'type': 'profile',
            'profileData': profile
        }

    def _push(self, d):
        res = requests.post(
            'https://api.clevertap.com/1/upload',
            json={'d': d},
            headers={
                'X-CleverTap-Account-Id': self.account_id,
                'X-CleverTap-Passcode': self.passcode,
                'Content-Type': 'application/json; charset=utf-8',
            })
        return res.json()

    def push(self):
        req = request.get_json()
        event_name = req.get('event')
        event_props = req.get('properties')
        profile = req.get('profile')
        identity = req['identity']

        if event_name is not None:
            res = self._push([
                self._get_event(identity, event_name, event_props)
            ])
        elif profile is not None:
            res = self._push([
                self._get_profile(identity, profile)
            ])
        else:
            res = {
                'status': 'failed',
                'reason': 'At least one of profile or event must be specified'
            }

        return self.end(res)

    @staticmethod
    def end(res):
        resp = make_response(json.dumps(res))
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return resp


if __name__ == '__main__':
    if os.getenv('ACCOUNT_ID') is None \
            or os.getenv('ACCOUNT_PASSCODE') is None:
        print('Environment variable ACCOUNT_ID/ACCOUNT_PASSCODE not found.')
        sys.exit(1)

    handler = Handler()
    handler.app.add_url_rule('/push', 'push', handler.push,
                             methods=['post'])
    handler.app.run(host='0.0.0.0', port=8000)
