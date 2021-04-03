from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email_task(title, slug, description, price):
    context = {
        'title': title,
        'slug': slug,
        'description': description,
        'price': price,
    }
    from_email, to = 'from@xxx.com', 'to@xxx.com'
    email_subject = 'Thank you'
    email_body = render_to_string('account/email/email_message.txt', context)
    email = EmailMultiAlternatives(
        email_subject,
        email_body,
        from_email,
        [to],
    )
    return email.send()