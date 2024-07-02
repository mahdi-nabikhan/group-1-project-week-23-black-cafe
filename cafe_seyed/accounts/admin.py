from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
# Register your models here.


class CustomUserAdmin(UserAdmin):
    # form = UserChangeForm
    # add_form = UserCreationForm
    model=CustomUser
    list_display=["email","is_superuser","is_staff","is_active",]
    list_filter=["email","is_superuser","is_staff","is_active",]
    
    fieldsets=((None,{"fields":("email","password",'age','city')}),
               ("Personal info", {"fields": ("first_name", "last_name")}),
               ("Persmissions",{'fields':("is_superuser","is_staff","is_active","groups","user_permissions")}),
               )
    
    add_fieldsets=((None,{"classes":("wide"),
                          "fields":("email","password1","password2","age","city","is_staff","is_active","groups","user_permissions")}),
                   )
    search_fields=["email"]
    ordering=["email"]


admin.site.register(CustomUser,CustomUserAdmin)