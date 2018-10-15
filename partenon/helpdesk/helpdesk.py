import os
from oraculo.gods.faveo import APIClient

class NotSetHelpDeskUserInstance(Exception):
    pass


class BaseHelpDesk(object):

    def __init__(self):
        self._client = APIClient()


class BaseEntityHelpDesk(object):

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Topic(BaseEntityHelpDesk):
    pass


class Priority(BaseEntityHelpDesk):
    pass


class HelpDeskGetEntity(BaseHelpDesk):
    _url = None
    _entity = None

    @staticmethod
    def get_entitys(self):
        response = self._client.get(self._url)
        return map(self._entity, response.get('result'))


class Topics(HelpDeskGetEntity):
    _url = 'api/v1/helpdesk/help-topic'
    _entity = Topic


class HelpDeskTicket(BaseEntityHelpDesk, BaseHelpDesk):
    _user = None
    _client = APIClient()
    _department = os.environ.get('PARTENON_DEPARTMENT')
    _create_url = 'api/v1/helpdesk/create'
    _list_url = 'api/v1/helpdesk/my-tickets-user'

    def create(self, subject, body, priority, topic):
        body = dict(
            subject=subject, body=body, first_name=self._user.first_name,
            email=self._user.email, priority=priority.id, help_topic=topic.id,
            dept=self._department)

        response = self._client.post(self._create_url, body).get('response')
        return HelpDeskTicket(**response)
    
    def list(self):
        if not self._user:
            raise NotSetHelpDeskUserInstance('Need set _user instance')

        params = dict(user_id=self._user.id)
        response = self._client.get(self._list_url, params)
        return [HelpDeskTicket(**ticket) for ticket in response.get('tickets')]


class HelpDeskUser(BaseEntityHelpDesk, BaseHelpDesk):
    _url = 'api/v1/helpdesk/register'
    _search_url = 'api/v1/helpdesk/agents'

    def __init__(self, *args, **kwargs):
        self.ticket = HelpDeskTicket(**{'_user': self})
        super().__init__(*args, **kwargs)

    @staticmethod
    def get(email,
            url='api/v1/helpdesk/collaborator/search',
            client=APIClient()):
        import ipdb; ipdb.set_trace()
        response = client.get(url, params={'term': email})
        return HelpDeskUser(response.get('result')[0])

    @staticmethod
    def create_user(
            email, first_name, last_name,
            url='api/v1/helpdesk/register',
            client=APIClient()):
        params = dict(email=email, first_name=first_name, last_name=last_name)
        result = client.post(url, params)
        return HelpDeskUser(**result[0].get('user'))


class HelpDesk(object):
    pass
