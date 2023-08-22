from django.urls import include, path, re_path
from rest_framework import routers


from .views import BlockViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'titles', BlockViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Используем слаги в URL-путях
    re_path(r'^titles/(?P<id>\d+)/', include(router.urls)),
    re_path(r'^titles/(?P<id>\d+)/', include(router.urls)),
    
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]