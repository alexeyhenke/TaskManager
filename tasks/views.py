# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # Импортируем защиту
from .models import Task
from django.contrib.auth.forms import UserCreationForm # Импортируем готовую форму
from django.contrib.auth import login # Функция для автоматического входа после регистрации



@login_required(login_url='/login/')  # Если пользователь не вошел, его кинет на /login/
def index(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if not action:
            title_from_form = request.POST.get('task_title')
            # Важно: Передаем текущего пользователя request.user при создании
            Task.objects.create(title=title_from_form, user=request.user)
        elif action == 'complete':
            task_id = request.POST.get('task_id')
            # Для безопасности ищем задачу только среди задач текущего пользователя
            task = Task.objects.get(id=task_id, user=request.user)
            task.is_completed = True
            task.save()
        elif action == 'delete':
            task_id = request.POST.get('task_id')
            task = Task.objects.get(id=task_id, user=request.user)
            task.delete()

        current_tab = request.GET.get('tab', 'active')
        return redirect(f'/?tab={current_tab}')

    status = request.GET.get('tab', 'active')

    # Везде добавляем фильтр .filter(user=request.user), чтобы видеть ТОЛЬКО СВОИ задачи
    active_count = Task.objects.filter(is_completed=False, user=request.user).count()

    if status == 'completed':
        tasks = Task.objects.filter(is_completed=True, user=request.user).order_by('-created_at')
    else:
        tasks = Task.objects.filter(is_completed=False, user=request.user).order_by('-created_at')

    context = {
        'tasks': tasks,
        'current_tab': status,
        'active_count': active_count
    }
    return render(request, 'tasks/index.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Сохраняем нового пользователя в базу данных
            user = form.save()
            # Автоматически логиним пользователя, чтобы ему не нужно было входить заново
            login(request, user)
            # Перенаправляем на главную страницу
            return redirect('/')
    else:
        # Если пользователь просто открыл страницу — показываем пустую форму
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
