from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Custom SessionAuthentication class that does NOT enforce CSRF validation.
    This allows API calls to work without explicitly passing the X-CSRFToken header.
    """

    def enforce_csrf(self, request):
        return  # Disable CSRF check