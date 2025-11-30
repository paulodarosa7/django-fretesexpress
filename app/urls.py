from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    
    # Rotas user
    path('user/login/', views.login_user, name='login_user'),
    path('user/cadastro/', views.cadastro_user, name='cadastro_user'),
    path('user/welcome/', views.welcome_user, name='welcome_user'),
    
    
    #NAVBAR USUARIO
    path('user/perfil/<int:id>/', views.perfil_user, name='perfil_user'),
    path('user/perfil/<int:id>/editar/', views.editar_perfil_user, name='editar_perfil_user'),
    path('user/<int:id>/meus/fretes/', views.fretes_solicitados, name='fretes_solicitados'),
    
    
    
    #solicitar frete
    # path('user/fretes/historico/', views.fretes_solicitados, name='fretes_solicitados'),
    path('user/<int:id>/fretes/solicitar/', views.solicitar_frete, name='solicitar_frete'),
    path('user/<int:id>/frete/concluido/', views.frete_concluido, name='frete_concluido'),
    path('frete/<int:frete_id>/status/', views.status_frete, name='status_frete'),
    path('frete/<int:frete_id>/editar/', views.editar_frete, name='editar_frete'),
    path('frete/<int:frete_id>/cancelar/', views.cancelar_frete, name='cancelar_frete'),
    
    
    
    # rotas freteiro
    path('motorista/login/', views.login_freteiro, name='login_freteiro'),
    path('motorista/cadastro/', views.cadastro_freteiro, name='cadastro_freteiro'),
    path('motorista/welcome/', views.welcome_freteiro, name='welcome_freteiro'),
    
    #NAVBAR FRETEIRO
    path('freteiro/perfil/<int:id>/', views.perfil_freteiro, name='perfil_freteiro'),
    path('freteiro/perfil/<int:id>/editar/', views.editar_perfil_freteiro, name='editar_perfil_freteiro'),
    
    
    # aceitar frete
    path('motorista/fretes/disponiveis/', views.fretes_disponiveis, name='fretes_disponiveis'),
    path('motorista/frete/<int:frete_id>/aceitar/', views.aceitar_frete, name='aceitar_frete'),
    path('motorista/fretes/status/<int:frete_id>', views.status_frete, name='status_frete_freteiro'),
    path('motorista/<int:id>/meus/fretes/', views.fretes_aceitos, name='fretes_aceitos'),
    path('motorista/<int:id>/recusar/frete/<int:frete_id>/', views.recusar_frete, name='recusar_frete'),


    #SAIR
    path('logout/', views.logout, name='logout'),

    #CALCULO DA ROTA
    path('frete/<int:frete_id>/calcular/rota/', views.calcular_rota, name='calcular_rota'),



]