from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Service, Project, PortfolioImage, Testimonial, SiteSetting, ContactSubmission, Technology

def get_site_settings():
    """Get site settings or create default ones"""
    try:
        return SiteSetting.objects.first() or SiteSetting.objects.create(
            site_name="DevPortfolio",
            site_description="Professional Web Development Services"
        )
    except:
        return SiteSetting.objects.create(
            site_name="DevPortfolio",
            site_description="Professional Web Development Services"
        )

def home(request):
    """Homepage view with featured services and projects"""
    site_settings = get_site_settings()
    featured_services = Service.objects.filter(is_active=True, is_featured=True)[:6]
    featured_projects = Project.objects.filter(is_featured=True)[:6]
    
    # Technology stack for icons
    tech_stack = Technology.objects.filter(is_active=True).order_by('category', 'order')[:12]
    
    # Get background images for sections
    hero_bg = PortfolioImage.objects.filter(category='hero', is_active=True).first()
    services_bg = PortfolioImage.objects.filter(category='services', is_active=True).first()
    tech_bg = PortfolioImage.objects.filter(category='background', is_active=True).first()
    projects_bg = PortfolioImage.objects.filter(category='projects', is_active=True).first()
    testimonials_bg = PortfolioImage.objects.filter(category='testimonial', is_active=True).first()
    cta_bg = PortfolioImage.objects.filter(category='cta', is_active=True).first()
    
    featured_testimonials = Testimonial.objects.filter(is_featured=True)[:4]
    
    context = {
        'site_settings': site_settings,
        'featured_services': featured_services,
        'featured_projects': featured_projects,
        'tech_stack': tech_stack,
        'hero_bg': hero_bg,
        'services_bg': services_bg,
        'tech_bg': tech_bg,
        'projects_bg': projects_bg,
        'testimonials_bg': testimonials_bg,
        'cta_bg': cta_bg,
        'featured_testimonials': featured_testimonials,
    }
    return render(request, 'home.html', context)

def services(request):
    """Services page view with all active services"""
    site_settings = get_site_settings()
    services = Service.objects.filter(is_active=True).order_by('order')
    
    # Get service-related images
    service_bg_images = PortfolioImage.objects.filter(category='services', is_active=True).order_by('order')[:10]
    service_icons = PortfolioImage.objects.filter(category='icon', is_active=True).order_by('order')[:12]
    pattern_images = PortfolioImage.objects.filter(category='pattern', is_active=True).order_by('order')[:4]
    
    # Technology stack
    tech_stack = Technology.objects.filter(is_active=True).order_by('category', 'order')
    
    context = {
        'site_settings': site_settings,
        'services': services,
        'service_bg_images': service_bg_images,
        'service_icons': service_icons,
        'pattern_images': pattern_images,
        'tech_stack': tech_stack,
    }
    return render(request, 'services.html', context)

def service_detail(request, service_id):
    """Service detail page"""
    site_settings = get_site_settings()
    service = get_object_or_404(Service, id=service_id, is_active=True)
    related_projects = Project.objects.filter(services=service)[:4]
    
    context = {
        'site_settings': site_settings,
        'service': service,
        'related_projects': related_projects,
    }
    return render(request, 'service_detail.html', context)

def projects(request):
    """Projects page view with all projects"""
    site_settings = get_site_settings()
    projects = Project.objects.all().order_by('order', '-completion_date')
    
    # Get project-related images
    project_bg_images = PortfolioImage.objects.filter(category='projects', is_active=True).order_by('order')[:8]
    gallery_images = PortfolioImage.objects.filter(category='general', is_active=True).order_by('order')[:12]
    pattern_images = PortfolioImage.objects.filter(category='pattern', is_active=True).order_by('order')[:3]
    
    # Get all services for filtering
    services = Service.objects.filter(is_active=True)
    
    context = {
        'site_settings': site_settings,
        'projects': projects,
        'project_bg_images': project_bg_images,
        'gallery_images': gallery_images,
        'pattern_images': pattern_images,
        'services': services,
    }
    return render(request, 'projects.html', context)

def project_detail(request, project_id):
    """Project detail page"""
    site_settings = get_site_settings()
    project = get_object_or_404(Project, id=project_id)
    related_projects = Project.objects.filter(services__in=project.services.all()).exclude(id=project.id).distinct()[:3]
    
    context = {
        'site_settings': site_settings,
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'project_detail.html', context)

def contact(request):
    """Contact page view"""
    site_settings = get_site_settings()
    
    # Get contact-related images
    contact_images = PortfolioImage.objects.filter(category='contact', is_active=True).order_by('order')[:6]
    pattern_images = PortfolioImage.objects.filter(category='pattern', is_active=True).order_by('order')[:2]
    general_images = PortfolioImage.objects.filter(category='general', is_active=True).order_by('order')[:4]
    
    if request.method == 'POST':
        # Process contact form
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save to database
        ContactSubmission.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Send email (configure email settings in production)
        try:
            send_mail(
                f'Portfolio Contact: {subject}',
                f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
                email,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            # Log error but don't show to user
            print(f"Email sending failed: {e}")
        
        messages.success(request, f"Thank you {name}! Your message has been sent. We'll get back to you soon.")
        return redirect('contact')
    
    context = {
        'site_settings': site_settings,
        'contact_images': contact_images,
        'pattern_images': pattern_images,
        'general_images': general_images,
    }
    return render(request, 'contact.html', context)

def about(request):
    """About page view"""
    site_settings = get_site_settings()
    
    # Get statistics
    total_projects = Project.objects.count()
    total_services = Service.objects.filter(is_active=True).count()
    total_clients = Testimonial.objects.count()
    
    # Technology stack by category
    frontend_tech = Technology.objects.filter(category='frontend', is_active=True)
    backend_tech = Technology.objects.filter(category='backend', is_active=True)
    database_tech = Technology.objects.filter(category='database', is_active=True)
    mobile_tech = Technology.objects.filter(category='mobile', is_active=True)
    cloud_tech = Technology.objects.filter(category='cloud', is_active=True)
    
    context = {
        'site_settings': site_settings,
        'total_projects': total_projects,
        'total_services': total_services,
        'total_clients': total_clients,
        'frontend_tech': frontend_tech,
        'backend_tech': backend_tech,
        'database_tech': database_tech,
        'mobile_tech': mobile_tech,
        'cloud_tech': cloud_tech,
    }
    return render(request, 'about.html', context)

@require_POST
def subscribe_newsletter(request):
    """Handle newsletter subscription"""
    email = request.POST.get('email')
    
    if email:
        # Here you would typically save to a newsletter model
        # For now, we'll just return success
        return JsonResponse({'success': True, 'message': 'Successfully subscribed to newsletter!'})
    
    return JsonResponse({'success': False, 'message': 'Please provide a valid email address.'})

def handler404(request, exception):
    """Custom 404 handler"""
    site_settings = get_site_settings()
    return render(request, '404.html', {'site_settings': site_settings}, status=404)

def handler500(request):
    """Custom 500 handler"""
    site_settings = get_site_settings()
    return render(request, '500.html', {'site_settings': site_settings}, status=500)