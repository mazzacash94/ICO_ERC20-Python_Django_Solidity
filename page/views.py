from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from .forms import registrationForm
from .utils import *
from .models import Wallet, History
from .forms import offerForm
from .serializers import HistorySerializer
from django.contrib.auth.models import User
from rest_framework import viewsets


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer


def logIn(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)
            return redirect("../")

    return render(request, 'login.html')


def registration(request):

    if request.method == 'POST':

        form = registrationForm(request.POST)

        if form.is_valid():

            form.save()
            users = User.objects.order_by("-date_joined")
            lastUser = User.objects.get(username=users[0])
            account = newAccount()
            Wallet.objects.create(user=lastUser, address=account[0], privateKey=account[1])
            return redirect('../')

        else:

            form = registrationForm()

    else:

        form = registrationForm()

    return render(request, "registration.html", {'form': form})

# consente ad utente di effettuare il logout dal sito


def logout(request):

    django_logout(request)

    return redirect("../")


def home(request):

    user = request.user
    form = offerForm(request.POST)
    supply = int(totalSupply())
    percentSupply = float(supply / 10)

    if user.is_authenticated:
        wallet = Wallet.objects.get(user=user)
        balanceEther = getBalanceEther(wallet.address)
        balanceToken = getBalanceToken(wallet.address)
        if request.method == "POST":
            if form.is_valid():
                offer = request.POST.get('offer')
                tx = buyToken(wallet.privateKey, int(offer), wallet.address, int(offer)/10)
                messages.info(request, tx)
                return redirect("/")
        else:
            form = offerForm()

        return render(request, 'index.html', {'form': form, 'wallet': wallet, 'balanceEther': balanceEther,
                      'balanceToken': balanceToken, 'supply': supply, 'percentSupply': percentSupply})

    return render(request, 'index.html', {'form': form, 'supply': supply, 'percentSupply': percentSupply})
