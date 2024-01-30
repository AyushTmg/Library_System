from rest_framework_simplejwt.tokens import RefreshToken


#! Generates token manually
def get_tokens_for_user(user):
    """
    Custom JWT token generating method
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh':str(refresh),
        'access': str(refresh.access_token),
    }