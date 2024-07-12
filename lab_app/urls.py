from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'lab_app'

urlpatterns = [
    path('',views.home_page_view,name='home_page_view'),
    path('banner-image-upload/', views.upload_banner_image, name='banner_image_upload'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_category/', views.add_category, name='add_category'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)