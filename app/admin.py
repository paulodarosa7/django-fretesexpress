from django.contrib import admin
from .models import Usuario, Freteiro, solicitarFrete

# Configurações do Admin para cada modelo
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'tel', 'cpf', 'data_nascimento')
    search_fields = ('nome', 'email', 'cpf', 'tel')
    list_filter = ('data_nascimento',)

@admin.register(Freteiro)
class FreteiroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'tel', 'cpf', 'cidade', 'estado', 'data_nascimento')
    search_fields = ('nome', 'email', 'cpf', 'tel', 'cidade', 'estado')
    list_filter = ('cidade', 'estado')

@admin.register(solicitarFrete)
class SolicitarFreteAdmin(admin.ModelAdmin):
    list_display = ('id', 'produto', 'usuario', 'freteiro', 'status', 'data_solicitacao', 'hora_solicitacao', 'valor')
    search_fields = ('produto', 'usuario__nome', 'freteiro__nome', 'status', 'endereco_coleta', 'endereco_entrega')
    list_filter = ('status', 'data_solicitacao')


#matar sessões?