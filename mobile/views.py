from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from mobile.models import Snippet, Aptekalar, Sotuvchilar, Order, OrderItem, Dorilar, OrderQarz, OrderQarzItem
from mobile.serializers import (
    QarzdorHistorySerializer,
    SnippetSerializer, 
    AptekalarSerializer, 
    SotuvchilarSerializer, 
    DorilarSerializer, 
    QarzdorSerializer, 
    )
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
import json
from datetime import datetime, timedelta
# Create your views here.


@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['POST'])
def get_aptekalar_list(request):
    """
    Aptekalar ro'yxati
    """
    if request.method == 'POST':
        got_token = request.data['token']
        token = Token.objects.get(key=got_token)
        user = token.user
        sotuvchi = Sotuvchilar.objects.get(user=user)

        apteka = Aptekalar.objects.filter(user=sotuvchi.id)
        aptekalar = AptekalarSerializer(apteka, many=True)
        data = {"aptekalar": aptekalar.data}
        return Response(data)


@api_view(['POST'])
def add_aptekalar(request):
    """
    Aptekalar ro'yxati
    """
    if request.method == 'POST':
        got_token = request.data['token']
        data = request.data
        token = Token.objects.get(key=got_token)
        user = token.user
        sotuvchi = Sotuvchilar.objects.get(user=user)
        new_data = {"user": sotuvchi.id, "name": data['name'], 'description': data['description']}

        aptekalar = AptekalarSerializer(data=new_data)

        if aptekalar.is_valid():
            aptekalar.save()
            return Response(new_data, status=status.HTTP_201_CREATED)
        return Response(aptekalar.errors, status=status.HTTP_400_BAD_REQUEST)


        
        


