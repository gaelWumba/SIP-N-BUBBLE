import jwt
from django.conf import settings
from django.http import JsonResponse
from django.db import connection

def jwt_required(f):
    def wrap(request, *args, **kwargs):
        # Exclure certaines URL de la nécessité du JWT
        if 'login' in request.path or 'register' in request.path:
            return f(request, *args, **kwargs)
        
        token = request.COOKIES.get('jwt')
        if not token:
            return JsonResponse({'error': 'Authorization token is missing'}, status=403)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user = payload['email']
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Authorization token has expired'}, status=403)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=403)
        
        return f(request, *args, **kwargs)
    
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def admin_required(f):
    def wrap(request, *args, **kwargs):
        token = request.COOKIES.get('jwt')
        if not token:
            return JsonResponse({'error': 'Authorization token is missing'}, status=403)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            email = payload['email']

            # Vérifier si l'utilisateur est un admin
            with connection.cursor() as cursor:
                cursor.execute("SELECT role FROM users WHERE email = %s", [email])
                result = cursor.fetchone()
                if result and result[0] == 'admin':
                    request.user = email
                else:
                    return JsonResponse({'error': 'Access denied: admin required'}, status=403)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Authorization token has expired'}, status=403)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=403)
        
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap

