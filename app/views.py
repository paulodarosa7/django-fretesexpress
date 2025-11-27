from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from .models import Usuario, Freteiro, solicitarFrete
from datetime import date
from django.contrib import messages
from .forms import UsuarioForm, FreteiroForm, FreteForm
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
                    'erro': 'erro',
                    'active': 'usuario'
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

    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        request.session.flush()
        return redirect('login_user')

    return render(request, 'tela_inicial_usuario.html', {'usuario': usuario})


# NAVBAR DO USUARIO
# perfil do usuario
def perfil_user(request, id):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login_user')

    usuario = get_object_or_404(Usuario, id=usuario_id)

    return render(request, 'perfil/perfil_user.html', {'usuario': usuario})


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

    return render(request, 'perfil/editar_perfil_user.html', {'usuario': usuario})


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

        try:
            data_solicitacao = date(int(ano), int(mes), int(dia))
        except ValueError:
            messages.error(request, "Data inválida. Verifique o dia, mês e ano.")
            return redirect('solicitar_frete', id=usuario_id)

        if data_solicitacao < date.today():
            messages.error(request, "A data de entrega não pode ser no passado.")
            return redirect('solicitar_frete', id=usuario_id)

        novo_frete.data_solicitacao = data_solicitacao

        novo_frete.hora_solicitacao = request.POST.get('hora_solicitacao')


        novo_frete.status = "pendente"
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


#tela de notificações de frete e seus status de forma prévia (fretes já solicitados)
 ########## EM DESENVOLVIMENTO....
# lista os fretes solicitados pelo usuario
# def notificacoes_fretes(request):
#     usuario_id = request.session.get('usuario_id')
#     if not usuario_id:
#         return redirect('login_user')  # redireciona se não estiver logado

# verifica o status do frete escolhido
# o usuario vê o status do seu frete
def status_frete(request, frete_id):
    usuario_id = request.session.get('usuario_id')
    freteiro_id = request.session.get('freteiro_id')

    if not usuario_id and not freteiro_id:
        return redirect('login_user')

    frete = get_object_or_404(solicitarFrete, id=frete_id)
    #para usuario
    
    usuario = None
    freteiro = None
    
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
    freteiro_id = request.session.get('freteiro_id') # verifica se o freteiro está logado
    if not freteiro_id:
        return redirect('login_freteiro')

    frete = get_object_or_404(solicitarFrete, id=frete_id)

    if frete.status in ["concluido", "cancelado"]:
        messages.error(request, "Este frete já foi encerrado!")
        return redirect('listar_fretes')

    frete.status = "cancelado"
    frete.save()

    messages.success(request, "Frete cancelado com sucesso!")
    return redirect('fretes_solicitados',  id=request.session.get('usuario_id'))

#usuario edita o frete
def editar_frete(request, frete_id):
    usuario_id = request.session.get('usuario_id') # verifica se o freteiro está logado
    if not usuario_id:
        return redirect('login_user')
    
    frete = get_object_or_404(solicitarFrete, id=frete_id)
    
    if request.method == "POST":
        frete.produto = request.POST.get("produto")
        frete.peso = request.POST.get("peso")
        frete.largura = request.POST.get("largura")
        frete.altura = request.POST.get("altura")
        frete.endereco_coleta = request.POST.get("endereco_coleta")
        frete.endereco_entrega = request.POST.get("endereco_entrega")
        
        frete.dia = request.POST.get('dia')
        frete.mes = request.POST.get('mes')
        frete.ano = request.POST.get('ano')
        try:
            nova_data_solicitacao = date(int(frete.ano), int(frete.mes), int(frete.dia))
        except ValueError:
            messages.error(request, "Data inválida. Verifique o dia, mês e ano.")
            return redirect('editar_frete', frete_id=frete_id)

        if nova_data_solicitacao < date.today():
            messages.error(request, "A data de entrega não pode ser no passado.")
            return redirect('editar_frete', frete_id=frete_id)   
        
        frete.data_solicitacao = nova_data_solicitacao
        frete.hora_solicitacao = request.POST.get("hora_solicitacao")
        frete.peso = request.POST.get("peso")
        frete.save()
        return redirect('fretes_solicitados',  id=request.session.get('usuario_id'))
    return render(request, 'tela_editar_frete.html',  {'frete': frete})
        

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
                    'active': 'freteiro'
                })
        except Freteiro.DoesNotExist:
            return render(request, 'tela_motorista.html', {
                'erro': 'Freteiro não encontrado',
                'active': 'freteiro'
            })
    return render(request, 'tela_motorista.html', {
        'active': 'motorista'
        })

