from django.db import models
from django.conf import settings
from django.utils import timezone




# !Book Model
class Book(models.Model):
    """
    Assumption: Havent used the BookId attribute
    because Django automatically adds an id field 
    to serve as the primary key
    """
    title=models.CharField(max_length=100)
    ISBN=models.CharField(max_length=100)
    genre=models.CharField(max_length=50)
    published_at=models.DateField()
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='book')

    def __str__(self) -> str:
        return self.title




# !Book Detail
class BookDetail(models.Model):
    number_of_pages=models.PositiveIntegerField()
    publisher=models.CharField(max_length=100)
    language=models.CharField(max_length=50)
    
    """
    Assumption: Haven't used DetailId attribute instead used
    the foreign key  book model as primary key 
    """
    book=models.OneToOneField(Book,on_delete=models.CASCADE,primary_key=True,related_name='book_detail')

    def __str__(self) -> str:
        return  f"{self.publisher}_{self.book}"



# !Borrow Book 
class BorrowedBook(models.Model):
    borrowed_at=models.DateField(auto_now_add=True)
    returned_at=models.DateField(null=True,blank=True)
    is_returned=models.BooleanField(default=False)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='borrowed_book')
    book=models.OneToOneField(Book,on_delete=models.PROTECT,related_name='borrowed_book',primary_key=True)


    def __str__(self) -> str:
        return f"{self.user} borrowed {self.book}"
    

    def book_returned(self):
        """
        Custom method to mark the book as returned.
        """
        if not self.is_returned:
            self.is_returned = True
            self.returned_at = timezone.now().date()
            self.save()
