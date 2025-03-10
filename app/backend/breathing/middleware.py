import firebase_admin
from firebase_admin import auth, credentials
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.functional import empty
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

class FirebaseAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        if not firebase_admin._apps:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
            firebase_admin.initialize_app(cred)

    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                # Verify the Firebase token
                decoded_token = auth.verify_id_token(token)
                firebase_uid = decoded_token['uid']
                
                # Get or create user in Django
                user, created = User.objects.get_or_create(
                    firebase_uid=firebase_uid,
                    defaults={
                        'username': decoded_token.get('email', firebase_uid),
                        'email': decoded_token.get('email', ''),
                    }
                )
                
                # Update user information if needed
                if not created and user.email != decoded_token.get('email'):
                    user.email = decoded_token.get('email', '')
                    user.save()
                
                request.user = user
            except Exception as e:
                raise AuthenticationFailed(str(e))
        
        response = self.get_response(request)
        return response 