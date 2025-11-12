from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from .models import Usuario, Freteiro, solicitarFrete
from datetime import date
from django.contrib import messages
from .forms import UsuarioForm, FreteiroForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


#   NAO ESTOU UTILIZANDO O LOGIN_REQUIRED DO DJANGO, POIS ESTOU FAZENDO MINHA PRÓPRIA AUTENTICAÇÃO.
#   ENTÃO, PARA AS ROTAS QUE PRECISAM DE AUTENTICAÇÃO, ESTOU VERIFICANDO MANUALMENTE SE O USUÁRIO ESTÁ LOGADO.
# COM:   usuario_id = request.session.get('usuario_id')
#        if not usuario_id:
#           return redirect('login_user')
#   PARA ISSO, ESTOU ARMAZENANDO O ID DO USUÁRIO NA SESSÃO APÓS O LOGIN E VERIFICANDO ESSA INFORMAÇÃO NAS VIEWS.
#   SE O ID NÃO ESTIVER PRESENTE NA SESSÃO, O USUÁRIO SERÁ REDIRECIONADO PARA A TELA DE LOGIN.
#   ISSO É FEITO PARA AS ROTAS DE USUÁRIO E FRETEIRO QUE EXIGEM AUTENTICAÇÃO.
#   PARA A UTILIZAÇÃO DO LOGIN_REQUIRED DO DJANGO, SERIA NECESSÁRIO INTEGRAR O SISTEMA DE AUTENTICAÇÃO DO DJANGO,
#   O QUE NÃO FOI FEITO NESTE PROJETO.

# Create your views here.
def index(request):
    return render(request, 'index.html')



# Seção Usuário
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            usuario = Usuario.objects.get(email=email)
            if usuario.senha == senha:
                request.session['usuario_id'] = usuario.id
                return redirect('welcome_user')
            else:
                return render(request, 'tela_user.html', {
                    'erro': 'Senha incorreta',
                    'active': 'usuario'
                })
        except Usuario.DoesNotExist:
            return render(request, 'tela_user.html', {
                'erro': 'Usuário não encontrado',
                'active': 'usuario'
            })

    return render(request, 'tela_user.html', {'active': 'usuario'})


def cadastro_user(request):
    if request.method == 'POST':
        novo_usuario = Usuario()
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        tel = request.POST.get('tel')
        cpf = request.POST.get('cpf')
        
        # juntar os dados e formar a data_nascimento
        dia = request.POST.get('dia')
        mes = request.POST.get('mes')
        ano = request.POST.get('ano')
        
        data_nascimento = f"{ano}-{mes}-{dia}"
        novo_usuario.data_nascimento = data_nascimento
    
    
        novo_usuario.nome = nome
        novo_usuario.email = email
        novo_usuario.senha = senha
        novo_usuario.tel = tel
        novo_usuario.cpf = cpf
        
        novo_usuario.save()
        
        # verificar o que já foi cadastrado até o momento.
        # usuarios = { Usuario.objects.all() }
        # return render(request, 'listar_usuarios.html', {'usuarios': usuarios})
        return redirect('welcome_user')   

        
    return render(request, 'tela_cadastro_usuario.html')   
      
