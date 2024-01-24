from .signals import book_returned
from .models import (
    Profile,
    Genre,
    Book,
    BookImage,
    Reply,
    Reservation,
    Review,
    ReturnBook,
    Borrow
)


from rest_framework import serializers


from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import F 



# !Serializer for Profile
class ProfileSerializer(serializers.ModelSerializer):
    name=serializers.SerializerMethodField(method_name='get_name')
    pk=serializers.UUIDField(read_only=True)

    class Meta:
        model=Profile
        fields=['pk','name','bio','profile_pic','birth_date','location','phone_number']


    def get_name(self,profile):
        return f"{profile.user.first_name} {profile.user.last_name}"

    

# !Serializer for Book's Genre
class GenreSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)

    class Meta:
        model=Genre
        fields=['id','title']



# !Serializer for Book's Image
class BookImageSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)

    class Meta:
        model=BookImage
        fields=['id','image']


    def create(self, validated_data):
        book_id=self.context['book_id']
        return BookImage.objects.create(book_id=book_id,**validated_data)




# !Serializer for Book
class BookSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    genre=serializers.StringRelatedField()
    images=BookImageSerializer(many=True,read_only=True)

    class Meta:
        model=Book
        fields=['id','title','description','author','is_available','quantity','genre','images']


# !Serializer for Book
class ReviewSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    book=serializers.StringRelatedField()
    fullname=serializers.SerializerMethodField(method_name='get_fullname')


    class Meta:
        model=Review
        fields=['id','fullname','book','description','date']


    def get_fullname(self,review:Review):
        return f"{review.user.first_name} {review.user.last_name}"
    

    def create(self, validated_data):
        book_id= self.context['book_id']
        user_id=self.context['user_id']
        return Review.objects.create(user_id=user_id,book_id=book_id,**validated_data)




# !Serializer for Reply
class ReplySerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    fullname=serializers.SerializerMethodField(method_name='get_fullname')


    class Meta:
        model=Review 
        fields=['id','fullname','description','date']


    def get_fullname(self,reply:Reply):
        return f"{reply.user.first_name} {reply.user.last_name}"
    

    def create(self, validated_data):
        review_id=self.context['review_id']
        user_id=self.context['user_id']
        return Reply.objects.create(review_id=review_id,user_id=user_id,**validated_data)
    

# !Serializer for Creating Borrw object
class CreateBorrowSerializer(serializers.Serializer):
    user_id=serializers.IntegerField()
    duration=serializers.IntegerField()


    def create(self, validated_data):
        with transaction.atomic():
            user_id = validated_data['user_id']
            User = get_user_model()
            user = User.objects.get(pk=user_id)

            try:
                existing_borrow = Borrow.objects.get(user=user)
                raise serializers.ValidationError(_("You can't borrow books until you return all the borrowed books"))
            except Borrow.DoesNotExist:
                pass


            if not user.reservation.exists():
                    raise serializers.ValidationError(_("You haven't reserved any book to borrow"))
            

            if self.validated_data['duration'] > 10 and not (user.is_staff or user.is_superuser):
                raise serializers.ValidationError(_("Normal user cant set duration more than 10"))
            


            reservation=Reservation.objects.filter(user_id=user_id).prefetch_related('book')
            borrow = Borrow(
                user=user,
                date=timezone.now().date(),
                duration=validated_data['duration']
            )
            borrow.save() 


            try:
                    for item in reservation:
                        borrow.book.add(item.book)
                        book=Book.objects.get(id=item.book.id)
                        book.quantity-=1
                        book.save()
                    reservation.delete()
                    return borrow
            
            except Exception:
                raise serializers.ValidationError(_("Some error occured during reservation"))
            


# !Serializer for Updating Borrow object
class UpdateBorrowSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Borrow
        fields=['duration']
    
    
    def validate_duration(self, value):
        if value is not None and value > 10 and not (self.instance.user.is_staff or self.instance.user.is_superuser):
            raise serializers.ValidationError(_("Normal user can't set duration more than 10"))
        return value


