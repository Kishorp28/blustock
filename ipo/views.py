from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from .models import Company, IPO, Document, FAQ
from .serializers import (
    CompanySerializer, IPOSerializer, DocumentSerializer,
    IPOListSerializer, IPOStatisticsSerializer
)
from django.conf import settings
from django.templatetags.static import static
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, SignInForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator


def home(request):
    from .models import IPO, FAQ
    ipos_qs = IPO.objects.filter(status='upcoming').select_related('company').prefetch_related('documents')
    ipos = []
    for ipo in ipos_qs:
        doc = ipo.documents.first() if hasattr(ipo, 'documents') else None
        
        rhp_pdf_url = None
        drhp_pdf_url = None
        
        if doc:
            try:
                if doc.rhp_pdf and hasattr(doc.rhp_pdf, 'url'):
                    rhp_pdf_url = request.build_absolute_uri(doc.rhp_pdf.url)
            except Exception as e:
                print(f"Error getting RHP URL for {ipo.company.name}: {e}")
                
            try:
                if doc.drhp_pdf and hasattr(doc.drhp_pdf, 'url'):
                    drhp_pdf_url = request.build_absolute_uri(doc.drhp_pdf.url)
            except Exception as e:
                print(f"Error getting DRHP URL for {ipo.company.name}: {e}")
        
        ipos.append({
            'company_name': ipo.company.name,
            'company_logo': ipo.company.logo_url if ipo.company.logo_url else None,
            'price_band': f"Rs {ipo.price_band_lower} - {ipo.price_band_upper}" if ipo.price_band_lower and ipo.price_band_upper else 'Not Issued',
            'open_date': ipo.open_date,
            'close_date': ipo.close_date,
            'issue_size': ipo.issue_size,
            'issue_type': dict(IPO.ISSUE_TYPE_CHOICES).get(ipo.issue_type, ipo.issue_type),
            'listing_date': ipo.listing_date if ipo.listing_date else None,
            'rhp_pdf_url': rhp_pdf_url,
            'drhp_pdf_url': drhp_pdf_url,
        })
    faqs = FAQ.objects.filter(active=True).order_by('order')
    context = {'ipos': ipos, 'faqs': faqs}
    return render(request, 'upcoming_ipos.html', context)


