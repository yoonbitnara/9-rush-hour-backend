import json
import uuid
import jwt
from datetime               import datetime

from django.views           import View
from django.http            import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from user.utils             import login_decorator

from user.models            import *
from order.models           import * 
from product.models         import * 

from lush.settings          import (
        SECRET_KEY,
        ALGORITHMS
        )

class OrderView(View):
    @login_decorator
    def get(self, request):
        data = json.loads(request.body)

        # bringing the user_id
        access_token = request.headers.get('authorization')
        decoded_token = jwt.decode(access_token, SECRET_KEY, ALGORITHMS)
        decoded_user_id = decoded_token['id']
        
        user = UserInfo.objects.get(id=decoded_user_id)

        # displaying user info
        user_info = {
            "name"         : user.name,
            "address"      : user.address,
            "phone_number" : user.phone_number,
            "email"        : user.email
            }
        
        shipping_method = data['shipping_method']
        # shipping info - default shipping address (기본 배송지)
        if shipping_method == 'default':
            default_shipping = ShippingList.objects.filter(default=True).get(user_id=decoded_user_id)

            shipping_info = {
                "recipient"    : default_shipping.recipient,
                "address"      : default_shipping.address,
                "phone_number" : default_shipping.phone_no
                }

        # shipping info - same as the user_info (주문자정보와 동일)
        elif shipping_method == 'same_user':
            shipping_info = {
                "recipient"    : user.name,
                "address"      : user.address,
                "phone_number" : user.phone_number
                }
        
        # payment_method 
        payment = Order.objects.filter(user_info_id = decoded_user_id).values()[0]
        payment_method = {
            "payment_method" : payment['payment_id']
            }

        return JsonResponse({
            "user_info"       : user_info,
            "shipping_info"   : shipping_info,
            "payment_method"  : payment_method
            }, status=200)

    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            # bringing the user_id
            access_token = request.headers.get('authorization')
            decoded_token = jwt.decode(access_token, SECRET_KEY, ALGORITHMS)
            decoded_user_id = decoded_token['id']

            # shipping info - 직접입력일때
            shipping_info = ShippingInfo.objects.create(
                name             = data["name"],
                address          = data["address"],
                phone_no         = data["phone_no"],
                message          = data["message"]
            )
            
            # generating a random order number
            random_order_no = "lush_"+uuid.uuid4().hex+"_"+datetime.strftime(datetime.today(),"%Y%m%d") 
            
            order = Order.objects.create(
                user_info_id    = decoded_user_id, 
                order_no        = random_order_no, 
                price           = data['total_price'], 
                payment_id      = data['payment_id'], 
                order_status_id = 1, 
                shipping        = shipping_info 
                )

            # saving product numbers
            product_id_list = data['product_number']
            for i in product_id_list:
                OrderItem.objects.create(order=order, product=Product.objects.get(product_number=i))

            return JsonResponse({"message": "SUCCESSFULLY_SAVED"}, status = 200)

        except Order.DoesNotExist:
            return JsonResponse({"message": "INVALID_ORDER"}, status = 400)
