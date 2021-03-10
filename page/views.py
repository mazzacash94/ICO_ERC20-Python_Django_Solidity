from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from .forms import registrationForm
from .utils import *
from .models import Wallet, History
from .forms import purchaseForm
from rest_framework import viewsets
from .serializers import HistorySerializer
from django.contrib.auth.models import User


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
    form = purchaseForm(request.POST)
    supply = int(totalSupply())
    percentSupply = float(supply / 10)

    if user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                offer = request.POST.get('offer')
                address = request.POST.get('address')
                tx = buyToken(int(offer), address)
                messages.info(request, tx)
        else:
            form = purchaseForm()

        return render(request, 'index.html', {'form': form, 'supply': supply, 'percentSupply': percentSupply, 'contractCreator': contractCreator, 'contractAddress': contractAddress})

    return render(request, 'index.html', {'form': form, 'supply': supply, 'percentSupply': percentSupply, 'contractCreator': contractCreator, 'contractAddress': contractAddress})

def faucet(request):

    if request.method == 'POST':
        getEther(request.POST.get("address"), request.POST.get('ether'))
        return redirect("../")
    return render(request, 'faucet.html')



