import pytest
from flask import Flask

@pytest.fixture(scope='module')
def app() -> Flask:
    print(""" Provides an instance of our Flask app """)
    from app import Handler
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
     
    return handler.app
