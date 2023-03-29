import secrets
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin ,BaseUserManager
# Create your models here.
import secrets
import string




class Department(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Role(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class UserManager(BaseUserManager):

    def create_user(self, first_name, last_name,email,password,**extra_fields):
        if not first_name:
            raise ValueError('Invalid first name')
        if not last_name:
            raise ValueError('Invalid last name')
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name , email=email , **extra_fields)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self,first_name, last_name,email,password, **extra_fields):

        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must be given is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must be given is_superuser=True')
        return self.create_user(first_name, last_name ,email,password,**extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL , null=True , blank=True , related_name='department')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL , null=True , blank=True , related_name='role')
    first_name = models.CharField(_('First Name of User'),blank = True, max_length = 20)
    last_name = models.CharField(_('Last Name of User'),blank = True, max_length = 20)
    slug = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(unique=True )
    is_email_verified = models.BooleanField(default=True)
    slug = models.CharField(max_length=100, null=True , blank=True )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    


    objects= UserManager()

    USERNAME_FIELD ="email"
    REQUIRED_FIELDS = ['first_name', 'last_name']


    # class Meta:
    #     permissions = (
	# 		("can_approve_expense", "To approve expense"),
	# 		("can_reject_expense", "To reject expense"), 
	# 		("can_disburse_expense", "To disburse expense"),
    #     )


    @property
    def is_head_of_department(self):
        return self.groups.filter(name="head_of_department")

    @property
    def is_requester(self):
        return self.groups.filter(name="requester")
    
    @property
    def is_cost_management(self):
        return self.groups.filter(name="cost_management")
    
    @property
    def is_line_executive(self):
        return self.groups.filter(name="line_executive")
    
    @property
    def is_md(self):
        return self.groups.filter(name="md")
    
    @classmethod
    def is_email_exist(cls, mail ):
        return cls.objects.filter(email=mail).exists()



    def __str__(self):
        return self.email 



        

class ExpenseRequest(models.Model):
    request_department = models.ForeignKey(Department, related_name='expense', on_delete=models.SET_NULL , null=True)
    request_user = models.ForeignKey(CustomUser, related_name='user_expense', on_delete=models.SET_NULL , null=True)
    title = models.CharField(max_length=200)
    description = models.TextField() 
    amount = models.IntegerField()
    is_hod = models.BooleanField(default=False)
    is_line_executive = models.BooleanField(default=False)
    is_cost_manager = models.BooleanField(default=False)
    is_md = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_disbursed = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    slug = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f'{self.request_department}  {self.amount} {self.request_user}'
    
    @property
    def add_commas(self):
        number_str = str(self.amount)
        digits = list(number_str)
        digits.reverse()
        digits_count = 0
        formatted_number = ''
        for digit in digits:
            if digits_count % 3 == 0 and digits_count != 0:
                formatted_number += ','
            formatted_number += digit
            digits_count += 1
        formatted_number = formatted_number[::-1]
        return formatted_number


    def reject(self):
        self.is_rejected = True
        return True 






class DepartmentUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE ) 
    department = models.ForeignKey(Department, on_delete=models.CASCADE ) 
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)