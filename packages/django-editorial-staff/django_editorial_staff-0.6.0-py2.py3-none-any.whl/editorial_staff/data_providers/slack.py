# Imports from Django.  # NOQA
from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse
from django.utils import dateformat as df
from django.utils import timezone


# Imports from editorial-staff.
# from editorial_staff.utils import get_random_anonymous_animal


# Imports from other dependencies.
import probablepeople
from slacker import Slacker


SLACK_CONNECTION = Slacker(getattr(settings, 'SLACK_TOKEN', ''))


class SlackProvider(object):
    def __init__(self):
        self.connection = SLACK_CONNECTION

    def get_all_staffers(self, include_bots=False, include_deleted=False,
                         excluded_email_domains=[]):
        slack_users = self.connection.users.list().body['members']

        if not include_bots:
            slack_users = [
                _ for _ in slack_users
                if _['is_bot'] is False and _['id'] != 'USLACKBOT'
            ]

        if not include_deleted:
            slack_users = [_ for _ in slack_users if _['deleted'] is False]

        if len(excluded_email_domains) > 0:
            slack_users = [
                _ for _ in slack_users
                if _['profile']['email'].split('@')[1]
                not in excluded_email_domains
            ]

        return slack_users

    def get_staffer(self, queried_email, excluded_email_domains=[]):
        """Return a user if found in Slack."""
        users = self.get_all_staffers(
            include_bots=False,
            include_deleted=False,
            excluded_email_domains=excluded_email_domains
        )

        for user in users:
            user_email = user['profile'].get('email', None)
            if user_email is not None:
                if user_email.lower() == queried_email.lower():
                    return user
        return None

    def format_staffer(self, user_data, exclude_email=False):
        """TK."""
        staffer_formatted = {}

        profile = user_data['profile']

        if exclude_email is not True:
            staffer_formatted['email'] = profile.get('email')

        staffer_formatted['first_name'] = None
        staffer_formatted['last_name'] = None
        staffer_formatted['full_name'] = None

        full_name = profile.get('real_name', '').strip()
        if len(full_name) > 0:
            name_parts, name_type = probablepeople.tag(full_name)
            if all([
                name_type == 'Person',
                'GivenName' in name_parts,
                'Surname' in name_parts
            ]):
                formatted_first_name = name_parts['GivenName']

                if 'MiddleName' in name_parts:
                    formatted_first_name = '{} {}'.format(
                        formatted_first_name,
                        name_parts['MiddleName']
                    )

                if 'Nickname' in name_parts:
                    formatted_nickname = name_parts['Nickname'].replace(
                        '(',
                        ''
                    ).replace(
                        ')',
                        ''
                    )
                    formatted_first_name = '{} "{}"'.format(
                        formatted_first_name,
                        formatted_nickname
                    )

                staffer_formatted['first_name'] = formatted_first_name
                staffer_formatted['last_name'] = name_parts['Surname']
                staffer_formatted['full_name'] = full_name
            else:
                staffer_formatted['last_name'] = full_name
                staffer_formatted['full_name'] = full_name

        staffer_formatted['image_url'] = profile.get('image_72', '')

        return staffer_formatted

    def post_new_staffer_message(self, options, staffer):
        channel_name = options.get('notification_channel', None)

        if channel_name is not None:
            app_icon_url = '{}{}'.format(
                getattr(settings, 'STAFF_BASE_URL', ''),
                static('editorial_staff/img/staff-icon.png')
            )

            self.connection.chat.post_message(
                channel=channel_name,
                username='New staffer alert',
                icon_url=app_icon_url,
                attachments=self.generate_staffer_slack_attachment(staffer)
            )

    def generate_staffer_slack_attachment(self, staffer):
        staffer_edit_link = '{}{}'.format(
            getattr(settings, 'STAFF_BASE_URL', ''),
            reverse(
                'editorial_staff:staffer-edit',
                kwargs={'pk': staffer.pk}
            )
        )

        staffer_created_date = staffer.created.astimezone(
            timezone.get_default_timezone()
        )

        staffer_card = {
            'fallback': 'New staffer created: {}'.format(staffer.full_name),
            'color': '#00695C',
            'pretext': 'There\'s a new face in the staff management app!',
            'fields': [
                {
                    'title': 'Name',
                    'value': staffer.full_name,
                    'short': True,
                },
                {
                    'title': 'Email',
                    'value': staffer.email,
                    'short': True,
                },
                {
                    'title': 'Date & time created',
                    'value': '{} at {}'.format(
                        df.format(staffer_created_date, 'N j, Y'),
                        df.format(staffer_created_date, 'g:i a'),
                    ),
                    'short': True,
                },
                {
                    'title': 'Active?',
                    'value': 'Yes' if staffer.active is True else 'No',
                    'short': True,
                },
                {
                    'title': 'Edit URL',
                    'value': staffer_edit_link,
                    'short': False,
                },
            ],
            'image_url': staffer.image_url,
            'thumb_url': staffer.image_url,
        }

        return [staffer_card]
