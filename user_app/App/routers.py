from rest_framework import routers
from App import views

router = routers.DefaultRouter()

router.register('User', views.UserViewSet,basename='user')