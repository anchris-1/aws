from django.contrib import admin
from django.utils.html import format_html
from .models import Service, Project, PortfolioImage, Testimonial, SiteSetting, ContactSubmission, Technology

class ImageAdminMixin:
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Preview'

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'logo_preview', 'updated_at']
    readonly_fields = ['logo_preview_large', 'favicon_preview', 'hero_preview', 'contact_preview', 'admin_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_description')
        }),
        ('Logo & Favicon', {
            'fields': ('logo', 'favicon', 'logo_preview_large', 'favicon_preview')
        }),
        ('Background Images', {
            'fields': ('default_hero_image', 'contact_background', 'admin_background', 'hero_preview', 'contact_preview', 'admin_preview')
        }),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="30" height="30" style="object-fit: contain;" />', obj.logo.url)
        return "-"
    logo_preview.short_description = 'Logo'

    def logo_preview_large(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="200" style="border-radius: 10px; margin: 10px 0;" />', obj.logo.url)
        return "No logo uploaded"
    logo_preview_large.short_description = 'Logo Preview'

    def favicon_preview(self, obj):
        if obj.favicon:
            return format_html('<img src="{}" width="32" height="32" style="border-radius: 5px;" />', obj.favicon.url)
        return "No favicon uploaded"
    favicon_preview.short_description = 'Favicon Preview'

    def hero_preview(self, obj):
        if obj.default_hero_image:
            return format_html('<img src="{}" width="300" style="border-radius: 10px; margin: 10px 0;" />', obj.default_hero_image.url)
        return "No default hero image"
    hero_preview.short_description = 'Hero Image Preview'

    def contact_preview(self, obj):
        if obj.contact_background:
            return format_html('<img src="{}" width="300" style="border-radius: 10px; margin: 10px 0;" />', obj.contact_background.url)
        return "No contact background image"
    contact_preview.short_description = 'Contact Background Preview'

    def admin_preview(self, obj):
        if obj.admin_background:
            return format_html('<img src="{}" width="300" style="border-radius: 10px; margin: 10px 0;" />', obj.admin_background.url)
        return "No admin background image"
    admin_preview.short_description = 'Admin Background Preview'

    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'order', 'is_active', 'is_featured', 'image_preview', 'created_at']
    list_editable = ['order', 'is_active', 'is_featured']
    list_filter = ['is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['image_preview_large', 'background_preview']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'icon')
        }),
        ('Images', {
            'fields': ('featured_image', 'background_image', 'image_preview_large', 'background_preview')
        }),
        ('Pricing', {
            'fields': ('price', 'price_description')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active', 'is_featured')
        }),
    )

    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.featured_image.url)
        return "-"
    image_preview.short_description = 'Image'

    def image_preview_large(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="300" style="border-radius: 10px; margin: 10px 0;" />', obj.featured_image.url)
        return "No featured image uploaded"
    image_preview_large.short_description = 'Featured Image Preview'

    def background_preview(self, obj):
        if obj.background_image:
            return format_html('<img src="{}" width="300" style="border-radius: 10px; margin: 10px 0;" />', obj.background_image.url)
        return "No background image uploaded"
    background_preview.short_description = 'Background Image Preview'

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'client_name', 'completion_date', 'is_featured', 'order', 'image_preview']
    list_editable = ['order', 'is_featured']
    list_filter = ['is_featured', 'completion_date', 'services']
    search_fields = ['title', 'client_name', 'description']
    filter_horizontal = ['services', 'additional_images']
    date_hierarchy = 'completion_date'
    readonly_fields = ['image_preview_large', 'gallery_preview']
    fieldsets = (
        ('Project Details', {
            'fields': ('title', 'description', 'image')
        }),
        ('Additional Media', {
            'fields': ('additional_images', 'gallery_preview')
        }),
        ('Client Information', {
            'fields': ('client_name', 'project_url', 'github_url', 'completion_date')
        }),
        ('Categorization', {
            'fields': ('services', 'is_featured', 'order')
        }),
        ('Preview', {
            'fields': ('image_preview_large',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Main Image'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="300" style="border-radius: 10px; margin: 10px 0;" />', obj.image.url)
        return "No main image uploaded"
    image_preview_large.short_description = 'Main Image Preview'

    def gallery_preview(self, obj):
        images = obj.additional_images.all()[:4]
        if images:
            preview_html = '<div style="display: flex; gap: 10px; flex-wrap: wrap; margin: 10px 0;">'
            for image in images:
                preview_html += f'<img src="{image.image.url}" width="80" height="80" style="object-fit: cover; border-radius: 5px;" />'
            preview_html += '</div>'
            if obj.additional_images.count() > 4:
                preview_html += f'<p>+ {obj.additional_images.count() - 4} more images</p>'
            return format_html(preview_html)
        return "No additional images"
    gallery_preview.short_description = 'Gallery Preview'

@admin.register(PortfolioImage)
class PortfolioImageAdmin(admin.ModelAdmin, ImageAdminMixin):
    list_display = ['title', 'category', 'is_active', 'order', 'image_preview', 'created_at']
    list_editable = ['category', 'is_active', 'order']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['image_preview_large']
    fieldsets = (
        ('Image Information', {
            'fields': ('title', 'description', 'image', 'category')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Preview', {
            'fields': ('image_preview_large',)
        }),
    )

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="400" style="border-radius: 10px; margin: 10px 0; max-width: 100%;" />', obj.image.url)
        return "No image uploaded"
    image_preview_large.short_description = 'Large Preview'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'company', 'rating', 'is_featured', 'order', 'image_preview']
    list_editable = ['rating', 'is_featured', 'order']
    list_filter = ['is_featured', 'rating', 'created_at']
    search_fields = ['client_name', 'company', 'content']
    readonly_fields = ['image_preview_large']
    fieldsets = (
        ('Testimonial Content', {
            'fields': ('client_name', 'company', 'content', 'rating')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'order')
        }),
        ('Preview', {
            'fields': ('image_preview_large',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Client Photo'

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="150" style="object-fit: cover; border-radius: 50%; margin: 10px 0;" />', obj.image.url)
        return "No client photo uploaded"
    image_preview_large.short_description = 'Client Photo Preview'

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'submitted_at', 'read']
    list_filter = ['read', 'submitted_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'submitted_at']
    list_editable = ['read']
    
    def has_add_permission(self, request):
        return False

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'order', 'is_active']
    list_editable = ['category', 'proficiency', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name']
    ordering = ['category', 'order']

# Custom Admin Site Header
admin.site.site_header = "Portfolio Admin Panel"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to Portfolio Administration"