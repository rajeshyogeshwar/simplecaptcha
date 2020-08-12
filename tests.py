from api import app
from captcha import Captcha
from starlette.testclient import TestClient


def test_get_captcha():

    client = TestClient(app)
    response = client.get('/get-captcha/')
    assert response.status_code == 200


def test_post_captcha():

    client = TestClient(app)
    response = client.post('/get-captcha/')
    assert response.status_code == 405


def test_post_verify_captcha():

    client = TestClient(app)
    captcha = Captcha()
    response = client.post(
        '/verify-captcha/',
        headers={
            'Content-Type': 'application/json'
        },
        json={
            'widget_id': captcha.widget_id,
            'input': ''.join(captcha.characters)
        })

    assert response.status_code == 200


def test_get_verify_captcha():

    client = TestClient(app)
    response = client.get(
        '/verify-captcha/',
        headers={
            'Content-Type': 'application/json'
        })

    assert response.status_code == 405


if __name__ == '__main__':
    test_get_captcha()
    test_post_captcha()
    test_post_verify_captcha()
    test_post_verify_captcha()
