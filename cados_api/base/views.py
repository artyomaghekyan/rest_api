from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Advocate, Company
from .serializers import AdvocateSerializer, CompanySerializer
from django.db.models import Q 
from django.core import exceptions
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticated



# Create your views here.

@api_view(['GET'])
def endpoints(request):
    data = ['/advocates', 'advocates/:username']
    return Response(data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def advocates_list(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query == None:
            query = ''
        advocates = Advocate.objects.filter(Q(username__icontains=query) | Q(bio__icontains=query))
        serializer = AdvocateSerializer(advocates, many=True)
        return Response(serializer.data)

    if request.method == "POST":
       advocate = Advocate.objects.create(
            username=request.data['username'],
            bio=request.data['bio'])
       serializer = AdvocateSerializer(advocate, many=False)

       return Response(serializer.data)
             

class AdvocateDetail(APIView):

    def get_object(self, username):
        try:
            return Advocate.objects.get(username=username)
        except Advocate.DoesNotExist:
            raise Advocate
            
    def get(self, request, username):
        advocate = self.get_object(username)
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)
    
    def put(self, request, username):
        advocate = self.get_object(username)

        advocate.username = request.data['username']
        advocate.bio = request.data['bio']
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)
        
        

    def delete(self, request, username):
        advocate = self.get_object(username)
        serializer = AdvocateSerializer(advocate, many=False)
        advocate.delete()
        return Response("User was deleted")
        

# @api_view(['GET', 'PUT', 'DELETE'])
# def advocate_detail(request, username):
#     try:
#         advocate = self.get_object(username)
#     except Advocate.DoesNotExist:
#         raise Http404()

#     if request.method == 'GET':
#         serializer = AdvocateSerializer(advocate, many=False)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         advocate.username = request.data['username']
#         advocate.bio = request.data['bio']
#         advocate.save()
#         serializer = AdvocateSerializer(advocate, many=False)
#         return Response(serializer.data)

#     elif request.method == 'DELETE':
#         advocate.delete()
#         return Response("User was deleted")


@api_view(['GET'])
def companies_list(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)

