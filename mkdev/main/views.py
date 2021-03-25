from django.shortcuts import render


def index(request):
    turn_on_block = False
    return render(request, 'main/index.html', {'turn_on_block': turn_on_block})
