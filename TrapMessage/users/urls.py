from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from . import views

app_name = "users"

urlpatterns = [
    path('list/', staff_member_required(views.UserListView.as_view()), name="user_list"),
    path('login/', views.LoginView.as_view(), name='login'),

    path('<int:pk>/', staff_member_required(views.UserDetailView.as_view()), name="user_details"),
    path('new/', staff_member_required(views.UserCreateView.as_view()), name="user_create"),
    path('<int:pk>/update/', staff_member_required(views.UserUpdateView.as_view()), name='user_update'),
    path('<int:pk>/admin_update/', staff_member_required(views.AdminUpdateView.as_view()), name='admin_update'),
    path('<int:pk>/delete/', staff_member_required(views.UserDeleteView.as_view()), name='user_delete'),

    path("<int:pk>/password_change/", views.password_change, name="password_change"),
]
