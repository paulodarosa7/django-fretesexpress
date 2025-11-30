from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from .models import Usuario, Freteiro, solicitarFrete
from datetime import date
from django.contrib import messages
from .forms import UsuarioForm, FreteiroForm, FreteForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json



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
                    'erro': 'erro',
                    'active': 'usuario' #ativa o botao usuario
                })
        except Usuario.DoesNotExist:
            return render(request, 'tela_user.html', {
                'erro': 'erro',
                'active': 'usuario'
            })

    return render(request, 'tela_user.html', {
        'active': 'usuario'
        })


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
        request.session['usuario_id'] = novo_usuario.id
        return redirect('welcome_user')   

        
    return render(request, 'tela_cadastro_usuario.html')   
      
# tela inicial
def welcome_user(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login_user')
    
    usuario = Usuario.objects.get(id=usuario_id)

    return render(request, 'tela_inicial_usuario.html', {
        'usuario': usuario
    })
    


# NAVBAR DO USUARIO
# perfil do usuario
def perfil_user(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login_user')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    return render(request, 'perfil/perfil_user.html', {
        'usuario': usuario
    })


# editar perfil do usuario
def editar_perfil_user(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login_user')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == "POST":
        usuario.nome = request.POST.get("nome")
        usuario.email = request.POST.get("email")
        usuario.tel = request.POST.get("tel")
        usuario.save()

        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect('perfil_user', id=usuario_id)

    return render(request, 'perfil/editar_perfil_user.html', {
        'usuario': usuario
    })


def solicitar_frete(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login_user')

    if usuario_id != id: #impede que um usuario acesse outro pela URL
        return redirect('welcome_user')

    usuario_logado = Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        frete = solicitarFrete()

        frete.produto = request.POST.get('produto')
        frete.peso = request.POST.get('peso')
        frete.largura = request.POST.get('largura')
        frete.altura = request.POST.get('altura')
        frete.comprimento = request.POST.get('comprimento')
        frete.valor = request.POST.get('valor')
        frete.endereco_coleta = request.POST.get('endereco_coleta')
        frete.endereco_entrega = request.POST.get('endereco_entrega')
        frete.hora_solicitacao = request.POST.get('hora_solicitacao')

        dia = request.POST.get('dia')
        mes = request.POST.get('mes')
        ano = request.POST.get('ano')

        data_solicitacao = date(int(ano), int(mes), int(dia))
        
        if data_solicitacao < date.today():
            return render(request, 'tela_solicitar_frete.html', {
                    'usuario': usuario_logado,  
                    'erro': 'erro',
                })
        frete.data_solicitacao = data_solicitacao
        frete.hora_solicitacao = request.POST.get('hora_solicitacao')


        frete.status = "pendente"
        frete.usuario = usuario_logado

        frete.save()
        return redirect('frete_concluido', id=usuario_id)

    return render(request, 'tela_solicitar_frete.html', {
        'usuario': usuario_logado
        })


# tela de frete após a sua conclusão
# apos o pedido de frete - o usuario virá para essa tela
def frete_concluido(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login_user')  # redireciona se não estiver logado

    usuario = Usuario.objects.get(id=usuario_id)
    frete = solicitarFrete.objects.filter(usuario=usuario).last()
    
    return render(request, 'tela_frete_concluido.html', {
        'frete': frete
    })

def fretes_solicitados(request, id):
    # confirma se o usuário está logado
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login_user')

    # impede acessar fretes de outro usuário pela URL
    if usuario_id != id:
        return redirect('login_user')

    usuario = Usuario.objects.get(id=usuario_id)
    # esta causando problemas de misturar os cancelados com os ativos
    fretes = solicitarFrete.objects.filter(usuario=usuario).order_by('-data_solicitacao')

    return render(request, 'tela_fretes_solicitados.html', {
        'fretes': fretes,
        'usuario': usuario
    })

# verifica o status do frete escolhido
# o usuario vê o status do seu frete
def status_frete(request, frete_id):
    # verifica login
    usuario_id = request.session.get('usuario_id')
    freteiro_id = request.session.get('freteiro_id')

    if not usuario_id and not freteiro_id:
        return redirect('login_user')

    frete = get_object_or_404(solicitarFrete, id=frete_id)
    #para usuario
    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)
        return render(request, 'status_frete_usuario.html', {
            'frete': frete,
            'usuario': usuario
        })
    #para freteiro
    if freteiro_id:
        freteiro = Freteiro.objects.get(id=freteiro_id)
        return render(request, 'status_frete_freteiro.html', {
            'frete': frete,
            'freteiro': freteiro

        })
    
#usuario cancela o frete
def cancelar_frete(request, frete_id):
    usuario_id = request.session.get('usuario_id') # verifica se o freteiro está logado
    if not usuario_id:
        return redirect('login_user')

    frete = get_object_or_404(solicitarFrete, id=frete_id)

    frete.status = "cancelado"
    frete.save()

    return redirect('fretes_solicitados',  id=request.session.get('usuario_id'))

#usuario edita o frete
def editar_frete(request, frete_id):
    usuario_id = request.session.get('usuario_id') # verifica se o freteiro está logado
    if not usuario_id:
        return redirect('login_user')
    
    novo_frete = get_object_or_404(solicitarFrete, id=frete_id)
    
    if request.method == "POST":
        novo_frete.produto = request.POST.get("produto")
        novo_frete.peso = request.POST.get("peso")
        novo_frete.largura = request.POST.get("largura")
        novo_frete.altura = request.POST.get("altura")
        novo_frete.comprimento = request.POST.get("comprimento")
        novo_frete.endereco_coleta = request.POST.get("endereco_coleta")
        novo_frete.endereco_entrega = request.POST.get("endereco_entrega")
        
        novo_frete.dia = request.POST.get('dia')
        novo_frete.mes = request.POST.get('mes')
        novo_frete.ano = request.POST.get('ano')
        
        nova_data_solicitacao = date(int(novo_frete.ano), int(novo_frete.mes), int(novo_frete.dia))
           
        if nova_data_solicitacao < date.today():
            return render(request, 'tela_editar_frete.html', {
                    'frete': novo_frete,
                    'erro': 'erro'
                })
    
        novo_frete.data_solicitacao = nova_data_solicitacao
        novo_frete.hora_solicitacao = request.POST.get("hora_solicitacao")
        novo_frete.peso = request.POST.get("peso")
        novo_frete.save()
        return redirect('fretes_solicitados',  id=request.session.get('usuario_id'))
    return render(request, 'tela_editar_frete.html',  {
        'frete': novo_frete
    })
        

# interação entre usuarios e freteiros
# sessão de escolha de fretes
def fretes_disponiveis(request):
    
    freteiro_id = request.session.get('freteiro_id') # verifica se o freteiro está logado
    if not freteiro_id:
        return redirect('login_freteiro')
    
    fretes = solicitarFrete.objects.filter(status="pendente")
    
    return render(request, 'tela_fretes_disponiveis.html', {
        'fretes': fretes
        })



# Sessão freteiro
def login_freteiro(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            freteiro = Freteiro.objects.get(email=email)
            if freteiro.senha == senha:
                request.session['freteiro_id'] = freteiro.id
                return redirect('welcome_freteiro')
            else:
                return render(request, 'tela_motorista.html', {
                    'erro': 'Senha incorreta',
                    'active': 'motorista' #ativa o botao motorista
                })
        except Freteiro.DoesNotExist:
            return render(request, 'tela_motorista.html', {
                'erro': 'Freteiro não encontrado',
                'active': 'motorista'
            })
    return render(request, 'tela_motorista.html', {
        'active': 'motorista'
        })

def welcome_freteiro(request):
    freteiro_id = request.session.get('freteiro_id')
    if not freteiro_id:
        return redirect('login_freteiro')

    freteiro = Freteiro.objects.get(id=freteiro_id)
 
    return render(request, 'tela_inicial_freteiro.html', {
        'freteiro': freteiro
        })


def perfil_freteiro(request, id):
    freteiro_id = request.session.get('freteiro_id')
    if not freteiro_id:
        return redirect('login_freteiro')

    freteiro = get_object_or_404(Freteiro, id=freteiro_id)

    return render(request, 'perfil/perfil_freteiro.html', {'freteiro': freteiro})

def editar_perfil_freteiro(request, id):
    freteiro_id = request.session.get('freteiro_id')
    if not freteiro_id:
        return redirect('login_user')

    freteiro = get_object_or_404(Freteiro, id=freteiro_id)

    if request.method == "POST":
        freteiro.nome = request.POST.get("nome")
        freteiro.email = request.POST.get("email")
        freteiro.tel = request.POST.get("tel")
        freteiro.cidade = request.POST.get("cidade")
        freteiro.estado = request.POST.get("estado")
        freteiro.save()

        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect('perfil_freteiro', freteiro_id)

    return render(request, 'perfil/editar_perfil_freteiro.html', {'freteiro': freteiro})


def cadastro_freteiro(request):
    novo_freteiro = Freteiro()
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        confirmar_email = request.POST.get('confirmar_email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        tel = request.POST.get('tel')
        cpf = request.POST.get('cpf')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')
        # juntar os dados e formar a data_nascimento
        dia = request.POST.get('dia')
        mes = request.POST.get('mes')
        ano = request.POST.get('ano')
        
        data_nascimento = f"{ano}-{mes}-{dia}"
        novo_freteiro.data_nascimento = data_nascimento
        novo_freteiro.nome = nome
        novo_freteiro.email = email
        novo_freteiro.senha = senha
        novo_freteiro.tel = tel
        novo_freteiro.cpf = cpf
        novo_freteiro.cidade = cidade
        novo_freteiro.estado = estado
    
        novo_freteiro.save() 
        request.session['freteiro_id'] = novo_freteiro.id
        return redirect('welcome_freteiro')

    return render(request, 'tela_cadastro_freteiro.html')  

# fretes e freteiros
def aceitar_frete(request, frete_id):
    freteiro_id = request.session.get('freteiro_id')
    if not freteiro_id:
        return redirect('login_freteiro')

    frete = get_object_or_404(solicitarFrete, id=frete_id)

    if frete.status == "pendente":
        frete.status = "aceito"
        frete.freteiro_id = freteiro_id
        frete.save()
        return render(request, 'status_frete_freteiro.html', {
            'frete': frete,
        })
    else:
        return render(request, 'tela_fretes_disponiveis.html', {
            'frete': frete,
            'erro': f"Puts, acho que esse frete não está disponível. Status atual: {frete.status}"
        })



# ver fretes em andamento
def fretes_aceitos(request, id):
    # confirma se o usuário está logado
    freteiro_id = request.session.get('freteiro_id')
    if not freteiro_id:
        return redirect('login_user')

    # impede acessar fretes de outro usuário pela URL
    if freteiro_id != id:
        return redirect('login_user')

    freteiro = Freteiro.objects.get(id=freteiro_id) # pega id para que ele veja apenas os seus fretes

    fretes = solicitarFrete.objects.filter(freteiro=freteiro).order_by('data_solicitacao') #ordena os recentes por primeiro

    return render(request, 'tela_fretes_solicitados.html', {
        'fretes': fretes,
        'freteiro': freteiro
    })

def recusar_frete(request, id, frete_id):
    freteiro_id = request.session.get('freteiro_id')
    if not freteiro_id:
        return redirect('login_user')

    frete = get_object_or_404(solicitarFrete, id=frete_id)

    # impede recusar frete que não pertence ao freteiro
    if frete.freteiro_id != freteiro_id:
        return redirect('fretes_aceitos', freteiro_id)

    # remover o freteiro e voltar para fila
    frete.freteiro = None
    frete.status = "pendente"
    frete.save()

    return redirect('fretes_aceitos', id=freteiro_id)

  #logoff
def logout(request):
    request.session.flush()
    return redirect('login_user')


#Calcular rota
def calcular_rota(request, frete_id):    

    frete = solicitarFrete.objects.get(id=frete_id)


#dados frete
    data = json.loads(request.body) #  recebe os dados do javascript
    peso_bruto = float(frete.peso)  # em kg
    comprimento = float(frete.comprimento) 
    altura =  float(frete.altura) 
    largura = float(frete.largura) # em kg    
    distancia = float(data.get("distancia_km"))

    
    #calcular frete    
    #converter cm p m
    comprimento = comprimento / 100
    altura = altura / 100
    largura = largura / 100
        
    peso_cubado =  comprimento * altura * largura * 300  # fórmula do peso cubado em kg

    # determina o peso efetivo pelo maior peso
    peso_efetivo = max(peso_bruto, peso_cubado)
    
    peso_minimo = 20  # peso mínimo em kg
    peso_excedente=max(0, peso_efetivo-20)
    
    custo_km = 2.00  # custo por km
    custo_p_kg = 0.50  # custo por kg acima do peso mínimo (20kg)
    preco_minimo = 50.00  # custo mínimo do frete
    
    valor_custo = (distancia * custo_km) + (peso_excedente * custo_p_kg)
    print(valor_custo)
    if valor_custo < preco_minimo:
        valor_custo = preco_minimo
        
    if distancia <= 2:
        valor_custo = preco_minimo  # taxa adicional para distâncias curtas
    frete.distancia_km = distancia
    frete.custo_frete = valor_custo
    frete.save()

    return JsonResponse({
        'success': True,
        'valor_custo': valor_custo
    })


#apresenta a rota e custo
