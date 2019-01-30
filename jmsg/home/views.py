from django.shortcuts import render
from django.http import JsonResponse
from core.models import User


def index(request):
    return render(request, "index.html")


def contact_list(request):
    status = False
    error = None
    status_code = 400
    data = dict()

    try:
        if request.user.is_authenticated:
            user_list = User.objects.exclude(pk=request.user.pk).all()
        else:
            user_list = User.objects.all()
        data = [{'id': user.id, 'username': user.username} for user in user_list]
        status = True
        error = None
        status_code = 200

    except AssertionError as ae:
        status = False
        status_code = 400
        error = str(ae)
        data = dict()

    except Exception as e:
        error = "Something went wrong"
        status_code = 500
        status = False
        data = dict()

    response_data = {
        'status': status,
        'error': error,
        'data': data
    }
    return JsonResponse(data=response_data, status=status_code)