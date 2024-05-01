from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from haberler.models import Makale, Gazeteci
from haberler.api.serializers import MakaleSerializer, GazeteciSerializer
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404


## class api view
class MakaleApiView(APIView):
    def get(self, request):
        makaleler = Makale.objects.all()
        serializer = MakaleSerializer(makaleler, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MakaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MakaleDetailApiView(APIView):
    def get_object(self, request, pk):
        makale_instance = get_object_or_404(Makale, pk=pk)
        return makale_instance

    def get(self, request, pk):
        makale = self.get_object(request, pk)
        serializer = MakaleSerializer(makale)
        return Response(serializer.data)

    def put(self, request, pk):
        makale = self.get_object(request, pk)
        serializer = MakaleSerializer(makale, data=request.data)
        if serializer.is_valid():
            serializer.update(makale, request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({
            'error': {
                'code': 404,
                'message': f'{serializer.errors}'
            }
        }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        makale = self.get_object(request, pk)
        makale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GazeteciApiView(APIView):
    def get(self, request):
        gazeteciler = Gazeteci.objects.all()
        serializer = GazeteciSerializer(gazeteciler, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = GazeteciSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response('Hata', status=status.HTTP_400_BAD_REQUEST)


class GazeteciDetailApiView(APIView):
    def get_object(self, request, pk):
        gazeteci_instance = get_object_or_404(Gazeteci, pk=pk)
        return gazeteci_instance

    def get(self, request, pk):
        gazeteci = self.get_object(request, pk)
        serializer = GazeteciSerializer(gazeteci)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        gazeteci = self.get_object(request, pk)
        serializer = GazeteciSerializer(gazeteci, data=request.data)
        if serializer.is_valid():
            serializer.update(gazeteci, request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({
            'error': {
                'code': 404,
                'message': f'{serializer.errors}'
            }
        }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        gazeteci = self.get_object(request, pk)
        gazeteci.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# # function  api_view
# @api_view(['GET', 'POST'])
# def makale_api_view(request):
#     if request.method == 'GET':
#         makaleler = Makale.objects.all()
#         # makaleler = Makale.objects.filter(aktif=True)
#         serializer = MakaleSerializer(makaleler, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = MakaleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response('Hata', status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def makale_detail_api_view(request, pk):
#     try:
#         makale_instance = Makale.objects.get(pk=pk)
#     except Makale.DoesNotExist:
#         return Response({
#             'error': {
#                 'code': 404,
#                 'message': 'Makale does not exist'
#             }
#         }, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = MakaleSerializer(makale_instance)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     elif request.method == 'PUT':
#         serializer = MakaleSerializer(makale_instance, data=request.data)
#         if serializer.is_valid():
#             serializer.update(makale_instance, request.data)
#             print(request.data, serializer.data)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#
#         return Response({
#             'error': {
#                 'code': 404,
#                 'message': f'{serializer.errors}'
#             }
#         }, status=status.HTTP_404_NOT_FOUND)
#     elif request.method == 'DELETE':
#         makale_instance.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
