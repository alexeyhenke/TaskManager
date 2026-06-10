# Create your models here.
from django.db import models
from django.contrib.auth.models import User # Импортируем модель пользователя

class Task(models.Model):
    # Новое поле: связь с пользователем.
    # models.CASCADE означает: если удалить пользователя, удалятся и все его задачи.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    # Заголовок задачи, максимум 200 символов
    title = models.CharField(max_length=200)
    # Статус: выполнена задача или нет (по умолчанию — нет)
    is_completed = models.BooleanField(default=False)
    # Дата создания задачи (добавляется автоматически)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
