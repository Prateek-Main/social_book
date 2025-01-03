from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from .models import CustomUser, UploadedFiles
from django.utils.html import format_html

class UploadedFilesInline(admin.TabularInline):
    model = UploadedFiles
    extra = 1
    fields = ('title', 'file', 'description', 'cost', 'published_year', 'visibility')
    readonly_fields = ('file',)

    # You can limit the number of displayed files (for example, show only the first one)
    def has_add_permission(self, request, obj):
        return False  # Disable adding new files directly from here

    def has_change_permission(self, request, obj):
        return False  # Disable editing files directly from here


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # Add the UploadedFiles inline to the user view
    inlines = [UploadedFilesInline]

    # Update list_display to show uploaded file details (you can adjust as needed)
    list_display = ("email", "is_staff", "is_active", "public_visibility", "birth_year", "age", "address", "uploaded_files")
    
    # Adding method to display uploaded files
    def uploaded_files(self, obj):
        files = UploadedFiles.objects.filter(user=obj)
        return format_html('<br>'.join([f'<a href="{file.file.url}" target="_blank">{file.title}</a>' for file in files]))

    list_filter = ("email", "is_staff", "is_active", "public_visibility")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("public_visibility", "birth_year", "address")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active", "public_visibility", "birth_year", "address", "groups", "user_permissions"),
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UploadedFiles)
