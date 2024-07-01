from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status, viewsets, decorators
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

            return Response({'status': 'Платеж успешно обработан'}, status=status.HTTP_200_OK)
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


def success_page():
    pass
