from django.db import models
from decimal import Decimal


class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"


class IPO(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('listed', 'Listed'),
    ]

    ISSUE_TYPE_CHOICES = [
        ('book_building', 'Book Building'),
        ('fixed_price', 'Fixed Price'),
        ('auction', 'Auction'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='ipos')
    price_band_lower = models.DecimalField(max_digits=10, decimal_places=2)
    price_band_upper = models.DecimalField(max_digits=10, decimal_places=2)
    open_date = models.DateField()
    close_date = models.DateField()
    issue_size = models.DecimalField(max_digits=15, decimal_places=2, help_text="Issue size in crores")
    issue_type = models.CharField(max_length=20, choices=ISSUE_TYPE_CHOICES, default='book_building')
    listing_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    ipo_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    listing_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_market_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.name} - {self.status.title()}"

    @property
    def price_band(self):
        return f"₹{self.price_band_lower} - ₹{self.price_band_upper}"

    @property
    def listing_gain(self):
        if self.ipo_price and self.listing_price and self.ipo_price > 0:
            return round(((self.listing_price - self.ipo_price) / self.ipo_price) * 100, 2)
        return None

    @property
    def current_return(self):
        if self.ipo_price and self.current_market_price and self.ipo_price > 0:
            return round(((self.current_market_price - self.ipo_price) / self.ipo_price) * 100, 2)
        return None

    class Meta:
        ordering = ['-open_date']


class Document(models.Model):
    ipo = models.ForeignKey(IPO, on_delete=models.CASCADE, related_name='documents')
    rhp_pdf = models.FileField(upload_to='ipo_documents/rhp/', null=True, blank=True, help_text="Red Herring Prospectus")
    drhp_pdf = models.FileField(upload_to='ipo_documents/drhp/', null=True, blank=True, help_text="Draft Red Herring Prospectus")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Documents for {self.ipo.company.name} IPO"

    class Meta:
        verbose_name_plural = "Documents"


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
