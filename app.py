# -*- coding: utf-8 -*-
import json
import os
import sys

import requests
from flask import Flask, make_response, request
from time import sleep


class Handler:
    app = Flask(__name__)

    def __init__(self):
        #super().__init__()
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

    @staticmethod
    def _get_eventDelails(eventName, fromDate, toDate):
        return {
            'event_name': eventName,
            'from': fromDate,
            'to': toDate or {}
        }

    @staticmethod
    def _get_eventCount(eventName, eventProps, fromDate, toDate):
        return {
            'event_name': eventName,
            'event_properties': eventProps,
            'from': fromDate,
            'to': toDate or {}
        }

    @staticmethod
    def _get_profileCount(eventName, eventProps, fromDate, toDate):
        return {
            'event_name': eventName,
            'event_properties':eventProps,
            'from': fromDate,
            'to': toDate or {}
        }

    @staticmethod
    def _get_userProfile(eventName, fromDate, toDate):
        return {
            'event_name': eventName,
            'from': fromDate,
            'to': toDate or {}
        }

    @staticmethod
    def _deleteByIdentity(identity):
        return {
            'identity': identity or {}
        }

    @staticmethod
    def _deleteByGuid(guid):
        return {
            'guid': guid or {}
        }

    @staticmethod
    def end(res, response_code=200):
        resp = make_response(json.dumps(res), response_code)
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        return resp

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

        response_code = 202
        if res['status'] != 'success':
            response_code = 400

        return self.end(res, response_code)

    

    def _eventDetails(self, d):
        eventRes = requests.post(
            'https://api.clevertap.com/1/events.json?batch_size=50',
            json={"data":d},
            headers={
                'X-CleverTap-Account-Id': self.account_id,
                'X-CleverTap-Passcode': self.passcode,
                'Content-Type': 'application/json; charset=utf-8',
            })
        
        cursor = eventRes.json()["cursor"]
        eventUrl='https://api.clevertap.com/1/events.json?cursor='+cursor
        if cursor=='':
            finalResponse = {
                   'status': 'failed',
                   'reason': 'The cursor is not returned in the response, which means there are no more events.'
                    }
        else:
            finalResponse = requests.get(
            eventUrl,
            headers={
                'X-CleverTap-Account-Id': self.account_id,
                'X-CleverTap-Passcode': self.passcode,
                'Content-Type': 'application/json; charset=utf-8',
            })
        
        return finalResponse.json()
        
    def getEvent(self):
        req = request.get_json()
        eventName = req.get('event')
        fromDate = req.get('from')
        toDate = req.get('to')

        if eventName is not None:
            res = self._eventDetails(
                self._get_eventDelails(eventName, fromDate, toDate)
            )
        else:
            res = {
                'status': 'failed',
                'reason': 'The event name must be specified'
            }

        response_code = 202
        if res['status'] != 'success':
            response_code = 400

        return self.end(res, response_code)

    

    def _eventCount(self, d):
        res = requests.post(
            'https://api.clevertap.com/1/counts/events.json',
            json={'d':d},
            headers={
                'X-CleverTap-Account-Id': self.account_id,
                'X-CleverTap-Passcode': self.passcode,
                'Content-Type': 'application/json; charset=utf-8',
            })
        
        eventStatus = res.json()["status"]
        
        if eventStatus == "partial":
            reqID = res.json()["req_id"]
            eventCountUrl = 'https://api.clevertap.com/1/counts/events.json?req_id='+reqID
            finalCount = requests.get(
            eventCountUrl,
            headers={
                'X-CleverTap-Account-Id': self.account_id,
                'X-CleverTap-Passcode': self.passcode,
                'Content-Type': 'application/json; charset=utf-8',
            })
        else:
            finalCount = res
            
        return finalCount.json()

    def getEventCount(self):
        req = request.get_json()
        eventName = req.get('event')
        eventProps = req.get('properties')
        fromDate = req.get('from')
        toDate = req.get('to')

        if eventName is not None:
            res = self._eventCount([
                self._get_eventCount(eventName, eventProps, fromDate, toDate)
            ])
        else:
            res = {
                'status': 'failed',
                'reason': 'The event name must be specified'
            }

        response_code = 202
        if res['status'] != 'success':
            response_code = 400

        return self.end(res, response_code)

    

    def _profileCount(self, d):
        res = requests.post(
            'https://api.clevertap.com/1/counts/profiles.json',
            json={'data': d},
            headers={
                'X-CleverTap-Account-Id': self.account_id,
                'X-CleverTap-Passcode': self.passcode,
                'Content-Type': 'application/json; charset=utf-8',
            })
        eventStatus = res.json()["status"]
        
        if eventStatus == "partial":
            reqID = res.json()["req_id"]
            eventCountUrl = 'https://api.clevertap.com/1/counts/profiles.json?req_id='+reqID
            finalCount = requests.get(
            eventCountUrl,
            headers={
                'X-CleverTap-Account-Id': self.account_id,
                'X-CleverTap-Passcode': self.passcode,
                'Content-Type': 'application/json; charset=utf-8',
            })
        else:
            finalCount = res
            
        return finalCount.json()

    def getProfileCount(self):
        req = request.get_json()
        eventName = req.get('event')
        eventProps = req.get('properties')
        fromDate = req.get('from')
        toDate = req.get('to')

        if eventName is not None:
            res = self._profileCount([
                self._get_profileCount(eventName, eventProps, fromDate, toDate)
            ])
        else:
            res = {
                'status': 'failed',
                'reason': 'The event name must be specified'
            }

        response_code = 202
        if res['status'] != 'success':
            response_code = 400

        return self.end(res, response_code)

    

    def _userProfile(self, d):
        userRes = requests.post(
            'https://api.clevertap.com/1/profiles.json?batch_size=50',
            json={'data': d},
            headers={
                'X-CleverTap-Account-Id': self.account_id,
                'X-CleverTap-Passcode': self.passcode,
                'Content-Type': 'application/json; charset=utf-8',
            })

        profileCursor=userRes.json()["cursor"]
        profileUrl='https://api.clevertap.com/1/profiles.json?cursor='+profileCursor
        if profileCursor=='':
            finalResponse = {
                   'status': 'failed',
                   'reason': 'The cursor is not returned in the response, which means there are no more matching user profiles.'
                    }
        else:
            finalResponse = requests.post(
            profileUrl,
            headers={
                'X-CleverTap-Account-Id': self.account_id,
                'X-CleverTap-Passcode': self.passcode,
                'Content-Type': 'application/json; charset=utf-8',
            })
        return finalResponse.json()
        
    def getUserProfile(self):
        req = request.get_json()
        eventName = req.get('event')
        fromDate = req.get('from')
        toDate = req.get('to')

        if eventName is not None:
            res = self._userProfile([
                self._get_userProfile(eventName, fromDate, toDate)
            ])
        else:
            res = {
                'status': 'failed',
                'reason': 'The event name must be specified'
            }

        response_code = 202
        if res['status'] != 'success':
            response_code = 400

        return self.end(res, response_code)

    

    

    def _delete(self, d):
        deleteResp = requests.post(
            'https://api.clevertap.com/1/delete/profiles.json',
            json=d,
            headers={
                'X-CleverTap-Account-Id': self.account_id,
                'X-CleverTap-Passcode': self.passcode,
                'Content-Type': 'application/json; charset=utf-8',
            })
        return deleteResp.json()

    def deleteUserProfile(self):
        req = request.get_json()
        identity = req.get('identity')
        guid = req.get('guid')

        if identity is not None:
            res = self._delete(
                self._deleteByIdentity(identity)
            )
        elif guid is not None:
            res = self._delete(
                self._deleteByGuid(guid)
            )
        else:
            res = {
                'status': 'failed',
                'reason': 'At least one of identity or guid must be specified'
            }

        response_code = 202
        if res['status'] != 'success':
            response_code = 400

        return self.end(res, response_code)

    
if __name__ == '__main__':
    if os.getenv('ACCOUNT_ID') is None \
            or os.getenv('ACCOUNT_PASSCODE') is None:
        print('Environment variable ACCOUNT_ID/ACCOUNT_PASSCODE not found.')
        sys.exit(1)

    handler = Handler()
    handler.app.add_url_rule('/push', 'push', handler.push,
                             methods=['post'])
    handler.app.add_url_rule('/getEvent', 'getEvent', handler.getEvent,
                             methods=['post'])
    handler.app.add_url_rule('/getEventCount', 'getEventCount', handler.getEventCount,
                             methods=['post'])
    handler.app.add_url_rule('/getUserProfile', 'getUserProfile', handler.getUserProfile,
                             methods=['post'])
    handler.app.add_url_rule('/getProfileCount', 'getProfileCount', handler.getProfileCount,
                             methods=['post'])
    handler.app.add_url_rule('/deleteUserProfile', 'deleteUserProfile', handler.deleteUserProfile,
                             methods=['post'])
    handler.app.run(host='0.0.0.0', port=8000)
