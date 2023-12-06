from celery import shared_task 
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import *
from django.core.exceptions import ObjectDoesNotExist

@shared_task(name='reservation_notification')
def send_reservation_notification(reservation_id):
        try:
                reservation=Reservation.objects.select_related('user').get(id=reservation_id)
                user_email = reservation.user.email
                subject = 'Reservation Notification'
                context={'user':reservation.user,'book':reservation.book,'reservation':reservation}
                message=render_to_string('emails/send_reservation_notification.html',context)
                send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user_email],html_message=message)
        except ObjectDoesNotExist:
                print(f"Reservation with ID {reservation_id} does not exist.")
        except Exception as e:
                print(f"An error occurred while sending reservation notification: {e}")    

@shared_task(name='borrow_notification')
def send_borrow_notification(borrow_id):
        try:
                borrow=Borrow.objects.get(pk=borrow_id).select_related('user')
                user_email = borrow.user.email
                subject = 'Borrow Notification'
                context = {'user': borrow.user,'borrow':borrow}
                message = render_to_string('emails/send_borrow_notification.html', context)
                send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user_email], html_message=message)
        except ObjectDoesNotExist:
                print(f"Borrow with ID {borrow_id} does not exist.")
        except Exception as e:
                print(f"An error occurred while sending borrow notification: {e}")


@shared_task(name='returned_book_notification')
def send_book_return_notification(return_id):
        try:
                return_book=ReturnBook.objects.select_related('user').get(pk=return_id)
                user_email = return_book.user.email
                subject = 'Return_book Notification'
                context={'user':return_book.user}
                message=render_to_string('emails/send_return_book_notification.html',context)
                send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [user_email],html_message=message)
        except ObjectDoesNotExist:
                print(f"return_book with ID {return_id} does not exist.")
        except Exception as e:
                print(f"An error occurred while sending return_book notification: {e}")    
