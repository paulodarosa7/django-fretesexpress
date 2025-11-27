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
    
class solicitarFrete(models.Model):
    produto = models.CharField(max_length=100)
    peso = models.FloatField()
    largura = models.FloatField()
    altura = models.FloatField()
    valor = models.FloatField()
    endereco_coleta = models.CharField(max_length=200)
    endereco_entrega = models.CharField(max_length=200)
    data_solicitacao = models.DateField(null=False)
    hora_solicitacao = models.TimeField(null=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=20, default="pendente") # determina o status atual do frete
    # um para muitos
    freteiro = models.ForeignKey("Freteiro", null=True, on_delete=models.SET_NULL)  # chave estrangeira de freteiro, para o mesmo poder aceitar um frete
                                                                                    #  de um requerente. Se está nulo é porque ninguem aceirou a corrida     


    def __str__(self):
        return self.produto

class Rota(models.Model):
    origem = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    distancia = models.FloatField()
    custo = models.FloatField()
    tempo_minutos = models.IntegerField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origem} - {self.destino} - R${self.custo}"