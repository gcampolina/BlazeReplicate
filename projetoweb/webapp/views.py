from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import CustomUser
from .forms import FotoPerfilForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'home.html')

def login_view(request):
    modal_show = False  # Começa com o modal não mostrando
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirecione para a página desejada após o login
            return redirect('home')
        else:
            messages.warning(request, 'Usuário ou senha inválido')
            modal_show = 'login'
    
    return render(request, 'home.html', {'modal_show': modal_show})


@login_required
def conta(request):
    if request.method == 'POST':
        form = FotoPerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('conta')  # Redireciona para a mesma página para ver as mudanças
    else:
        form = FotoPerfilForm(instance=request.user)

    # Passe tanto o formulário quanto o usuário para o contexto
    context = {'form': form, 'usuario': request.user}
    return render(request, 'conta.html', context)


def cadastro(request):
    modal_show = False  # Começa com o modal não mostrando

    if request.method == "POST":
        username = request.POST.get('username')
        nome = request.POST.get('name')
        email = request.POST.get('email')
        senha = request.POST.get('password')
        confirmacao_senha = request.POST.get('password2')

        if senha != confirmacao_senha:
            messages.warning(request, 'As senhas não coincidem.')
            modal_show = 'cadastro'

        else:
            user = CustomUser.objects.filter(username=username).first()

            if user:
                messages.warning(request, 'O usuário fornecido já está em uso.')
                modal_show = 'cadastro'
                
            else:
                user = CustomUser.objects.create_user(username=username, email=email, password=senha)
                user.first_name = nome
                user.save()
                return redirect('home')  # Redireciona para 'home' se o cadastro for bem-sucedido

    return render(request, 'home.html', {'modal_show': modal_show})
