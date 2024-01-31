from django.contrib import admin
from .models import (
    Book,
    BookDetail,
    BorrowedBook,
    BorrowHistory
)



"""  
Just Some Basic Admin Panel Customization 
For Library
"""


# !Admin Inline For Book
class BookDetailInline(admin.TabularInline):
    model=BookDetail
    extra = 1
    autocomplete_fields=['book']
    


# !Admin Interface for Book  Model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id','title','ISBN','user','genre','published_at']
    list_per_page=10
    inlines=[BookDetailInline]
    search_fields=['title']




# !Admin Interface for BookDetail  Model
@admin.register(BorrowedBook)
class BoorrowedBooklAdmin(admin.ModelAdmin):
    list_display = ['pk','user','book','borrowed_at','returned_at']
    list_per_page=10
    autocomplete_fields=['book','user']




# !Admin Interface for Book  Borrow History
@admin.register(BorrowHistory)
class BookAdmin(admin.ModelAdmin):
    list_display = ['pk','user','book','borrowed_at','returned_at']
    list_per_page=10
    autocomplete_fields=['book','user']

