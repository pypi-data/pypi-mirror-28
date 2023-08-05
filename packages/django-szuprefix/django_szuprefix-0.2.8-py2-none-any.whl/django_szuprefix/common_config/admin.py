from django.contrib import admin

from . import models
from django.contrib.contenttypes.admin import GenericTabularInline


class ImagesInline(GenericTabularInline):
    model = models.Image
    fields = ("file",)


class SettingInline(GenericTabularInline):
    model = models.Setting
    fields = ("name", "json_data",)
    extra = 0


class AttachmentInline(GenericTabularInline):
    model = models.Attachment
    fields = ("file",)
    extra = 0


# Register your models here.
class TrashAdmin(admin.ModelAdmin):
    list_display = ("content_type", "object_id", "create_time")
    readonly_fields = ("content_type", "object_id", "create_time", "json_data")

    def has_add_permission(self, request):
        return False


class SettingAdmin(admin.ModelAdmin):
    list_display = ("name", "content_type", "object_id")
    # readonly_fields = ("content_type", "object_id", "json_data")

    # def has_add_permission(self, request):
    #     return False


class ImageAdmin(admin.ModelAdmin):
    list_display = ("create_time", "owner", "create_time")
    readonly_fields = ("owner", "content_type")


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("create_time", "owner", "file", "create_time")
    readonly_fields = ("owner", "content_type")


class ExcelTaskAdmin(admin.ModelAdmin):
    list_display = ("create_time", "owner", "name", "status")
    readonly_fields = ("owner", "content_type")
    inlines = (AttachmentInline,)


admin.site.register(models.Image, ImageAdmin)
admin.site.register(models.Attachment, AttachmentAdmin)
admin.site.register(models.ExcelTask, ExcelTaskAdmin)

admin.site.register(models.Trash, TrashAdmin)
admin.site.register(models.Setting, SettingAdmin)
