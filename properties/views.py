from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Property
from .serializer import PropertySerializer
from django.contrib.auth.models import User
from rest_framework import permissions


# Create your views here.

class PropertyListAPIView(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request,format=None):
        data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'subscription_status': request.data.get('subscription_status'),
            'image': request.data.get('image'),
        }
        serializer = PropertySerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PropertyDetailAPIView(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            return Response({'error': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, *args, **kwargs):
        property_details = self.get_object(pk)
        if property_details is None:
            return Response({'error': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PropertySerializer(property_details)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        properties = self.get_object(pk)
        if properties is None:
            return Response({'error': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)
        data = {
            'user': request.user.id,
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'subscription_status': request.data.get('subscription_status'),
            'image': request.data.get('image')
        }

        serializer = PropertySerializer(instance=properties, data=data, partial=True)
        if serializer.is_valid():
            if properties.user.id == request.user.id:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': 'You are not allowed to edit this property'},
                            status=status.HTTP_403_FORBIDDEN)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        prop = self.get_object(pk)
        if prop is None:
            return Response({'error': 'Property not found'}, status=status.HTTP_404_NOT_FOUND)
        if prop.user.id == request.user.id:
            prop.delete()
            return Response({'message': 'Property deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'You are not allowed to delete this property'}, status=status.HTTP_403_FORBIDDEN)


# TODO: get user properties by id
class UserPropertyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username, *args, **kwargs):
        user = User.objects.filter(username=username).first()
        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        properties = Property.objects.filter(user=user)
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
