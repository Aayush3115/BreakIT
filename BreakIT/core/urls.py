from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('group/create/', views.create_group, name='create_group'),
    path('group/<int:group_id>/expense/create/', views.create_expense, name='create_expense'),
    
]
