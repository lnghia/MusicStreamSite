from django.contrib.auth.models import AbstractUser
from django.db import models
from itsdangerous import Serializer, TimedJSONWebSignatureSerializer as TokenSerializer
from django.conf import settings


class User(AbstractUser):
    name = models.CharField(max_length=100)
    first_name = None
    last_name = None
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.email

    def generate_confirmation_token(self, expire=3600):
        serializer = TokenSerializer(settings.SECRET_KEY, expires_in=expire)
        return serializer.dumps({'id': self.id})

    def verify_confirmation_token(self, token):
        serializer = TokenSerializer(settings.SECRET_KEY)

        try:
            data = serializer.loads(token)
        except:
            return False

        if data.get('id') and data.get('id') == self.id:
            self.is_active = True
            self.save()

            return True

        return False
