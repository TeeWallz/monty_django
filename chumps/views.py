# views.py
from pathlib import Path
from django.shortcuts import render
from django.http import JsonResponse
from django.templatetags.static import static
import datetime
import json
from .models import Chump

APP_DIR = Path(__file__).resolve().parent
from .services import (
    get_chumps, 
    get_streak_status, 
    get_stats, 
    get_timeline_data,
    get_chumps_by_year  # Add this import
)

def chumps_api(request):
    return JsonResponse(get_chumps(), safe=False)

def index(request):
    chumps = get_chumps()
    return render(request, 'index.html', {
        'chumps': chumps,
        "streak_status": get_streak_status(chumps[0]['streak']) if chumps else None,
        "stats": get_stats(chumps),
    })

def index_1990(request):
    chumps = get_chumps()
    return render(request, '1990/index.html', {
        'chumps': chumps,
        "streak_status": get_streak_status(chumps[0]['streak']) if chumps else None,
        "stats": get_stats(chumps),
    })

def entry_1990(request):
    return render(request, '1990/entry.html', {})

def timeline_json(request):
    timeline = get_timeline_data()
    return JsonResponse(timeline, safe=False)

def history(request):
    # Get chumps grouped by year
    chumps_by_year = get_chumps_by_year()
    
    # read background image list from data folder
    with open(APP_DIR / 'data' / 'backgrounds.json') as f:
        background_images = [static(f'images/bg/bgg/{img}') for img in json.load(f)]
    
    return render(request, '1990/history.html', {
        'chumps': get_chumps(),
        'chumps_by_year': chumps_by_year,
        'background_images': background_images,
    })

def stats(request):
    return render(request, '1990/stats.html', {
        'chumps': get_chumps(),
        # "stats": get_stats(get_chumps()),
    })

def cool_pix(request):
    return render(request, '1990/cool_pix.html')

def wpaper(request):
    return render(request, '1990/wpaper.html')

def mycats(request):
    return render(request, '1990/mycats.html')
