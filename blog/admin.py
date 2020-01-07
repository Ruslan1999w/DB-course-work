from django.contrib import admin
from .models import Book, Users, Authors, UserCategory

admin.site.register(Book)
admin.site.register(Users)
admin.site.register(Authors)
admin.site.register(UserCategory)
