from .models import (
    Book,
    BookDetail,
    BorrowedBook,
)

from .serializers import (
    BookSerializer,
    GetBookDetailSerializer,
    UpdateBookDetailSerializer,
    UserSerializer

)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import  HTTP_200_OK
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from django.contrib.auth import get_user_model



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

    def get_serializer_class(self):
        if self.request.method in ['GET','HEAD','OPTIONS']:
               return GetBookDetailSerializer
        return UpdateBookDetailSerializer
     

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
    


class UserListView(APIView):
    serailizer_class=UserSerializer

    def get(self,request) -> Response:
        User = get_user_model()
        user = User.objects.all()
        serializer = self.serailizer_class(user,many=True)
        return  Response(serializer.data,status=HTTP_200_OK)
         







     
