from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from django.contrib.auth.models import User
from django.db.models import Q

@login_required
def chat_list_view(request):
    chats = Chat.objects.filter(participants=request.user)

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        if user_id:
            other_user = get_object_or_404(User, id=user_id)
            # Используем Q для фильтрации, чтобы найти чат, который содержит и текущего пользователя, и другого пользователя
            chat = Chat.objects.filter(Q(participants=request.user) & Q(participants=other_user)).first()
            if not chat:
                chat = Chat.objects.create()
                chat.participants.add(request.user, other_user)
            # Перенаправление в подробности чата
            return redirect('chat_detail', chat_id=chat.id)

    users = User.objects.exclude(id=request.user.id)  # Исключаем самого себя
    return render(request, 'chat/chat_list.html', {'chats': chats, 'users': users})
@login_required
def chat_detail_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.user not in chat.participants.all():
        return redirect('chat_list')  # Перенаправляем, если пользователь не в чате

    messages = chat.messages.order_by('timestamp')  # Теперь получаем сообщения через chat.messages

    if request.method == 'POST':
        content = request.POST.get('content')
        file = request.FILES.get('file')  # Получаем файл из запроса

        other_user = chat.participants.exclude(id=request.user.id).first()  # Находим другого участника чата

        if content or file:  # Создаем сообщение только если есть текст или файл
            Message.objects.create(
                chat=chat,
                sender=request.user,
                receiver=other_user,
                content=content,
                file=file  # Передаем файл в модель
            )
        return redirect('chat_detail', chat_id=chat.id)

    return render(request, 'chat/chat_detail.html', {'chat': chat, 'messages': messages})
