from django.contrib import admin
from .models import Book, Users, Authors, UserCategory, Comment, BookAndAuthors

admin.site.register(Book)
admin.site.register(Users)
admin.site.register(Authors)
admin.site.register(UserCategory)
admin.site.register(Comment)
admin.site.register(BookAndAuthors)
