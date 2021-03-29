from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from .forms import registrationForm
from .utils import *
from .models import History
from rest_framework import viewsets
from .serializers import HistorySerializer


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

    supply = totalSupply()
    percentage = supply/10
    return render(request, 'index.html', {'contractCreator': contractCreator,
                                          "supply": supply,
                                          "contractAddress": contractAddress,
                                          "percentage": percentage,})


def faucet(request):

    if request.method == 'POST':
        address = request.POST.get("address")
        ether = request.POST.get('getEther')
        tx = getEther(address, ether)
        messages.info(request, tx)
        return redirect("../")
    return render(request, 'faucet.html')


def profile(request):

    if request.method == 'POST':
        address = request.POST.get("address")
        balance = getBalance(address)
        if balance == 0:
            balance = "You haven't any token!"
            return render(request, 'profile.html', {'balance': balance})
        return render(request, 'profile.html', {'balance': balance})
    return render(request, 'profile.html')