# tela inicial
def welcome_user(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login_user')

    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        request.session.flush()
        return redirect('login_user')

    return render(request, 'tela_inicial_usuario.html', {'usuario': usuario})

# Solicitar frete
def solicitar_frete(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login_user')

    if usuario_id != id:
        return redirect('welcome_user')

    usuario_logado = Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        novo_frete = solicitarFrete()
        novo_frete.produto = request.POST.get('produto')
        novo_frete.peso = request.POST.get('peso')
        novo_frete.largura = request.POST.get('largura')
        novo_frete.altura = request.POST.get('altura')
        novo_frete.valor = request.POST.get('valor')
        novo_frete.endereco_coleta = request.POST.get('endereco_coleta')
        novo_frete.endereco_entrega = request.POST.get('endereco_entrega')

        dia = request.POST.get('dia')
        mes = request.POST.get('mes')
        ano = request.POST.get('ano')
        novo_frete.data_entrega = f"{ano}-{mes}-{dia}"
        novo_frete.hora = request.POST.get('hora')
        novo_frete.usuario = usuario_logado
        novo_frete.save()

        return redirect('frete_concluido', id=usuario_id)


    return render(request, 'tela_solicitar_frete.html', {'usuario': usuario_logado})

# tela de frete após a sua conclusão
# apos o pedido de frete - o usuario virá para essa tela
def frete_concluido(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login_user')  # redireciona se não estiver logado

    usuario = Usuario.objects.get(id=usuario_id)
    fretes = solicitarFrete.objects.filter(usuario=usuario)
    
    return render(request, 'tela_frete_concluido.html', {
        'fretes': fretes
    })

#tela de notificações de frete e seus status de forma prévia (fretes já solicitados)
 ########## EM DESENVOLVIMENTO....
# lista os fretes solicitados pelo usuario
# def notificacoes_fretes(request):
#     usuario_id = request.session.get('usuario_id')
#     if not usuario_id:
#         return redirect('login_user')  # redireciona se não estiver logado

    


# verifica o status do frete escolhido
# o usuario vê o status do seu frete
def status_frete(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login_user')

    try:
        frete = solicitarFrete.objects.filter(usuario_id=usuario_id).last()
    except solicitarFrete.DoesNotExist:
        frete = None

    return render(request, 'tela_status_frete.html', {'frete': frete})



# Seção freteiro
def login_freteiro(request):
    return render(request, 'tela_motorista.html', {'active': 'motorista'})

@login_required
def welcome_freteiro(request):
    return render(request, 'tela_inicial_freteiro.html') 



def cadastro_freteiro(request):
    novo_freteiro = Freteiro()
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        tel = request.POST.get('tel')
        cpf = request.POST.get('cpf')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')
        # juntar os dados e formar a data_nascimento
        dia = request.POST.get('dia')
        mes = request.POST.get('mes')
        ano = request.POST.get('ano')
        
        if dia and mes and ano:
            try:
                data_nascimento = date(int(ano), int(mes), int(dia))
            except ValueError:
                data_nascimento = None  
        else:
            data_nascimento = None
            
        if not nome or not email or not senha or not cpf:
            return render(request, 'tela_cadastro_freteiro.html', {
                'erro': 'Preencha todos os campos obrigatórios.'
            })
        novo_freteiro.data_nascimento = data_nascimento

        novo_freteiro.nome = nome
        novo_freteiro.email = email
        novo_freteiro.senha = senha
        novo_freteiro.tel = tel
        novo_freteiro.cpf = cpf
        novo_freteiro.cidade = cidade
        novo_freteiro.estado = estado
    
        novo_freteiro.save()    
        return redirect('welcome_freteiro')

    return render(request, 'tela_cadastro_freteiro.html')  


# Administração geral
def listar_usuarios_geral(request):
    query = request.GET.get('q', '')  # pega o valor do campo de pesquisa

    if query:
        # Filtra por nome ou email contendo o texto
        usuarios = Usuario.objects.filter(
            nome__icontains=query
        ) | Usuario.objects.filter(
            email__icontains=query
        )
        freteiros = Freteiro.objects.filter(
            nome__icontains=query
        ) | Freteiro.objects.filter(
            email__icontains=query
        )
    else:
        
        freteiros = Freteiro.objects.all()
        usuarios = Usuario.objects.all()
        
    return render(request, 'administrar_usuarios.html', {
        'freteiros': freteiros,
        'usuarios': usuarios,
        'query': query
    })
        


def update_geral(request, id, tipo):
    if tipo == 'freteiro':
        post = get_object_or_404(Freteiro, id=id)
        form_class = FreteiroForm
    elif tipo == 'usuario':
        post = get_object_or_404(Usuario, id=id)
        form_class = UsuarioForm
    else:
        return redirect('listar_usuarios_geral')

    form = form_class(request.POST or None, request.FILES or None, instance=post)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('listar_usuarios_geral')

    return render(request, 'update.html', {
        'form': form,
        'tipo': tipo,
        'post': post
    })


def excluir_geral(request, id, tipo):
    if tipo == 'freteiro':
        post = get_object_or_404(Freteiro, id=id) #xconsulta de freteiro
    elif tipo == 'usuario':
        post = get_object_or_404(Usuario, id=id) # consulta de usuario
    else:
        return redirect('listar_usuarios_geral')

    if request.method == 'POST':
        post.delete()
        return redirect('listar_usuarios_geral')

    return render(request, 'delete.html', {
        'post': post,
        'tipo': tipo
    })
    
def listar_por_cidade(request, cidade):
    freteiros = Freteiro.objects.filter(cidade__iexact=cidade)
    return render(request, 'listar_por_cidade.html', {'freteiros': freteiros, 'cidade': cidade})
  

