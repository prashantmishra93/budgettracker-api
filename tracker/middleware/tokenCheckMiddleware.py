# myapp/middleware.py
import jwt
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime

class TokenCheckMiddleware:
    """
    Middleware to check if JWT token is expired.
    """
    
    EXEMPT_URLS = [
        '/api/login',
        '/api/register',
        '/api/allUsers',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    # middleware intercepts request before view runs
    def __call__(self, request):
        path = request.path
        # Skip exempt URLs
        if path in self.EXEMPT_URLS:
            return self.get_response(request)

        token = request.headers.get('Authorization', None)
        if token:
            try:
                # Remove 'Bearer ' prefix if present
                if token.startswith('Bearer '):
                    token = token.split(' ')[1]

                # Decode token
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                
                # Optional: check expiration manually
                exp = payload.get('exp')
                if exp and datetime.utcnow().timestamp() > exp:
                    return JsonResponse({"error": "Token has expired"}, status=401)

                # Attach user info to request if needed
                request.user_id = payload.get('user_id')

            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Token has expired"}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"error": "Invalid token"}, status=401)
        else:
            return JsonResponse({"error": "Authorization token required"}, status=401)

        response = self.get_response(request)
        return response
