from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    LoginWithPassword,
    # VerifyOTP,
    UpdateProfile,
    get_categories,
    get_subcategories,
    add_service,
    get_subcategories_by_category,
    RegisterUser,
    AddressListCreateView,
    AddressUpdateView,
)

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginWithPassword.as_view(), name='login'),
    # path('verify-otp/', VerifyOTP.as_view(), name='verify-otp'),
    path('update-profile/', UpdateProfile.as_view(), name='update-profile'),
    path('categories/', get_categories, name='categories'),
    path('category/<int:category_id>/', get_subcategories_by_category, name='get_subcategories_by_category'),
    path('subcategories/', get_subcategories, name='subcategories'),
    path('services/', add_service, name='add-service'),
    path('addresses/', AddressListCreateView.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/', AddressUpdateView.as_view(), name='address-update'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
