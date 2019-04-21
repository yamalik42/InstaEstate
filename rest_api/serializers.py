from rest_framework import serializers
from .models import Profile, Property, PropertyImage, Inquiry
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        p_word = validated_data.get('password')
        validated_data['password'] = make_password(p_word)
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        if 'password' in validated_data:
            instance.password = make_password(validated_data.get('password'))
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False    
    )

    class Meta:
        model = Profile
        fields = '__all__'


class PropertyImageSerializer(serializers.ModelSerializer):
    property = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Property.objects.all()
    )
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = PropertyImage
        exclude = ('id',)


class PropertySerializer(serializers.ModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(
        required=False,
        many=False,
        queryset=User.objects.all()
    )
    listing_date = serializers.DateField(
        format="%B %-d",
        required=False
    )

    class Meta:
        model = Property
        fields = '__all__'


class InquirySerializer(serializers.ModelSerializer):
    property = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Property.objects.all()
    )

    class Meta:
        model = Inquiry
        exclude = ('sent_date',)