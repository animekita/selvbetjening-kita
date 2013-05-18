
import datetime

from django.core.management.base import NoArgsCommand
from django.conf import settings

from kita_website.apps.webfactionemail.models import Email


class Command(NoArgsCommand):

    def _get_webfaction_session(self):
        import xmlrpclib

        server = xmlrpclib.ServerProxy('https://api.webfaction.com/')
        session_id, account = server.login(settings.NOTIFY_WEBFACTIONEMAIL['USERNAME'],
                                           settings.NOTIFY_WEBFACTIONEMAIL['PASSWORD'])

        return server, session_id

    def handle_noargs(self, **options):

        server, session_id = self._get_webfaction_session()

        for email in Email.objects.all():

            if email.marked_for_deletion:
                server.delete_email(session_id, email.email)
                email.delete(sync_delete=True)
                continue

            if email.last_synced is None:
                server.create_email(session_id, email.email, email.targets)
            else:
                server.update_email(session_id, email.email, email.targets)

            email.last_synced = datetime.datetime.now()
            email.save()
