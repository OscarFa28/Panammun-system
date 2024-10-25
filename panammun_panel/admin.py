from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import Panammun_edition, Committee, Country, CustomUser

class PanammunEditionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_registration_date', 'start_choose_date', 'start_mun_date', 'notes', 'actual')
    search_fields = ('name',)

class CommitteeAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'panammun_edition', 'notes')
    search_fields = ('name', 'language')
    list_filter = ('panammun_edition',)

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'committee', 'notes')
    search_fields = ('name',)
    list_filter = ('committee',)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'phone_number_2', 'account_type', 'panammun_edition', 'committee_staff', 'country', 'verified', 'voucher')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('account_type', 'panammun_edition', 'committee_staff', 'country')

    def save_model(self, request, obj, form, change):
        if not change: 
            password = form.cleaned_data.get('password')
            if password:
                obj.set_password(password)
        obj.save()

# Register your models here
admin.site.register(Panammun_edition, PanammunEditionAdmin)
admin.site.register(Committee, CommitteeAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
