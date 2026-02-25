from django.contrib import admin
from .models import Book, Transaction
from .models import Membership

admin.site.register(Membership)
admin.site.register(Book)
admin.site.register(Transaction)
admin.site.site_header = "Library Management Admin"
admin.site.index_title = "Welcome to Library Dashboard"