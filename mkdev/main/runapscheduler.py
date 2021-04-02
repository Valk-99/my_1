from datetime import timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from django.utils import timezone
from django.contrib.sites.models import Site
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from main.models import Product, Seller, Subscriber

scheduler = BackgroundScheduler()


def products_of_the_week():
    domain = Site.objects.get_current().domain
    products_last_week = timezone.now().date() - timedelta(days=7)
    monday_of_last_week = products_last_week - timedelta(days=(products_last_week.isocalendar()[2] - 1))
    monday_of_this_week = monday_of_last_week + timedelta(days=7)
    sub = Subscriber.objects.values_list('user__email', flat=True)
    product = Product.objects.filter(create_date__gte=monday_of_last_week, create_date__lt=monday_of_this_week)
    subject, from_email, to = 'Subject', 'from@xxx.com', sub
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