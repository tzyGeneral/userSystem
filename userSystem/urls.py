"""userSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from userSystem import views

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    url(r'^main/api/hello$', views.Hello.as_view()),
    url(r'^main/api/login', views.AuthView.as_view()),
    url(r'^main/api/checkToken', views.TokenCheckView.as_view()),

    url(r'^main/api/getPermissions', views.GetPermissionsView.as_view()),
    url(r'^main/api/permission', views.PermissionsView.as_view()),
    url(r'^main/api/role', views.RoleView.as_view()),
    url(r'^main/api/user', views.UserView.as_view())
]
