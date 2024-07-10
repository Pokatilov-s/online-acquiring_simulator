from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status, viewsets, decorators, generics
from .models import Payment
from .serializers import PaymentSerializer, ProcessPaymentSerializer
from .tasks import send_webhook_notifications
from .services import creating_notification_record


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        """Создать платёж"""
        payment = serializer.save()
        payment.payment_url = self.request.build_absolute_uri(
            reverse('payment_page', kwargs={'payment_uuid': payment.uuid})
        )
        payment.save()

    @decorators.action(methods=['POST'], detail=True, serializer_class=ProcessPaymentSerializer)
    def process_payment(self, request, pk=None):
        """Оплатить"""
        payment = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            payment.status = 'completed'
            payment.save()

            task = send_webhook_notifications.delay(payment.uuid)
            task_id = task.id
            creating_notification_record(payment=payment, status_notif='CREATED',
                                         description=f'Создана задача на уведомление task {task_id}',
                                         type_notif='webhook')

            return Response({'status': 'success', 'message': 'Платеж успешно обработан'},
                            status=status.HTTP_200_OK)
        return Response({'status': 'Ошибка платежа'}, status=status.HTTP_400_BAD_REQUEST)


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


def success_page(request):
    """Вернуть страницу успешного платежа"""
    receipt = {
        'id': '808800808080',
        'created_at': datetime.now(),
        'payment_type': 'Online',
        'total_amount': 200.00,
        'currency': 'RUB'
    }
    products = [
        {
            'name': 'Python course',
            'quantity': 1,
            'price_per_unit': 100.00,
            'total_price': 100.00
        },
        {
            'name': 'Python course + ',
            'quantity': 1,
            'price_per_unit': 100.00,
            'total_price': 100.00
        },
        {
            'name': 'JAVA course',
            'quantity': 1,
            'price_per_unit': 100.00,
            'total_price': 100.00
        },
    ]
    return render(request, 'receipt.html', {'receipt': receipt, 'products': products})


class ReceiptPayment(generics.RetrieveAPIView):
    pass
