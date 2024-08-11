from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_all),
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('signup/', views.user_signup),
    path('create/',views.create_student),
    path('view/<int:student_id>', views.view_student),
    path('delete/<int:student_id>/', views.delete_item),

    #rest api
    path('api/students/', views.student_list),
    path('api/students/<int:pk>/', views.student_detail),
]