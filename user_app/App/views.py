from django.contrib.auth import  get_user_model
from django.contrib.auth.models import User
from rest_framework import viewsets
from .pagination import UserPagination
from rest_framework.response import Response
from .models import User
from .serializers import TokenSerializer
from dj_rest_auth.views import LoginView
from django.contrib.auth.hashers import make_password
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView
from .serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from django.db.models.signals import post_save
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from user_app import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from rest_framework.decorators import api_view
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """ User Create View  """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('username', 'email', 'id')
    search_fields = ('first_name', 'last_name')

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        else:
            return User.objects.none()

    def perform_create(self, serializer):
        # Hash password
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()


class UserListView(ListAPIView):
    """ User List View  """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('username', 'email', 'id')
    search_fields = ('first_name', 'last_name')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        elif self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        else:
            return User.objects.none()


class UserDetailView(RetrieveUpdateDestroyAPIView):
    """ User RetriveUpdateDetele View  """

    ueryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all ()
        elif self.request.user.is_authenticated:
            return User.objects.filter ( id=self.request.user.id )
        else:
            return User.objects.none ()

    def perform_create(self, serializer):
        # Hash password
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()


@receiver(post_save, sender=User)
def send_activation_mail(sender, instance, created, **kwargs):
    if created:
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        token = account_activation_token.make_token(instance)
        subject = "Account Verification link "
        message = 'Click on the below link\n\nhttp://127.0.0.1:8000/activate/' + str(uid) + '/' + str(token) + ''
        send_mail(subject,
                  message,
                  settings.EMAIL_HOST_USER,
                  [instance.email],
                  fail_silently=False, )


@api_view(('GET',))
def activate(request, uidb64, token):
    """ Activate User account API """

    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:

        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return Response('Thank you for your email confirmation. Now you can login your account.')
    else:
        return Response('Activation link is invalid!')


class CustomLoginAPI(LoginView):
    """ Custom Login API """

    def get_response(self):
        serializer_class = TokenSerializer
        serializer = serializer_class(instance=self.token)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenGenerator(PasswordResetTokenGenerator):
    """ Custom Reset Api """
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp) +
                    six.text_type(user.is_active))

account_activation_token = TokenGenerator()



