from payment.models import PaymentNotifications


def creating_notification_record(payment, status_notif, description, type_notif):
    PaymentNotifications.objects.create(
        payment=payment,
        status=status_notif,
        description=description,
        type=type_notif,
    )
