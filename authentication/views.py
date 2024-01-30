from .models import User 
from .serializers import (
    UserRegistrationSerializer,
)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.permissions import AllowAny


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
