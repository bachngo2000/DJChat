from django.contrib import admin

from .models import Category, Channel, Server

# start to add some data to our tables

# register these models onto the Django admin site, so we can actually be able to administrate, add data, remove data, and so on from these tables
# directly from the admin site
admin.site.register(Channel)

admin.site.register(Server)

admin.site.register(Category)
