from django.urls import path
from mobile import views

urlpatterns = [
    path('mobile/', views.snippet_list),
    path('mobile/<int:pk>/', views.snippet_detail),

    path('enter_data/', views.enter_data),
    path('get_aptekalar_list/', views.get_aptekalar_list),
    path('add_apteka/', views.add_aptekalar),
    path('sotuvchilar_list/', views.sotuvchilar_list),
    path('dorilar_list/', views.dorilar_list),
    path('store/', views.store),
    path('sotuvchi/', views.sotuvchi),
    path('sotuvchi/qarzdorlar/', views.sotuvchi_qarzdorlari),
    path('sotuvchi/qarzdorlar/tolash/', views.sotuvchi_qarzdor_tolov),
    path('sotuvchi/qarzdorlar/history/', views.sotuvchi_qarzdor_history),
    path('sotuvchi/apteka/history/', views.sotuvchi_apteka_history),
    path('sotuvchi/single_day_statistics/', views.statistics_for_single_day),
]