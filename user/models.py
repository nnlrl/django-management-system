import hashlib
from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import validators
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings

from .user_manger import CustomUserManager


@deconstructible
class StudentIdValidator(validators.RegexValidator):
    regex = r'^[0-9]{8,8}$'
    message = _(
        'Enter a valid student id. This value may contain eight digits.'
    )
    flags = 0


# Create your models here.
class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    studentid_validator = StudentIdValidator()
    userid = models.CharField(_("学号"), unique=True, primary_key=True,
                              max_length=8)
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'required': _("Please enter a valid username."),
        },
    )
    email = models.EmailField(_('email address'), unique=True)
    confirmed = models.BooleanField(_("Confirmed"), default=False)
    education = models.CharField(_("education"), default='', max_length=150)
    location = models.CharField(_("location"), default='', max_length=150)
    about_me = models.CharField(_("about me"), default='', max_length=150)

    USERNAME_FIELD = "userid"
    REQUIRED_FIELDS = ['username', 'email']

    objects = CustomUserManager()

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    # 生成确认信息的token
    def generate_confirm_token(self, expiration: Optional[int] = 3600):
        s = Serializer(settings.SECRET_KEY, expiration)
        return s.dumps({"confirm": self.userid}).decode("utf-8")

    # 确认注册
    def confirm_token(self, token: str):
        s = Serializer(settings.SECRET_KEY)
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False
        if data.get("confirm") != self.userid:
            return False
        self.confirmed = True
        return True

    def __str__(self):
        return self.username


