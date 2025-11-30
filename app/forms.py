from django import forms

from .models import Usuario, Freteiro, solicitarFrete

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'senha', 'tel', 'cpf', 'data_nascimento']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }
        
class FreteiroForm(forms.ModelForm):
    class Meta:
        model = Freteiro
        fields = ['nome', 'email', 'senha', 'tel', 'cpf', 'data_nascimento', 'cidade', 'estado']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }
    
class FreteForm(forms.ModelForm):
    class Meta:
        model = solicitarFrete
        fields = ['produto', 'peso', 'largura', 'comprimento','altura', 'valor', 'endereco_coleta', 'endereco_entrega']
        widgets = {
            'produto': forms.Textarea(attrs={'rows': 2}),
            'endereco_coleta': forms.Textarea(attrs={'rows': 2}),
            'endereco_entrega': forms.Textarea(attrs={'rows': 2})
        }

