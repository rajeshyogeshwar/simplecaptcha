from starlette.routing import Route
from starlette.applications import Starlette
from captcha import Captcha, verify_user_captcha
from starlette.responses import Response, JSONResponse


async def get_captcha(request):

    try:

        captcha = Captcha()
        data = {
            'widget_id': captcha.widget_id,
            'captcha_b64': captcha.b64_string
        }

        return JSONResponse(data)

    except Exception:
        response = Response('Error generating captcha',
                            status_code=500, media_type='text/plain')
        return response


async def verify_captcha(request):

    try:

        data = await request.json()
        is_verified = verify_user_captcha(
            data.get('widget_id'), data.get('input'))

        if not is_verified:

            captcha = Captcha()

            response = JSONResponse({
                'is_verified': is_verified,
                'widget_id': captcha.widget_id,
                'captcha_b64': captcha.b64_string
            })

        else:

            response = JSONResponse({'is_verified': is_verified})

        return response

    except Exception:
        response = Response('Error verifying captcha',
                            status_code=500, media_type='text/plain')
        return response


app = Starlette(
    routes=[
        Route('/get-captcha/', get_captcha, methods=['GET']),
        Route('/verify-captcha/', verify_captcha, methods=['POST'])
    ]
)
