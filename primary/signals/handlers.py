from django.db.models import signals
from django.conf import settings
from django.dispatch import receiver
from primary.models import Profile,Reservation,Borrow
from primary.tasks import send_borrow_notification,send_reservation_notification,send_book_return_notification
from . import book_returned
@receiver(signals.post_save,sender=settings.AUTH_USER_MODEL)
def create_user_profile_signal(sender,**kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])

@receiver(signals.post_save, sender=Borrow)
def borrow_notification(sender, instance, created, **kwargs):
    if created:
        send_borrow_notification.delay(instance.pk)
        print("Sent borrow notification")

@receiver(signals.post_save, sender=Reservation)
def reservation_notification(sender, instance, created, **kwargs):
    if created:
        send_reservation_notification.delay(instance.id)
        print("Sent reservation notification")

@receiver(book_returned)
def book_returned_notification(sender,**kwargs):
    send_book_return_notification(kwargs['return_book'])
    print("Book return notification sent")
    


    