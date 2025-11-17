from django.db import models

# Create your models here.
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    tel = models.CharField(max_length=15)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField(null=True, blank=True)


    def __str__(self):
        return self.nome

class Freteiro(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    tel = models.CharField(max_length=15, blank=True, null=True)
    cpf = models.CharField(max_length=14, unique=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    data_nascimento = models.DateField(null=True, blank=True)
    
class solicitarFrete(models.Model):
    produto = models.CharField(max_length=100)
    peso = models.FloatField()
    largura = models.FloatField()
    altura = models.FloatField()
    valor = models.FloatField()
    endereco_coleta = models.CharField(max_length=200)
    endereco_entrega = models.CharField(max_length=200)
    data_solicitacao = models.DateField(auto_now_add=True)
    hora_solicitacao = models.TimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=20, default="pendente") # determina o status atual do frete
    freteiro = models.ForeignKey("Freteiro", null=True, blank=True, on_delete=models.SET_NULL) # chave estrangeira de freteiro, para o mesmo poder aceitar um frete
                                                                                               #  de um requerente. Se está nulo é porque ninguem aceirou a corrida     


    def __str__(self):
        return self.produto