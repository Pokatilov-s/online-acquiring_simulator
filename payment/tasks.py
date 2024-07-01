from celery import shared_task
from requests import RequestException, HTTPError
import requests


@shared_task(bind=True, autoretry_for=(RequestException, HTTPError), retry_backoff=5, retry_jitter=False,
             retry_kwargs={'max_retries': 3})
def send_webhook_notifications(self, pk_payment):
    from payment.models import Payment
    from payment.services import creating_notification_record

    payment = Payment.objects.get(pk=pk_payment)
    task_id = self.request.id

    type_notif = 'webhook'

    url = payment.webhook_url
    message = {
        'payment_id': str(payment.uuid),
        'status': payment.status
    }

    if self.request.retries < self.max_retries:
        try:
            response = requests.post(url=url, json=message)
            response.raise_for_status()

            status_task = 'SUCCESS'
            description = f"Уведомление успешно отправлено task {task_id}"

            creating_notification_record(payment=payment, status_notif=status_task,
                                         description=description,
                                         type_notif=type_notif)
        except Exception as e:
            status_task = 'RETRY'
            description = f'Task {task_id}, ERROR MESSAGE: {e}'

            creating_notification_record(payment=payment, status_notif=status_task,
                                         description=description,
                                         type_notif=type_notif)
            raise

    else:
        status_task = 'FAILED'
        description = f"Достигнут лимит попыток оправки уведомления task {task_id}"

        creating_notification_record(payment=payment, status_notif=status_task,
                                     description=description,
                                     type_notif=type_notif)
