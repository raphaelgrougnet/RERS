from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Importe le fichier views depuis le dossier courant
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profil, name='profil'),
    path('accounts/signup/', views.register, name='register'),
    path('add_offer/', views.add_offer, name='add_offer'),
    path('add_know/', views.add_know, name='add_know'),
    path('details/<int:id>', views.details_offer, name='details_offer'),
    path('api/add_ask/<int:id>', views.add_ask, name='add_ask'),
    path('api/delete_offer/<int:id>', views.delete_offer, name='delete_offer'),
    path('api/modify_status-offer/<int:id>', views.modify_status_offer, name='modify_status_offer'),
    path('api/delete_ask/<int:id>', views.delete_ask, name='delete_ask'),
    path('api/add_user', views.add_user, name='add_user'),
]
