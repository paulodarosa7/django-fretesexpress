from django.contrib import admin
from .models import Usuario, Freteiro, solicitarFrete

# Configurações do Admin para cada modelo

admin.site.register(Usuario)
admin.site.register(Freteiro)
admin.site.register(solicitarFrete)


#matar sessões?