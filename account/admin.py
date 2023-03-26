from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser , Department , ExpenseRequest , Role ,  DepartmentUser
# Register your models here.

class CustomModelAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email' , 'department'] 
    
class ExpenseRequestModelAdmin(admin.ModelAdmin):
    list_display = ['request_department', 'request_user', 'amount', 'is_completed']



class UserAdmin(UserAdmin):
    ordering= ('-date_joined',)
    list_filter = ['first_name','email']
    list_display = ['first_name','email','is_active','is_staff']
    search_fields =  ('first_name', 'last_name','email')
    fieldsets = (
        (None, { 'fields': ('first_name', 'last_name','email', 'role', 'department')}),  
        ('Permissions',{'fields':('is_staff','is_active','is_superuser','groups',"user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),}),)
    

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Department)
admin.site.register(DepartmentUser)
admin.site.register(Role) 
admin.site.register(ExpenseRequest, ExpenseRequestModelAdmin)