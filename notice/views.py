from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Notice, Ack
from .forms import AckForm


@login_required
def index(request):
    return render(request, 'notice/index.html', {
        'notices': Notice.objects.filter(published=True).order_by('-post_time'),
    })


@login_required
def detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk, published=True)
    person = request.user.person
    if request.method == 'POST':
        form = AckForm(request.POST)
        if form.is_valid():
            Ack.objects.update_or_create(
                notice=notice,
                person=person,
            )
            messages.success(request, '已确认阅读该通知。')
            return redirect('report:home')
    else:
        form = AckForm()
        notice.read_count = F('read_count') + 1
        notice.save(update_fields=('read_count',))
        notice.refresh_from_db(fields=('read_count',))
    return render(request, 'notice/detail.html', {
        'notice': notice,
        'form': form,
    })
