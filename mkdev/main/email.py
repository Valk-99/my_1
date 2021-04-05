# from main.models import Subscriber

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from main.models import Subscriber


def send_email_task(title, slug, description, price):
    sub = Subscriber.objects.values_list('user__email', flat=True)
    email_subject = 'Thank you'
    context = {
        'title': title,
        'slug': slug,
        'description': description,
        'price': price,
    }
    email_body = render_to_string('account/email/email_message.txt', context)
    from_email, to = 'from@xxx.com', sub
    email = EmailMultiAlternatives(
        email_subject,
        email_body,
        from_email,
        [to],
    )
    return email.send()