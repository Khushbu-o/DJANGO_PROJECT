from django.urls import path
from ok_fashion import settings
from user import views
from django.conf.urls.static import static
from ok_fashion.settings import DEBUG,MEDIA_URL,MEDIA_ROOT

urlpatterns = [
    path('', views.index, name='index'),
    path('home/',views.home,name='home'),
    path('upload/', views.upload_clothes, name='upload-clothes'),
    path('home/update/<int:clothes_id>', views.update, name='update_book'),
    path('home/delete/<int:clothes_id>', views.delete, name='delete_book'),
    path('about/',views.about,name='about')
]

if DEBUG:
    urlpatterns += static(MEDIA_URL,document_root=MEDIA_ROOT)