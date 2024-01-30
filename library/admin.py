from django.contrib import admin
from .models import (
    Book,
    BookDetail,
    BorrowedBook
)


    


"""  
Just Some Basic Admin Panel Customization 
For Library
"""
# !Admin Interface for Book  Model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id','title','ISBN','user','genre','published_at']
    list_per_page=10
    search_fields=['title']




"""  
Just Some Basic Admin Panel Customization 
For Library
"""
# !Admin Interface for BookDetail  Model
@admin.register(BookDetail)
class BookDetailAdmin(admin.ModelAdmin):
    list_display = ['pk','book','publisher','language','number_of_pages']
    list_per_page=10
    autocomplete_fields=['book']




"""  
Just Some Basic Admin Panel Customization 
For Library
"""
# !Admin Interface for BookDetail  Model
@admin.register(BorrowedBook)
class BoorrowedBooklAdmin(admin.ModelAdmin):
    list_display = ['user','book','borrowed_at','returned_at']
    list_per_page=10
    autocomplete_fields=['book','user']
