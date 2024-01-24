from .models import (
        Profile,
        Genre,
        Book,
        BookImage,
        Review,
        Reply,
        ReturnBook,
        Reservation,
        Borrow
)


from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html,urlencode
from django.urls import reverse



# !For User Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
        list_per_page=10
        list_display=['first_name','last_name','user_id']
        autocomplete_fields=['user']



# !For User Books Genre
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
        list_per_page=10
        list_display=['id','title','books']
        search_fields=['title__istartswith']
        fields=['title']


        def books(self,genre):
                url=reverse('admin:primary_book_changelist')+"?"+urlencode({'genre':str(genre.id)})
                return format_html("<a href='{}' target='_blank'>{}</a>",url,genre.book_count)


        def get_queryset(self, request) :
                return super().get_queryset(request).annotate(book_count=Count('book'))




# !For User Books Image
class BookImageInline(admin.TabularInline):
        model = BookImage
        extra = 3 
        fields=['image']
        readonly_fields=['thumbnail']

        def thumbnail(self,instance):
                if instance.image.name!='':
                        return format_html(f"<img src='{instance.image.url}' class='thumbnail'/>")                     
                return ""



# !For User Books 
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
        list_per_page=10
        list_display=['id','title','description','author','is_available','quantity','genre','reviews','borrowers','reservers']
        fields=['title','description','author','is_available','quantity','genre']        
        list_filter=['quantity']
        list_select_related=['genre']
        list_per_page=10
        inlines=[BookImageInline]
        search_fields=['title__istartswith']
        autocomplete_fields=['genre'] 


        def reviews(self,book):
                url=reverse('admin:primary_review_changelist')+"?"+urlencode({'book':str(book.id)})
                return format_html("<a href='{}' target='_blank'>{}</a>",url,book.review_count)
        

        def borrowers(self,book):
                url=reverse('admin:primary_borrow_changelist')+"?"+urlencode({'book':str(book.id)})
                return format_html("<a href='{}' target='_blank'>{}</a>",url,book.borrow_count)
        

        def reservers(self,book):
                url=reverse('admin:primary_reservation_changelist')+"?"+urlencode({'book':str(book.id)})
                return format_html("<a href='{}' target='_blank'>{}</a>",url,book.reservation_count)


        def get_queryset(self, request) :
                return super().get_queryset(request).annotate(review_count=Count('review'),borrow_count=Count('borrow'),reservation_count=Count('reservation'))
        

        class Media:
                css={
                        'all':['css/styles.css']
                }



# !For User Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
        list_per_page=10
        list_display=['id','user','book','description','replies']
        fields=['user','book','description']
        autocomplete_fields=['user','book']
        search_fields=['description__istartswith']

        def replies(self,review):
                url=reverse('admin:primary_reply_changelist')+"?"+urlencode({'review':str(review.id)})
                return format_html("<a href='{}' target='_blank'>{}</a>",url,review.reply_count)


        def get_queryset(self, request) :
                return super().get_queryset(request).annotate(reply_count=Count('reply'))



# !For User Review Reply
@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
        list_per_page=10
        list_display=['user','review','description']
        fields=['user','review','description']
        autocomplete_fields=['user','review']



# !For User Reservation
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
        list_per_page=10   
        list_display=['id','user','book','date']
        fields=['user','book']
        autocomplete_fields=['user','book']






# !For User Borrowings 
@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
        list_per_page=10
        fields=['user','book','duration']
        list_display=['user','duration','due_date','date']
        list_editable=['duration','due_date']
        autocomplete_fields=['user','book']   






# !For Returned Books 
@admin.register(ReturnBook)
class ReturnAdmin(admin.ModelAdmin):
        list_per_page=10
        list_display=['user','display_books','returned_at']
        list_select_related=['user']
        autocomplete_fields=['user','book']
        readonly_fields = ['returned_at']

        def display_books(self, obj):
                return ', '.join([book.title for book in obj.book.all()])
