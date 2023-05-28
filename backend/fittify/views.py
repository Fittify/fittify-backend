from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.authentication import TokenAuthentication
from .permissions import IsOwner


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserInfoView(APIView):
    permission_classes = (IsAdminUser|IsOwner, )

    def get(self, request, user_id=None):
        if user_id:
            return self.view_user_info(request, User.objects.get(pk=user_id))
        return self.view_user_info(request, request.user)

    def put(self, request, user_id=None):
        if user_id:
            return self.edit_user(request, User.objects.get(pk=user_id))
        return self.edit_user(request, request.user)

    def delete(self, request, user_id=None):
        if user_id:
            return self.delete_user(request, User.objects.get(pk=user_id))
        return self.delete_user(request, request.user)

    def view_user_info(self, request, user):
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def edit_user(self, request, user):
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=400)
    
    def delete_user(self, request, user):
        try:
            user.delete()
            return Response({"detail": "User deleted succesfully."})
        except User.DoesNotExist:
            return Response({"detail": "User doesn't exist."}, status=404)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, ) 
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Logged out succesfully."})


class UserListView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# class UserEditView(APIView):
#     permission_classes = (IsAdminUser|IsOwner, )

#     def put(self, request, user_id=None):
#         if user_id:
#             return self.edit_user(request, User.objects.get(pk=user_id))
        
#         return self.edit_user(request, request.user)
    
#     def edit_user(self, request, user):
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.error, status=400)


# class UserDeleteView(APIView):
#     permission_classes = (IsAdminUser|IsOwner, )

#     def delete(self, request, user_id=None):
#         if user_id:
#             return self.delete_user(request, User.objects.get(pk=user_id))
        
#         return self.delete_user(request, request.user)
    
#     def delete_user(self, request, user):
#         try:
#             user.delete()
#             return Response({"detail": "User deleted succesfully."})
#         except User.DoesNotExist:
#             return Response({"detail": "User doesn't exist."}, status=404)
    

class UserChangePasswordView(APIView):
    permission_classes = (IsAdminUser|IsOwner, )

    def put(self, request, user_id=None):
        if user_id:
            return self.change_password(request, User.objects.get(pk=user_id))
        else:
            return self.change_password(request, request.user)

    def change_password(self, request, user):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('password')
            new_password2 = serializer.validated_data.get('password2')

            if new_password != new_password2:
                return Response({"detail": "New passwords are different."}, status=400)

            if not user.check_password(old_password):
                return Response({"detail": "Old password is incorrect."}, status=400)

            user.set_password(new_password)
            user.save()

            return Response({"detail": "Password changed successfully."})

        return Response(serializer.errors, status=400)
