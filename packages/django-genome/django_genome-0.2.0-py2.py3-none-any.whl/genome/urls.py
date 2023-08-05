# -*- coding: utf-8 -*-
from rest_framework import routers

from . import viewsets


router = routers.SimpleRouter()
router.register(r'genes', viewsets.GeneViewSet)
router.register(r'transcripts', viewsets.TranscriptViewSet)
router.register(r'exons', viewsets.ExonViewSet)

default_router = routers.DefaultRouter()
default_router.register(r'genes', viewsets.GeneViewSet)
default_router.register(r'transcripts', viewsets.TranscriptViewSet)
default_router.register(r'exons', viewsets.ExonViewSet)


urlpatterns = default_router.urls
