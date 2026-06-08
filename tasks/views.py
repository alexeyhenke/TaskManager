# Create your views here.

from django.shortcuts import render, redirect
from .models import Task

def index(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if not action:
            title_from_form = request.POST.get('task_title')
            Task.objects.create(title=title_from_form)
        elif action == 'complete':
            task_id = request.POST.get('task_id')
            task = Task.objects.get(id=task_id)
            task.is_completed = True
            task.save()
        elif action == 'delete':
            task_id = request.POST.get('task_id')
            task = Task.objects.get(id=task_id)
            task.delete()

        # При перенаправлении сохраняем текущую вкладку в адресе строки
        current_tab = request.GET.get('tab', 'active')
        return redirect(f'/?tab={current_tab}')

    # --- ЛОГИКА ВКЛАДОК И СЧЕТЧИКА ---
    # Получаем из адреса параметр ?tab=... (по умолчанию открыта вкладка 'active')
    status = request.GET.get('tab', 'active')

    # Считаем, сколько всего НЕвыполненных задач осталось в базе
    active_count = Task.objects.filter(is_completed=False).count()

    # Фильтруем задачи в зависимости от выбранной вкладки
    if status == 'completed':
        tasks = Task.objects.filter(is_completed=True).order_by('-created_at')
    else:
        tasks = Task.objects.filter(is_completed=False).order_by('-created_at')

    # Передаем в HTML список задач, имя активной вкладки и счетчик
    context = {
        'tasks': tasks,
        'current_tab': status,
        'active_count': active_count
    }
    return render(request, 'tasks/index.html', context)
