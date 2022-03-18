from django.conf.urls import include
from django.urls import path
from candlecommapi.views import register_user, login_user
from rest_framework import routers
from candlecommapi.views import ScentView
from candlecommapi.views import CandleView
from candlecommapi.views.jarcolor import JarColorView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'scents', ScentView, 'scent')
router.register(r'candles', CandleView, 'candle')
router.register(r'jarcolors', JarColorView, 'jar_color') 


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
