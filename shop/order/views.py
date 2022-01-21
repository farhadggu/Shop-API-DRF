from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from zeep import Client
from shop.settings import ZARINPAL_MERCHANT_ID as MERCHANT
from .serializers import (
    OrderSerializer,
    CreateOrderSerializer,
    UpdateOrderSerializer,
    SendRequestSerializer,
    VerifySerializer
)
from .models import Order, PurchaseHistory


class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={'user': self.request.user})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        elif self.request.method == "PATCH":
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user_id=user.id)

    serializer_class = OrderSerializer


client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')

class SendRequestAPIView(APIView):
    serializer_class = SendRequestSerializer
    
    def post(self, request, *args, **kwargs):
        data = PurchaseHistory.objects.get(email=request.user.email)
        if data.price != None:
            amount = data.price
            if int(amount) < 2000:
                return Response({'details': 'The minimum charge should be 2000 TOMAN'})
            description = "شارژ کیف پول"
            email=data.email
            domain = request.get_host()
            CallbackURL = domain +'/api/zarinpal/verify/'
            result = client.service.PaymentRequest(MERCHANT, amount, description, email, CallbackURL=CallbackURL)
            if result.Status == 100:
                instance = PurchaseHistory(name=data.name , email=email , price=amount , Authority=result.Authority)
                instance.save()
                return Response({'redirect to : ': 'https://www.zarinpal.com/pg/StartPay/' + str(result.Authority)},
                                status=200)
            else:
                return Response({'Error code: ' : str(result.Status)},status=400)
        else:
            return Response({'details': 'Invalid input value'})


class VerifyAPIView(APIView):
    serializer_class = VerifySerializer

    def get(self, request, *args, **kwargs):
        if request.GET.get('Status') == 'OK':
            autho = request.GET.get('Authority')
            try:
                obj = PurchaseHistory.objects.get(Authority=autho)
            except:
                return Response({'details': 'Authority Code not found'})
            amount = obj.price
            result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
            obj.Status = result.Status
            obj.RefID = result.RefID
            obj.save()
            if result.Status == 100:
                obj.is_paid = True
                obj.save()
                return Response({'details': 'Transaction success. RefID: ' + str(result.RefID)}, status=200)
            elif result.Status == 101:
                return Response({'details': 'Transaction submitted'}, status=200)
            else:
                return Response({'details': 'Transaction failed . error code : ' + str(result.Status) }, status=200)
        else:
            return Response({'details': 'Transaction failed or canceled by user'}, status=200)