import random
import string
from oraculo.gods import faveo
from partenon.helpdesk import HelpDeskUser, Topic, Priority


def generate_random_strin(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def test_can_create_user():
    client = faveo.APIClient()
    email = "%s@example.com" % generate_random_strin(4)
    body = {'email': email, 'first_name': 'test', 'last_name': 'test'}
    user = HelpDeskUser.create_user(**body)

    user_keys = [
        'updated_at', 'email', 'first_name',
        'mobile', 'id', 'user_name', 'email_verify',
        'role', 'created_at', 'agent_tzone', 'mobile_otp_verify',
        'last_name']
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
    priority = Priority(**dict(id=2))
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
    priority = Priority(**dict(id=2))
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

    import ipdb; ipdb.set_trace()
    HelpDeskUser.create_user(**body)
    user = HelpDeskUser.get(email)
    
    user_keys = [
        'updated_at', 'email', 'first_name',
        'mobile', 'id', 'user_name', 'email_verify',
        'role', 'created_at', 'agent_tzone', 'mobile_otp_verify',
        'last_name']
    for key in user_keys:
        assert(hasattr(user, key))