from django.shortcuts import render, redirect
from django.http import HttpResponse

from tasks.models import Task

# Create your views here.

def index(request):
    # Если пользователь нажал кнопку на форме (отправил POST-запрос)
    if request.method == 'POST':
        # Проверяем, какая именно форма пришла
        action = request.POST.get('action')

        # 1. Если это добавление новой задачи (у нее нет action)
        if not action:
            title_from_form = request.POST.get('task_title')
            Task.objects.create(title=title_from_form)

        # 2. Если нажали кнопку «Выполнено»
        elif action == 'complete':
            task_id = request.POST.get('task_id')
            task = Task.objects.get(id=task_id)  # Находим задачу по ID
            task.is_completed = True  # Меняем статус
            task.save()  # Сохраняем изменения в базе

        # 3. Если нажали кнопку «Удалить»
        elif action == 'delete':
            task_id = request.POST.get('task_id')
            task = Task.objects.get(id=task_id)  # Находим задачу
            task.delete()  # Удаляем ее из базы

        # Перезагружаем страницу, чтобы сбросить отправку формы
        return redirect('/')

    # Если это обычный заход на страницу (GET-запрос)
    tasks = Task.objects.all()
    ## return HttpResponse("Привет! Это мой менеджер задач.")
    return render(request, 'tasks/index.html', {'tasks': tasks})
