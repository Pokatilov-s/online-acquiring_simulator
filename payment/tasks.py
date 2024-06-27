from celery import shared_task
from requests import RequestException, HTTPError
import requests



@shared_task(bind=True, autoretry_for=(RequestException, HTTPError), retry_backoff=5, retry_jitter=False,
             retry_kwargs={'max_retries': 3})
def send_webhook_notifications(self, pk_payment):
    from payment.models import Payment, PaymentNotifications
    payment = Payment.objects.get(pk=pk_payment)
    url = payment.webhook_url
    data = {
        'payment_id': str(payment.uuid),
        'status': payment.status
    }
    if self.request.retries != self.max_retries:
        response = requests.post(url=url, json=data)
        response.raise_for_status()
    else:
        print(f"Достигнут лимит попыток оправки уведомления task {self.request.id}")

    PaymentNotifications.objects.create(
        payment=payment,
        status=self.request.state,
        description=self.request.id,
        )
