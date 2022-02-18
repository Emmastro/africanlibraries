from account.models import Reader
from django.http import JsonResponse # For AJAX Requests

# Create your views here.

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': Reader.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)