# !Serializer for Borrow object 
class BorrowSerializer(serializers.ModelSerializer):
    pk=serializers.UUIDField(read_only=True)
    due_date=serializers.DateField(read_only=True)
    book=serializers.SerializerMethodField(method_name='get_books')
    fullname=serializers.SerializerMethodField(method_name='get_fullname')


    class Meta:
        model=Borrow
        fields=['pk','fullname','book','duration','date','due_date']


    def get_fullname(self,borrow:Borrow):
        return f"{borrow.user.first_name} {borrow.user.last_name}"
    

    def get_books(self,borrow:Borrow):
        return ", ".join(book.title for book in borrow.book.all())
  
    
            
# !Serializer for Reservation on Books 
class ReservationSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    book=serializers.StringRelatedField()
    fullname=serializers.SerializerMethodField(method_name='get_fullname')


    class Meta:
        model=Reservation
        fields=['id','fullname','book','date']


    def get_fullname(self,reservation:Reservation):
        return f"{reservation.user.first_name} {reservation.user.last_name}"


    def validate(self, data):
        book_id = self.context['book_id']
        user_id = self.context['user_id']

        book = Book.objects.get(pk=book_id)
        if not book.is_available:
            raise serializers.ValidationError(_(f"{book} is not available for reservation at the moment"))

        if Reservation.objects.filter(user_id=user_id, book_id=book_id).exists():
            raise serializers.ValidationError(_("User can't reserve the same book multiple times"))

        return data
    

    def create(self, validated_data):
        book_id=self.context['book_id']
        user_id=self.context['user_id']
        return Reservation.objects.create(book_id=book_id,user_id=user_id,**validated_data)


    
# !Serializer for Creating a ReturnBook Object 
class CreateReturnSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()


    class Meta:
        model = ReturnBook
        fields = ['user_id', 'book']


    def create(self, validated_data):
        with transaction.atomic():
            try:
                user_id = validated_data['user_id']
                user=get_user_model().objects.get(pk=user_id)

                borrow = Borrow.objects.prefetch_related('book').get(user=user)
                returned_books = validated_data['book']
                return_book, created = ReturnBook.objects.get_or_create(user=user)
                return_book.book.add(*returned_books)
                borrow.book.remove(*returned_books)


                Book.objects.filter(pk__in=[book.pk for book in returned_books]).update(quantity=F('quantity') + 1)


                if borrow.book.count() == 0:
                    borrow.delete()
                    book_returned.send_robust(self.__class__,return_book=return_book.pk)
                return return_book
            
            
            except Exception as error:
                raise serializers.ValidationError(_(f"User has'nt borrowed the book,{error}"))
                

# !Serializer for Updating a ReturnBook Object 
class UpdateReturnSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=ReturnBook
        fields=['book']


    def update(self, instance, validated_data):
        with transaction.atomic():
            try:
                user_id = self.context['user_id']
                user=get_user_model().objects.get(pk=user_id)


                borrow = Borrow.objects.prefetch_related('book').get(user=user)
                returned_books = validated_data['book']
                instance.book.add(*returned_books)
                borrow.book.remove(*returned_books)


                Book.objects.filter(pk__in=[book.pk for book in returned_books]).update(quantity=F('quantity') + 1)


                if borrow.book.count() == 0:
                    borrow.delete()
                    book_returned.send_robust(self.__class__,return_book=instance.pk)

                return instance
            
            except Exception as error:
                raise serializers.ValidationError(_(f"User has'nt borrowed the book,{error}"))
                

    
# !Serializer for ReturnBook 
class ReturnSerializer(serializers.ModelSerializer):
    returned_books = serializers.SerializerMethodField(method_name='get_books')
    borrowed_books = serializers.SerializerMethodField(method_name='get_borrowed_books')


    class Meta:
        model=ReturnBook
        fields=['pk','returned_at','returned_books','borrowed_books']


    def get_books(self,return_book:ReturnBook):
        return ", ".join(book.title for book in return_book.book.all())
    

    def get_borrowed_books(self, return_book: ReturnBook):
        try:
            borrow = return_book.user.borrow
            return ", ".join(book.title for book in borrow.book.all())
        except Borrow.DoesNotExist:
            return "All the borrowed books have been successfully returned"


            

