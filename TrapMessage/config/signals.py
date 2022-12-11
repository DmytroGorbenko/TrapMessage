from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver


@receiver(user_logged_out)
def clean_the_user_configs(sender, user, **kwargs):
    if not user.is_staff:
        for config in user.configs.all():
            user.configs.remove(config)