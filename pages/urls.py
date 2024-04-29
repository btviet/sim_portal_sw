from django.urls import path
from django.http import HttpResponse
from .views import HomePageView, SESCPageView, HESCPageView, RESCPageView, IESCPageView, \
GESCPageView, homepage_view,\
FlarealertPageView,eCallistoPageView, CactusPageView, dbem, \
ComeSEPPageView, SYMHPageView, kp, TestPageView, synoptic_view, \
solarwind, protonflux, solarmap, TECPageView, AEPageView, pcn, anemos


urlpatterns = [
    #path("", HomePageView.as_view(), name='home'),
    path("", homepage_view, name='home'),
    path('sesc/',SESCPageView.as_view(), name='sesc'),
    path('hesc/', HESCPageView.as_view(), name='hesc'),
    path('resc/', RESCPageView.as_view(), name='resc'),
    path('iesc/', IESCPageView.as_view(), name='iesc'),
    path('gesc/', GESCPageView.as_view(), name='gesc'),
    path('sesc/sidc_solarmap/', solarmap,name='solarmap'),
    path('sesc/flarealert/', FlarealertPageView.as_view(), name='flarealert'),
    path('sesc/ecallisto/', eCallistoPageView.as_view(), name='ecallisto'),
    path('sesc/cactus/', CactusPageView.as_view(), name='cactus'),
    path('sesc/synoptic/', synoptic_view, name='synoptic'),
    path('hesc/dbem/', dbem, name='dbem'),
    path('hesc/protonflux/', protonflux, name='protonflux'),
    path('hesc/solarwind/', solarwind, name='solarwind'),
    path('resc/anemos/', anemos, name='anemos'),
    path('resc/comesep/', ComeSEPPageView.as_view(), name='comesep'),
    path('gesc/symh/', SYMHPageView.as_view(), name='symh'),
    path('gesc/kp/', kp, name='kp'),
    path('gesc/pcn/', pcn, name='pcn'),
    path('gesc/ae/', AEPageView.as_view(), name='ae'),
    path('iesc/tec/', TECPageView.as_view(), name='tec'),
    path('test/', TestPageView.as_view(), name='test'),
]