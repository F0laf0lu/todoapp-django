from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from . models import Todo
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

# Create your views here.


today = datetime.now().strftime("%Y-%m-%d")


def home(request, current_date=today):

    # if current_date is None:
    #     current_date = datetime.now().date() 

    current_date = datetime.strptime(current_date, "%Y-%m-%d").date()

    # New dates 
    previous_date = current_date - timedelta(days=1)
    next_date = current_date + timedelta(days=1)

    tasks = Todo.objects.all().filter(created_at__date=current_date) #lists tasks per date

    context = {
        'current_date': current_date,
        'previous_date': previous_date,
        'next_date': next_date,
        'tasks': tasks,
        'today':today    
    }

    
    return render(request, 'index.html', context)

def add_task(request, current_date):
    if request.method == 'POST':
        task = request.POST['task']
        due_date_str = request.POST['due_date']

        if not due_date_str:
            return JsonResponse({'status': 'error', 'message': 'Due date is required'})

        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M').replace(tzinfo=None)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid date and time format'})

        task = Todo(task=task, due_date=due_date)  
        task.save()

        return redirect("home", current_date=current_date)

    return redirect("home", current_date=current_date)

def delete_task(request, id, current_date):
    task = get_object_or_404(Todo, id=id)
    task.delete()
    return redirect("home", current_date=current_date)

def mark_task(request, id):
    task = get_object_or_404(Todo, id=id)

    if request.method == 'POST':
        complete_status = request.POST.get('complete') == 'true'
        task.completed = complete_status
        task.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
    
