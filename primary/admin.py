from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.db.models.aggregates import Count
from django.http.request import HttpRequest
from django.utils.html import format_html,urlencode
from django.urls import reverse
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
        list_display=['first_name','last_name','user_id']
        autocomplete_fields=['user']
        list_per_page=10

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
        list_display=['id','title','books']
        list_per_page=10
        fields=['title']
        search_fields=['title__istartswith']

        def books(self,genre):
                url=reverse('admin:primary_book_changelist')+"?"+urlencode({'genre':str(genre.id)})
                return format_html("<a href='{}' target='_blank'>{}</a>",url,genre.book_count)

        def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
                return super().get_queryset(request).annotate(book_count=Count('book'))


class BookImageInline(admin.TabularInline):
        model = BookImage
        extra = 3 
        fields=['image']
        readonly_fields=['thumbnail']

        def thumbnail(self,instance):
                if instance.image.name!='':
                        return format_html(f"<img src='{instance.image.url}' class='thumbnail'/>")                     
                return ""

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
        list_display=['id','title','description','author','is_available','quantity','genre','reviews','borrowers','reservers']
        fields=['title','description','author','is_available','quantity','genre']        
        list_per_page=10
        list_select_related=['genre']
        list_filter=['quantity']
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

        def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
                return super().get_queryset(request).annotate(review_count=Count('review'),borrow_count=Count('borrow'),reservation_count=Count('reservation'))
        
        class Media:
                css={
                        'all':['css/styles.css']
                }

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
        list_display=['id','user','book','description','replies']
        fields=['user','book','description']
        list_per_page=10
        autocomplete_fields=['user','book']
        search_fields=['description__istartswith']

        def replies(self,review):
                url=reverse('admin:primary_reply_changelist')+"?"+urlencode({'review':str(review.id)})
                return format_html("<a href='{}' target='_blank'>{}</a>",url,review.reply_count)

        def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
                return super().get_queryset(request).annotate(reply_count=Count('reply'))


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
        list_display=['user','review','description']
        fields=['user','review','description']
        list_per_page=10
        autocomplete_fields=['user','review']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
        list_display=['id','user','book','date']
        fields=['user','book']
        list_per_page=10   
        autocomplete_fields=['user','book']
@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
        fields=['user','book','duration']
        list_display=['user','duration','due_date','date']
        list_per_page=10
        list_editable=['duration','due_date']
        autocomplete_fields=['user','book']   


@admin.register(ReturnBook)
class ReturnAdmin(admin.ModelAdmin):
        list_display=['user','display_books','returned_at']
        list_per_page=10
        list_select_related=['user']
        autocomplete_fields=['user','book']
        readonly_fields = ['returned_at']

        def display_books(self, obj):
                return ', '.join([book.title for book in obj.book.all()])
