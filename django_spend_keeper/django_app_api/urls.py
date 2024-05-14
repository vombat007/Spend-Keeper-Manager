from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import RegisterView, AccountDetailView, CategoryListView, TransactionCreateView, SavingCreateView

urlpatterns = [

    path('api/registration/', RegisterView.as_view(), name='registration'),
    # path('api/registration/', views.registration, name='registration'),

    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/account/', views.AccountDetailView.as_view(), name='user-account-detail'),
    path('api/categories/', views.CategoryListView.as_view(), name='category-list'),
    path('api/transactions/create/', views.TransactionCreateView.as_view(), name='transaction-create'),
    path('api/savings/create/', views.SavingCreateView.as_view(), name='saving-create'),

    # Swagger URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

]
