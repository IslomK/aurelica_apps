import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, DatabaseError
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Payment, Invoice
from api.serializers import PaymentCreateSerializer, PaymentSerializer
from core.exceptions import BadRequest, NotFoundError


class PaymentView(APIView):
    def post(self, request):
        serializer = PaymentCreateSerializer(data=request.data)

        if not serializer.is_valid():
            raise BadRequest(serializer.errors)

        invoice_id = serializer.validated_data.get('invoice_id')

        with transaction.atomic():
            try:
                invoice = Invoice.objects.get(id=invoice_id)

                payment = Payment.objects.create(
                    invoice_id=invoice_id,
                    amount=invoice.amount,
                    name="{}_{}".format(invoice_id, datetime.datetime.now())
                )
            except ObjectDoesNotExist:
                raise BadRequest("No invoice found")
            except DatabaseError as ex:
                raise ex

        return Response(data={
            "status": "SUCCESS",
            "payment_details": PaymentSerializer(payment).data
        })


class PaymentDetailView(APIView):
    def get(self, request):
        payment_id = request.GET.get('payment_id', None)

        if not payment_id:
            raise BadRequest("payment_id query param required")

        try:
            payment = Payment.objects.get(id=payment_id)
        except ObjectDoesNotExist:
            raise NotFoundError("No payment found with id {}".format(payment_id))

        serializer = PaymentSerializer(payment)

        return Response(serializer.data)