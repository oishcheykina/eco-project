from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('upload-tree/', upload_tree_view, name='upload_tree'),
    path('profile/', profile, name='profile'),
    path('my_trees/', my_trees, name='my_trees'),
    path('tree/<int:tree_id>/', tree_detail, name='tree_detail'),
    path('register/', register_view, name='register'),
    path('login/', custom_login, name='login'),
    path('reset-password/', reset_password_view, name='reset_password'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('rules/', rules, name='rules'),
    path('eco-ranking/', ranking, name='eco_ranking'),
]