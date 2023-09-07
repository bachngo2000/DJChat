from rest_framework import serializers

from .models import Category, Channel, Server


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"


class ServerSerializer(serializers.ModelSerializer):
    # create new field
    # serializes the number of members data so we can return it to the frontend
    # SerializerMethodField allows you to include any custom methods to the serializer to generate a field value that is not derived from the model attributes
    # we're deriving a value from the utilizing annotate
    num_members = serializers.SerializerMethodField()

    channel_server = ChannelSerializer(many=True)

    category = serializers.StringRelatedField()

    class Meta:
        model = Server
        # fields = "__all__"
        # exclude the member field in the returned view, instead we'll use annotate to display the number of members in a server instead
        exclude = ("member",)

    # custom method to pass some data into the num_members field
    # tell Django that the num_members data in views.py is related to the  num_members field we created above and want to serialize
    # So when the data is serialized, Django will hit num_members and simply ask itself, well, what does this data return refer to?
    # Well, it's going to fire off the function get_num_members and then it's going to grab the num_members data from the queryset instance
    # and then replace this field with the num_members from the database if it exists. If it doesn't exist, it's just going to return none.
    def get_num_members(self, obj):
        if hasattr(obj, "num_members"):
            return obj.num_members
        return None

    # So it is possible for us to manipulate, change the serialized object or once the data has been serialized and we can do that through the function to_representation.
    # So this is going to provide us the option now of manipulating the data. So at this point, let's imagine we have requested data from the database. We've now serialized that data and now we're in a place where we can make some additional changes.
    # So what we're going to do here is if num_members doesn't have any values, we're simply just going to remove that field from being returned to the frontend.
    # So now we can use that context information in the serializer in views.py to finish off the to_representation. So what we're going to do here,
    # is if this data, if we have specified to return the number of members, then we're going to return that field. If we haven't specified that, then we're simply not going to return that field.
    # So here, first of all, we need to grab the data, the serialized data. So we're going to grab the num_members from context.
    def to_representation(self, instance):
        data = super().to_representation(instance)
        num_members = self.context.get("num_members")
        if not num_members:
            data.pop("num_members", None)
        return data
