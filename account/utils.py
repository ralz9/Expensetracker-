from django.core.mail import send_mail

def send_activation_code(email, code):
    send_mail(
        'Activate your account',
        f'Привет перейди по ссылке что бы активировать http://localhost:8000/api/v1/account/activate/{code}',
        'rodiondereha@gmail.com',
        [email]
    )
