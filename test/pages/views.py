from django.shortcuts import render
from mobile.models import OrderQarzItem, Sotuvchilar, Order, OrderQarz
from datetime import date
import datetime
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

def people_detail(request, id):
    order = Order.objects.get(sotuvchi=id)
    orderqarz = OrderQarz.objects.filter(order=order.id)
    qarz = order.orderqarz_set.all()
    bugungi_list = []
    today_total_price = 0
    for i in orderqarz:
        bugungili_sotilganlar = OrderQarzItem.objects.filter(orderQarz=i.id, bought_day=date.today())
        if(bugungili_sotilganlar):
            for j in bugungili_sotilganlar:
                today_total_price += j.umumiy_summa
                bugungi_list.append(j)
    total = 0
    total_amount = 0
    for i in qarz:
        total_amount += i.get_cart_total
        total += i.get_cart_items
    
    context = { 
        "umumiy_sotilgan_summa": total_amount,
        "nechi_marta_sotgan": total,
        "nechi_marta_sotgan": total,
        "bugungi_list": bugungi_list,
        "today_total_price": today_total_price
    }
    return render(request, "pages/project-detail.html", context)

def people_edit(request):
    return render(request, "pages/project-edit.html")

def people_add(request):
    return render(request, "pages/project-add.html")