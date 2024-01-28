from django.urls import path
from django.conf import settings
from .views import login, logout, sign_up


urlpatterns = [
    path('login', login, name='login'),
    path('logout/', logout, name='logout'),
    path('sign-up/', sign_up, name='sign-up')
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
