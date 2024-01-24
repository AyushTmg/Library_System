from celery import shared_task 
from django.core.mail import send_mail

# @shared_task
# def wish_birthday(name):
#     print("Happy birthday, {}!".format(name))
#     return "have a good day"

    
@shared_task(name='Hello')
def say_hello(name):
    return f"Hello {name}"



