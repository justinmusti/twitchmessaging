from django.shortcuts import render, redirect
from django.contrib.auth import logout as logout_user, authenticate, login as login_user
from django.http import JsonResponse
import json
from django.db.models import Q
from core.models import User, Conversation, Message
from django.views.decorators.csrf import ensure_csrf_cookie, requires_csrf_token
# Create your views here.


@ensure_csrf_cookie
def register(request):
    if request.user.is_authenticated:
        return render(request, 'error.html', {'error': "Seems like you are already logged in"})
    return render(request, 'register.html')


@ensure_csrf_cookie
def login(request):
    return render(request, 'login.html')


def login_do(request):
    status = False
    status_code = 413
    error = None
    data = {}
    try:
        post = json.loads(request.body)
        username = post.get('username', None)
        password = post.get('password', None)

        assert username, "Username cannot be empty."
        assert password, "Password cannot be empty."
        username = username.lower()
        if not User.objects.filter(username=username).exists():
            raise AssertionError('No account with given username')

        # authenticate user
        user = authenticate(request, username=username, password=password)
        if not user:
            raise AssertionError('Invalid username or password.')
        login_user(request, user)
        status = True
        error = None
        status_code = 200
        data = {}

    except AssertionError as ae:
        status = False
        error = str(ae)
        status_code = 400
        data = {}

    except Exception as e:
        import traceback
        traceback.print_exc()
        status = False
        status_code = 500
        data = {}
        error = "Something went wrong."

    response_data = {
        'status': status,
        'error': error,
        'data': data
    }

    return JsonResponse(data=response_data, status=status_code)


def logout(request):
    logout_user(request)
    return redirect('/')


def register_do(request):
    status = False
    status_code = 413
    error = None
    data = {'login': False}
    try:
        assert not request.user.is_authenticated, "There is already a user session."
        post = json.loads(request.body)
        username = post.get('username', None)
        password = post.get('password', None)
        assert username, "A username must be provided."
        assert password, "A password must be provided."
        username = str(username).lower()
        if User.objects.filter(username=username).exists():
            raise AssertionError('This username is already taken.')

        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        if user.pk:
            # Login user
            user = authenticate(request, username=username, password=password)
            if user:
                login_user(request, user)
                data['login'] = True
            status = True
            status_code = 201
            error = None

    except AssertionError as ae:
        status = False
        error = str(ae)
        status_code = 400
    except Exception as e:
        import traceback
        traceback.print_exc()
        error = 'Something went wrong. Sorry for the inconvenience.'
        status_code = 500
        data = {}
    response_data = {
        'status': status,
        'error': error,
        'data': data
    }
    return JsonResponse(data=response_data, status=status_code)


def conversation(request, user_id):
    status = False
    status_code = 413
    error = None
    data = {}
    try:
        assert request.user.is_authenticated, "You must be logged in to make a conversation."
        current_user = request.user
        trg_user = User.objects.get(pk=user_id)
        if Conversation.objects.\
            filter(Q(sender=current_user, receiver=trg_user)| Q(sender=trg_user, receiver=current_user))\
                .exists():
            # Retrive the conversation if already exists.
            convo = Conversation.objects. \
                filter(Q(sender=current_user, receiver=trg_user) | Q(sender=trg_user, receiver=current_user)) \
                .first()
        else:
            convo = Conversation.objects.create(
                sender=current_user,
                receiver=trg_user
            )
        status = True
        status_code = 200
        error = None
        data = {
            'conversation_id': convo.pk
        }
    except AssertionError as ae:
        status = False
        status_code = 400
        error = str(ae)
        data = {}
    except Exception as e:
        status = False
        status_code = 500
        error = "Something went wrong."
        data = {}

    response_data = {
        'status': status,
        'error': error,
        'data': data
    }

    return JsonResponse(data=response_data, status=status_code)


def messages(request, conversation_id):
    status = False
    status_code = 413
    error = None
    data = {}
    try:
        assert request.user.is_authenticated, "You must be logged in to make a conversation."
        current_user = request.user
        convo = Conversation.objects.get(pk=conversation_id)
        messages_list = Message.objects.filter(conversation=convo).all()
        status = True
        status_code = 200
        error = None
        data = {
            'messages': [{
                'sender_id': msg.user.pk.__str__(),
                'sender_username': msg.user.username,
                'text': msg.text,
                'created_at': msg.created_at

            } for msg in messages_list]
        }
    except AssertionError as ae:
        status = False
        status_code = 400
        error = str(ae)
        data = {}
    except Exception as e:
        import traceback
        traceback.print_exc()
        status = False
        status_code = 500
        error = "Something went wrong."
        data = {}

    response_data = {
        'status': status,
        'error': error,
        'data': data
    }

    return JsonResponse(data=response_data, status=status_code)


def create_message(request, conversation_id):
    status = False
    status_code = 413
    error = None
    data = {}
    try:

        assert request.user.is_authenticated, "You must be logged in to make a conversation."

        payload = json.loads(request.body)
        text = payload.get('message', None)
        assert text, "Can\'t sent empty message."
        user = request.user
        convo = Conversation.objects.get(pk=conversation_id)
        msg = Message.objects.create(
            conversation=convo,
            user=user,
            text=text
        )
        status = True
        status_code = 201
        error = None
        data = {
            'message': {
                'sender_id': msg.user.pk.__str__(),
                'sender_username': msg.user.username,
                'text': msg.text,
                'created_at': msg.created_at
            }

        }

    except AssertionError as ae:
        status = False
        status_code = 400
        error = str(ae)
        data = {}
    except Exception as e:
        import traceback
        traceback.print_exc()
        status = False
        status_code = 500
        error = "Something went wrong."
        data = {}

    response_data = {
        'status': status,
        'error': error,
        'data': data
    }

    return JsonResponse(data=response_data, status=status_code)