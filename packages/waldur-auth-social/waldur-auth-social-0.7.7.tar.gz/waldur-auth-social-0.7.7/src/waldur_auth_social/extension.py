from __future__ import unicode_literals

from waldur_core.core import WaldurExtension


class AuthSocialExtension(WaldurExtension):

    class Settings:
        # wiki: https://opennode.atlassian.net/wiki/display/WD/AuthSocial+plugin+configuration
        WALDUR_AUTH_SOCIAL = {
            'GOOGLE_SECRET': 'CHANGE_ME_TO_GOOGLE_SECRET',
            'FACEBOOK_SECRET': 'CHANGE_ME_TO_FACEBOOK_SECRET',
            'SMARTIDEE_SECRET': 'CHANGE_ME_TO_SMARTIDEE_SECRET',
            'USER_ACTIVATION_URL_TEMPLATE': 'http://example.com/#/activate/{user_uuid}/{token}/',
        }

    @staticmethod
    def django_app():
        return 'waldur_auth_social'

    @staticmethod
    def django_urls():
        from .urls import urlpatterns
        return urlpatterns
