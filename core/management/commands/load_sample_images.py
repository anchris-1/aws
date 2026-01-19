import os
from django.core.management.base import BaseCommand
from django.core.files import File
from core.models import PortfolioImage

class Command(BaseCommand):
    help = 'Load sample portfolio images'

    def handle(self, *args, **options):
        # Sample image URLs (you can replace these with actual image downloads)
        sample_images = [
            {
                'title': 'Web Development Hero',
                'category': 'hero',
                'description': 'Modern web development workspace',
            },
            {
                'title': 'Coding Environment',
                'category': 'hero', 
                'description': 'Developer coding environment setup',
            },
            {
                'title': 'Service Background',
                'category': 'services',
                'description': 'Background image for services section',
            },
            {
                'title': 'Project Showcase',
                'category': 'projects',
                'description': 'Background for projects section',
            },
            {
                'title': 'Abstract Tech Background',
                'category': 'background',
                'description': 'Abstract technology background pattern',
            },
        ]

        for image_data in sample_images:
            # Create placeholder images (in production, you'd download actual images)
            portfolio_image, created = PortfolioImage.objects.get_or_create(
                title=image_data['title'],
                defaults={
                    'category': image_data['category'],
                    'description': image_data['description'],
                    'is_active': True,
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created sample image: {image_data["title"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Image already exists: {image_data["title"]}')
                )