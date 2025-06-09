from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'prices', views.CryptoPriceViewSet)
router.register(r'metadata', views.CryptoMetaDataViewSet)
router.register(r'trending', views.TrendingCryptoViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
] 