
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny
from rest_framework import permissions
from rest_framework import status
from .permissions import IsUserOrAdminForDelete,ReviewAndReplyPermission,IsUserOrAdminOnly,IsNormalUserOrAdmin
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .pagination import Default




class ProfileViewSet(ModelViewSet):
    http_method_names=['get','put']
    serializer_class = ProfileSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Profile.objects.all().select_related('user')
        elif self.request.user.is_authenticated:
            return Profile.objects.filter(user=self.request.user).select_related('user')
         

class GenreViewset(ModelViewSet):
    queryset=Genre.objects.all()
    serializer_class=GenreSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]

class BookImageViewSet(ModelViewSet):
    serializer_class=BookImageSerializer

    def get_queryset(self):
        book_id=self.kwargs['book_pk']
        return BookImage.objects.filter(book_id=book_id)
    
    def get_serializer_context(self):
        return {'book_id':self.kwargs['book_pk']}
    
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]
        
class BookViewSet(ModelViewSet):
    queryset=Book.objects.select_related('genre').prefetch_related('images').all()
    filter_backends=[DjangoFilterBackend,SearchFilter]
    filterset_fields=['genre']
    search_fields=['title','author']
    serializer_class=BookSerializer
    pagination_class=Default

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]

class ReviewViewSet(ModelViewSet):
    serializer_class=ReviewSerializer
    permission_classes=[ReviewAndReplyPermission,IsUserOrAdminForDelete,IsAuthenticated]
    filter_backends=[OrderingFilter]
    ordering_fields=['date']

    def get_queryset(self):
        book_id=self.kwargs['book_pk']
        return Review.objects.filter(book_id=book_id).select_related('user','book')
    
    def get_serializer_context(self):
        book_id=self.kwargs['book_pk']
        user_id=self.request.user.id
        return {'book_id':book_id,'user_id':user_id}
    

class ReplyViewSet(ModelViewSet):
    serializer_class=ReplySerializer
    permission_classes=[ReviewAndReplyPermission,IsUserOrAdminForDelete,IsAuthenticated]

    def get_queryset(self):
        review_id=self.kwargs['review_pk']
        return Reply.objects.filter(review_id=review_id).select_related('user')
    
    def get_serializer_context(self):
        review_id=self.kwargs['review_pk']
        user_id=self.request.user.id
        return {'review_id':review_id,'user_id':user_id}

    
class ReservationViewSet(ModelViewSet):
    http_method_names=('get', 'head', 'options','post','delete')
    serializer_class=ReservationSerializer
    permission_classes=[IsNormalUserOrAdmin,IsAuthenticated]
   
    def get_queryset(self):
        book_id=self.kwargs['book_pk']
        user_id=self.request.user.id
        if self.request.user.is_superuser or self.request.user.is_staff :
            return Reservation.objects.filter(book__id=book_id)
        return Reservation.objects.filter(user_id=user_id).select_related('user').prefetch_related('book')
    
    def get_serializer_context(self):
        book_id=self.kwargs['book_pk']
        user_id=self.request.user.id
        return {'book_id':book_id,'user_id':user_id}
    
class BorrowViewSet(ModelViewSet):
    serializer_class=BorrowSerializer
    permission_classes=[IsAdminUser]
    def get_queryset(self):
        return Borrow.objects.all().select_related('user').prefetch_related('book','user__reservation')
    
    def get_serializer_class(self):
        if self.request.method=='POST':
              return CreateBorrowSerializer
        if self.request.method=='PUT':
              return UpdateBorrowSerializer
        return BorrowSerializer 
    
    def create(self, request, *args, **kwargs):
        serializer=CreateBorrowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        borrow=serializer.save()
        serializer=BorrowSerializer(borrow)
        return Response(serializer.data)
    
    def get_serializer_context(self):
        if self.request.method == 'PUT':
            return {"user_id":self.kwargs['pk']}
        return super().get_serializer_context()

class ReturnBookViewSet(ModelViewSet):
    queryset = ReturnBook.objects.all().prefetch_related('user__borrow__book').select_related('user')
    permission_classes=[IsAdminUser]

    def get_serializer_class(self):
        if self.request.method=='POST':
              return CreateReturnSerializer
        if self.request.method==('PUT' or 'PATCH'):
              return UpdateReturnSerializer
        return ReturnSerializer 
    
        
    def create(self, request, *args, **kwargs):
        serializer=CreateReturnSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return_book=serializer.save()
        serializer=ReturnSerializer(return_book)
        return Response(serializer.data)
    
    def get_serializer_context(self):
        if self.request.method in ['PUT', 'PATCH']:
            user_id = self.kwargs['pk']
            return {'user_id': user_id}
        return super().get_serializer_context()
   