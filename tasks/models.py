# Create your models here.
from django.db import models

class Task(models.Model):
    # Заголовок задачи, максимум 200 символов
    title = models.CharField(max_length=200)
    # Статус: выполнена задача или нет (по умолчанию — нет)
    is_completed = models.BooleanField(default=False)
    # Дата создания задачи (добавляется автоматически)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