def welcome_freteiro(request):
    freteiro_id = request.session.get('freteiro_id')
    if not freteiro_id:
        return redirect('login_freteiro')

    try:
        freteiro = Freteiro.objects.get(id=freteiro_id)
    except Freteiro.DoesNotExist:
        request.session.flush()
        return redirect('login_freteiro')

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
        
        if dia and mes and ano:
            try:
                data_nascimento = date(int(ano), int(mes), int(dia))
            except ValueError:
                data_nascimento = None  
        else:
            data_nascimento = None
            
        # if not nome or not email or not senha or not cpf:
        #     return render(request, 'tela_cadastro_freteiro.html', {
        #         'erro': 'Preencha todos os campos obrigatórios.'
        # })
        
        # # validar email duplicado
        # if Freteiro.objects.filter(email=email).exists():
        #     return render(request, 'tela_cadastro_freteiro.html', {
        #         'erro': 'Email já cadastrado.'
        # })

        # # validar cpf duplicado
        # if Freteiro.objects.filter(cpf=cpf).exists():
        #     return render(request, 'tela_cadastro_freteiro.html', {
        #         'erro': 'CPF já cadastrado.'
        # })

        # # validar telefone duplicado
        # if tel and Freteiro.objects.filter(tel=tel).exists():
        #     return render(request, 'tela_cadastro_freteiro.html', {
        #         'erro': 'Telefone já cadastrado.'
        # })

        # # validar email = confirmar email
        # if email != confirmar_email:
        #     return render(request, 'tela_cadastro_freteiro.html', {
        #         'erro': 'Os emails não coincidem.'
        # })

        # # validar senha = confirmar senha
        # if senha != confirmar_senha:
        #     return render(request, 'tela_cadastro_freteiro.html', {
        #         'erro': 'As senhas não coincidem.'
        # })
        
            
        # hoje = date.today()
        
        # # calcular idade + 18 anos
        # idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day)) 
        
        # if idade < 18:
        #     return render(request, 'tela_cadastro_freteiro.html', {
        #         'erro': 'Você deve ter pelo menos 18 anos para se cadastrar como freteiro.'
        #     })
        
            
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
from django.shortcuts import render, redirect, get_object_or_404
from .models import solicitarFrete

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

    freteiro = Freteiro.objects.get(id=freteiro_id)

    fretes = solicitarFrete.objects.filter(freteiro=freteiro).order_by('-data_solicitacao')

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
        messages.error(request, "Você não tem permissão para recusar este frete.")
        return redirect('fretes_aceitos', freteiro_id)

    # remover o freteiro e voltar para fila
    frete.freteiro = None
    frete.status = "pendente"
    frete.save()

    messages.success(request, "Frete recusado com sucesso!")
    return redirect('fretes_aceitos', id=freteiro_id)


# gestão de fretes
def listar_fretes(request):
    usuario_id = request.session.get('usuario_id')
    freteiro_id = request.session.get('freteiro_id')

    # ADMIN / SUPORTE
    if not usuario_id and not freteiro_id:
        fretes = solicitarFrete.objects.all()
        return render(request, 'gestao_fretes/fretes_listar.html', {'fretes': fretes})

    # USUÁRIO
    if usuario_id:
        fretes = solicitarFrete.objects.filter(usuario_id=usuario_id)
        return render(request, 'gestao_fretes/fretes_listar.html', {'fretes': fretes})

    # FRETEIRO
    if freteiro_id:
        fretes = solicitarFrete.objects.filter(freteiro_id=freteiro_id)
        return render(request, 'gestao_fretes/fretes_listar.html', {'fretes': fretes})
    
    
# def atualizar_frete(request, id):
#     frete = get_object_or_404(solicitarFrete, id=id)

#     if request.method == "POST":
#         form = FreteForm(request.POST, instance=frete)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Frete atualizado com sucesso!")
#             return redirect('listar_fretes')
#     else:
#         form = FreteForm(instance=frete)

#     return render(request, 'gestao_fretes/fretes_editar.html', {'form': form, 'frete': frete})


# def cancelar_frete(request, id):
#     frete = get_object_or_404(solicitarFrete, id=id)

#     if frete.status in ["concluido", "cancelado"]:
#         messages.error(request, "Este frete já foi encerrado!")
#         return redirect('listar_fretes')

#     frete.status = "cancelado"
#     frete.save()

#     messages.success(request, "Frete cancelado com sucesso!")
#     return redirect('listar_fretes')

# def excluir_frete(request, id):
#     frete = get_object_or_404(solicitarFrete, id=id)

#     if frete.status in ["concluido", "cancelado"]:
#         messages.error(request, "Fretes concluídos/cancelados não podem ser excluídos.")
#         return redirect('listar_fretes')

#     if request.method == "POST":
#         frete.delete()
#         messages.success(request, "Frete excluído com sucesso!")
#         return redirect('listar_fretes')

#     return render(request, 'gestao_fretes/fretes_excluir.html', {
#         'frete': frete,
#     })


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
        
    return render(request, 'gestao_usuarios/administrar_usuarios.html', {
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

    return render(request, 'gestao_usuarios/update.html', {
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

    return render(request, 'gestao_usuarios/delete.html', {
        'post': post,
        'tipo': tipo
    })
    

  #logoff
def logout(request):
    request.session.flush()
    return redirect('login_user')


#Calcular rota
def calcular_rota(request, frete_id):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Exemplo: pegar o frete correspondente
        try:
            frete = Frete.objects.get(id=frete_id)
        except Frete.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Frete não encontrado'})

        # Salvar a rota associada ao frete
        Rota.objects.create(
            frete=frete,  # se você tiver FK
            origem=data['origem'],
            destino=data['destino'],
            distancia=float(data['distancia']),
            custo=float(data['custo']),
            tempo_minutos=int(data['tempoMinutos'])
        )

        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

#apresenta a rota e custo
