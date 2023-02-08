from os import name
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import User

User=get_user_model()

class UserSerializer(serializers.ModelSerializer):

    """  serializer for User model """
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','password','date_of_birth',
                  'phone_number','street','zipcode','city','state','country']
        read_only_fields = ["groups"]
        extra_kwargs={
            'password':{'write_only':True}
        }

class UpdateSerializer(serializers.ModelSerializer):
    """  serializer for User model """
    class Meta:
        model=User
        fields=['id','username','first_name','last_name','email','date_of_birth',
                  'phone_number','street','zipcode','city','state','country']

class TokenSerializer(serializers.ModelSerializer):
    """  serializer for Token model """

    user=serializers.SerializerMethodField('get_user')

    def get_user(self ,obj):
        """ customize fields for Login API """

        userdata=User.objects.filter(
            id=self.instance.user.id
        ).values ('id')

        return userdata

    class Meta:
        model=Token
        fields=['key','user']
