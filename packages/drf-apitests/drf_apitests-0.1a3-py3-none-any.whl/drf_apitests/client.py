from django.contrib import auth
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_jwt.settings import api_settings


class CustomAPIClient(APIClient):

    def __init__(self, auth=None, **kw):
        super().__init__(**kw)
        if auth:
            if isinstance(auth, str):
                auth = {'email': auth}
            self.bypass_login(**auth)

    def bypass_login(self, **filter):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        UserModel = auth.get_user_model()
        first = UserModel.objects.get(**filter)
        payload = jwt_payload_handler(first)
        token = jwt_encode_handler(payload)
        self.credentials(HTTP_AUTHORIZATION="{0} {1}".format(
            api_settings.JWT_AUTH_HEADER_PREFIX, token))

    def login(self, **credentials):
        """
        Returns True if login is possible
        """
        response = self.post('/api/v1/public/user/login/', credentials,
                             format='json')
        if response.status_code == status.HTTP_200_OK:
            self.credentials(
                HTTP_AUTHORIZATION="{0} {1}".format(
                    api_settings.JWT_AUTH_HEADER_PREFIX,
                    response.data['token']))
            return True
        else:
            return False
