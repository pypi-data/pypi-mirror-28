from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from models import Book, Appliances
from rest_framework.response import Response
from serializers import BookSerializer, AppliancesSerializer
from django.shortcuts import render_to_response


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


def index(request):
    return render_to_response("doc.html", context=None, content_type=None, status=None, using=None)


class AppliancesAPIError(Exception):
    pass


@api_view(['GET', 'POST', 'PUT'])
@csrf_exempt
def appliances(request, appliance_id=None):
    if request.method == 'GET':
        qd = request.GET
        appliances_details = Appliances.objects.all()
        appliances_serializer = AppliancesSerializer(appliances_details, many=True)
        return JsonResponse(appliances_serializer.data, safe=False)

    elif request.method == 'POST':

        appliances_serializer = AppliancesSerializer(data=request.data)
        if appliances_serializer.is_valid():
            appliances_serializer.save()
            return JsonResponse(appliances_serializer.data, status=201)
        return JsonResponse(appliances_serializer.errors, status=400)

    elif request.method == 'PUT':
        try:
            # print request.QuerySet
            if appliance_id:
                app_id = int(appliance_id)
                appliances_detail = Appliances.objects.get(id=app_id)
                for attribute, new_value in request.data.items():
                    print attribute, new_value
                    setattr(appliances_detail, attribute, new_value)
                    appliances_detail.save()

            appliances_details = Appliances.objects.all()
            appliances_serializer = AppliancesSerializer(appliances_details, many=True)
            return JsonResponse(appliances_serializer.data, safe=False)
        except AppliancesAPIError, err:
            return JsonResponse("{error: {}".format(str(err)), safe=False)


@api_view(['GET', 'POST'])
@csrf_exempt
def book_list(request, pk=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        print request.GET
        if pk:
            snippets = Book.objects.get(bookid=int(pk))
            serializer = BookSerializer(snippets)
            return Response(serializer.data)

        else:
            snippets = Book.objects.all()
            serializer = BookSerializer(snippets, many=True)
            return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        print request.POST

        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
