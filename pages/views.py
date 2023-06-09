from django.shortcuts import render
from datetime import date, timedelta, datetime
import datetime
from django.shortcuts import render
from mobile.models import Sotuvchilar, Order, OrderQarz, OrderQarzItem
from mobile.serializers import (
    QarzdorHistorySerializer,
    )
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
import json
from datetime import datetime, timedelta
# Create your views here.


def home(request):
    return render(request, "index.html")


def chart(request):
    return render(request, "pages/charts/chartjs.html")


def table(request):
    return render(request, "index.html")

def table1(request):
    return render(request, "index.html")


def table2(request):
    return render(request, "index.html")

def people(request):
    sellers = Sotuvchilar.objects.all()
    context = {"sellers": sellers}
    return render(request, "pages/projects.html", context)



def test(request):
    sellers = Sotuvchilar.objects.all()
    test = OrderQarzItem.objects.all()
    for i in test:
        print(i)


    context = {"sellers": sellers}
    return render(request, "pages/projects.html", context)

# def people_detail(request, id):
#     if request.method == "POST":
#         days = request.POST['days_detail']
#         if days == "three_days":
#             pass
#         elif days == "one_day":
#             pass
#         else:
#             pass
#     order = Order.objects.get(sotuvchi=id)
#     orderqarz = OrderQarz.objects.filter(order=order.id)
#     qarz = order.orderqarz_set.all()
#     bugungi_list = []
#     today_total_price = 0
#     for i in orderqarz:
#         bugungili_sotilganlar = OrderQarzItem.objects.filter(orderQarz=i.id, bought_day=date.today())
#         if(bugungili_sotilganlar):
#             for j in bugungili_sotilganlar:
#                 today_total_price += j.umumiy_summa
#                 bugungi_list.append(j)
#     total = 0
#     total_amount = 0
#     for i in qarz:
#         total_amount += i.get_cart_total
#         total += i.get_cart_items
    
#     context = { 
#         "umumiy_sotilgan_summa": total_amount,
#         "nechi_marta_sotgan": total,
#         "nechi_marta_sotgan": total,
#         "bugungi_list": bugungi_list,
#         "today_total_price": today_total_price
#     }
#     return render(request, "pages/project-detail.html", context)

def people_detail(request, id):
    how_many_day = 0
    day1 = date.today()
    total_amount = 0
    total_quantity = 0
    qancha_qarz = 0
    if request.method == "POST":
        days = request.POST['days_detail']
        if days == "three_days":
            how_many_day = 3
        elif days == "one_day":
            how_many_day = 1
        elif days == "one_month":
            how_many_day = day1.day
        elif days == "all":
            how_many_day = None
        else:
            how_many_day = 0
    order = Order.objects.get(sotuvchi=id)
    qarz = order.orderqarz_set.all()
    sotuvchi = Sotuvchilar.objects.get(id=id)
    try:
        order = Order.objects.get(sotuvchi=sotuvchi)
        print(order.get_cart_total)
        qarz = order.orderqarz_set.all()
        data = {"wanted_day":[]}

        for i in qarz:
            if how_many_day != None:
                for j in range(how_many_day):
                    d = day1 - timedelta(days=j)
                    qarzitems = i.orderqarzitem_set.filter(bought_day=d)
                    [data['wanted_day'].append(QarzdorHistorySerializer(i).data) for i in qarzitems]
                    for k in qarzitems:
                        total_quantity += k.quantity
                        total_amount += k.umumiy_summa
                        qancha_qarz += k.umumiy_summa
                        if k.completed == True:
                            qancha_qarz -= k.umumiy_summa
            else:
                qarzitems = i.orderqarzitem_set.values()
                data["wanted_day"] += qarzitems
                total_quantity = order.get_cart_items
                total_amount = order.get_cart_total
                qancha_qarz += i.get_cart_total 
                
    except ObjectDoesNotExist:
        return Response({"status": "qarzdorlar yo'q"})         
    context = { 
        "umumiy_sotilgan_summa": total_amount,
        "nechi_marta_sotgan": total_quantity,
        # "nechi_marta_sotgan": total,
        # "bugungi_list": bugungi_list,
        "qancha_qarz": qancha_qarz,
        "data": data
    }
    return render(request, "pages/project-detail.html", context)


def people_edit(request):
    return render(request, "pages/project-edit.html")

def people_add(request):
    return render(request, "pages/project-add.html")


    