from django.contrib import admin
from .models import Domain, Url, Category, Subdomain, Language
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError

import re


class DomainsListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('creator of the domain')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'created_by    '

    def lookups(self, request, model_admin):
        return (
            ('my_domains', _('My')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'my_domains':
            return queryset.filter(created_by=request.user)


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['url', "created_by", "created_at"]
    list_filter = (DomainsListFilter, )
    search_fields = ["url__url"]
    ordering = ['url__url']
    exclude = ('updated_by', 'updated_at', 'created_by', 'created_at')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.created_at = timezone.now()
        else:
            if not obj.created_by == request.user:
                raise ValidationError("Selected domain does not belong to you!")

        obj.updated_by = request.user
        obj.updated_at = timezone.now()

        super().save_model(request, obj, form, change)


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ['url', "created_by"]
    search_fields = ["url"]
    ordering = ['url']
    exclude = ('updated_by', 'updated_at', 'created_by', 'created_at')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Url.objects.all()
        return Url.objects.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.created_at = timezone.now()

            if re.search(r"www\.", obj.url):

                http, domain = re.search(r"(http[s]?)://www\.(.*\..*)", obj.url).groups()
                Url.objects.create(url=http + "://" + domain, created_by=obj.created_by, created_at=obj.created_at,
                                   updated_by=obj.updated_by, updated_at=obj.updated_at)

            else:
                http, domain = re.search(r"(http[s]?)://(.*\..*)", obj.url).groups()

                Url.objects.create(url=http + "://www." + domain, created_by=obj.created_by, created_at=obj.created_at,
                                   updated_by=obj.updated_by, updated_at=obj.updated_at)
        else:
            if not obj.created_by == request.user and not request.user.is_superuser:
                raise ValidationError("Selected domain does not belong to you!")

            pre_obj = Url.objects.filter(pk=obj.pk).first()

            if re.search(r"www\.", obj.url):
                pre_http, pre_domain = re.search(r"(http[s]?)://www\.(.*\..*)", pre_obj.url).groups()
                http, domain = re.search(r"(http[s]?)://www\.(.*\..*)", obj.url).groups()
            else:
                pre_http, pre_domain = re.search(r"(http[s]?)://(.*\..*)", pre_obj.url).groups()
                http, domain = re.search(r"(http[s]?)://(.*\..*)", obj.url).groups()

            Url.objects.filter(url__exact=pre_http + "://" + pre_domain)\
                .update(url=http + "://" + domain, updated_by=obj.updated_by, updated_at=obj.updated_at)
            Url.objects.filter(url__exact=pre_http + "://www." + pre_domain)\
                .update(url=http + "://www." + domain, updated_by=obj.updated_by, updated_at=obj.updated_at)

        obj.updated_by = request.user
        obj.updated_at = timezone.now()

        super().save_model(request, obj, form, change)


@admin.register(Subdomain)
class SubdomainAdmin(admin.ModelAdmin):
    list_display = ['id', 'subdomain']
    exclude = ('updated_by', 'updated_at', 'created_by', 'created_at')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.created_at = timezone.now()
        obj.updated_by = request.user
        obj.updated_at = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category']
    exclude = ('updated_by', 'updated_at', 'created_by', 'created_at')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.created_at = timezone.now()
        obj.updated_by = request.user
        obj.updated_at = timezone.now()
        super().save_model(request, obj, form, change)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['id', 'language']
    exclude = ('updated_by', 'updated_at', 'created_by', 'created_at')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.created_at = timezone.now()
        obj.updated_by = request.user
        obj.updated_at = timezone.now()
        super().save_model(request, obj, form, change)
