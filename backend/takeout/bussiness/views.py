# coding: utf-8
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from bussiness.serializers import SellerSerializer, StoreSerializer
from models.seller import Seller
from models.store import Store
from rest_framework.response import Response
from lib.utils.response import JsonResponse, JsonErrorResponse
from lib.utils.misc import get_update_dict_by_list
from django.db import models


class SellerList(APIView):
    def get(self, request):
        # 获取卖家列表
        sellers = [seller.to_string() for seller in Seller.objects.all()]
        return JsonResponse({"seller_list": sellers})

    def post(self, request):
        # 注册
        username = request.json.get("username")
        password = request.json.get("password")
        nickname = request.json.get("nickname")
        account_type = request.json.get("account_type")
        if not all([username, password, nickname, account_type]):
            return JsonErrorResponse("username, password, nickname, account_type are needed", 400)
        new_seller = Seller(
            username=username,
            password=password,
            nickname=nickname,
            account_type=account_type
        )
        try:
            new_seller.save()
        except Exception, e:
            print e
            return JsonErrorResponse("Fail" + e.message)
        print "新注册id：", new_seller.id
        print request.data
        print request.query_params
        return JsonResponse({"id": new_seller.id})


class SellerDetail(APIView):
    def get(self, request, seller_id):
        try:
            seller = Seller.objects.get(id=seller_id)
        except Seller.DoesNotExist:
            return JsonErrorResponse("Seller does not exist", 404)
        return JsonResponse({"seller": seller.to_detail_string()})

    def put(self, request, seller_id):
        # 更新个人信息
        update_item = ['nickname', 'password']
        update_dict = get_update_dict_by_list(update_item, request.json)
        modify_num = Seller.objects.filter(id=seller_id).update(**update_dict)
        if modify_num == 1:
            return JsonResponse({})
        return JsonErrorResponse("Update failed", 400)


class StoreList(APIView):
    def get(self, request):
        # 获取商店列表
        stores = [store.to_string() for store in Store.objects.all()]
        return JsonResponse({"store_list": stores})

    def post(self, request):
        # 创建商店
        owner = request.u
        name = request.json.get("name")
        address = request.json.get("address")
        announcement = request.json.get("announcement")
        description = request.json.get("description")
        phone = request.json.get("phone")
        if not all([owner, name, address, announcement, description]):
            return JsonErrorResponse("owner, name, address, announcement, description, phone are needed", 400)
        new_store = Store(
            name=name,
            address=address,
            announcement=announcement,
            description=description,
            phone=phone,
            owner=owner
        )
        try:
            new_store.save()
        except Exception, e:
            print e
            return JsonErrorResponse("Fail" + e.message)
        print "新注册id：", new_store.id
        return JsonResponse({"id": new_store.id})


class StoreDetail(APIView):
    def get(self, request, store_id):
        print store_id
        print request.json
        try:
            store = Store.objects.get(id=store_id)
        except Store.DoesNotExist:
            return JsonErrorResponse("Store does not exist", 404)
        return JsonResponse({"store": store.to_detail_string()})

    def put(self, request, store_id):
        # 更新信息
        update_item = ['name', 'address', 'announcement', 'description', 'phone']
        update_dict = get_update_dict_by_list(update_item, request.json)
        modify_num = Store.objects.filter(id=store_id).update(**update_dict)
        if modify_num == 1:
            return JsonResponse({})
        return JsonErrorResponse("Update failed", 400)