from payment.models import PaymentNotifications


def insert_notification_record(payment, status_notif, description, type_notif):
    """Вставить запись об уведомлении"""
    record = PaymentNotifications.objects.create(
        payment=payment,
        status=status_notif,
        description=description,
        type=type_notif,
    )
    return record
