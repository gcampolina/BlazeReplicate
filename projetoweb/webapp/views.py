from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
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

@login_required
def some_view(request):
    # Supõe-se que request.user seja o usuário logado
    context = {
        'saldo': request.user.saldo  # Acessa o saldo do usuário e passa para o template
    }
    return render(request, 'home.html', context)

@login_required
def alterar_senha(request):
    modal_show = False  # Inicialmente, o modal deve permanecer aberto
    if request.method == 'POST':
        senha_atual = request.POST.get('senha_atual')
        nova_senha = request.POST.get('nova_senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if nova_senha != confirmar_senha:
            messages.warning(request, 'As novas senhas não coincidem.')
            return redirect('conta')

        else:
            user = request.user
            if not user.check_password(senha_atual):
                messages.warning(request, 'A senha atual está incorreta.')
                return redirect('conta')
                

            else:
                user.set_password(nova_senha)
                user.save()
                # Atualize a sessão do usuário para manter a autenticação
                update_session_auth_hash(request, user)
                messages.success(request, 'Senha alterada com sucesso.')
                return redirect('conta')  # Redirecione apenas em caso de sucesso

    # Renderize a página 'conta' com o modal_show definido para manter o modal aberto
    return render(request, 'conta.html', {'modal_show': modal_show})





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
