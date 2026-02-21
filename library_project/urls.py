from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from library_app import views

def root_redirect(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        else:
            return redirect('/home/')
    return redirect('/accounts/login/')

urlpatterns = [
    path('', root_redirect),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('library_app.urls')),  # 👈 IMPORTANT
    path('home/', views.home, name='home'),
]