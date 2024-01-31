from .models import (
    Book,
    BookDetail,
    BorrowedBook,
)

from .serializers import (
    BookSerializer,
    GetBookDetailSerializer,
    UpdateBookDetailSerializer,
    UserListSerializer,
    UserDetailSerializer,
    GetUserBorrowedBookSerailizer,
    CreaterBorrowedBookSerailizer,
    ListBorrowedBookSerializer

)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import  HTTP_200_OK,HTTP_201_CREATED,HTTP_404_NOT_FOUND
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)


from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


User = get_user_model()



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
    



# ! Book Detail View 
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
            
            return (
                 BookDetail.objects
                 .filter(pk=pk)
                 .select_related('book')
                )
    

    def get_permissions(self):
        """
        set permission based on action 
        """
        if self.request.method in permissions.SAFE_METHODS:
            return  [AllowAny()]
        return [IsAuthenticated()]
    
    




 # ! Create Book Borrow View 
class CreateBookBorrowView(APIView):
    """
    Method to create borrow book instance when 
    user post 
    """
    serializer_class=CreaterBorrowedBookSerailizer
    permission_classes=[IsAuthenticated]


    def get(self, request, *args, **kwargs):
        """
        This methods helps to shows if a particular books 
        is available or not
        """
        user=request.user
        pk = self.kwargs['pk']

        user_borrow=BorrowedBook.objects.filter(user=user,pk=pk)
        other_borrow=BorrowedBook.objects.filter(pk=pk)
        
        # ! Checks if the logged in user has borrowed this book or not 
        if user_borrow.exists():
            return Response(
                "You've already borrowed this book",
                status=HTTP_200_OK
                )
        
        # ! Checks if any other user has borrowed this book or not
        elif other_borrow.exists():
             return Response(
                "Sorry Some other user has borrowed this book for now Please wait untill the book is returned and avaiable in library, Thank You",
                status=HTTP_404_NOT_FOUND
                )
        
        # ! It is executed if both of upper conditional statement is False 
        else:
            return get_object_or_404(Book,id=pk)


    def post(self, request, *args, **kwargs):
        """
        This method helps to add a new Book into database
        and also pass user_id and book_id present at URL
        parameter to serializer class
        """

        user_id=request.user.id
        pk = self.kwargs['pk']
        
        serializer=self.serializer_class(
             data=request.data,
             context={
                  'user_id':user_id,
                  'book_id':pk
                  }
            )
        
        #* validating and save the borrow book instance
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
             "You've Successfully Borrowed the book",
             status=HTTP_201_CREATED
            )
    



# ! User List View
class UserListView(APIView):
    serailizer_class=UserListSerializer

    def get(self,request) -> Response:
        """
        Return a list of all users
        """
        user = User.objects.all()
        serializer = self.serailizer_class(user,many=True)
        return  Response(serializer.data,status=HTTP_200_OK)
         



# ! User Detail View 
class UserDetailView(RetrieveUpdateAPIView):
    serializer_class=UserDetailSerializer

    def get_queryset(self):
            """
            Over Ridden queryset to filter User
            by primary key present in URL parameter
            """
            pk = self.kwargs['pk']

            return (
                User.objects
                .filter(pk=pk)
                .prefetch_related(
                    'book',
                    'borrowed_book',
                )
            )



    
# ! For Listing all the borrowed books from the library
class ListBorrowedBookView(ListAPIView):
     queryset=BorrowedBook.objects.all().select_related('book','user')
     serializer_class=ListBorrowedBookSerializer
     permission_classes=[IsAdminUser]
     



     