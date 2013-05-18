
import re

from django.db import models
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator, validate_email

email_prefix_regex = re.compile('^[a-z]+$')


def reserved_keywords_validator(value):
    return value not in ['admin', 'postmaster', 'pr', 'kontakt', 'teknik', 'plan', 'chibiplan', 'konkurrence']


def email_list_validator(value):
    for email in value.split(','):
        if not validate_email(email):
            return False

    return True


def generate_targets(users, groups, raw_emails):
    emails = set([user.email for user in users])
    emails.update([user.email for user in User.objects.filter(groups__in=groups)])
    emails.update(raw_emails)

    return ','.join(emails)


class Email(models.Model):

    email_prefix = models.CharField(max_length=24,
                                    validators=[reserved_keywords_validator,
                                                RegexValidator(email_prefix_regex)],
                                    unique=True,
                                    help_text='&lt;email_prefix&gt;@anime-kita.dk, only lowercase a-z is allowed.')

    forwards = models.ManyToManyField(User, related_name='email_forwards', blank=True)
    forwards_group = models.ManyToManyField(Group, related_name='email_forwards', blank=True)
    forwards_other = models.CharField(max_length=256, blank=True, validators=[email_list_validator])

    last_synced = models.DateTimeField(null=True, blank=True)

    marked_for_deletion = models.BooleanField(default=False)

    @property
    def email(self):
        return '%s@anime-kita.dk' % self.email_prefix

    @property
    def targets(self):
        targets = generate_targets(self.forwards.all(), self.forwards_group.all(), self.forwards_other.split(','))

        if targets == '':
            return 'kita_noreply'  # use the noreply inbox

        return targets

    def delete(self, *args, **kwargs):
        """
        We only want the sync script to do an actual deletion of this one
        """

        sync_delete = kwargs.pop('sync_delete', False)

        if sync_delete:
            super(Email, self).delete(*args, **kwargs)

        self.marked_for_deletion = True
        self.save()

    def __unicode__(self):
        return self.email


class MailingList(models.Model):

    email = models.CharField(max_length=128, unique=True)

    forwards = models.ManyToManyField(User, related_name='mailing_lists', blank=True)
    forwards_group = models.ManyToManyField(Group, related_name='mailing_lists', blank=True)
    forwards_other = models.CharField(max_length=256, blank=True, validators=[email_list_validator])

    last_synced = models.DateTimeField(null=True, blank=True)

    @property
    def targets(self):
        targets = generate_targets(self.forwards.all(), self.forwards_group.all(), self.forwards_other.split(','))

        if targets == '':
            return 'noreply@anime-kita.dk'  # redirect to nothing
        else:
            return targets





