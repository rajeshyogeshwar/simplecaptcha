# Captcha

Captcha is a micro application that provides endpoints to generate and verify a image captcha.
It is an ASGI application based on [starlette](https://github.com/encode/starlette) which uses [uvicorn](https://github.com/encode/uvicorn) as it's application server to serve the application.

## Deployment

Gunicorn, Nginx will be required to deploy the application on server of your choice. Documentation on how to deploy such an application can be found [here](https://www.uvicorn.org/deployment/). Captcha makes use of `.env` file to keep sensitive information. Repository contains an example file as to the information that is required. Prior to deployment ensure that you create a `.env` file in your project and add necessary information as per the example file. Failure to do so would render application not working.

## Endpoints
```
GET: /get-captcha/
```
Response:
```
{
   'widget_id': <alphanumeric_string>,
   'captcha_b64': <base64_string_for_a_png_image_captcha>
}
```
```
POST: /verify-captcha/
CONTENT-TYPE: application/json
DATA: {
        'widget_id': <alphanumeric_string>, 
        'input': <user_input>
      }

```
Response:
```
{
  'is_verified': true|false
}

In the case, where verification fails, response will also include a new widget_id and captcha_b64 for another attempt.
```

## Testing

Application has couple of simple test cases to test both the endpoints.

## Usage

The `get-captcha` API returns `widget_id` and `captcha_b64`. `captcha_b64` is a base64 string for the image captcha which can be directly assigned to `src` attribute of `img` HTML element. `widget_id` can be assigned to `data-*` attribute on the same `img` element. When the captcha is to be sent for verification, a json containing `widget_id` and `input` which represents user's input is to be passed. 