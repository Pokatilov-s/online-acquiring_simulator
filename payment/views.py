from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """Создать платёж"""
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.payment_url = self.request.build_absolute_uri(
            reverse('payment_page', kwargs={'payment_uuid': payment.uuid})
        )
        payment.save()


def payment_page(request, payment_uuid):
    """Сформировать платёжную страницу"""
    payment = get_object_or_404(Payment, uuid=payment_uuid)
    payment_info = {
        'uuid': payment.uuid,
        'description': payment.description,
        'amount': payment.amount,
        'currency': payment.currency,
        'redirect': payment.redirect_url
    }
    return render(request, 'payment_page.html', {'payment': payment_info})


def process_payment():
    pass


def success_page():
    pass
