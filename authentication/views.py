from .models import User 
from .tokens import get_tokens_for_user
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer
)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED
)


from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _ 






# ! View For User Registration 
class UserRegistrationView(APIView):
    serializer_class=UserRegistrationSerializer
    permission_classes=[AllowAny]

    def post(self,request) -> Response:
        """
        Method to create a new user.
        """
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_("User Registered successfully"),status=HTTP_201_CREATED)




# ! View For User Login
class UserLoginView(APIView):
    serializer_class=UserLoginSerializer
    permission_classes=[AllowAny]


    def post(self,request)-> Response:
        """
        Handles User login 
        """

        # Checking if the credentials are valid or not
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email=serializer.data.get('email')
        password = serializer.validated_data.get('password')
        user=authenticate(email=email,password=password)
        
        if user is not  None:
            token=get_tokens_for_user(user)
            return Response({"token":token,"message":"Logged in successfully"},status=HTTP_200_OK)
        else:
            return Response(_("Invalid Credential provided"),status=HTTP_401_UNAUTHORIZED)
            
