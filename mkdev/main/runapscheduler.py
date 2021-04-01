from django.contrib.sites.models import Site
from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from main.models import Product, Seller

scheduler = BackgroundScheduler()


def products_of_the_week():
    domain = Site.objects.get_current().domain
    product = Product.objects.filter(tags=3, is_active=True)[:3]
    subject, from_email, to = 'Subject', 'from@xxx.com', 'to@xxx.com'
    url = 'http://{domain}'.format(domain=domain)
    html_content = render_to_string('main/new_product_mail.html',
                                                {'varname': 'Новые продукты за неделю', 'url': url, 'product': product}),
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(
                subject,
                text_content,
                from_email,
                [to],
            )
    msg.send()


scheduler.add_job(products_of_the_week, "cron", week=1, id='products_of_the_week', replace_existing=True)
scheduler.start()