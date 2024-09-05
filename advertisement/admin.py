from django.contrib import admin
from .models import Advertisement, Author, Response, Subscription
from django.contrib import admin


admin.site.register(Advertisement)
admin.site.register(Author)
admin.site.register(Response)
admin.site.register(Subscription)