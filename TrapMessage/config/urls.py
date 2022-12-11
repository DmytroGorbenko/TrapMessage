from django.urls import path
from . import views

app_name = "config"

urlpatterns = [
    path('list/', views.ConfigListView.as_view(), name="config_list"),
    path('<int:pk>/', views.ConfigDetailView.as_view(), name="config_details"),
    path('new/', views.ConfigCreateView.as_view(), name="config_create"),
    path('<int:pk>/update/', views.ConfigUpdateView.as_view(), name='config_update'),
    path('<int:pk>/delete/', views.ConfigDeleteView.as_view(), name='config_delete'),

    path('<int:pk>/send/', views.send, name='send'),
    path('send_list/', views.send_list, name='send_list'),
]
