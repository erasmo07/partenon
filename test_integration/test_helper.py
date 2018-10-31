import random
import string
from oraculo.gods import faveo
from partenon.helpdesk import HelpDeskUser, Topic, Priority, Status


def generate_random_strin(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def test_can_create_user():
    email = "%s@example.com" % generate_random_strin(4)
    body = {'email': email, 'first_name': 'test', 'last_name': 'test'}
    user = HelpDeskUser.create_user(**body)

    user_keys = [
        'email', 'first_name', 'id', 'role', 'created_at', 'last_name']
    for key in user_keys:
        assert(hasattr(user, key))


def test_can_get_help_topics(url='api/v1/helpdesk/help-topic'):
    client = faveo.APIClient()
    topics = client.get(url)

    assert('result' in topics.keys())
    keys = ['id', 'topic', 'department']
    list_topics = topics.get('result')
    for topic in list_topics:
        for key in keys:
            assert(key in topic.keys())


"""
def test_can_get_help_topic_by_id(url='api/v1/helpdesk/help-topic'):
    client = faveo.APIClient()
    topics = client.get(url).get('result')
    first_topic = topics[0]
    new_url = "%s/%s" % (url, first_topic.get('id'))
    topic = client.get(new_url)
"""


def test_can_create_ticket():
    email = "%s@example.com" % generate_random_strin(4)
    body = {'email': email, 'first_name': 'test', 'last_name': 'test'}

    user = HelpDeskUser.create_user(**body)

    subject = generate_random_strin(60)
    body = generate_random_strin(150)
    priority = Priority(**dict(priority_id=2))
    topic = Topic(**dict(id=40))

    body = dict(subject=subject, body=body, priority=priority, topic=topic)
    ticket = user.ticket.create(**body)

    assert(hasattr(ticket, 'ticket_id'))


def test_can_list_my_tickets():
    email = "%s@example.com" % generate_random_strin(4)
    body = {'email': email, 'first_name': 'test', 'last_name': 'test'}

    user = HelpDeskUser.create_user(**body)

    subject = generate_random_strin(60)
    body = generate_random_strin(150)
    priority = Priority(**dict(priority_id=2))
    topic = Topic(**dict(id=40))

    body = dict(subject=subject, body=body, priority=priority, topic=topic)
    user.ticket.create(**body)

    tickets = user.ticket.list()
    for ticket in tickets:
        assert(hasattr(ticket, 'ticket_number'))
        assert(hasattr(ticket, 'ticket_status_name'))
        assert(hasattr(ticket, 'title'))


def test_can_search_user_by_email():
    email = "%s@example.com" % generate_random_strin(4)
    body = {'email': email, 'first_name': 'test', 'last_name': 'test'}

    HelpDeskUser.create_user(**body)
    user = HelpDeskUser.get(email)

    user_keys = [
        'email', 'first_name', 'id', 'role', 'last_name']
    for key in user_keys:
        assert(hasattr(user, key))


def test_can_search_status():
    status = Status.get_entitys()

    for state in status:
        assert(hasattr(state, 'id'))
        assert(hasattr(state, 'name'))

def test_can_search_status_by_name():
    state_open = Status.get_state_by_name('Open')

    assert(hasattr(state_open, 'id'))
    assert(hasattr(state_open, 'name'))
    assert(state_open.name == 'Open')

def test_can_close_a_ticket():
    email = "%s@example.com" % generate_random_strin(4)
    body = {'email': email, 'first_name': 'test', 'last_name': 'test'}

    user = HelpDeskUser.create_user(**body)

    subject = generate_random_strin(60)
    body = generate_random_strin(150)
    priority = Priority(**dict(priority_id=2))
    topic = Topic(**dict(id=40))

    body = dict(subject=subject, body=body, priority=priority, topic=topic)
    ticket = user.ticket.create(**body)

    ticket.close()

def test_can_change_status_ticket():
    email = "%s@example.com" % generate_random_strin(4)
    body = {'email': email, 'first_name': 'test', 'last_name': 'test'}

    user = HelpDeskUser.create_user(**body)

    subject = generate_random_strin(60)
    body = generate_random_strin(150)
    priority = Priority(**dict(priority_id=2))
    topic = Topic(**dict(id=40))

    body = dict(subject=subject, body=body, priority=priority, topic=topic)
    ticket = user.ticket.create(**body)

    state_resolve = Status.get_state_by_name('Resolved')

    ticket.change_state(state_resolve)
    assert(ticket.state.name == 'Resolved')    