
from .views import ( 
     UserListView,
     BookDetailView,
     UserDetailView,
     ReturnBookView,
     BooksListCreateView,
     CreateBookBorrowView,
     ListBorrowedBookView,
     ListBorrowedHistoryView

)
from django.urls import path


urlpatterns = [
    path('books/',BooksListCreateView.as_view(), name='library_books'),
    path('books/<str:pk>/',BookDetailView.as_view(), name='book_detail'),
    path('books/<str:pk>/borrow/',CreateBookBorrowView.as_view(),name='create_borrow_book'),
    path('user/',UserListView.as_view(), name='user_listing'),
    path('user/<str:pk>/',UserDetailView.as_view(), name='user_detail'),
    path('borrowed_books/',ListBorrowedBookView.as_view(), name='list_borrowed_book'),
    path('return_book/',ReturnBookView.as_view(),name='return_book'),
    path('borrowed_history/',ListBorrowedHistoryView.as_view(),name='list_borrowed_history'),


]