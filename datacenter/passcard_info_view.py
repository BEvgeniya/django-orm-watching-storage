from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from django.utils import timezone


def get_duration(visit):
    local_entry_time = timezone.localtime(visit.entered_at)
    if visit.leaved_at: 
        exit_time_local = timezone.localtime(visit.leaved_at)
    else:
        exit_time_local = timezone.now()
    
    return exit_time_local - local_entry_time


def is_visit_long(visit, minutes=60):
    duration = get_duration(visit)
    duration_minutes = int(duration.total_seconds() / 60)
    return duration_minutes > minutes
        
    
def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    
    for visit in visits:
        new_visit = {
            'entered_at': visit.entered_at,
            'duration': get_duration(visit),
            'is_strange': is_visit_long(visit)
        }
        this_passcard_visits.append(new_visit)

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)