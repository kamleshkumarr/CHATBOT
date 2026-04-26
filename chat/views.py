from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .ai import get_ai_response, get_sentiment, get_summary
from .models import ChatMessage, ChatSession
from django.shortcuts import render



def home(request):
    return render(request, 'home.html')


# -------------------------------
# Chat Page
# -------------------------------
@login_required
def chat_view(request, session_id=None):
    sessions = ChatSession.objects.filter(user=request.user)
    
    if session_id:
        current_session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    else:
        current_session = sessions.first()
        if not current_session:
            current_session = ChatSession.objects.create(user=request.user, title="First Chat")
        return redirect('chat_session', session_id=current_session.id)

    history = current_session.messages.all()
    return render(request, "chat.html", {
        "history": history, 
        "sessions": sessions,
        "current_session": current_session
    })

@login_required
def new_chat(request):
    session = ChatSession.objects.create(user=request.user, title="New Chat")
    return redirect('chat_session', session_id=session.id)


# -------------------------------
# CHATBOT (WITH MEMORY)
# -------------------------------
@login_required
def get_response(request):
    message_text = request.GET.get("message", "")
    session_id = request.GET.get("session_id")

    if not message_text or not session_id:
        return JsonResponse({"response": "Missing data."})

    current_session = get_object_or_404(ChatSession, id=session_id, user=request.user)

    # Save user message
    ChatMessage.objects.create(user=request.user, session=current_session, role='user', content=message_text)

    # Update session title if it's the first message
    if current_session.messages.count() <= 2 and current_session.title == "New Chat":
        current_session.title = message_text[:30] + ( '...' if len(message_text) > 30 else '')
        current_session.save()

    # Fetch history for AI context
    past_messages = current_session.messages.all().order_by('-timestamp')[:10]
    past_messages = reversed(past_messages)
    
    messages = [
        {"role": "system", "content": "You are a helpful and intelligent AI chatbot. Remember the user's name if they provide it."}
    ]
    for msg in past_messages:
        role = "user" if msg.role == 'user' else "assistant"
        messages.append({"role": role, "content": msg.content})
    
    reply = get_ai_response(messages)

    # Save bot reply
    if not reply:
        reply = "I'm sorry, I couldn't generate a response."
    
    ChatMessage.objects.create(user=request.user, session=current_session, role='bot', content=reply)

    return JsonResponse({"response": reply, "title": current_session.title})


# -------------------------------
# SENTIMENT
# -------------------------------
@login_required
def sentiment_view(request):
    message = request.GET.get("message", "")
    reply = get_sentiment(message)
    return JsonResponse({"response": reply})


# -------------------------------
# SUMMARY
# -------------------------------
@login_required
def summary_view(request):
    message = request.GET.get("message", "")
    reply = get_summary(message)
    return JsonResponse({"response": reply})

