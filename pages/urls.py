from django.urls import path
from pages import views

urlpatterns = [
    path('', views.home, name="home"),
    path('chart/', views.chart, name="chart"),
    path('table/', views.table, name="table"),
    path('table2/', views.table1, name="table1"),
    path('people/', views.people, name="people"),
    path('people/<int:id>', views.people_detail, name="people_detail"),
]