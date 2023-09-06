from django.urls import path, include
# Importe le fichier views depuis le dossier courant
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profil/', views.profil, name='profil'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('api/delete-offer/<int:id>', views.delete_offer, name='delete_offer'),
    path('api/modify-status-offer/<int:id>', views.modify_status_offer, name='modify_status_offer'),
    path('api/delete-ask/<int:id>', views.delete_ask, name='delete_ask'),
    path('api/add-user', views.add_user, name='add_user'),
]