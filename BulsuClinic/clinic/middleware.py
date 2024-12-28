from django.contrib.messages.context_processors import messages
from django.shortcuts import redirect
from django.contrib import messages

class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # if request.user.is_authenticated:
        #     if request.user.is_superuser:
        #             return redirect('manage_staff')
        return self.get_response(request)

