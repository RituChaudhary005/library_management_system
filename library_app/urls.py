from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from library_app import views
from . import views


def root_redirect(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        else:
            return redirect('home')
    return redirect('/accounts/login/')   # 👈 yaha change

urlpatterns = [
    path('', root_redirect),
    path('accounts/', include('django.contrib.auth.urls')),  # 👈 VERY IMPORTANT
    path('home/', views.home, name='home'),
     path('books/', views.book_list, name='book_list'),
    path('transactions/', views.transactions, name='transactions'),
    path('issue/<int:id>/', views.issue_book, name='issue_book'),
    path('return/<int:id>/', views.return_book, name='return_book'),
    path('signup/', views.signup, name='signup'),
    
    
]