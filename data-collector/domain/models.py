from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from validator_collection import validators, checkers
import requests


class Domain(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    about = models.CharField(
        max_length=1000,
        help_text="Define what the domain is about"
    )
    category = models.ManyToManyField(
        'Category',
        help_text='Select one or more category for the domain.'
    )
    url = models.OneToOneField(
        'Url',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Enter domain url in the given format: \n\tif unsecured domain http://www.example.xyz or http://example.xyz, \n\tif secured domain https://www.example.xyz or https://example.xyz'
    )

    subdomains = models.ForeignKey(
        'Subdomain',
        null=True,
        on_delete=models.SET_NULL,
        help_text='Subdomains are created to organize and navigate to different sections of your website\n\thttp://www.example.xyz/home, http://www.example.xyz/home/gallery, http://www.example.xyz/home/gallery/amsterdam\nA subdomain is an additional part to your main domain name such as \n\thome, home/gallery, home/gallery/amsterda. \nOnly, input subdomain part without pre/post leading slash. If there are more than one subdomain, seperate them with comma such as home,home/gallery'
    )
    languages = models.ManyToManyField(
        'Language',
        help_text='Select one or more language for the domain.'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        null=True,
        blank=True,
        related_name='updated_domains',
        related_query_name='updated_domain'
    )

    updated_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_domains',
        related_query_name='created_domain'
    )

    created_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Domain"
        verbose_name_plural = "Domains"

    def __str__(self):
        return self.url.url


class Url(models.Model):
    url = models.CharField(
        max_length=200,
        help_text='Enter an url',
        unique=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        null=True,
        blank=True,
        related_name='updated_urls',
        related_query_name='updated_url'
    )

    updated_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_urls',
        related_query_name='created_url'
    )

    created_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Url"
        verbose_name_plural = "Urls"

    def clean(self):

        if checkers.is_url(self.url):
            try:
                response = requests.head(self.url, timeout=10)

                if response.status_code >= 400:
                    raise ValidationError("The url DOES NOT EXIST!")
            except:
                raise ValidationError("The url DOES NOT EXIST!")

        else:
            raise ValidationError("The URL SCHEME is not correct! Example: https://www.example.com")

    def __str__(self):
        return self.url


class Subdomain(models.Model):
    subdomain = models.CharField(
        max_length=200,
        help_text='Enter a subdomain here such as home, or home/gallery. If there is more than 1, separate them by comma.'
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        null=True,
        blank=True,
        related_name='updated_subdomains',
        related_query_name='updated_subdomain'
    )

    updated_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_subdomains',
        related_query_name='created_subdomain'
    )

    created_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Subdomain"
        verbose_name_plural = "Subdomains"

    def __str__(self):
        return self.subdomain

class Category(models.Model):
    category = models.CharField(max_length=200,
                                help_text='Enter a domain category')

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        null=True,
        blank=True,
        related_name='updated_categories',
        related_query_name='updated_category'
    )

    updated_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_categories',
        related_query_name='created_category'
    )

    created_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category


class Language(models.Model):
    language = models.CharField(max_length=200,
                                help_text='Enter a site language')

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        null=True,
        blank=True,
        related_name='updated_languages',
        related_query_name='updated_language'
    )

    updated_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_languages',
        related_query_name='created_language'
    )

    created_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"

    def __str__(self):
        return self.language

