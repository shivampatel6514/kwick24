from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import User, Category, Subcategory, Service
from .serializers import UserSerializer, CategorySerializer, SubcategorySerializer, ServiceSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions
from .models import Address
from .serializers import AddressSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterUser(APIView):
    def post(self, request):
        try:
            data = request.data
            phone = data.get('phone')
            email = data.get('email')
            password = data.get('password')

            if not phone:
                return Response({'status': False, 'message': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

            if not password:
                return Response({'status': False, 'message': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(phone=phone).exists():
                return Response({'status': False, 'message': 'Phone number already registered'}, status=status.HTTP_400_BAD_REQUEST)

            if email and User.objects.filter(email=email).exists():
                return Response({'status': False, 'message': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

            # Create user with hashed password
            user = User.objects.create(
                phone=phone,
                username=phone,
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=email,
                password=make_password(password)  # Hash password before saving
            )
            print(make_password(password))
            return Response({'status': True, 'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# class LoginWithOTP(APIView):
#     def post(self, request):
#         try:
#             phone = request.data.get('phone')
#             if not phone:
#                 return Response({'status': False, 'message': 'Phone number is required'}, status=status.HTTP_200_OK)

#             # Ensure user is registered
#             if not User.objects.filter(phone=phone).exists():
#                 return Response({'status': False, 'message': 'User not registered'}, status=status.HTTP_200_OK)

#             # Mock OTP process
#             otp = '123456'  # In production, generate and send OTP via SMS
#             return Response({'status': True, 'otp': otp, 'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'status': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_message)


# class VerifyOTP(APIView):
#     def post(self, request):
#         try:
#             phone = request.data.get('phone')
#             otp = request.data.get('otp')

#             if otp != '123456':  # Mock OTP validation
#                 return Response({'status': False, 'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

#             user = User.objects.get(phone=phone)

#             # Generate JWT tokens
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'status': True,
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'user': UserSerializer(user).data
#             }, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({'status': False, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'status': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_message)

class LoginWithPassword(APIView):
    def post(self, request):
        try:
            phone = request.data.get('phone')
            password = request.data.get('password')

            if not phone or not password:
                return Response({'status': False, 'message': 'Phone and password are required'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(phone=phone).first()

            if user and user.check_password(password):  # Directly check password
                refresh = RefreshToken.for_user(user)
                return Response({
                    'status': True,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            else:
                return Response({'status': False, 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            # user = authenticate(username=phone, password=password)

            # if user is None:
            #     return Response({'status': False, 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            # # Generate JWT tokens
            # refresh = RefreshToken.for_user(user)
            # return Response({
            #     'status': True,
            #     'refresh': str(refresh),
            #     'access': str(refresh.access_token),
            #     'user': UserSerializer(user).data
            # }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            user = request.user
            data = request.data

            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.email = data.get('email', user.email)

            if 'password' in data and data['password']:
                user.password = make_password(data['password'])

            user.save()

            return Response({'status': True, 'data': UserSerializer(user).data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class UpdateProfile(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request):
#         try:
#             user = request.user
#             data = request.data

#             user.first_name = data.get('first_name', user.first_name)
#             user.last_name = data.get('last_name', user.last_name)
#             user.email = data.get('email', user.email)
#             user.save()

#             return Response({'status': True, 'data': UserSerializer(user).data}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'status': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_message)


# @api_view(['GET'])
# def get_categories(request):
#     try:
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({'status': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_message)

@api_view(['GET'])
def get_categories(request):
    try:
        categories = Category.objects.prefetch_related('subcategory_set').all()
        serializer = CategorySerializer(categories, many=True)
        return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_message)

@api_view(['GET'])
def get_subcategories_by_category(request, category_id):
    try:
        # Check if the category exists
        category = Category.objects.get(id=category_id)
        
        # Fetch all subcategories for the given category
        subcategories = Subcategory.objects.filter(category=category)
        serializer = SubcategorySerializer(subcategories, many=True)
        
        return Response({
            'status': True,
            'category': {
                'id': category.id,
                'name': category.name,
            },
            'subcategories': serializer.data
        }, status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        return Response({'status': False, 'message': 'Category not found'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_message)


# Get Subcategories
@api_view(['GET'])
def get_subcategories(request):
    try:
        subcategories = Subcategory.objects.all()
        serializer = SubcategorySerializer(subcategories, many=True)
        return Response({'status': True, 'data': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_message)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_service(request):
    try:
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'status': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'status': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_message)



# List and Create API
class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # List addresses of the logged-in user
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user to the address
        serializer.save(user=self.request.user)


# Update API
class AddressUpdateView(generics.UpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure users can only update their own addresses
        return Address.objects.filter(user=self.request.user)