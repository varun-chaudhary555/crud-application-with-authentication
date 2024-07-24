from django.urls import path
from .views import home_view, register_view, login_view,logout_view, index, detail, create, update, delete,deactivate_account

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('index/', index, name='index'),
    path('note/<int:id>/', detail, name='detail'),
    path('note/create/', create, name='create'),
    path('note/update/<int:id>/', update, name='update'),
    path('note/delete/<int:id>/', delete, name='delete'),
    path('deactivate_account/', deactivate_account, name='deactivate_account'),
]
