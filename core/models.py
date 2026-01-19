from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Leave empty for custom pricing"
    )
    price_description = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="e.g., 'Starting at', 'Per project', 'Monthly'"
    )
    icon = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="FontAwesome icon class like 'fas fa-code'"
    )
    featured_image = models.ImageField(
        upload_to='services/featured/',
        blank=True,
        null=True,
        help_text="Featured image for this service"
    )
    background_image = models.ImageField(
        upload_to='services/backgrounds/',
        blank=True,
        null=True,
        help_text="Background image for service detail page"
    )
    order = models.IntegerField(
        default=0,
        help_text="Order in which services appear (lower numbers first)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this service"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Feature this service on the homepage"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(
        upload_to='projects/',
        help_text="Upload a high-quality image of your project"
    )
    additional_images = models.ManyToManyField(
        'PortfolioImage',
        blank=True,
        related_name='project_galleries',
        help_text="Additional images for project gallery"
    )
    services = models.ManyToManyField(
        Service, 
        related_name='projects',
        help_text="Select services used in this project"
    )
    client_name = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Name of the client (optional)"
    )
    project_url = models.URLField(
        blank=True,
        help_text="Link to live project (optional)"
    )
    github_url = models.URLField(
        blank=True,
        help_text="Link to GitHub repository (optional)"
    )
    completion_date = models.DateField(
        null=True, 
        blank=True,
        help_text="When was this project completed?"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Feature this project on the homepage"
    )
    order = models.IntegerField(
        default=0,
        help_text="Order in which projects appear (lower numbers first)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

class PortfolioImage(models.Model):
    CATEGORY_CHOICES = [
        ('hero', 'Hero Section'),
        ('services', 'Services Section'),
        ('projects', 'Projects Section'),
        ('contact', 'Contact Section'),
        ('about', 'About Section'),
        ('background', 'Background Images'),
        ('pattern', 'Pattern Images'),
        ('icon', 'Icon Images'),
        ('testimonial', 'Testimonial Background'),
        ('cta', 'Call to Action Background'),
        ('general', 'General Images'),
    ]
    
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='portfolio/images/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'order', '-created_at']
        verbose_name = "Portfolio Image"
        verbose_name_plural = "Portfolio Images"

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

class Testimonial(models.Model):
    client_name = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    image = models.ImageField(
        upload_to='testimonials/',
        blank=True,
        null=True,
        help_text="Client photo (optional)"
    )
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        default=5
    )
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.client_name} - {self.company}"

class ContactSubmission(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, default="DevPortfolio")
    site_description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='site/logo/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/favicon/', blank=True, null=True)
    default_hero_image = models.ImageField(
        upload_to='site/hero/',
        blank=True,
        null=True,
        help_text="Default hero image when no portfolio images are available"
    )
    contact_background = models.ImageField(
        upload_to='site/contact/',
        blank=True,
        null=True,
        help_text="Background image for contact page"
    )
    admin_background = models.ImageField(
        upload_to='site/admin/',
        blank=True,
        null=True,
        help_text="Background image for admin panel"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSetting.objects.exists():
            # Update the existing instance
            existing = SiteSetting.objects.first()
            existing.site_name = self.site_name
            existing.site_description = self.site_description
            existing.logo = self.logo
            existing.favicon = self.favicon
            existing.default_hero_image = self.default_hero_image
            existing.contact_background = self.contact_background
            existing.admin_background = self.admin_background
            existing.save()
            return
        super().save(*args, **kwargs)

class Technology(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('tool', 'Tool'),
        ('mobile', 'Mobile'),
        ('cloud', 'Cloud'),
    ]
    
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, help_text="Font Awesome icon class")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='tool')
    proficiency = models.IntegerField(
        default=80,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Proficiency level from 0-100"
    )
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ['category', 'order', 'name']
    
    def __str__(self):
        return self.name