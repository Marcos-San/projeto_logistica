from importlib.metadata import requires

from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100, default="Nome")
    email = models.EmailField(default='teste@example.com')
    telefone = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Entrega(models.Model):
    STATUS_ENTREGA = [
        ('pendente', 'Pendente'),
        ('em_transito', 'Em trânsito'),
        ('entregue', 'Entregue'),
        ('cancelada', 'Cancelada'),
        ('remarcada', 'Remarcada'),
    ]

    codigo_rastreio = models.IntegerField(unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    endereco_origem = models.CharField(max_length=100)
    cep_origem = models.CharField(max_length=100)
    endereco_destino = models.CharField(max_length=100)
    cep_destino = models.CharField(max_length=8)
    status = models.CharField(max_length=100, choices=STATUS_ENTREGA, default='pendente')
    capacidade_necessaria = models.FloatField()
    valor_frete = models.FloatField()
    data_solicitacao = models.DateField()
    data_entrega_prevista = models.DateField()
    data_entrega_real = models.DateField(null=True, blank=True)
    obs = models.TextField()

    def __str__(self):
        return str(self.codigo_rastreio)

class Motorista(models.Model):
    STATUS_MOTORISTA = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('em_rota', 'Em Rota'),
        ('disponível', 'Disponivel'),
    ]

    TIPO_CNH = [
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    ]
    nome = models.CharField(max_length=100)
    cpf = models.IntegerField(unique=True)
    cnh = models.CharField(max_length=100, choices=TIPO_CNH)
    telefone = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS_MOTORISTA, default='ativo')
    data_cadastro = models.DateField()

    def __str__(self):
        return self.nome


class Veiculo(models.Model):
    STATUS_VEICULO = [
    ('disponivel', 'Disponível'),
    ('em_uso', 'Em uso'),
    ('manutencao', 'Manutenção'),
    ]
    TIPO_VEICULO = [
        ('carro', 'Carro'),
        ('van', 'Van'),
        ('caminha', 'Caminhão'),
    ]
    placa = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100, choices=TIPO_VEICULO)
    capacidade_maxima = models.FloatField()
    km_atual = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_VEICULO, default='disponivel')
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE)

    def __str__(self):
        return self.placa

class Rota(models.Model):
    STATUS_ROTA = [
        ('planejada','Planejada'),
        ('em_andamento', 'Em andamento'),
        ('concluida', 'Concluida'),
    ]
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    entrega = models.ForeignKey(Entrega, on_delete=models.CASCADE)
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data_rota = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_ROTA, default='planejada')
    capacidade_total_utilizada = models.FloatField()
    km_total_estimado = models.IntegerField()
    tempo_estimado = models.FloatField()

    def __str__(self):
        return self.nome

