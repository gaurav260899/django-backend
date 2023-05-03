# Django Import
from django.core import paginator
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import status

# Rest Framework Import
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import Serializer


# Local Import
from base.clients import clients
from base.models import *
from base.serializers import ClientSerializer

# Get all the clients with query


@api_view(['GET'])
def getClients(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    clients = Client.objects.filter(name__icontains=query).order_by('-_id')

    page = request.query_params.get('page')
    paginator = Paginator(clients, 8)

    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    if page == None:
        page = 1
    page = int(page)

    serializer = ClientSerializer(clients, many=True)
    return Response({'clients': serializer.data, 'page': page, 'pages': paginator.num_pages})

# Top Clients


# @api_view(['GET'])
# def getTopClients(request):
#     clients = Client.objects.filter(rating__gte=4).order_by('-rating')[0:5]
#     serializer = ClientSerializer(clients, many=True)
#     return Response(serializer.data)


# Get single client
@api_view(['GET'])
def getClient(request, pk):
    client = Client.objects.get(_id=pk)
    serializer = ClientSerializer(client, many=False)
    return Response(serializer.data)


# Create a new Clients
@api_view(['POST'])
@permission_classes([IsAdminUser])
def createClient(request):

    user = request.user
    client = Client.objects.create(
        user=user,
        name=" Client Name ",
        #category="Sample category",
        #description=" "
    )

    serializer = ClientSerializer(client, many=False)
    return Response(serializer.data)

# Update single clients


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateClient(request, pk):
    data = request.data
    client = Client.objects.get(_id=pk)

    client.name = data["name"]
    

    # client.category = data["category"]
    # client.description = data["description"]

    client.save()

    serializer = ClientSerializer(client, many=False)
    return Response(serializer.data)


# Delete a client
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteClient(request, pk):
    client = Client.objects.get(_id=pk)
    client.delete()
    return Response("Client deleted successfully")


# Upload Image of client
# @api_view(['POST'])
# def uploadImage(request):
#     data = request.data
#     client_id = data['client_id']
#     client = Client.objects.get(_id=client_id)
#     client.image = request.FILES.get('image')
#     client.save()
#     return Response("Image was uploaded")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createClientProject(request, pk):
    user = request.user
    client = Client.objects.get(_id=pk)
    data = request.data

    # 1 Project already Assigned
    alreadyExists = client.project_set.filter(user=user).exists()

    if alreadyExists:
        content = {'detail': 'Client already Assigned Project'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 2 
    elif data['project'] == 0:
        content = {'detail': 'Please Select a Project'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3 Create project
    else:
        project = Project.objects.create(
            user=user,
            client=client,
            name=user.first_name,
            # rating=data['rating'],
            # comment=data['comment'],
        )

        projects = client.project_set.all()
        client.numProjects = len(projects)

        total = 0

        for i in projects:
            total += i.rating
        client.rating = total / len(projects)
        client.save()

        return Response('Project Added')
