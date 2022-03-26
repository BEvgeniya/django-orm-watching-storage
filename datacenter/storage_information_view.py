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
        

def storage_information_view(request):
    non_leaved = Visit.objects.filter(leaved_at__isnull=True)
    non_closed_visits = []
    
    for visit in non_leaved:
        entered_at = timezone.localtime(visit.entered_at)
        new_visitor = {
            'who_entered': visit.passcard.owner_name,
            'entered_at': entered_at,
            'duration': get_duration(visit),
            'is_strange': is_visit_long(visit)
        }
        non_closed_visits.append(new_visitor)

    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    
    return render(request, 'storage_information.html', context)
