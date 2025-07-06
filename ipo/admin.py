from django.contrib import admin
from .models import Company, IPO, Document, FAQ


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(IPO)
class IPOAdmin(admin.ModelAdmin):
    list_display = ['company', 'status', 'price_band', 'issue_size', 'open_date', 'close_date', 'listing_gain', 'current_return']
    list_filter = ['status', 'issue_type', 'open_date', 'close_date']
    search_fields = ['company__name']
    readonly_fields = ['listing_gain', 'current_return', 'created_at', 'updated_at']
    date_hierarchy = 'open_date'
    
    fieldsets = (
        ('Company Information', {
            'fields': ('company',)
        }),
        ('IPO Details', {
            'fields': ('price_band_lower', 'price_band_upper', 'issue_size', 'issue_type', 'status')
        }),
        ('Dates', {
            'fields': ('open_date', 'close_date', 'listing_date')
        }),
        ('Pricing', {
            'fields': ('ipo_price', 'listing_price', 'current_market_price')
        }),
        ('Calculated Fields', {
            'fields': ('listing_gain', 'current_return'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['ipo', 'has_rhp', 'has_drhp', 'created_at']
    list_filter = ['created_at', 'ipo__status']
    search_fields = ['ipo__company__name']
    readonly_fields = ['created_at', 'updated_at']
    
    def has_rhp(self, obj):
        return bool(obj.rhp_pdf)
    has_rhp.boolean = True
    has_rhp.short_description = 'Has RHP'
    
    def has_drhp(self, obj):
        return bool(obj.drhp_pdf)
    has_drhp.boolean = True
    has_drhp.short_description = 'Has DRHP'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'active', 'created_at', 'updated_at')
    list_filter = ('active',)
    search_fields = ('question',)
    ordering = ('order',)
