from django.db.models import Count
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, Server
from .schema import server_list_docs
from .serializer import CategorySerializer, ServerSerializer

# views are Python functions or classes that receive a web request and return a web response. The response can be a simple HTTP response, an HTML template response, or an HTTP redirect response that redirects a user to another page.
# Views hold the logic that is required to return information as a response in whatever form to the user. As a matter of best practice, the logic that deals with views is held in the views.py file in a Django app.


class CategoryListViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


# Creating an API Endpoint for filtering servers by category. The endpoint will be able to take in a parameter, which is the category ID, and return a list of servers
# that are associated with that particular cateogory


# function-based views and class-based views
# utilizing viewsets, which is a class that provides CRUD operations that can be performed on a model using the API
# utilizing 1 endpoint and allows it to pass in multiple parameters in order to return different data/resources from this particular endpoint
class ServerListViewSet(viewsets.ViewSet):
    # represents a collection of all Server objects/data from the database
    queryset = Server.objects.all()
    # permission_classes = [IsAuthenticated]

    # list function in the viewSets is used for get request to retrieve a list of instances or objects from the database
    @server_list_docs
    def list(self, request):
        """Returns a list of servers filtered by various parameters.

        This method retrieves a queryset of servers based on the query parameters
        provided in the `request` object. The following query parameters are supported:

        - `category`: Filters servers by category name.
        - `qty`: Limits the number of servers returned.
        - `by_user`: Filters servers by user ID, only returning servers that the user is a member of.
        - `by_serverid`: Filters servers by server ID.
        - `with_num_members`: Annotates each server with the number of members it has.

        Args:
        request: A Django Request object containing query parameters.

        Returns:
        A queryset of servers filtered by the specified parameters.

        Raises:
        AuthenticationFailed: If the query includes the 'by_user' or 'by_serverid'
            parameters and the user is not authenticated.
        ValidationError: If there is an error parsing or validating the query parameters.
            This can occur if the `by_serverid` parameter is not a valid integer, or if the
            server with the specified ID does not exist.

        Examples:
        To retrieve all servers in the 'gaming' category with at least 5 members, you can make
        the following request:

            GET /servers/?category=gaming&with_num_members=true&num_members__gte=5

        To retrieve the first 10 servers that the authenticated user is a member of, you can make
        the following request:

            GET /servers/?by_user=true&qty=10

        """
        # capture the category id that is being passed into this endpoint from the get request that was sent
        category = request.query_params.get("category")
        # capture number of servers
        qty = request.query_params.get("qty")
        # a boolean
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        # a boolean
        with_num_members = request.query_params.get("with_num_members") == "true"

        # we may want to pre check whether the user is actually logged in or not before we allow the user to access some of the different end points here
        # So if the by user if the user ID is sent as a parameter to this endpoint and the user is not logged in, then we're going to tell them that the authentication is failed. You have to be authenticated to actually utilize that particular filter.
        # Now we can extend that and say, well, if in actual fact, if the by_user or the by_server ID parameter is sent across in the request, then the user has to be logged in. If they're not, then they are going to be provided the authentication failed response.
        # if by_user or by_serverid and not request.user.is_authenticated:
        # raise AuthenticationFailed()

        # we're storing the category id/data if it exists
        if category:
            # filter by id
            # self.queryset = self.queryset.filter(category=category)
            # filter by name
            self.queryset = self.queryset.filter(category__name=category)
        if by_user:
            if by_user and request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed()
        # annotation is a feature that allows you to add calculated fields to a queryset and to perform complex calculations on queryset data
        # whenever we select a particular server, we also want to include data related to how many members are in that server
        # here, we use annotation to add additional data to our server model/data that is returned back to the frontend
        if with_num_members:
            # num_members is a new field that we're going to create and include in our queryset
            self.queryset = self.queryset.annotate(num_members=Count("member"))
        if qty:
            # items from the beginning through int(qty)-1
            self.queryset = self.queryset[: int(qty)]
        if by_serverid:
            # if not request.user.is_authenticated:
            #     raise AuthenticationFailed()
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"Server with id {by_serverid} not found")
            except ValueError:
                raise ValidationError(detail=f"Server value error")

        # So what we're going to do here is we're going to utilize this boolean true with_num_members that we're going to pass in and we're going to pass that into the serializer.
        # So we're going to pass in the fact that we are trying to utilize this filter into the serializer. So we're going to pass that in as context. So in the serializer here, what we're going to do is we're going to add that in. So we're simply just going to specify context equals and I'm going to call that num. Members. And so there's key value situation going on here. So that needs to be that's the key. And then the value is going to be with Num members. So that's what we're passing in remembering the filter. So that's true. Or if we don't add that into our filter, that parameter false. So we're going to pass that in and we're going to use this information, reference this and use this information to decide whether to include the field in the return data, Right? So we're going to pass that into our serializer.
        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_members})
        return Response(serializer.data)
