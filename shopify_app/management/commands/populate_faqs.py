from django.core.management.base import BaseCommand
from shopify_app.models import FAQS  # Change to your actual app name if not `core`

class Command(BaseCommand):
    help = 'Insert predefined FAQs into the database'

    def handle(self, *args, **kwargs):
        faqs_data = [
            {"question": "What is a SAAS platform?", "answer": "SAAS platform is a cloud-based software service that allows users to access and use a variety of tools and functionality."},
            {"question": "How does billing work?", "answer": "We offer a variety of billing options, including monthly and annual subscription plans, as well as pay-as-you-go pricing for certain services."},
            {"question": "Can I get a refund for my subscription?", "answer": "We offer a 30-day money-back guarantee for most of its subscription plans."},
            {"question": "How do I cancel my subscription?", "answer": "To cancel your subscription, log in to your account and navigate to the subscription management page."},
            {"question": "Can I try this platform for free?", "answer": "We offer a free trial of its platform for a limited time."},
            {"question": "How do I access documentation?", "answer": "Documentation is available on the company's website and can be accessed by logging into your account."},
            {"question": "How do I contact support?", "answer": "You can contact support by submitting a request through the website or emailing support@example.com."},
            {"question": "Do you offer any discounts or promotions?", "answer": "We may offer discounts or promotions from time to time."},
            {"question": "How do we compare to other similar services?", "answer": "This platform is highly reliable and feature-rich, offering a variety of billing options."}
        ]

        created_count = 0
        for faq in faqs_data:
            obj, created = FAQS.objects.get_or_create(question=faq["question"], defaults={"answer": faq["answer"]})
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Inserted {created_count} new FAQs into the database."))
