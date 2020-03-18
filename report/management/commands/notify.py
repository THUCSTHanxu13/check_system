import json
import pathlib

from django.core.management.base import BaseCommand
from django.db.models import QuerySet
from django.conf import settings

from requests_oauthlib import OAuth2Session

from ...models import Person, Record, Entry
from ... import utils


FAKE_CALLBACK_URI = 'https://localhost/callback'
PROJECT_DIR = pathlib.Path(__file__).resolve().parent.parent.parent.parent
VAR_DIR = PROJECT_DIR / 'var'
TOKEN_PATH = VAR_DIR / 'token.json'

def save_token(token):
    TOKEN_PATH.write_text(json.dumps(token))

def load_token():
    return json.loads(TOKEN_PATH.read_text())

def authorize(*args, **kwargs):
    oauth = OAuth2Session(settings.OAUTH_CLIENT_ID, redirect_uri=FAKE_CALLBACK_URI)
    authorization_url, state = oauth.authorization_url(settings.OAUTH_AUTHORIZE_URL)
    print(authorization_url)
    authorization_response = input('Enter the full callback URL: ')
    token = oauth.fetch_token(
        settings.OAUTH_ACCESS_TOKEN_URL,
        authorization_response=authorization_response,
        client_secret=settings.OAUTH_CLIENT_SECRET,
    )
    print(token)
    save_token(token)

def get_oauth():
    token = load_token()
    oauth = OAuth2Session(
        settings.OAUTH_CLIENT_ID,
        token=token,
        auto_refresh_url=settings.OAUTH_REFRESH_TOKEN_URL,
        auto_refresh_kwargs={
            'client_id': settings.OAUTH_CLIENT_ID,
            'client_secret': settings.OAUTH_CLIENT_SECRET,
        },
        token_updater=save_token,
    )
    return oauth

def send(users, title, content, channel=['weixiao']):
    if not isinstance(users, list):
        users = [users]
    if not users:
        return
    oauth = get_oauth()
    resp = oauth.request('POST', settings.OAUTH_PUSH_NOTIFICATION_URL, data={
        'users': users,
        'title': title,
        'content': content,
        'channel': channel,
    })
    return resp.json()

def announce(message, recipients, context={}):
    if isinstance(message, pathlib.Path):
        message_path = message
    elif isinstance(message, str):
        message_path = VAR_DIR / message
    else:
        raise ValueError('invalid type of message')
    with open(message_path) as message_file:
        title = message_file.readline().strip()
        content = message_file.read().format(**context)
    if isinstance(recipients, QuerySet):
        users = [p.idnum for p in recipients]
    elif isinstance(recipients, list):
        users = recipients
    elif isinstance(recipients, str):
        users = [recipients]
    else:
        raise ValueError('invalid type of recipients')
    send(users, title, content)

def welcome(*args, **kwargs):
    users = kwargs.get('users')
    recipients = users if users else Person.objects.filter(user__isnull=False, is_welcomed=False)
    announce('welcome.txt', recipients)
    if isinstance(recipients, QuerySet):
        for person in recipients:
            person.is_welcomed = True
            person.save(update_fields=('is_welcomed',))
            print('Welcome {}'.format(person.name))
        print('Welcomed {} person(s)'.format(recipients.count()))

def ping(*args, **kwargs):
    users = kwargs.get('users')
    recipients = users if users else Person.objects.filter(user__isnull=False) \
        .exclude(id__in=Record.objects.filter(date=utils.local_date(), is_submitted=True).values('person_id'))
    announce('ping.txt', recipients)
    if isinstance(recipients, QuerySet):
        for person in recipients:
            print('Ping {}'.format(person.name))
        print('Pinged {} person(s)'.format(recipients.count()))

def approve(*args, **kwargs):
    users = kwargs.get('users')
    count = Entry.objects.filter(approve3_decision__isnull=True).count()
    if users and count:
        announce('approve.txt', users, {'count': count})

def test_get(*args, **kwargs):
    oauth = get_oauth()
    resp = oauth.request('GET', settings.OAUTH_USER_INFO_URL)
    print(resp.json())

def test_post(*args, **kwargs):
    users = kwargs.get('users')
    if users:
        welcome(users=users)

class Command(BaseCommand):
    help = 'Notify users'

    def add_arguments(self, parser):
        parser.add_argument('command', choices=(
            'authorize',
            'welcome',
            'ping',
            'approve',
            'test_get',
            'test_post',
        ))
        parser.add_argument('users', nargs='*')

    def handle(self, *args, **options):
        command = options['command']
        users = options['users']
        if command in globals():
            globals()[command](users=users)
        else:
            raise NotImplementedError('unknown command')
