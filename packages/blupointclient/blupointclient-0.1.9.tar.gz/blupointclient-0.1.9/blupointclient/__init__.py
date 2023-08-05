from tornado.httpclient import AsyncHTTPClient

from blupointclient.components.content import QuarkContent
from blupointclient.components.contents import  QuarkContents
from blupointclient.components.subject import QuarkSubject
from blupointclient.components.subjects import QuarkSubjects

class module_base():
    def __get_api_token(self):
        return self.cache_manager.cache('api_token')

    def __get_settings(self):
        return self.settings

class cms(module_base):

    BASE_API = None
    DOMAIN_ID = None

    def __init__(self, settings):
        self.content =  QuarkContent(settings)
        self.contents = QuarkContents(settings)
        self.subject = QuarkSubject(settings)
        self.subjects = QuarkSubjects(settings)


        """
            TODO :
            interaction_module
            interactions_module
            notification_module
            notifications_module
            user_module
            users_module
            user_form_module
            user_forms_module

        """



