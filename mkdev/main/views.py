from datetime import datetime

from django.shortcuts import render


def index(request):
    turn_on_block = True
    now = datetime.now()
    return render(request, 'main/index.html', {'turn_on_block': turn_on_block, 'now': now})
