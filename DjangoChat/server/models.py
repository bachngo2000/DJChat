from django.conf import settings
from django.db import models

# Create your models/tables here.

# Data that we need to store about a particular server


# model defines a Category (each model is a Python class)
# name and description are fields of the  Category model
# Each field is specified as a class attribute, and each attribute maps to a database column.
class Category(models.Model):
    name = models.CharField(max_length=100)
    # when the admin user adds a new role to the Category table, we don't have to supply a description, unlike name
    description = models.TextField(blank=True, null=True)

    # when we return objects from the Category table, we'll be able to easily identify that object by its name
    def __str__(self):
        return self.name


# model defines a Server (each model is a Python class)
# name and owner are fields of the Server model
# Each field is specified as a class attribute, and each attribute maps to a database column in the database table
class Server(models.Model):
    name = models.CharField(max_length=100)

    # owner is the user who built the server/channel
    # models.ForeignKey helps build a relationship from the owner field over to the user/account table that we created previously in the account class
    # If the user who built the server/channel is deleted, the owner field would then become blank, by using models.CASCADE, we're telling Django to delete the server that is
    # connected to the user
    # related_name helps make it easier for us to work with this relationaship when we're building queries
    # a server can only have 1 owner, but a user can be the owner of multiple servers
    # relationship: 1 to 1 connection from the server table to the user/account table
    # relationship: one to many connection from user/account table to server table, so we need a foreign key over to the user table
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner")

    # relationship between category and server models: each server belongs only to 1 category, while a category can have more than 1 servers => One to many
    # relationship between server and cateogry models: many to one
    # So the many side has this foreign key, so we need to build a foreign key from the server to the category (many to one) to associate categories to server
    # the category that a particular server belongs to
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="server_category")
    description = models.TextField(max_length=250, blank=True, null=True)
    # a server can have multiple members or users, and a user can be a member of multiple servers: many to many relationship between server and account/user tables
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner")
    topic = models.CharField(max_length=100)
    # a server can have multiple channels, but a channel can belong to one server
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="channel_server")

    # created a custom save method which allows us to modify the instance before it's saved to the database
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Channel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
