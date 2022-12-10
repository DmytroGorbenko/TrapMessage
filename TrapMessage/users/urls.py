from django.urls import path


from . import views

app_name = "users"

urlpatterns = [
    path('list/', views.UserListView.as_view(), name="user_list"),
    path('login/', views.LoginView.as_view(), name='login'),

    path('<int:pk>/', views.UserDetailView.as_view(), name="user_details"),
    path('new/', views.UserCreateView.as_view(), name="user_create"),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),

    path("<int:pk>/password_change/", views.password_change, name="password_change"),
]
