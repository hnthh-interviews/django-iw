import json

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

pytestmark = pytest.mark.django_db


def is_json(response):
    if response.has_header("content-type"):
        return "json" in response.get("content-type")

    return False


def decode_response(response):
    content = response.content.decode("utf-8", errors="ignore")

    return json.loads(content) if is_json(response=response) else content


class DRFClient(APIClient):
    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)

        self.user = user

        if user is not None:
            self.auth()
            self.set_headers()

    def auth(self):
        self.force_authenticate(self.user)

    def set_headers(self):
        token = AccessToken.for_user(self.user)

        self.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def unset_headers(self):
        self.credentials()

    def logout(self):
        self.unset_headers()

        super().logout()

    def call_api(self, *args, **kwargs):
        as_response = kwargs.pop("as_response", False)
        expected_status_code = kwargs.pop("expected_status_code")
        method = kwargs.pop("method")

        kwargs.setdefault("format", "json")

        response = getattr(super(), method)(*args, **kwargs)

        if as_response:
            return response

        content = decode_response(response=response)

        assert response.status_code == expected_status_code, (  # noqa: S101
            f"{response.status_code}, content: {content}"
        )

        return content

    def get(self, *args, **kwargs):
        kwargs.setdefault("expected_status_code", status.HTTP_200_OK)

        return self.call_api(*args, method="get", **kwargs)

    def delete(self, *args, **kwargs):
        kwargs.setdefault("expected_status_code", status.HTTP_204_NO_CONTENT)

        return self.call_api(*args, method="delete", **kwargs)

    def patch(self, *args, **kwargs):
        kwargs.setdefault("expected_status_code", status.HTTP_200_OK)

        return self.call_api(*args, method="patch", **kwargs)

    def post(self, *args, **kwargs):
        kwargs.setdefault("expected_status_code", status.HTTP_201_CREATED)

        return self.call_api(*args, method="post", **kwargs)

    def put(self, *args, **kwargs):
        kwargs.setdefault("expected_status_code", status.HTTP_200_OK)

        return self.call_api(*args, method="put", **kwargs)
