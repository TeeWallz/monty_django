# services.py
from .models import Chump, SpecialEvent, Era
import datetime
from collections import defaultdict

def get_streak_status(streak):
    averageExpectingGateDays = 7
    if streak <= 20:
        return "Recent loss against Monty Balboa"
    elif abs(streak - averageExpectingGateDays) <= averageExpectingGateDays:
        return "Expecting soon!"
    elif streak - averageExpectingGateDays >= 14:
        return "WAAAAY overdue!!"
    elif streak - averageExpectingGateDays >= 7:
        return "Overdue"
    else:
        return "Not expecting"

def get_stats(chumps):
    streaks = [chump['streak'] for chump in chumps]
    average = sum(streaks) / len(streaks) if streaks else 0
    median = sorted(streaks)[len(streaks) // 2] if streaks else 0
    max_value = max(streaks) if streaks else 0
    min_value = min(streaks) if streaks else 0
    normal_distribution = "N/A"
    return {
        'average': round(average, 2),
        'median': round(median, 2),
        'max': round(max_value, 2),
        'min': round(min_value, 2),
        'normal_distribution': normal_distribution,
    }

def get_chumps():
    chumps = Chump.objects.all().order_by('-date', 'date_order')
    chumps_list = []
    for chump in chumps:
        chumps_list.append(chump.__pojo__())

    # Calculate streaks
    for i in range(len(chumps_list)):
        if i == 0:
            # diff between date and today
            today = datetime.date.today()
            date_diff = (today - chumps_list[i]['date']).days
            chumps_list[i]['streak'] = date_diff
        elif i == len(chumps_list) - 1:
            chumps_list[i]['streak'] = 0
        else:
            date_diff = (chumps_list[i-1]['date'] - chumps_list[i]['date']).days
            chumps_list[i]['streak'] = date_diff
    
    return chumps_list

def get_chumps_by_year():
    """Group chumps by year for the history template"""
    chumps = get_chumps()
    
    # Group by year using defaultdict
    chumps_by_year_dict = defaultdict(list)
    
    for chump in chumps:
        year = chump['date'].year
        chumps_by_year_dict[year].append(chump)
    
    # Convert to list of dictionaries sorted by year (descending)
    chumps_by_year = []
    for year in sorted(chumps_by_year_dict.keys(), reverse=True):
        # Sort chumps within each year by date (newest first)
        chumps_in_year = sorted(
            chumps_by_year_dict[year], 
            key=lambda x: x['date'], 
            reverse=True
        )
        chumps_by_year.append({
            'year': year,
            'chumps': chumps_in_year
        })
    
    return chumps_by_year

def get_chumps_by_year_week():
    """Group chumps by year and week number"""
    chumps = get_chumps()
    chumps_by_year_week = defaultdict(lambda: defaultdict(list))
    
    for chump in chumps:
        year = chump['date'].year
        # Calculate week number
        week = chump['date'].isocalendar()[1]
        chumps_by_year_week[year][week].append(chump)
    
    return chumps_by_year_week

def get_special_events():
    special_events = SpecialEvent.objects.all().order_by('date')
    return [event.__pojo__() for event in special_events]

def get_eras():
    eras = Era.objects.all().order_by('start_date')
    return [era.__lib_pojo__() for era in eras]

def get_timeline_data():
    chumps = get_chumps()
    special_events = get_special_events()
    eras = get_eras()

    timeline = {
        'title': {
            'text': {
                'headline': "The Saga of Montague Street Bridge",
                'text': "A chronicle of Melbourne's most infamous bridge and its ongoing battle with vehicles"
            },
            'media': {
                'url': "/media/2010/header.jpg",
                'caption': "Montague Street Bridge"
            }
        },
        'eras': eras,
        'events': special_events,
    }

    for chump in chumps:
        event = {
            'start_date': {
                'year': chump['date'].year,
                'month': chump['date'].month,
                'day': chump['date'].day
            },
            'text': {
                'headline': f"<a href='{chump['url']}'>{chump['name']}</a>",
                'text': f"Strike occurred on {chump['localised_date']}."
            },
            'background': {
                'url': chump['media'][0]['url'] if chump.get('media') else None
            },
            'group': "strikes"
        }
        timeline['events'].append(event)

    return timeline