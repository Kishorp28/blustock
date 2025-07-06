from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, IPOViewSet, DocumentViewSet, home, ipo_detail, upcoming_ipos_view, signin_view, signup_view, admin_dashboard_view, manage_ipo_view, edit_ipo_view, delete_ipo_view, logout_view, ipo_subscription_view, ipo_allotment_view, settings_view, api_manager_view, accounts_view, help_view

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'ipos', IPOViewSet)
router.register(r'documents', DocumentViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('signin/', signin_view, name='signin'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('admin-dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('admin-manage-ipo/', manage_ipo_view, name='manage_ipo'),
    path('admin-edit-ipo/<int:ipo_id>/', edit_ipo_view, name='edit_ipo'),
    path('admin-delete-ipo/<int:ipo_id>/', delete_ipo_view, name='delete_ipo'),
    path('admin-ipo-subscription/', ipo_subscription_view, name='ipo_subscription'),
    path('admin-ipo-allotment/', ipo_allotment_view, name='ipo_allotment'),
    path('admin-settings/', settings_view, name='settings'),
    path('admin-api-manager/', api_manager_view, name='api_manager'),
    path('admin-accounts/', accounts_view, name='accounts'),
    path('admin-help/', help_view, name='help'),
    path('ipo/<int:ipo_id>/', ipo_detail, name='ipo_detail'),
    path('ipos/upcoming/', upcoming_ipos_view, name='upcoming_ipos'),
    path('api/', include(router.urls)),
] 