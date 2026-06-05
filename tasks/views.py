from django.shortcuts import render, redirect
from django.http import HttpResponse

from tasks.models import Task


# Create your views here.

def index(request):
    # Если пользователь нажал кнопку на форме (отправил POST-запрос)
    if request.method == 'POST':
        # Достаем текст, который пользователь ввел в поле input
        title_from_form = request.POST.get('task_title')

        # Создаем новую запись в базе данных
        Task.objects.create(title=title_from_form)

        # Перезагружаем страницу, чтобы сбросить отправку формы
        return redirect('/')

    # Если это обычный заход на страницу (GET-запрос)
    tasks = Task.objects.all()
    ## return HttpResponse("Привет! Это мой менеджер задач.")
    return render(request, 'tasks/index.html', {'tasks': tasks})
