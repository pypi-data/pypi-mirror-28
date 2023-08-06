# django-rest-framework-jwt-refresh-token

Plugin for [django-rest-framework-jwt](https://github.com/GetBlimp/django-rest-framework-jwt)
that supports [long running refresh tokens](https://auth0.com/docs/refresh-token).

[Documentation](https://lock8.github.io/django-rest-framework-jwt-refresh-token/)

Work initially done by [Nick Lang](https://github.com/fxdgear)
from that [pull request](https://github.com/GetBlimp/django-rest-framework-jwt/pull/94).

[![Build Status](https://travis-ci.org/lock8/django-rest-framework-jwt-refresh-token.svg?branch=master)](https://travis-ci.org/lock8/django-rest-framework-jwt-refresh-token)
[![codecov.io](https://codecov.io/github/lock8/django-rest-framework-jwt-refresh-token/coverage.svg?branch=master)](https://codecov.io/github/lock8/django-rest-framework-jwt-refresh-token?branch=master)

## Usage

For a given long refresh token (stored in DB), POSTing to the `delegate` endpoint will return a new JWT token.

```bash
http POST client_id=app grant_type="urn:ietf:params:oauth:grant-type:jwt-bearer" refresh_token=<REFRESH_TOKEN> api_type=app http://localhost:8000/delegate/
'{"token": "your_jwt_token_...", "refresh_token": "your long running refresh token..."}'
```

## Changelog

- 0.5 / 2018-01-25
    - Make `RefreshTokenViewSet` a `GenericViewSet` to take advantage of schema generation

- 0.4 / 2018-01-18
    - Expose revoke functions as an API action

        ```POST /refresh_tokens/{key}/revoke/```

- 0.3 / 2018-01-16
    - Add `refresh_token.revoke()` to replace the current refresh token

- 0.2 / 2017-10-20
    - Add compatibility with Django 2.0
    - Drop Django support below 1.11
    - Drop DRF support below 3.6

- 0.1.2 / 2016-01-28
    - Fix packaging

- 0.1.1 / 2016-01-28
    - Fix packaging

- 0.1.0 / 2016-01-28
    - Initial Release based on https://github.com/GetBlimp/django-rest-framework-jwt/pull/123
