from http import HTTPStatus

def test_push_request_event_name(client):
    data = {
        "event": "1Demo Even211",
        "identity": "1demo211",
        "properties": {
            "1demo211": "1event211"
        }
    }
    url = "/push"
    response = client.post(url, json=data)
    assert response.status_code == HTTPStatus.ACCEPTED

def test_push_request_profile(client):
    data = {
        "profile": {
            "Name": "Jack Montana",
            "Email": "jack@gmail.com",
            "Phone": "+14155551234",
            "Gender": "M",
            "Employed": "Y",
            "Education": "Graduate",
            "Married": "Y",
            "MSG-sms": "false",
            "Customer Type": "Platinum"
        },
        "identity": "1demo211",
        "properties": {
            "1demo211": "1event211"
        }
    }
    url = "/push"
    response = client.post(url, json=data)
    assert response.status_code == HTTPStatus.ACCEPTED

def test_push_no_arguments(client):
    data = {
        "identity": "1demo211",
        "properties": {
            "1demo211": "1event211"
        }
    }
    url = "/push"
    response = client.post(url, json=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST

def test_push_fail_request(client):
    data = {
        "event": "Demo Even18",
        "identity": "",
        "properties": {
            "demo18": "event18"
        }
    }
    url = "/push"
    response = client.post(url, json=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST

def test_get_event_request(client):
    data = {"event": "Demo Even18", "from": 20190717, "from": 20190718}
    url = "/getEvent"
    response = client.post(url, json=data)
    assert response.status_code == HTTPStatus.ACCEPTED

def test_get_event_fail_request(client):
    data = {"from": 0, "from": 0}
    url = "/getEvent"
    response = client.post(url, json=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST

def test_get_event_count_request(client):
    data = {
        "event": "Demo Even18",
        "properties": {
            "demo": "event"
        },
        "from": 20190717,
        "from": 20190718
    }
    url = "/getEventCount"
    response = client.post(url, json=data)
    assert response.status_code == HTTPStatus.ACCEPTED

def test_get_event_count_fail_request(client):
    data = {
        "properties": {
            "demo": "event"
        },
        "from": 20190717,
        "from": 20190718
    }
    url = "/getEventCount"
    response = client.post(url, json=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST

def test_get_user_profile_request(client):
    data = {"event": "Demo Even18", "from": 20190717, "from": 20190718}
    url = "/getUserProfile"
    response = client.post(url, json=data)
    assert response.status_code == HTTPStatus.ACCEPTED

def test_get_user_profile_fail_request(client):
    data = {"from": 20190717, "from": 20190718}
    url = "/getUserProfile"
    response = client.post(url, json=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST

def test_get_profile_count_request(client):
    data = {
        "event": "Demo Even18",
        "properties": {
            "demo": "event"
        },
        "from": 20190717,
        "from": 20190718
    }
    url = "/getProfileCount"
    response = client.post(url, json=data)
    assert response.status_code == HTTPStatus.ACCEPTED

def test_get_profile_count_fail_request(client):
    data = {
        "properties": {
            "demo": "event"
        },
        "from": 20190717,
        "from": 20190718
    }
    url = "/getProfileCount"
    response = client.post(url, json=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST

def test_delete_user_profile_request(client):
    data = {"identity": "demo"}
    url = "/deleteUserProfile"
    response = client.post(url, json=data)
    assert response.status_code == HTTPStatus.ACCEPTED

def test_delete_user_profile_fail_request(client):
    data = {}
    url = "/deleteUserProfile"
    response = client.post(url, json=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST    
