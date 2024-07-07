from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.serializers import (
    UserSerializer,
)
from myapp.models import (
    Users,
)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        pw = request.data.get("password")
        # TODO; include the hashing later on
        user = Users.objects.filter(username=username).values("password")
        if user[0].get("password") == pw:
            response_data = {"message": "Login Successfully"}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {"message": "Invalid credentials"}
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)


class CreateUserView(APIView):
    def post(self, request):
        user_instance = UserSerializer(data=request.data)
        if user_instance.is_valid():
            user_instance.save()
            response_data = {
                "message": "User Created Successfully!",
                "data": user_instance.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(user_instance.errors, status=status.HTTP_401_UNAUTHORIZED)
