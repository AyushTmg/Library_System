
from .views import ( 
     BooksListCreateView,
     BookDetailView,
     UserListView,
     UserDetailView

)
from django.urls import path


urlpatterns = [
    path('books/',BooksListCreateView.as_view(), name='library_books'),
    path('books/<str:pk>/',BookDetailView.as_view(), name='book_detail'),
    path('user/',UserListView.as_view(), name='user_listing'),
    path('user/<str:pk>/',UserDetailView.as_view(), name='user_detail'),

]