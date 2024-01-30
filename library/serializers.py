from .models import (
    Book,
    BookDetail,
    BorrowedBook,
)


from rest_framework import serializers
from rest_framework.serializers import ModelSerializer





# ! Book Detail Serializer
class  InputBookDetailSerializer(ModelSerializer):
    """
    Used for creating a new book detail record.
    at the time of creating a book instance
    """
    class Meta:
        model = BookDetail
        fields=['publisher','language','number_of_pages']
    



#! Book Serializer
class BookSerializer(ModelSerializer):
    book_detail=InputBookDetailSerializer(write_only=True)
    user=serializers.StringRelatedField()


    class  Meta:
        model = Book
        fields=[
            'id',
            'title',
            'ISBN',
            'user',
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
    



# ! Full Book Detail Serializer
class  BookDetailSerializer(ModelSerializer):
    book=serializers.StringRelatedField()
    class Meta:
        model = BookDetail
        fields=['book','publisher','language','number_of_pages']

        
