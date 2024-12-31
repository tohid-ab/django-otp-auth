from django.urls import path, include

from .auth.urls import urlpatterns as auth_urls


urlpatterns = [
    path('auth/', include(auth_urls)),
]