from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserViewSet, ParagraphViewSet, search

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'paragraphs', ParagraphViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search/<str:word>/', search, name='search'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
