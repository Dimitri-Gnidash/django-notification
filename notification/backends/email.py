from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext

from notification import backends


class EmailBackend(backends.BaseBackend):
    spam_sensitivity = 2

    def can_send(self, user, notice_type):
        can_send = super(EmailBackend, self).can_send(user, notice_type)
        if can_send and user.email:
            return True
        return False

    def deliver(self, recipient, sender, notice_type, extra_context):

        context = self.default_context()
        context.update({
            "recipient": recipient,
            "sender": sender,
            "notice": ugettext(notice_type.display),
        })
        context.update(extra_context)

        messages = self.get_formatted_messages((
            "short.txt",
            "full.txt",
            "notice.html",
            "full.html",
        ), notice_type.label, context)

        from notification.models import Notice
        notice = Notice.objects.create(recipient=recipient, message=messages["notice.html"],
            notice_type=notice_type, on_site=True, sender=sender)
