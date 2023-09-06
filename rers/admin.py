from django.contrib import admin
from .models import Offre, Echange, Savoir, User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class OffreAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_user', 'id_savoir')

class EchangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'demande_by', 'id_offre', 'date', 'status')

class SavoirAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'description')

    

admin.site.register(Offre, OffreAdmin)
admin.site.register(Echange, EchangeAdmin)
admin.site.register(Savoir, SavoirAdmin)
admin.site.register(User, UserAdmin)