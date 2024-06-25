from django.urls import path
from .views import PaymentViewSet, payment_page, process_payment, success_page
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'', PaymentViewSet, basename='pay')

urlpatterns = [
    path('payment_page/<uuid:payment_uuid>/', payment_page, name='payment_page'),
    # path('process_payment', process_payment, name='process_payment'),
    path('success_page', success_page, name='success_page')
]

urlpatterns += router.urls
