from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['uuid', 'amount', 'currency', 'description', 'status', 'created_at', 'payment_url', 'redirect_url']

