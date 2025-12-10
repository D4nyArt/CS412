# File: authentication.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 12/9/2025
# Description: Custom authentication classes for the project.

from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions

class CustomTokenAuthentication(TokenAuthentication):
    """
    Custom Token Authentication class that checks for 'X-Authorization' header
    in addition to the standard 'Authorization' header.
    """
    def authenticate(self, request):
        """
        Authenticate the request using the token from the header.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            tuple: (user, token) if authentication succeeds, None otherwise.
        """
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
