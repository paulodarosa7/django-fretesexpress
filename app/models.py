from django.db import models

# Create your models here.
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    tel = models.CharField(max_length=15)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    
    def __str__(self):
        return self.nome

class Freteiro(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)
    tel = models.CharField(max_length=15,)
    cpf = models.CharField(max_length=14, unique=True)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    data_nascimento = models.DateField()
    
    def __str__(self):
        return self.nome
    
class solicitarFrete(models.Model):
    produto = models.CharField(max_length=100)
    peso = models.FloatField()
    largura = models.FloatField()
    altura = models.FloatField()
    comprimento = models.FloatField()
    valor = models.FloatField()
    endereco_coleta = models.CharField(max_length=200)
    endereco_entrega = models.CharField(max_length=200)
    data_solicitacao = models.DateField(null=False)
    hora_solicitacao = models.TimeField(null=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    distancia_km = models.FloatField(null=True)
    custo_frete = models.FloatField(null=True)  
    # tempo_frete = models.CharField(max_length=50, null=True) 
    
    status = models.CharField(max_length=20, default="pendente") # determina o status atual do frete
    # um para muitos
    freteiro = models.ForeignKey("Freteiro", null=True, on_delete=models.SET_NULL)  # chave estrangeira de freteiro, para o mesmo poder aceitar um frete
                                                                                    #  de um requerente. Se está nulo é porque ninguem aceirou a corrida 
                                                                                    # nao pode ser cascade pq se o freteiro for deletado, o frete continua existindo    


    def __str__(self):
        return self.produto

