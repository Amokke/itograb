from django.conf.urls.static import static
from django.urls import path

from recepts.recepts import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('user/', views.user, name='user'),
    path('logout/', views.user_logout, name='logout'),
    path('cooker/', views.cooker, name='cooker'),
    path('recepe_add/', views.recipe_add, name='recepe_add'),
    path('recepe_edit/<int:recepe_id>', views.recepe_edit, name='recepe_edit'),
    path('recepe_detail/<int:recepe_id>', views.recepe_detail, name='recepe_detail'),
    path('recepe_delete/<int:recepe_id>', views.recepe_delete, name='recepe_delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.handler404

handler500 = views.handler500
