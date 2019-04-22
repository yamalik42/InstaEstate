from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_api.serializers import UserSerializer, ProfileSerializer
from rest_api.models import Property
import requests as Req
from InstaEstate.settings import SERVER_URL
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Check if buyer/seller can send/view enquiry(s)
def enq_auth(user, prop_pk):
    if prop_pk:
        prop = Property.objects.get(pk=prop_pk)

        if not user.profile.seller:
            if len(prop.inquiry_set.all().filter(buyer=user)):
                return False
            return True

        return prop.seller == user

    return user.profile.seller


# Check if request user is allowed to update/create properties
def prop_mod_auth(user, old_prop=False):
    if not user.is_anonymous and old_prop:
        return user == old_prop.seller
    elif not user.is_anonymous:
        return user.profile.seller

    return False


# Simple login authentication with redirection to detail page if all is well
def check_login_cred(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect(f'/user/detail/{user.pk}')
    else:
        request.session['login_fail'] = True
        return redirect(f'/login/')


# Very basic logout and redirect to home
def logout_view(request):
    logout(request)
    return redirect('/')


# Filter for property lists
def paginate_filter_props(params):
    if len(params):
        clean_dat = {k: v for k, v in params.items() if v != ''}
        props = Property.objects.filter(**clean_dat)
    else:
        props = Property.objects.all()
    
    return Paginator(props, 6)
    
    
