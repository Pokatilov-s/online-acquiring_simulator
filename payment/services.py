from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from payment.models import PaymentNotifications
from multipledispatch import dispatch


class DescriptionPaymentSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    quantity = serializers.IntegerField(min_value=1, max_value=1000)
    price_per_unit = serializers.DecimalField(max_digits=10, decimal_places=2)


def creating_notification_record(payment, status_notif, description, type_notif):
    PaymentNotifications.objects.create(
        payment=payment,
        status=status_notif,
        description=description,
        type=type_notif,
    )


@dispatch(str)
def description_validate(description):
    if len(description.strip()) < 5:
        raise ValidationError('Длинна описания должна быть не менее 5 символов')
    return True


@dispatch(list)
def description_validate(description):
    for obj in description:
        serializer = DescriptionPaymentSerializer(data=obj)
        serializer.is_valid(raise_exception=True)
