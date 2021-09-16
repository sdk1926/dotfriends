import jwt

from django.http.response import HttpResponse
from django.http      import JsonResponse
from django.conf import settings

from .models import Category, User

def input_validator(func):
    def wraper(self, request, *args, **kwargs):
        try:
            offset   = int(request.GET.get('offset', 1))
            limit    = int(request.GET.get('limit', 12))
            order    = request.GET.get('order', 'id')
            category = request.GET.get('category', 0)
            sale     = int(request.GET.get('sale', 0))
            new      = int(request.GET.get('new', 0))

            if new != 1 and new != 0: 
                return HttpResponse(status=400)
            
            if sale != 1 and sale != 0: 
                return HttpResponse(status=400)
    
            if category == '' or category and not (Category.objects.filter(id=int(category)).exists()):
                return HttpResponse(status=404)

            if not (order == 'id' or order == '-id' or order == '?'\
                or order=='-popular' or order=='-updated_at' or order =='price' or order =='-price'):
                return HttpResponse(status=400) 
        except ValueError:
            return HttpResponse(status=400)
        return func(self, request, *args, **kwargs)
    return wraper

def visitor_validator(func):
    def wraper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization',None)
            if not access_token:
                request.user = None
                return func(self, request, *args, **kwargs)
            token = jwt.decode(access_token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=token['id'])
            request.user = user.id
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_USER'},status=401)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE':'INVALID_TOKEN'},status=401)
        return func(self, request, *args, **kwargs)
    return wraper