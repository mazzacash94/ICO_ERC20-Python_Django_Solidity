from . import views
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register("transactions", views.HistoryViewSet)

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.logIn, name="login"),
    path('registration', views.registration, name="registration"),
    path('logout', views.logout, name="logout"),
    path('faucet', views.faucet, name="faucet"),
    path('profile', views.profile, name="profile"),
    path('list/', include(router.urls)),
    path('admin', views.adminPanel, name="admin_panel"),
    path('transfer', views.transferPage, name="transfer")
]
