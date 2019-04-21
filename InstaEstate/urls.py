"""InstaEstate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from rest_api.views import (
    get_recent_props, create_user, update_user, create_update_property,
    create_enquiry
)
from controller.views import check_login_cred, logout_view
from render_forms.views import (
    UserProfileFormView, HomeView, LoginView, UserDetailView, 
    PropertyFormView, PropertyDetailView, EnquiryFormView, EnquiryList
)
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view()),
    path('login/', LoginView.as_view()),
    path('login/check/', check_login_cred),
    path('logout/', logout_view),
    path('user/', UserProfileFormView.as_view()),
    path('user/create/', create_user),
    path('user/update/<int:pk>/', UserProfileFormView.as_view()),
    path('user/detail/<int:pk>/', UserDetailView.as_view()),
    path('property/create/', PropertyFormView.as_view()),
    path('property/detail/<int:pk>/', PropertyDetailView.as_view()),
    path('property/update/<int:pk>/', PropertyFormView.as_view()),
    path('property/enquire/<int:pk>/', EnquiryFormView.as_view()),
    path('property/enquire/list/', EnquiryList.as_view()),
    path('property/enquire/list/<int:pk>/', EnquiryList.as_view()),
    path('api/property/create/', create_update_property),
    path('api/property/update/<int:pk>/', create_update_property),
    path('api/property/enquire/<int:pk>/', create_enquiry),
    path('api/user/update/', update_user),
    path('api/property/recent/', get_recent_props),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)