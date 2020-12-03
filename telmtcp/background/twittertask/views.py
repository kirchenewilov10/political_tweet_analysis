from django.shortcuts import render
from django.http import HttpResponse
from background_task.models import Task
from . import tasks
# Create your views here.

def register_twitter_task(request):
    task = list(Task.objects.filter(task_name='telmtcp.background.twittertask.tasks.process_twitter_data_update').values())
    queue = "twitter"
    if len(task) == 0:
        tasks.process_twitter_data_update(repeat=Task.DAILY, queue=queue, verbose_name="twitter")

    return HttpResponse('ok')