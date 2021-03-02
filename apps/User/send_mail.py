from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from Test_job.settings import EMAIL_HOST_USER as activation_email


def send_confirmation_email(user):
    context = {
        "user": user,
        "activation_code": user.activation_code
    }
    msg_html = render_to_string("user/email.html", context)
    plain_message = strip_tags(msg_html)
    subject = "Активация аккаунта"
    to_emails = user.email
    mail.send_mail(
        subject,
        plain_message,
        activation_email,
        [to_emails, ],
        html_message=msg_html
    )
