
from .views import ( 
     BooksListCreateView,
     BookDetailView

)
from django.urls import path


urlpatterns = [
    path('books/',BooksListCreateView.as_view(), name='library_books'),
    path('books/<str:pk>/',BookDetailView.as_view(), name='book_detail'),

]