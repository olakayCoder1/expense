from django.shortcuts import render
from django.contrib.auth import get_user_model 
from rest_framework import generics , status
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer , UserRegistrationSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated , AllowAny
from django.conf import settings

# Create your views here.

Users = get_user_model()

def home(request):
    user = Users.objects.get(id=1)
    access = user.get_user_permissions()
    print(user.get_all_permissions())
    if request.user.has_perms('account.add_expenserequest'):
        return render(request, 'cost-management-dashboard.html')
    return render(request, 'home.html')


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    print(request.data)
    serializer = UserRegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data['response'] = "User created successfully.You can now log in"
        return Response(data)
        
    else:
        data = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['GET'])
def user_view(request):
    print(request.user)
    user = Users.objects.get(id=request.user.id)
    data = {'username': user.username , 'email': user.email}
    serializer = UserSerializer(data).data
    return Response(serializer)


class GetUserView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get(self , request , *arg , **kwarg):
        user = Users.objects.get(id=request.user.id)
        serializer = self.get_serializer(data = user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

get_user = GetUserView.as_view()



class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data , context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.id,
            'user': user.username,
            'email': user.email,
            'token': token.key
            })

obtain_token = CustomAuthToken.as_view()