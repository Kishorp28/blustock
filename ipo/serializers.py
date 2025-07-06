from rest_framework import serializers
from .models import Company, IPO, Document


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'logo', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'ipo', 'rhp_pdf', 'drhp_pdf', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class IPOSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.IntegerField(write_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    price_band = serializers.ReadOnlyField()
    listing_gain = serializers.ReadOnlyField()
    current_return = serializers.ReadOnlyField()

    class Meta:
        model = IPO
        fields = [
            'id', 'company', 'company_id', 'price_band_lower', 'price_band_upper',
            'price_band', 'open_date', 'close_date', 'issue_size', 'issue_type',
            'listing_date', 'status', 'ipo_price', 'listing_price', 'current_market_price',
            'listing_gain', 'current_return', 'documents', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'price_band', 'listing_gain', 'current_return', 'created_at', 'updated_at']


class IPOListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_logo = serializers.ImageField(source='company.logo', read_only=True)
    price_band = serializers.ReadOnlyField()
    listing_gain = serializers.ReadOnlyField()
    current_return = serializers.ReadOnlyField()
    rhp_pdf_url = serializers.SerializerMethodField()
    drhp_pdf_url = serializers.SerializerMethodField()

    def get_rhp_pdf_url(self, obj):
        doc = obj.documents.first()
        if doc and doc.rhp_pdf:
            request = self.context.get('request')
            return request.build_absolute_uri(doc.rhp_pdf.url) if request else doc.rhp_pdf.url
        return None

    def get_drhp_pdf_url(self, obj):
        doc = obj.documents.first()
        if doc and doc.drhp_pdf:
            request = self.context.get('request')
            return request.build_absolute_uri(doc.drhp_pdf.url) if request else doc.drhp_pdf.url
        return None

    class Meta:
        model = IPO
        fields = [
            'id', 'company_name', 'company_logo', 'price_band', 'open_date', 
            'close_date', 'issue_size', 'status', 'listing_gain', 'current_return',
            'rhp_pdf_url', 'drhp_pdf_url'
        ]


class IPOStatisticsSerializer(serializers.Serializer):
    total_ipos = serializers.IntegerField()
    upcoming_ipos = serializers.IntegerField()
    ongoing_ipos = serializers.IntegerField()
    listed_ipos = serializers.IntegerField()
    average_listing_gain = serializers.FloatField()
    average_current_return = serializers.FloatField() 