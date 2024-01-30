from .models import (
    Book,
    BookDetail,
    BorrowedBook,
)

from .serializers import (
    BookSerializer,
    BookDetailSerializer
)

from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView




#! Book Listing and Creating View
class  BooksListCreateView(ListCreateAPIView):
    """
    ListCreateAPIView is used for listing books
    and creating  a new book
    """
    queryset = Book.objects.all().select_related('user')
    serializer_class=BookSerializer


    def get_serializer_context(self):
        """
        user_id context provided to the serializer
        """
        return {'user_id':self.request.user.id}
    

    def get_permissions(self):
        """
        set permission based on action 
        """
        if self.request.method in permissions.SAFE_METHODS:
            return  [AllowAny()]
        return [IsAuthenticated()]
    



# ! BookDetai View 
class BookDetailView(RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView is used  for 
    retrieving a single instance of a model 
    for display,update and delete
    """
    serializer_class = BookDetailSerializer


    def get_queryset(self):
            """
            Over Ridden queryset to filter BookDetail
            by primary key present in URL parameter
            """
            pk = self.kwargs['pk']
            return BookDetail.objects.filter(pk=pk).select_related('book')
    

    def get_permissions(self):
        """
        set permission based on action 
        """
        if self.request.method in permissions.SAFE_METHODS:
            return  [AllowAny()]
        return [IsAuthenticated()]