@api_view(['GET', 'POST'])
def dorilar_list(request):
    """
    dorilar ro'yxati
    """
    if request.method == 'GET':
        dorilar = Dorilar.objects.all()
        dorilar_j = DorilarSerializer(dorilar, many=True)
        return Response(dorilar_j.data)

    elif request.method == 'POST':
        dorilar_j = DorilarSerializer(data=request.data)
        if dorilar_j.is_valid():
            dorilar_j.save()
            return Response(dorilar_j.data, status=status.HTTP_201_CREATED)
        return Response(dorilar_j.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
def sotuvchilar_list(request):
    """
    Sotuvchilar ro'yxati
    """
    if request.method == 'GET':
        sotuvchi = Sotuvchilar.objects.all()
        sotuvchilar = SotuvchilarSerializer(sotuvchi, many=True)
        return Response(sotuvchilar.data)

    elif request.method == 'POST':
        sotuvchilar = SotuvchilarSerializer(data=request.data)
        if sotuvchilar.is_valid():
            sotuvchilar.save()
            return Response(sotuvchilar.data, status=status.HTTP_201_CREATED)
        return Response(sotuvchilar.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def store(request):
    if request.method == "POST":
        got_token = request.data['token']
        try:
            dori_id = request.data['dori_id']
            apteka_id = request.data['apteka_id']
            status = request.data['status']
            token = Token.objects.get(key=got_token)
            apteka = Aptekalar.objects.get(id=apteka_id)
            user = token.user
            dori = Dorilar.objects.get(id=dori_id)
            sotuvchi = Sotuvchilar.objects.get(user=user)
            order, created  = Order.objects.get_or_create(sotuvchi=sotuvchi, complete=False)
            if int(dori.available) > int(request.data['quantity']):
                orderItems = OrderItem.objects.create(order=order, apteka=apteka, dorilar=dori, quantity=request.data['quantity'])
                orderQarz, completed = OrderQarz.objects.get_or_create(order=order, apteka=apteka, dorilar=dori)
                orderQarz.qoldi += orderItems.get_total
                quantity = int(request.data['quantity'])
                orderQarz.quantity += quantity
                orderQarz.save()
                if int(status) == 1:
                    status_bool = True
                    orderqarzitem = OrderQarzItem.objects.create(orderQarz=orderQarz, apteka=apteka, dorilar=dori, quantity=orderItems.quantity, completed=status_bool)
                    orderqarzitem.qoldi = 0
                    orderqarzitem.save()
                elif int(status) == 0:
                    status_bool = False
                    OrderQarzItem.objects.create(orderQarz=orderQarz, apteka=apteka, dorilar=dori, quantity=orderItems.quantity, completed=status_bool)

                count = int(dori.available)
                count -= int(orderItems.quantity)
                dori.available = count
                dori.save()

                

                return Response({"status":"Muvaffaqiyatli saqlandi"})
            return Response({"status": "Omborda yetarli maxsulot yo'q"})
        except ObjectDoesNotExist:
            return Response({"error": "keylarda xatolik bor"})

    return Response({"j":"keldi"})


@api_view(['POST'])
def sotuvchi(request):
    if request.method == "POST":
        got_token = request.data['token']
        apteka_id = request.data['apteka_id']
        token = Token.objects.get(key=got_token)
        user = token.user
        sotuvchi = Sotuvchilar.objects.get(user=user)
        try:
            order = Order.objects.get(sotuvchi=sotuvchi)
            qarz = order.orderqarz_set.filter(apteka=apteka_id)
            total = 0
            total_amount = 0
            for i in qarz:
                total_amount += i.get_cart_total
                total += i.get_cart_items
            
            data = { 
                "umumiy_sotilgan_summa": total_amount,
                "nechi_marta_sotgan": total
            }
            return Response(data)
        except ObjectDoesNotExist:
            order = None
    return Response({"j":"keldi"})


@api_view(['POST'])
def sotuvchi_qarzdorlari(request):
    if request.method == "POST":
        got_token = request.data['token']
        token = Token.objects.get(key=got_token)
        user = token.user
        sotuvchi = Sotuvchilar.objects.get(user=user)
        try:
            order = Order.objects.get(sotuvchi=sotuvchi)
            qarz = order.orderqarz_set.values()
            qarz_obj = order.orderqarz_set.all()
            qarz_json = list(qarz)
            for i in range(len(qarz_obj)):
                qarz_json[i]['total'] = qarz_obj[i].get_total
            data = { 
                "qarzdorlar": qarz_json,
            }
            return Response(data)
        except ObjectDoesNotExist:
            return Response({"error": "qarzdorlar yo'q"})
    return Response({"j":"keldi"})


@api_view(['POST'])
def sotuvchi_qarzdor_tolov(request):
    if request.method == "POST":
        summa = int(request.data['summa'])
        id = request.data['qarz_id']
        try:
            qarz = OrderQarzItem.objects.get(id=id)
            data = {
                "status": "to'lanmagan"
            }
        
            if summa <= qarz.qoldi:
                qarz.qoldi -= summa
                print(qarz.qoldi)
                qarz.save()
                data = {"satus": "to'landi"}

            if qarz.qoldi == 0:
                qarz.completed = True
                qarz.save()

            qarz.save()
            print(qarz.qoldi)
            

            return Response(data)
        except ObjectDoesNotExist:
            return Response({"error": "qarzdorlar yo'q"})
    return Response({"j":"keldi"})




@api_view(['POST'])
def sotuvchi_qarzdor_history(request):
    if request.method == "POST":
        got_token = request.data['token']
        token = Token.objects.get(key=got_token)
        user = token.user
        sotuvchi = Sotuvchilar.objects.get(user=user)
        try:
            order = Order.objects.get(sotuvchi=sotuvchi)
            qarz = order.orderqarz_set.all()
            data = {}
            for i in range(len(qarz)):
                qarzitem = qarz[i].orderqarzitem_set.values()
                data[qarz[i].dorilar.name] = list(qarzitem)
            return Response(data)
        except ObjectDoesNotExist:
            return Response({"error": "qarzdorlar yo'q"})
    return Response({"j":"keldi"})


@api_view(['POST'])
def sotuvchi_apteka_history(request):
    if request.method == "POST":
        got_token = request.data['token']
        apteka_id = request.data['apteka_id']
        token = Token.objects.get(key=got_token)
        user = token.user
        sotuvchi = Sotuvchilar.objects.get(user=user)
        try:
            order = Order.objects.get(sotuvchi=sotuvchi)
            qarz = order.orderqarz_set.filter(apteka=apteka_id)
            data = {"history":[]}
            for i in range(len(qarz)):
                qarzitem = list(qarz[i].orderqarzitem_set.values())
                data['history'].extend(qarzitem)
 
            return Response(data)
            
        except ObjectDoesNotExist:
            return Response({"status": "qarzdorlar yo'q"})
    return Response({"j":"keldi"})


@api_view(['POST'])
def statistics_for_single_day(request):
    if request.method == "POST":
        got_token = request.data['token']
        day = request.data['day']
        how_many_day = int(request.data['days'])
        token = Token.objects.get(key=got_token)
        user = token.user
        sotuvchi = Sotuvchilar.objects.get(user=user)
        day1 = datetime.strptime(day, "%Y-%m-%d").date()
        try:
            order = Order.objects.get(sotuvchi=sotuvchi)
            qarz = order.orderqarz_set.all()
            data = {"wanted_day":[]}
            
            for i in qarz:
                for j in range(how_many_day):
                    d = day1 - timedelta(days=j)
                    qarzitems = i.orderqarzitem_set.filter(bought_day=d)
                    [data['wanted_day'].append(QarzdorHistorySerializer(i).data) for i in qarzitems]
            print(data)
            return Response(data)
            
        except ObjectDoesNotExist:
            return Response({"status": "qarzdorlar yo'q"})
    return Response({"j":"keldi"})



