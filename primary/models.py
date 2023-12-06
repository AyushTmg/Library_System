from collections.abc import Iterable
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.conf import settings
from django.contrib import admin
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from  django.core.exceptions import ValidationError
from uuid import uuid4

 
# !User Profile Model 
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True,related_name='profile')
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profile/",null=True, blank=True)
    birth_date=models.DateField(null=True, blank=True)
    location=models.CharField(max_length=50, null=True, blank=True)
    phone_number=models.IntegerField(null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

    @admin.display(ordering='user_first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user_last_name')
    def last_name(self):
        return self.user.last_name
    
    
#! Book Genre Model
class Genre(models.Model):
    id=models.UUIDField(unique=True,primary_key=True,default=uuid4)
    title = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.title

# !Book Model
class Book(models.Model):
    id=models.UUIDField(unique=True,primary_key=True,default=uuid4)
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=100,null=True,blank=True)
    author=models.CharField(max_length=100,null=True,blank=True)
    is_available=models.BooleanField(default=True)
    quantity=models.SmallIntegerField(
        validators=[
                    MinValueValidator(1),
                    MaxValueValidator(100)
                    ]
    )
    genre=models.ForeignKey(Genre, on_delete=models.PROTECT,related_name='book')

#? For changing the availability status
    def save(self, *args, **kwargs):
        if self.quantity < 1:
            self.is_available = False
        if self.quantity > 1:
            self.is_available = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class BookImage(models.Model):
    id=models.UUIDField(unique=True,primary_key=True,default=uuid4)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name='images')
    image=models.ImageField(upload_to='book_image/')
    

    
# ! Book Review Model
class Review(models.Model):
    id=models.UUIDField(unique=True,primary_key=True,default=uuid4)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='review')
    book=models.ForeignKey(Book, on_delete=models.CASCADE,related_name='review')
    description=models.CharField(max_length=300)
    date=models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.description

# !Book Review's Reply Model
class Reply(models.Model):
    id=models.UUIDField(unique=True,primary_key=True,default=uuid4)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='reply')
    review=models.ForeignKey(Review, on_delete=models.CASCADE,related_name='reply')
    description=models.CharField(max_length=300)
    date=models.DateField(auto_now_add=True) 

    def __str__(self) -> str:
        return self.description


    
# ! Book Reservation Model
class Reservation(models.Model):
    id=models.UUIDField(unique=True,primary_key=True,default=uuid4)
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='reservation')
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='reservation')
    date = models.DateField(auto_now_add=True)

    def clean(self):
        if not self.book.is_available:
            raise ValidationError(_(f'{self.book} is not available for reservation at the moment\n'))
        if Reservation.objects.filter(user=self.user,book=self.book).exists():
            raise ValidationError(_("User can't reserve the same book multiple times"))
        if self.user.reservation.count() > 10 and not ( self.user.is_staff or  self.user.is_superuser):
            raise ValidationError(_('User cannot reserve more than 10 books.'))
        return super().clean()

    def __str__(self):
        return f"{self.user} has reserved {self.book.title}"


# !Book Borrow Model
class Borrow(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='borrow',primary_key=True)
    book=models.ManyToManyField(Book,related_name='borrow')
    date=models.DateField(auto_now_add=True)
    duration=models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(90)
        ]
    )
    due_date=models.DateField(null=True,blank=True)

    def clean(self):
        if self.duration >10 and not (self.user.is_staff or self.user.is_superuser):
            raise ValidationError(_('Normal user cant set duration more than 10'))
        
        if Borrow.objects.get(user=self.user):
            raise ValidationError(_("You can't borrow books untill you return all the borrowed books"))
        
        if Reservation.objects.filter(user=self.user).exists():
                    raise ValidationError(_("You haven't reserved any book to borrow"))
        
        return super().clean()
    

# ? To calculate the due date
    def save(self, *args, **kwargs):
        if self.date is None:
            self.date = timezone.now().date()
        self.due_date = self.date + timedelta(days=self.duration)
        super().save(*args, **kwargs)



class ReturnBook(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='return_book',primary_key=True)
    returned_at=models.DateField(auto_now_add=True)
    book = models.ManyToManyField('Book', related_name='returned_books')
    # late_fee = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    
    # def calculate_late_fee(self):
    #     self.returned_at=timezone.now().date()
    #     if self.returned_at<=self.user.borrow.due_date:
    #         return 0.0
    #     late_days=(self.returned_at-self.user.borrow.due_date).days
    #     late_fee=late_days*25.0
    #     return late_fee
    
    # def save(self, *args, **kwargs):
    #     self.late_fee = self.calculate_late_fee()
    #     super().save(*args, **kwargs)



        

