from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Server
from .serializer import ServerSerializer

# views are Python functions or classes that receive a web request and return a web response. The response can be a simple HTTP response, an HTML template response, or an HTTP redirect response that redirects a user to another page.
# Views hold the logic that is required to return information as a response in whatever form to the user. As a matter of best practice, the logic that deals with views is held in the views.py file in a Django app.

# Creating an API Endpoint for filtering servers by category. The endpoint will be able to take in a parameter, which is the category ID, and return a list of servers
# that are associated with that particular cateogory


# function-based views and class-based views
# utilizing viewsets, which is a class that provides CRUD operations that can be performed on a model using the API
# utilizing 1 endpoint and allows it to pass in multiple parameters in order to return different data/resources from this particular endpoint
class ServerListViewSet(viewsets.ViewSet):
    # represents a collection of all Server objects/data from the database
    queryset = Server.objects.all()

    # list function in the viewSets is used for get request to retrieve a list of instances or objects from the database
    def list(self, request):
        # capture the category id that is being passed into this endpoint from the get request that was sent
        category = request.query_params.get("category")
        # number of servers
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"

        # we're storing the category id/data if it exists
        if category:
            # filter by id
            # self.queryset = self.queryset.filter(category=category)
            # filter by name
            self.queryset = self.queryset.filter(category__name=category)
        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)
        if qty:
            # # items from the beginning through int(qty)-1
            self.queryset = self.queryset[: int(qty)]

        serializer = ServerSerializer(self.queryset, many=True)
        return Response(serializer.data)
