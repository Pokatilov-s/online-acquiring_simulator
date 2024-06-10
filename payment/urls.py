from django.urls import path
from .views import CreatePaymentViewSet, payment_page
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'', CreatePaymentViewSet, basename='pay')

urlpatterns = [
    path('payment_page/<uuid:payment_uuid>/', payment_page, name='payment_page')
]

urlpatterns += router.urls
