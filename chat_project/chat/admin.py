from django.contrib import admin
from .models import Chat, Message

# Регистрация моделей в админке
admin.site.register(Chat)
admin.site.register(Message)
