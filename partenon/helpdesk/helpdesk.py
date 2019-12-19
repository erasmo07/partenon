import os
from oraculo.gods import faveo, faveo_db, exceptions
from . import entitys, base
from .exceptions import (
    DoesNotExist, NotSetHelpDeskUserInstance,
    NotIsInstance)


class Prioritys(object):
    _url = 'api/v1/helpdesk/priority'
    _entity = entitys.Priority
    objects = base.BaseManageEntity(_url, _entity, key_name='priority')


class Topics(object):
    _url = 'api/v1/helpdesk/help-topic'
    _entity = entitys.Topic
    objects = base.BaseManageEntity(_url, _entity, key_name='topic')

    
class Deparments(object):
    _url = 'api/v1/helpdesk/department'
    _entity = entitys.Department
    objects = base.BaseManageEntity(_url, _entity)


class Status(base.BaseManageEntity):
    _url = 'api/v1/helpdesk/dependency'
    _entity = entitys.State
    _client = faveo.APIClient

    @staticmethod
    def get_entitys(
            entity=entitys.State,
            url='api/v1/status',
            client=faveo_db.APIClient):
        client = client()
        response = client.get(url)
        return [entity(**state) for state in response]

    @staticmethod
    def get_state_by_name(
            name,
            entity=entitys.State,
            url='api/v1/status',
            client=faveo_db.APIClient):
        client = client()
        response = client.get(url, params=dict(name=name))
        return entity(**response[0])
    
    @staticmethod
    def get_by_id(
            id,
            entity=entitys.State,
            url='api/v1/status',
            client=faveo_db.APIClient):
        client = client()
        response = client.get(url, params=dict(id=id))
        return entity(**response[0])



class HelpDeskTicket(
        base.BaseEntityHelpDesk,
        base.BaseHelpDesk):
    _user = None
    _client = faveo.APIClient()
    _status_close_name = 'Closed'
    _department = os.environ.get('PARTENON_DEPARTMENT')
    _create_url = 'api/v1/helpdesk/create'
    _list_url = 'api/v1/helpdesk/my-tickets-user'
    _url_detail = 'api/v1/helpdesk/ticket'
    _url_to_change_status = 'api/v2/helpdesk/status/change'
    _url_to_add_note = 'api/v1/helpdesk/internal-note'
    ticket_name = None
    ticket_id = None

    @property
    def state(self):
        if not self.ticket_name:
            response = self._client.get(
                self._url_detail, params=dict(id=self.ticket_id))
            ticket = response.get('data').get('ticket')
            self.ticket_name = ticket.get('status_name')
        return Status.get_state_by_name(self.ticket_name)
    
    @property
    def user(self):
        return self._user
    
    @staticmethod
    def get_specific_ticket(
        ticket_id,
        url='api/v1/helpdesk/ticket',
        client=faveo.APIClient):
        client = client()
        response = client.get(url, params=dict(id=ticket_id))
        ticket_detail = response.get('data').get('ticket')
        ticket_detail['ticket_id'] = ticket_detail['id']
        user = HelpDeskUser(**ticket_detail.get('from'))
        return HelpDeskTicket(_user=user, **ticket_detail)

    def add_note(self, note, user):
        body = dict(ticket_id=self.ticket_id, user_id=user.id, body=note)
        response = self._client.post(self._url_to_add_note, body=body)
        return response

    def create(self, subject, body, priority, topic, department):
        if not isinstance(priority, entitys.Priority):
            raise NotIsInstance('Priority not is instance of Priority')
        
        if not isinstance(topic, entitys.Topic):
            raise NotIsInstance('Topic not is instance of Topic')
        
        if not isinstance(department, entitys.Department):
            raise NotIsInstance('Department not is instance of Department')
        
        body = dict(
            subject=subject, body=body, first_name=self._user.first_name,
            email=self._user.email, priority=priority.priority_id,
            help_topic=topic.id, dept=department.id)

        response = self._client.post(self._create_url, body).get('response')
        return self.get_specific_ticket(response.get('ticket_id'))

    def list(self):
        if not self._user:
            raise NotSetHelpDeskUserInstance('Need set _user instance')

        params = dict(user_id=self._user.id)
        response = self._client.get(self._list_url, params)

        if not isinstance(response, dict) and response.get('tickets', None):
            raise NotIsInstance(response.get('error'))

        return [HelpDeskTicket(**ticket) for ticket in response.get('tickets')]

    def change_state(self, state):
        body = dict(ticket_id=self.ticket_id, status_id=state.id)
        response = self._client.post(self._url_to_change_status, body)
        return response.get('success')

    def close(self):
        state_close = Status.get_state_by_name(self._status_close_name)
        body = dict(ticket_id=self.ticket_id, status_id=state_close.id)
        response = self._client.post(self._url_to_change_status, body)
        return response.get('success')
    

class HelpDeskUser(base.BaseEntityHelpDesk, base.BaseHelpDesk):
    _url = 'api/v1/helpdesk/register'
    _search_url = 'api/v1/helpdesk/agents'

    def __init__(self, *args, **kwargs):
        self.ticket = HelpDeskTicket(**{'_user': self})
        super().__init__(*args, **kwargs)

    @staticmethod
    def get(email,
            url='api/v1/users',
            client=faveo_db.APIClient):
        client = client()
        response = client.get(url, params={'email': email})
        return HelpDeskUser(**response) if response else None

    @staticmethod
    def create_user(
            email, first_name, last_name,
            url='api/v1/helpdesk/register',
            client=faveo.APIClient):
        
        client = client()
        user = HelpDeskUser.get(email)
        if user:
            return user

        params = dict(email=email, first_name=first_name, last_name=last_name)
        result = client.post(url, params)
        return HelpDeskUser(**result[0].get('user'))


class HelpDesk(object):
    user = HelpDeskUser
    topics = Topics
    prioritys = Prioritys 
    departments = Deparments
    status = Status
    ticket = HelpDeskTicket

