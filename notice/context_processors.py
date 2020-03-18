from .models import Notice


def num_pending_notices(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'person'):
        return {}
    person = request.user.person
    num = Notice.objects.filter(published=True, to_ack=True).exclude(id__in=person.acked_notices.all()).count()
    return {
        'num_pending_notices': num,
    }
