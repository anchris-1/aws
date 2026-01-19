from django.contrib.admin import AdminSite
from django.contrib import admin

class CustomAdminSite(AdminSite):
    site_header = "Portfolio Admin - Modern Dashboard"
    site_title = "Portfolio Admin"
    index_title = "Welcome to Portfolio Administration"
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

# Create an instance of the custom admin site
custom_admin_site = CustomAdminSite(name='custom_admin')

# Register default admin models
custom_admin_site.register(admin.models.LogEntry)