from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, w222orld. You're at the polls index.")