def ipo_detail(request, ipo_id):
    ipo = get_object_or_404(IPO, id=ipo_id)
    
    status_badge_classes = {
        'upcoming': 'bg-warning',
        'ongoing': 'bg-info',
        'listed': 'bg-success',
    }
    status_badge_class = status_badge_classes.get(ipo.status, 'bg-secondary')
    
    context = {
        'ipo': ipo,
        'status_badge_class': status_badge_class,
    }
    return render(request, 'ipo_detail.html', context)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class IPOViewSet(viewsets.ModelViewSet):
    queryset = IPO.objects.select_related('company').prefetch_related('documents')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'issue_type']
    search_fields = ['company__name']
    ordering_fields = ['open_date', 'close_date', 'issue_size', 'listing_date']
    ordering = ['-open_date']

    def get_serializer_class(self):
        if self.action == 'list':
            return IPOListSerializer
        return IPOSerializer

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        total_ipos = IPO.objects.count()
        upcoming_ipos = IPO.objects.filter(status='upcoming').count()
        ongoing_ipos = IPO.objects.filter(status='ongoing').count()
        listed_ipos = IPO.objects.filter(status='listed').count()
        
        listed_ipos_with_gain = IPO.objects.filter(
            status='listed', 
            ipo_price__isnull=False, 
            listing_price__isnull=False,
            ipo_price__gt=0
        )
        
        avg_listing_gain = listed_ipos_with_gain.aggregate(
            avg_gain=Avg('listing_price') - Avg('ipo_price')
        )['avg_gain']
        
        if avg_listing_gain:
            avg_listing_gain_percent = (avg_listing_gain / listed_ipos_with_gain.aggregate(avg_ipo=Avg('ipo_price'))['avg_ipo']) * 100
        else:
            avg_listing_gain_percent = 0.0

        listed_ipos_with_current = IPO.objects.filter(
            status='listed',
            ipo_price__isnull=False,
            current_market_price__isnull=False,
            ipo_price__gt=0
        )
        
        avg_current_return = listed_ipos_with_current.aggregate(
            avg_return=Avg('current_market_price') - Avg('ipo_price')
        )['avg_return']
        
        if avg_current_return:
            avg_current_return_percent = (avg_current_return / listed_ipos_with_current.aggregate(avg_ipo=Avg('ipo_price'))['avg_ipo']) * 100
        else:
            avg_current_return_percent = 0.0

        data = {
            'total_ipos': total_ipos,
            'upcoming_ipos': upcoming_ipos,
            'ongoing_ipos': ongoing_ipos,
            'listed_ipos': listed_ipos,
            'average_listing_gain': round(avg_listing_gain_percent, 2),
            'average_current_return': round(avg_current_return_percent, 2),
        }
        
        serializer = IPOStatisticsSerializer(data)
        return Response(serializer.data)


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.select_related('ipo__company')
    serializer_class = DocumentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ipo__company__name', 'ipo__status']

    @action(detail=True, methods=['post'])
    def upload_rhp(self, request, pk=None):
        document = self.get_object()
        if 'rhp_pdf' in request.FILES:
            document.rhp_pdf = request.FILES['rhp_pdf']
            document.save()
            return Response({'message': 'RHP uploaded successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def upload_drhp(self, request, pk=None):
        document = self.get_object()
        if 'drhp_pdf' in request.FILES:
            document.drhp_pdf = request.FILES['drhp_pdf']
            document.save()
            return Response({'message': 'DRHP uploaded successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)


def upcoming_ipos_view(request):
    from .models import IPO, FAQ
    ipos_qs = IPO.objects.filter(status='upcoming').select_related('company').prefetch_related('documents')
    ipos = []
    for ipo in ipos_qs:
        doc = ipo.documents.first() if hasattr(ipo, 'documents') else None
        
        rhp_pdf_url = None
        drhp_pdf_url = None
        
        if doc:
            try:
                if doc.rhp_pdf and hasattr(doc.rhp_pdf, 'url'):
                    rhp_pdf_url = request.build_absolute_uri(doc.rhp_pdf.url)
            except Exception as e:
                print(f"Error getting RHP URL for {ipo.company.name}: {e}")
                
            try:
                if doc.drhp_pdf and hasattr(doc.drhp_pdf, 'url'):
                    drhp_pdf_url = request.build_absolute_uri(doc.drhp_pdf.url)
            except Exception as e:
                print(f"Error getting DRHP URL for {ipo.company.name}: {e}")
        
        ipos.append({
            'company_name': ipo.company.name,
            'company_logo': ipo.company.logo_url if ipo.company.logo_url else None,
            'price_band': f"Rs {ipo.price_band_lower} - {ipo.price_band_upper}" if ipo.price_band_lower and ipo.price_band_upper else 'Not Issued',
            'open_date': ipo.open_date,
            'close_date': ipo.close_date,
            'issue_size': ipo.issue_size,
            'issue_type': dict(IPO.ISSUE_TYPE_CHOICES).get(ipo.issue_type, ipo.issue_type),
            'listing_date': ipo.listing_date if ipo.listing_date else None,
            'rhp_pdf_url': rhp_pdf_url,
            'drhp_pdf_url': drhp_pdf_url,
        })
    faqs = FAQ.objects.filter(active=True).order_by('order')
    context = {'ipos': ipos, 'faqs': faqs}
    return render(request, 'upcoming_ipos.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def admin_dashboard_view(request):
    from ipo.models import IPO
    total_ipos = IPO.objects.count()
    ipos_in_gain = sum(1 for ipo in IPO.objects.all() if ipo.listing_gain and ipo.listing_gain > 0)
    ipos_in_loss = sum(1 for ipo in IPO.objects.all() if ipo.listing_gain and ipo.listing_gain < 0)
    not_in_loss = total_ipos - ipos_in_loss
    not_in_gain = total_ipos - ipos_in_gain
    upcoming = IPO.objects.filter(status='upcoming').count()
    new_listed = IPO.objects.filter(status='listed').count()
    ongoing = IPO.objects.filter(status='ongoing').count()
    context = {
        'total_ipos': total_ipos,
        'ipos_in_gain': ipos_in_gain,
        'ipos_in_loss': ipos_in_loss,
        'not_in_loss': not_in_loss,
        'not_in_gain': not_in_gain,
        'main_board_upcoming': upcoming,
        'main_board_new_listed': new_listed,
        'main_board_ongoing': ongoing,
    }
    return render(request, 'admin_dashboard.html', context)


def signin_view(request):
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin_dashboard')
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'form': form})


@login_required
def manage_ipo_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        ipos = IPO.objects.select_related('company').filter(
            company__name__icontains=search_query
        )
    else:
        ipos = IPO.objects.select_related('company').all()
    
    paginator = Paginator(ipos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'manage_ipo.html', {
        'ipos': page_obj,
        'search_query': search_query,
        'page_obj': page_obj,
    })


@login_required
def edit_ipo_view(request, ipo_id):
    ipo = get_object_or_404(IPO, id=ipo_id)
    
    if request.method == 'POST':
        ipo.company.name = request.POST.get('company_name', ipo.company.name)
        ipo.company.save()
        
        ipo.price_band_lower = request.POST.get('price_band_lower', ipo.price_band_lower)
        ipo.price_band_upper = request.POST.get('price_band_upper', ipo.price_band_upper)
        ipo.open_date = request.POST.get('open_date', ipo.open_date)
        ipo.close_date = request.POST.get('close_date', ipo.close_date)
        ipo.issue_size = request.POST.get('issue_size', ipo.issue_size)
        ipo.issue_type = request.POST.get('issue_type', ipo.issue_type)
        ipo.status = request.POST.get('status', ipo.status)
        
        listing_date = request.POST.get('listing_date')
        if listing_date:
            ipo.listing_date = listing_date
        else:
            ipo.listing_date = None
            
        ipo.save()
        messages.success(request, f'IPO for {ipo.company.name} updated successfully!')
        return redirect('manage_ipo')
    
    companies = Company.objects.all()
    context = {
        'ipo': ipo,
        'companies': companies,
        'status_choices': IPO.STATUS_CHOICES,
        'issue_type_choices': IPO.ISSUE_TYPE_CHOICES,
    }
    return render(request, 'edit_ipo.html', context)


@login_required
@require_POST
def delete_ipo_view(request, ipo_id):
    ipo = get_object_or_404(IPO, id=ipo_id)
    company_name = ipo.company.name
    ipo.delete()
    messages.success(request, f'IPO for {company_name} deleted successfully!')
    return redirect('manage_ipo')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')


@login_required
def ipo_subscription_view(request):
    """IPO Subscription management page."""
    # Get all IPOs for subscription management
    ipos = IPO.objects.select_related('company').all()
    context = {
        'ipos': ipos,
        'total_subscriptions': 0,  # Placeholder for subscription count
        'active_subscriptions': 0,  # Placeholder for active subscriptions
    }
    return render(request, 'ipo_subscription.html', context)


@login_required
def ipo_allotment_view(request):
    """IPO Allotment management page."""
    # Get all IPOs for allotment management
    ipos = IPO.objects.select_related('company').all()
    context = {
        'ipos': ipos,
        'total_allotments': 0,  # Placeholder for allotment count
        'pending_allotments': 0,  # Placeholder for pending allotments
    }
    return render(request, 'ipo_allotment.html', context)


@login_required
def settings_view(request):
    """Settings management page."""
    context = {
        'system_settings': {
            'site_name': 'Bluestock IPO Management',
            'admin_email': 'admin@bluestock.com',
            'max_file_size': '10MB',
            'auto_backup': True,
        }
    }
    return render(request, 'settings.html', context)


@login_required
def api_manager_view(request):
    """API Manager page."""
    context = {
        'api_keys': [
            {'name': 'Primary API Key', 'key': 'bs_****_****_****_****', 'created': '2024-01-15', 'status': 'Active'},
            {'name': 'Test API Key', 'key': 'bs_test_****_****', 'created': '2024-01-10', 'status': 'Active'},
        ],
        'api_usage': {
            'total_requests': 15420,
            'requests_today': 234,
            'rate_limit': '1000/hour',
        }
    }
    return render(request, 'api_manager.html', context)


@login_required
def accounts_view(request):
    """Accounts management page."""
    from django.contrib.auth.models import User
    users = User.objects.all()
    context = {
        'users': users,
        'total_users': users.count(),
        'active_users': users.filter(is_active=True).count(),
    }
    return render(request, 'accounts.html', context)


@login_required
def help_view(request):
    """Help and documentation page."""
    context = {
        'help_sections': [
            {
                'title': 'Getting Started',
                'content': 'Learn how to navigate and use the IPO management system effectively.',
                'icon': 'fas fa-rocket'
            },
            {
                'title': 'Managing IPOs',
                'content': 'Add, edit, and delete IPO listings with detailed company information.',
                'icon': 'fas fa-chart-line'
            },
            {
                'title': 'User Management',
                'content': 'Manage user accounts, permissions, and access controls.',
                'icon': 'fas fa-users'
            },
            {
                'title': 'API Documentation',
                'content': 'Integrate with external systems using our REST API.',
                'icon': 'fas fa-code'
            },
        ]
    }
    return render(request, 'help.html', context)
