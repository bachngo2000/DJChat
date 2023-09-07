from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .validators import validate_icon_image_size, validate_image_file_exstension


def server_icon_upload_path(instance, filename):
    return f"server/{instance.id}/server_icons/{filename}"


def server_banner_upload_path(instance, filename):
    return f"server/{instance.id}/server_banner/{filename}"


# method to specify where the files are stored
def category_icon_upload_path(instance, filename):
    # return the actual location of where we're going to store this image
    return f"category/{instance.id}/category_icon/{filename}"


# Create your models/tables here.

# Data that we need to store about a particular server


# model defines a Category (each model is a Python class)
# name and description are fields of the  Category model
# Each field is specified as a class attribute, and each attribute maps to a database column.
class Category(models.Model):
    name = models.CharField(max_length=100)
    # when the admin user adds a new role to the Category table, we don't have to supply a description, unlike name
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(upload_to=category_icon_upload_path, null=True, blank=True)

    # method that allows us to, if we upload a new image, delete the old one
    # save the new image, whenever we save smth in this model, this method will be initiated
    def save(self, *args, **kwargs):
        # check to see if this is a new category or we're just updating an existing category
        # if the data does have an id, it means that the category that we're trying to save information about already exists
        if self.id:
            # initiate a query on the category table and grab the data related to the category we're trying to update
            # get_object_or_404 - shortcut to create a query that's going to return one object or else a 404
            existing = get_object_or_404(Category, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
        self.name = self.name.lower()
        super(Category, self).save(*args, **kwargs)

    # Django signals - when an event takes place in the model here, we can capture the fact that that event has taken place, and we can then go ahead and
    # perform additional tasks
    # delete is an event, and we're looking out for it
    @receiver(models.signals.pre_delete, sender="server.Category")
    # if we delete a category, we also delete the image icon
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

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

    banner = models.ImageField(
        upload_to=server_banner_upload_path,
        null=True,
        blank=True,
        validators=[validate_image_file_exstension],
    )
    icon = models.ImageField(
        upload_to=server_icon_upload_path,
        null=True,
        blank=True,
        validators=[validate_icon_image_size, validate_image_file_exstension],
    )

    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(Server, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
            if existing.banner != self.banner:
                existing.banner.delete(save=False)
        super(Server, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Server")
    def server_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon" or field.name == "banner":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self):
        return f"{self.name}-{self.id}"


class Channel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner")
    topic = models.CharField(max_length=100)
    # a server can have multiple channels, but a channel can belong to one server
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="channel_server")

    def __str__(self):
        return self.name
