from rest_framework import generics
from .models import (
    Profile, Property, PropertyImage, Inquiry
)
from django.contrib.auth.models import User
from .serializers import (
    ProfileSerializer, UserSerializer, PropertySerializer, 
    PropertyImageSerializer, InquirySerializer
)
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import login
from django.core.mail import send_mail


def create_user(request):
    if request.method == 'POST':
        user_serial = UserSerializer(data=request.POST)
        prof_serial = ProfileSerializer(data=request.POST)

        if user_serial.is_valid() and prof_serial.is_valid():
            new_user = user_serial.save()

            prof_kwargs = {'user': new_user}
            if len(request.FILES):
                prof_kwargs['image'] = request.FILES['image']
            new_prof = prof_serial.save(**prof_kwargs)

            login(request, new_user)
            return redirect(f'/user/detail/{new_user.pk}/')

    return HttpResponse('bad request')


def update_user(request):
    if request.method == 'POST':
        clean_dat = {k: v for k, v in request.POST.items() if v != ''}

        if len(request.FILES):
            clean_dat['image'] = request.FILES['image']

        profile = request.user.profile

        user_serial = UserSerializer(request.user, data=clean_dat, partial=1)
        prof_serial = ProfileSerializer(profile, data=clean_dat, partial=1)

        if user_serial.is_valid() and prof_serial.is_valid():
            user = user_serial.save()
            prof_serial.save()

        return redirect(f'/user/detail/{user.pk}/')
    
    return redirect('/')


# FBView to get 3 most recent properties for home page display
def get_recent_props(request):
    recent_props = Property.objects.all()[::-1][:3]
    prop_serials = list()
    
    for prop in recent_props:
        img_url = {'img_url': prop.propertyimage_set.first().image.url}
        prop_serials.append({**PropertySerializer(prop).data, **img_url})

    return JsonResponse({'props': prop_serials})
    

def save_prop_imgs(images, serial, prop_pk):
    img_list = dict(images).get('image', [])
    img_objs = [{'property': prop_pk, 'image': img} for img in img_list]
    img_serials = [serial(data=img_data) for img_data in img_objs]

    for serial in img_serials:
        if serial.is_valid():
            serial.save()


def create_update_property(request, pk=False):
    if request.method == 'POST':
        if not pk:
            prop_serial = PropertySerializer(data=request.POST)
            if prop_serial.is_valid():
                pk = prop_serial.save(seller=request.user).pk
                save_prop_imgs(request.FILES, PropertyImageSerializer, pk)

                return redirect(f'/property/detail/{pk}/')

        clean_dat = {k: v for k, v in request.POST.items() if v != ''}

        try:
            prop = Property.objects.get(pk=pk)
            prop_serial = PropertySerializer(prop, data=clean_dat, partial=1)

            if prop_serial.is_valid():
                prop_serial.save()
                save_prop_imgs(request.FILES, PropertyImageSerializer, pk)
                return redirect(f'/property/detail/{pk}/')

        except Property.DoesNotExist:
            return redirect('/')

    return redirect('/')


def create_enquiry(request, pk=False):
    if request.method == 'POST' and pk:
        comment = request.POST['comment']
        data = {'comment': comment, 'property': pk, 'buyer': request.user.pk}
        enq_serial = InquirySerializer(data=data)

        if enq_serial.is_valid():
            enquiry = enq_serial.validated_data
            # add prop link with cred hash if free
            mssg = (f"{enquiry['buyer'].username} has made an enquiry on your"
                    f" property (Property No. {enquiry['property'].pk}).\n"
                    f"They commented:\n{enquiry['comment']}")
            enq_serial.save()
            send_mail(
                f'New Inquiry',
                mssg,
                'yash.malik@tothenew.com',
                [enquiry['property'].seller.profile.email],
                fail_silently=False,
            )

            return redirect(f'/property/detail/{pk}/')

    return redirect('/')


def list_enquiry(request):
    pass
        

