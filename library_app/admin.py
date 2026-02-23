from django.contrib import admin
from .models import Book, Transaction

admin.site.register(Book)
admin.site.register(Transaction)
admin.site.site_header = "Library Management Admin"
admin.site.index_title = "Welcome to Library Dashboard"