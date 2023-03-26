import secrets
import string
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from .models import ExpenseRequest






@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def token_generator_signal(sender, instance , created , **kwarg):
    if created:
        alphabet = string.ascii_letters + string.digits
        random_string = ''.join(secrets.choice(alphabet) for i in range(20))
        print(random_string)
        user_identifier = random_string+str(instance.id)
        instance.slug = user_identifier
        print(user_identifier)
        instance.save()




@receiver(post_save,sender=ExpenseRequest)
def token_generator_signal(sender, instance , created , **kwarg):
    if created:
        alphabet = string.ascii_letters + string.digits
        random_string = ''.join(secrets.choice(alphabet) for i in range(20))
        user_identifier = random_string+str(instance.id)
        instance.slug = user_identifier
        instance.save()