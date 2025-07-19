from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.urls import reverse

def send_password_reset_email(request, user):
    

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    
    reset_url = request.build_absolute_uri(
    reverse('reset-password-page', args=[uid, token])  # Use the HTML page view name!
    )


    subject = 'Password Reset Request'
    message = f'Hi {user.username}, click the link to reset your password:\n\n{reset_url}'

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # From email
        [user.email],             # To email
        fail_silently=False,
    )
