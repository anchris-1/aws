from django.core.management.base import BaseCommand
from django.core.files import File
from core.models import Service, Project, PortfolioImage, Testimonial, SiteSetting, Technology
from datetime import date, timedelta
import os

class Command(BaseCommand):
    help = 'Setup portfolio with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Setting up portfolio sample data...')
        
        # Create Site Settings
        site_settings, created = SiteSetting.objects.get_or_create(
            id=1,
            defaults={
                'site_name': 'DevPortfolio',
                'site_description': 'Professional Web Development Services - Creating exceptional digital experiences that drive business growth and user engagement.',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Created site settings'))
        
        # Create Technologies
        technologies_data = [
            # Frontend
            {'name': 'React', 'icon': 'fab fa-react', 'category': 'frontend', 'proficiency': 90},
            {'name': 'Vue.js', 'icon': 'fab fa-vuejs', 'category': 'frontend', 'proficiency': 85},
            {'name': 'Angular', 'icon': 'fab fa-angular', 'category': 'frontend', 'proficiency': 80},
            {'name': 'JavaScript', 'icon': 'fab fa-js', 'category': 'frontend', 'proficiency': 95},
            {'name': 'TypeScript', 'icon': 'fas fa-code', 'category': 'frontend', 'proficiency': 88},
            {'name': 'HTML5', 'icon': 'fab fa-html5', 'category': 'frontend', 'proficiency': 98},
            {'name': 'CSS3', 'icon': 'fab fa-css3-alt', 'category': 'frontend', 'proficiency': 95},
            {'name': 'Tailwind CSS', 'icon': 'fas fa-wind', 'category': 'frontend', 'proficiency': 92},
            
            # Backend
            {'name': 'Python', 'icon': 'fab fa-python', 'category': 'backend', 'proficiency': 95},
            {'name': 'Django', 'icon': 'fas fa-server', 'category': 'backend', 'proficiency': 90},
            {'name': 'Node.js', 'icon': 'fab fa-node-js', 'category': 'backend', 'proficiency': 85},
            {'name': 'Express.js', 'icon': 'fas fa-bolt', 'category': 'backend', 'proficiency': 82},
            
            # Database
            {'name': 'PostgreSQL', 'icon': 'fas fa-database', 'category': 'database', 'proficiency': 88},
            {'name': 'MongoDB', 'icon': 'fas fa-leaf', 'category': 'database', 'proficiency': 80},
            {'name': 'Redis', 'icon': 'fas fa-memory', 'category': 'database', 'proficiency': 75},
            
            # Mobile
            {'name': 'React Native', 'icon': 'fab fa-react', 'category': 'mobile', 'proficiency': 85},
            {'name': 'Flutter', 'icon': 'fas fa-mobile', 'category': 'mobile', 'proficiency': 78},
            
            # Cloud
            {'name': 'AWS', 'icon': 'fab fa-aws', 'category': 'cloud', 'proficiency': 82},
            {'name': 'Docker', 'icon': 'fab fa-docker', 'category': 'cloud', 'proficiency': 80},
            {'name': 'Kubernetes', 'icon': 'fas fa-ship', 'category': 'cloud', 'proficiency': 75},
            
            # Tools
            {'name': 'Git', 'icon': 'fab fa-git-alt', 'category': 'tool', 'proficiency': 95},
            {'name': 'GitHub', 'icon': 'fab fa-github', 'category': 'tool', 'proficiency': 90},
            {'name': 'VS Code', 'icon': 'fas fa-code', 'category': 'tool', 'proficiency': 92},
        ]
        
        for tech_data in technologies_data:
            tech, created = Technology.objects.get_or_create(
                name=tech_data['name'],
                defaults=tech_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created technology: {tech_data["name"]}'))
        
        # Create Sample Services
        services_data = [
            {
                'name': 'Web Application Development',
                'description': 'Custom web applications built with modern technologies like Django, React, and PostgreSQL. We create scalable solutions that grow with your business. Our full-stack development approach ensures seamless integration between frontend and backend components.',
                'price': 5000,
                'price_description': 'Starting at',
                'icon': 'fas fa-laptop-code',
                'order': 1,
                'is_featured': True,
            },
            {
                'name': 'E-commerce Solutions',
                'description': 'Complete online store development with payment integration, inventory management, and responsive design optimized for conversions. We build secure, scalable e-commerce platforms that drive sales and enhance customer experience.',
                'price': 7500,
                'price_description': 'Starting at',
                'icon': 'fas fa-shopping-cart',
                'order': 2,
                'is_featured': True,
            },
            {
                'name': 'Mobile App Development',
                'description': 'Cross-platform mobile applications that work seamlessly on iOS and Android, built with React Native for cost-effective development. We create intuitive mobile experiences that engage users and deliver business value.',
                'price': 10000,
                'price_description': 'Starting at',
                'icon': 'fas fa-mobile-alt',
                'order': 3,
                'is_featured': True,
            },
            {
                'name': 'API Development & Integration',
                'description': 'RESTful API development and third-party service integration to connect your applications with external systems and services. We build robust, well-documented APIs that follow best practices.',
                'price': 3000,
                'price_description': 'Starting at',
                'icon': 'fas fa-plug',
                'order': 4,
                'is_featured': False,
            },
            {
                'name': 'UI/UX Design',
                'description': 'User-centered design solutions that create intuitive, beautiful interfaces. We conduct user research, create wireframes, and design pixel-perfect interfaces that enhance user engagement.',
                'price': 2500,
                'price_description': 'Starting at',
                'icon': 'fas fa-palette',
                'order': 5,
                'is_featured': False,
            },
            {
                'name': 'DevOps & Deployment',
                'description': 'CI/CD pipeline setup, cloud infrastructure management, and deployment automation. We ensure your applications are deployed securely and scale efficiently in production environments.',
                'price': 2000,
                'price_description': 'Monthly',
                'icon': 'fas fa-cloud-upload-alt',
                'order': 6,
                'is_featured': False,
            },
        ]
        
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created service: {service_data["name"]}'))
        
        # Create Sample Portfolio Images (placeholders - in real scenario, you'd add actual images)
        portfolio_images = [
            {'title': 'Web Development Hero', 'category': 'hero', 'description': 'Modern web development workspace'},
            {'title': 'Coding Environment', 'category': 'hero', 'description': 'Developer coding setup'},
            {'title': 'Service Background 1', 'category': 'services', 'description': 'Background for services section'},
            {'title': 'Project Showcase', 'category': 'projects', 'description': 'Project display background'},
            {'title': 'Contact Background', 'category': 'contact', 'description': 'Contact page background'},
            {'title': 'Tech Pattern 1', 'category': 'pattern', 'description': 'Technology pattern background'},
            {'title': 'Testimonial Background', 'category': 'testimonial', 'description': 'Testimonials section background'},
            {'title': 'CTA Background', 'category': 'cta', 'description': 'Call to action background'},
        ]
        
        for image_data in portfolio_images:
            image, created = PortfolioImage.objects.get_or_create(
                title=image_data['title'],
                defaults=image_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created portfolio image: {image_data["title"]}'))
        
        # Create Sample Testimonials
        testimonials_data = [
            {
                'client_name': 'John Smith',
                'company': 'Tech Solutions Inc.',
                'content': 'The web application developed by this team exceeded our expectations. They delivered on time and within budget, and the quality of their work is outstanding. Our operational efficiency has improved by 40% since launch.',
                'rating': 5,
                'is_featured': True,
                'order': 1,
            },
            {
                'client_name': 'Sarah Johnson',
                'company': 'Creative Agency',
                'content': 'Professional, responsive, and highly skilled. Our e-commerce platform has seen a 60% increase in conversions since they rebuilt it. The team truly understands both technical requirements and business objectives.',
                'rating': 5,
                'is_featured': True,
                'order': 2,
            },
            {
                'client_name': 'Michael Chen',
                'company': 'StartUp Ventures',
                'content': 'Outstanding mobile app development service. They delivered a cross-platform app that works flawlessly on both iOS and Android. The user experience is smooth and the performance is excellent.',
                'rating': 5,
                'is_featured': True,
                'order': 3,
            },
            {
                'client_name': 'Emily Rodriguez',
                'company': 'Digital Marketing Pro',
                'content': 'The API integration work was completed ahead of schedule and works perfectly. Their documentation is thorough and their support has been exceptional. Highly recommended for any complex integration projects.',
                'rating': 4,
                'is_featured': True,
                'order': 4,
            },
        ]
        
        for testimonial_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                client_name=testimonial_data['client_name'],
                company=testimonial_data['company'],
                defaults=testimonial_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created testimonial: {testimonial_data["client_name"]}'))
        
        self.stdout.write(self.style.SUCCESS('✓ Portfolio setup completed successfully!'))
        self.stdout.write(self.style.SUCCESS('✓ You can now run the development server and visit /admin to manage your portfolio.'))