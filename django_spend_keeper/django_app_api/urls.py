from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import RegisterView, AccountsListView, CategoryListCreateView, SavingCreateView, \
    AccountDetailView, TransactionListCreateView, TransactionDetailView

urlpatterns = [

    path('api/registration/', RegisterView.as_view(), name='registration'),
    # path('api/registration/', views.registration, name='registration'),

    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/accounts/', AccountsListView.as_view(), name='user-account-detail'),
    path('api/account/<int:pk>/', AccountDetailView.as_view(), name='account-detail'),

    path('api/transactions/', TransactionListCreateView.as_view(), name='transaction-create'),
    path('api/transaction/<int:pk>/', TransactionDetailView.as_view(), name='transaction-create'),

    path('api/categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('api/categorie/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),

    # Swagger URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

]
