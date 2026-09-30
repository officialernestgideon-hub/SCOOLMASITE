import os

import resend

from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string


class ResendPasswordResetForm(PasswordResetForm):

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        api_key = os.environ.get("RESEND_API_KEY")

        if not api_key:
            raise RuntimeError(
                "RESEND_API_KEY is not configured."
            )

        resend.api_key = api_key

        subject = render_to_string(
            subject_template_name,
            context
        ).strip()

        message = render_to_string(
            email_template_name,
            context
        )

        params = {
            "from": from_email or "onboarding@resend.dev",
            "to": [to_email],
            "subject": subject,
            "html": message.replace("\n", "<br>"),
        }

        resend.Emails.send(params)