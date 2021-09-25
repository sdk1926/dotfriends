import jwt
import functools, time

from django.http.response import HttpResponse
from django.http      import JsonResponse
from django.conf import settings
from django.db   import connection, reset_queries
from django.conf import settings

from .models import Category, User

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

import functools, time
from django.db   import connection, reset_queries
from django.conf import settings


def query_debugger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        reset_queries()
        number_of_start_queries = len(connection.queries)
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        end    = time.perf_counter()
        number_of_end_queries = len(connection.queries)
        print(f"-------------------------------------------------------------------")
        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {number_of_end_queries-number_of_start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        print(f"-------------------------------------------------------------------")
        return result
    return wrapper