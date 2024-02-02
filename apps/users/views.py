from .models import User
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import MyAuthTokenSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


@api_view(["POST"])
def login(request):
    if request.method == "POST":
        serializer = MyAuthTokenSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            user_serializer = UserSerializer(user)
            return Response({
                'success': True,
                'token': token.key,
                'user': user_serializer.data
            })
        else:
            return Response({
                'success': False,
                'error': serializer.errors
            })


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def logout(request):
    try:
        request.user.auth_token.delete()
        return Response({'success': True})
    except Exception as e:
        return Response(
            {
                'success': False,
                'error': e.args[0]
            }
        )


@api_view(["POST"])
def sign_up(request):
    if request.method == "POST":
        try:
            user = User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password'],
            )

            user.photo = request.data.get('photo', None)
            user.save()
        except Exception as e:
            return Response(
                data={
                    "success": False,
                    "error": e.args[0],

                },
                status=status.HTTP_200_OK
            )
        return Response(
            data={
                "success": True,
                "message": "User Created Successfully",
                "user": UserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )
