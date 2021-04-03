from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from .forms import registrationForm
from .utils import *
from .models import History
from rest_framework import viewsets
from .serializers import HistorySerializer

# serialize faucet transactions


class HistoryViewSet(viewsets.ModelViewSet):

    queryset = History.objects.all()
    serializer_class = HistorySerializer


# login view

def logIn(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)
            return redirect("../")

    return render(request, 'login.html')

# registration view


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

# homepage with data about supply automatically updated at every transaction


def home(request):

    finish = endDate()
    supply = totalSupply()
    percentage = supply/10
    if request.method == "POST":
        transaction = request.POST.get("transaction");
        History.objects.create(contractTx=transaction)
        return redirect("/")
    return render(request, 'index.html', {'contractCreator': contractCreator,
                                          "supply": supply,
                                          "contractAddress": contractAddress,
                                          "percentage": percentage, "finish" : finish})

# faucet view to get test ether from the first Ganache account


def faucet(request):

    if request.method == 'POST':
        address = request.POST.get("address")
        ether = request.POST.get('getEther')
        tx = getEther(address, ether)
        messages.info(request, tx)
        return redirect("../")
    return render(request, 'faucet.html')

# profile view to get the current token balance of address


def profile(request):

    if request.method == 'POST':
        address = request.POST.get("address")
        balance = getBalance(address)
        if balance == 0:
            balance = "You haven't any token!"
            return render(request, 'profile.html', {'balance': balance})
        return render(request, 'profile.html', {'balance': balance})
    return render(request, 'profile.html')

# admin panel to control and modify the state of the ico


def adminPanel(request):

    return render(request, "admin.html", {"contractCreator" : contractCreator,
                                          "contractAddress" : contractAddress})

# page available only at the end of the sale where users can transfer their tokens to other own address on different platforms


def transferPage(request):

    return render(request, "transfer.html", {"contractAddress" : contractAddress})