from django.shortcuts import render
from datetime import datetime, timezone


# DATE LOGIC
def get_current_year():
    return datetime.now(tz=timezone.utc).year


# ####################### BASIC VIEWS #######################
def home(request):
    # DONE Rebuild Home page
    if request.user.is_authenticated:
        context = {
            'title': 'Cosmic Christ Love',
            'year': get_current_year(),
        }
    else:
        context = {
            'title': 'Cosmic Christ Love',
            'year': get_current_year(),
        }

    return render(request, 'home.html', context)
