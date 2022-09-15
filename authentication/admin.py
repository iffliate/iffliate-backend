from django.contrib import admin
from .models import User, Shop
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms

class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields = '__all__'
        
    def clean_password(self):
        return self.initial["password"]

class MyUserAdmin(admin.ModelAdmin):
    form = UserAdminChangeForm
    ordering = ["email"]
    list_display = ["email", "first_name", "last_name", "is_active"]
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields':('email', 'password',)}),
        ('About', {'fields':('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields':('is_active', 'is_superuser', 'is_admin', 'is_staff',)}),
    )
    
admin.site.register(User, MyUserAdmin)

class ShopAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
admin.site.register(Shop, ShopAdmin)
