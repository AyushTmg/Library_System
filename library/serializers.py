from .models import (
    Book,
    BookDetail,
    BorrowedBook,
)


from rest_framework import serializers
from rest_framework.serializers import ModelSerializer,ValidationError


from django.conf import settings 
from django.contrib.auth import get_user_model


User = get_user_model()


# ! Book Detail Serializer
class  InputBookDetailSerializer(ModelSerializer):
    """
    Used for creating a new book detail record.
    at the time of creating a book instance
    """
    class Meta:
        model = BookDetail
        fields=[
            'publisher',
            'language',
            'number_of_pages'
        ]
    



#! Book Serializer
class BookSerializer(ModelSerializer):
    book_detail=InputBookDetailSerializer(write_only=True)


    class  Meta:
        model = Book
        fields=[
            'id',
            'title',
            'ISBN',
            'genre',
            'published_at',
            'book_detail',
        ]


    def create(self, validated_data):
        """
        Over Riding the Create method to create both
        book and book detail from th validated data
        """
        book_detail_data = validated_data.pop('book_detail')
        user_id=self.context['user_id']

        book = Book.objects.create(user_id=user_id,**validated_data)
        BookDetail.objects.create(book=book, **book_detail_data)

        return book
    



# !for Retrieving Book Detail Serializer
class  GetBookDetailSerializer(ModelSerializer):
    book=BookSerializer()

    class Meta:
        model = BookDetail
        fields=[
            'book',
            'publisher',
            'language',
            'number_of_pages'
        ]




# ! For Updating  The Book Details
class  UpdateBookDetailSerializer(ModelSerializer):
    book=serializers.StringRelatedField()

    class Meta:
        model = BookDetail
        fields=[
            'book',
            'publisher',
            'language',
            'number_of_pages'
        ]




# ! Get Borrowed Book Serialzer
class GetUserBorrowedBookSerailizer(ModelSerializer):
    returned_status=serializers.SerializerMethodField('get_return_status')
    book=BookSerializer()

    def get_return_status(self,borrowwed_book):
        """
        Custom serailizer field fro showing 
        returned book status 
        """
        if borrowwed_book.returned_at==None:
            return  "Not Returned Yet"
        else:
            return "ALready Returned"
        
    class Meta:
        model=BorrowedBook
        fields=[
            'pk',
            'book',
            'borrowed_at',
            'returned_at',
            'returned_status',
        ]




# ! Get Borrowed Book Serialzer
class CreaterBorrowedBookSerailizer(ModelSerializer):
    pk=serializers.ReadOnlyField()
        
    class Meta:
        model=BorrowedBook
        fields=[
            'pk'
        ]

    def validate(self,attrs):
        """
        This method is for handeling exceptions since we 
        have already  defined a CreateBoorrowBook View
        """
        user_id= self.context['user_id']
        book_id =self.context['book_id']

        user_has_borrowed=BorrowedBook.objects.filter(user_id=user_id,book_id=book_id)
        others_has_borrowed=BorrowedBook.objects.filter(book_id=book_id)

        # ! Checks if the logged in user has borrowed this book or not 
        if user_has_borrowed.exists():
            raise ValidationError("You have already borrow this book")
        
        # ! Checks if any other user has borrowed this book or not
        if others_has_borrowed.exists():
            raise ValidationError(
                "Sorry Some other has user has borrowed this book for now Please wait untill the book isreturned and avaiable in library,Thank You"
            )
        
        return attrs
    

    def create(self, validated_data):
        """
        Overriding to use custom method of creating
        borrow book instance 
        """
        user_id= self.context['user_id']
        book_id =self.context['book_id']
        return BorrowedBook.objects.create(user_id=user_id,book_id=book_id)




# !User List Serializer
class UserListSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['id','fullname']




# ! User Detail Serializer
class UserDetailSerializer(ModelSerializer):
    book=BookSerializer(many=True,read_only=True)
    borrowed_book=GetUserBorrowedBookSerailizer(many=True,read_only=True)

    class Meta:
        model=User
        fields=[
            'id',
            'fullname',
            'book',
            'borrowed_book'
        ]



# ! Book List Serializer 
class ListBorrowedBookSerializer(ModelSerializer):
    book=BookSerializer()
    user=serializers.StringRelatedField()
    returned_status=serializers.SerializerMethodField('get_return_status')

    def get_return_status(self,borrowwed_book):
        """
        Custom serailizer field fro showing 
        returned book status 
        """
        if borrowwed_book.returned_at==None:
            return  "Not Returned Yet"
        else:
            return "ALready Returned"
        

    class Meta:
        model=BorrowedBook
        fields=[
            'pk',
            'user',
            'book',
            'borrowed_at',
            'returned_at',
            'returned_status',

        ]