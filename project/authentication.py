from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions

class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # Try standard header first
        result = super().authenticate(request)
        if result:
            return result
            
        # Try X-Authorization header if standard one failed/missing
        # Apache/WSGI often strips 'Authorization' but passes 'X-Authorization'
        token = request.META.get('HTTP_X_AUTHORIZATION')
        if not token:
            return None
            
        # Validate the token format (should be "Token <key>")
        try:
            auth_type, token_key = token.split()
            if auth_type.lower() != 'token':
                return None
        except ValueError:
            return None
            
        return self.authenticate_credentials(token_key)
