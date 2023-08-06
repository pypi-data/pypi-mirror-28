# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os
from unicodedata import normalize

import django

if django.VERSION >= (1, 10):
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible, force_text
from django.utils.translation import ugettext_lazy as _

import django_mobile_app_distribution.settings as app_dist_settings
from django_mobile_app_distribution.exceptions import MobileAppDistributionConfigurationException
from django_mobile_app_distribution.storage import CustomFileSystemStorage

if six.PY2:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin


log = logging.getLogger(__name__)


_MISSING_SITE_MESSAGE = "The site framework's domain name is used to generate the plist and binary links.  " \
                        "Please configure your current site properly. Also make sure that the SITE_ID in your " \
                        "settings file matches the primary key of your current site."

def normalize_filename(dirname, filename):
    dirname = force_text(dirname)
    filename = force_text(normalize('NFKD', filename).encode('ascii', 'ignore'))
    return force_text(os.path.join(dirname, filename))


def normalize_ios_filename(instance, filename):
    return normalize_filename(app_dist_settings.MOBILE_APP_DISTRIBUTION_IOS_UPLOAD_TO_DIRECTORY_NAME, filename)


def normalize_android_filename(instance, filename):
    return normalize_filename(app_dist_settings.MOBILE_APP_DISTRIBUTION_ANDROID_UPLOAD_TO_DIRECTORY_NAME, filename)

def normalize_image_filename(instance, filename):
    return normalize_filename(app_dist_settings.MOBILE_APP_DISTRIBUTION_APP_ICON_DIRECTORY_NAME, filename)


@python_2_unicode_compatible
class UserInfo(models.Model):
    user = models.OneToOneField(User, verbose_name=_('user'), on_delete=models.deletion.CASCADE)
    language = models.CharField(max_length=20, choices=app_dist_settings.LANGUAGES, default=app_dist_settings.ENGLISH, verbose_name=_('language'))

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Extended user info')
        verbose_name_plural = _('Extended user info')


@python_2_unicode_compatible
class App(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, default=None, related_name='apps', verbose_name=_('User'), on_delete=models.deletion.CASCADE)
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='apps',
        default=None,
        verbose_name=_('Groups')
    )
    name = models.CharField(max_length=200, verbose_name=_('App name'))
    comment = models.CharField(max_length=200, verbose_name=_('Comment'), blank=True, null=True)
    version = models.CharField(max_length=200, verbose_name=_('Bundle version'))
    updatedAt = models.DateTimeField(auto_now=True, editable=False, verbose_name=_('updated date'))
    createdAt = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('created date'))

    def __str__(self):
        return self.name


class IosApp(App):

    operating_system = models.CharField(
        max_length=50,
        choices=app_dist_settings.OS_CHOICES,
        default=app_dist_settings.IOS,
        verbose_name=_('Operating system'),
        editable=False
    )
    app_binary = models.FileField(upload_to=normalize_ios_filename, verbose_name=_('IPA file'))
    bundle_identifier = models.CharField(
        max_length=200,
        verbose_name=_('Bundle identifier'),
        default='',
        help_text=_('e.g. org.example.app')
    )
    display_image = models.ImageField(
        upload_to=normalize_image_filename,
        verbose_name=_('display image'),
        default='',
        help_text='57x57 PNG',
        blank=True
    )
    full_size_image = models.ImageField(
        upload_to=normalize_image_filename,
        verbose_name=_('full size image'),
        default='',
        help_text='512x512 PNG',
        blank=True
    )

    def get_binary_url(self):
        if not self.app_binary:
            return None
        Site.objects.clear_cache()
        try:
            Site.objects.get_current()
        except Exception:
            raise MobileAppDistributionConfigurationException(_MISSING_SITE_MESSAGE)

        return urljoin(Site.objects.get_current().domain, self.app_binary.url)

    def get_plist_url(self):
        Site.objects.clear_cache()
        current_site = None
        try:
            current_site = Site.objects.get_current()
        except Exception:
            raise MobileAppDistributionConfigurationException(_MISSING_SITE_MESSAGE)
        return urljoin(
            current_site.domain,
            reverse('django_mobile_app_distribution_ios_app_plist', kwargs={'app_id': self.pk})
        )

    def get_display_image_url(self):
        Site.objects.clear_cache()
        current_site = None
        try:
            current_site = Site.objects.get_current()
        except Exception:
            raise MobileAppDistributionConfigurationException(_MISSING_SITE_MESSAGE)

        return urljoin(Site.objects.get_current().domain, self.display_image.url)

    def get_full_size_image_url(self):
        Site.objects.clear_cache()
        current_site = None
        try:
            current_site = Site.objects.get_current()
        except Exception:
            raise MobileAppDistributionConfigurationException(_MISSING_SITE_MESSAGE)

        return urljoin(Site.objects.get_current().domain, self.full_size_image.url)

    class Meta:
        verbose_name = _('iOS App')
        verbose_name_plural = _('iOS Apps')
        ordering = ('name', 'operating_system', '-version', '-updatedAt',)


fs = CustomFileSystemStorage()


class AndroidApp(App):
    operating_system = models.CharField(
        max_length=50,
        choices=app_dist_settings.OS_CHOICES,
        default=app_dist_settings.ANDROID,
        verbose_name=_('Operating system'),
        editable=False
    )
    app_binary = models.FileField(upload_to=normalize_android_filename, verbose_name=_('APK file'), storage=fs)

    class Meta:
        verbose_name = _('Android App')
        verbose_name_plural = _('Android Apps')
        ordering = ( 'name', 'operating_system', '-version', '-updatedAt',)


def create_user_info(sender, instance, created, **kwargs):
    try:
        instance.userinfo
    except Exception:
        try:
            UserInfo.objects.create(user=instance)
        except Exception:
            # happens when creating a superuser when syncdb is run before the tables are installed
            pass

post_save.connect(create_user_info, sender=User)
