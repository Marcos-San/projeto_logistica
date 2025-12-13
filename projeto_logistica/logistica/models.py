from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver


# CLIENTE ------------------------

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']



# MOTORISTA -----------------------------

class Motorista(models.Model):
    STATUS_MOTORISTA = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('em_rota', 'Em Rota'),
        ('disponivel', 'Disponível'),
    ]

    TIPO_CNH = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    ]

    # Relacionamento com User do Django
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='motorista_profile',
        null=True,
        blank=True,
        verbose_name='Usuário do Sistema'
    )

    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    cnh = models.CharField(max_length=2, choices=TIPO_CNH)
    telefone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_MOTORISTA, default='disponivel')
    data_cadastro = models.DateField(auto_now_add=True)  # Mantenha auto_now_add=True

    # Campos para controle de convite
    token_convite = models.CharField(max_length=100, blank=True, null=True)
    token_validade = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.nome

    @property
    def username(self):
        """Retorna o username baseado no CPF"""
        if self.user:
            return self.user.username
        return ''.join(filter(str.isdigit, self.cpf))

    @property
    def email(self):
        """Retorna o email do usuário"""
        if self.user:
            return self.user.email
        return None

    @property
    def is_active(self):
        """Verifica se o usuário está ativo"""
        if self.user:
            return self.user.is_active
        return False

    def criar_usuario(self, senha=None):
        """Cria um usuário para o motorista e adiciona ao grupo Motoristas"""
        if self.user:
            return self.user, None  # Já tem usuário

        # Gerar username baseado no CPF
        username = ''.join(filter(str.isdigit, self.cpf))

        # Verificar se username já existe
        if User.objects.filter(username=username).exists():
            username = f"{username}_{self.id}"

        # Gerar senha se não for fornecida
        if not senha:
            import random
            import string
            senha = ''.join(random.choices(string.digits, k=4)) + '@Motorista'

        try:
            # Criar usuário
            user = User.objects.create_user(
                username=username,
                password=senha,
                email=f"{username}@logitrans.com.br",
                first_name=self.nome.split()[0],
                last_name=' '.join(self.nome.split()[1:]) if len(self.nome.split()) > 1 else '',
                is_staff=False,
                is_superuser=False,
                is_active=True
            )

            # ADICIONAR AO GRUPO MOTORISTAS (grupo que você criou no admin)
            try:
                grupo_motorista = Group.objects.get(name='Motoristas')
                user.groups.add(grupo_motorista)
                print(f"✅ Usuário {username} adicionado ao grupo Motoristas")
            except Group.DoesNotExist:
                # Se o grupo não existir, criar automaticamente
                grupo_motorista = Group.objects.create(name='Motoristas')
                user.groups.add(grupo_motorista)
                print(f"⚠️ Grupo Motoristas não existia. Criado automaticamente.")
            except Exception as e:
                print(f"⚠️ Erro ao adicionar ao grupo: {str(e)}")

            # Vincular ao motorista
            self.user = user
            self.save()

            return user, senha

        except Exception as e:
            # Em caso de erro, tentar criar com username alternativo
            try:
                username = f"{username}_{self.id}_{random.randint(1000, 9999)}"
                user = User.objects.create_user(
                    username=username,
                    password=senha,
                    email=f"{username}@logitrans.com.br",
                    first_name=self.nome.split()[0],
                    last_name=' '.join(self.nome.split()[1:]) if len(self.nome.split()) > 1 else ''
                )

                # Adicionar ao grupo Motoristas
                grupo_motorista = Group.objects.get_or_create(name='Motoristas')[0]
                user.groups.add(grupo_motorista)

                self.user = user
                self.save()

                return user, senha

            except Exception as e2:
                raise Exception(f"Erro ao criar usuário: {str(e2)}")

    def adicionar_ao_grupo_motoristas(self):
        """Adiciona o usuário do motorista ao grupo Motoristas"""
        if not self.user:
            return False

        try:
            grupo_motorista = Group.objects.get(name='Motoristas')
            if grupo_motorista not in self.user.groups.all():
                self.user.groups.add(grupo_motorista)
                self.user.save()
                return True
            return False
        except Group.DoesNotExist:
            # Criar o grupo se não existir
            grupo_motorista = Group.objects.create(name='Motoristas')
            self.user.groups.add(grupo_motorista)
            self.user.save()
            return True
        except Exception as e:
            print(f"Erro ao adicionar ao grupo: {str(e)}")
            return False

    def remover_do_grupo_motoristas(self):
        """Remove o usuário do motorista do grupo Motoristas"""
        if not self.user:
            return False

        try:
            grupo_motorista = Group.objects.get(name='Motoristas')
            if grupo_motorista in self.user.groups.all():
                self.user.groups.remove(grupo_motorista)
                self.user.save()
                return True
            return False
        except Exception as e:
            print(f"Erro ao remover do grupo: {str(e)}")
            return False

    def esta_no_grupo_motoristas(self):
        """Verifica se o usuário está no grupo Motoristas"""
        if not self.user:
            return False

        try:
            grupo_motorista = Group.objects.get(name='Motoristas')
            return grupo_motorista in self.user.groups.all()
        except Group.DoesNotExist:
            return False

    def resetar_senha(self):
        """Reseta a senha do motorista"""
        if not self.user:
            return None

        import random
        import string
        nova_senha = ''.join(random.choices(string.digits, k=4)) + '@Motorista'

        self.user.set_password(nova_senha)
        self.user.save()

        return nova_senha

    def bloquear_acesso(self):
        """Bloqueia o acesso do motorista"""
        if self.user:
            self.user.is_active = False
            self.user.save()
            return True
        return False

    def liberar_acesso(self):
        """Libera o acesso do motorista"""
        if self.user:
            self.user.is_active = True
            self.user.save()
            return True
        return False

    class Meta:
        verbose_name = 'Motorista'
        verbose_name_plural = 'Motoristas'
        ordering = ['nome']


# Signal para sincronizar nome quando motorista for atualizado
@receiver(post_save, sender=Motorista)
def atualizar_nome_usuario(sender, instance, **kwargs):
    """Atualiza o nome do usuário quando o nome do motorista é alterado"""
    if instance.user:
        # Atualizar primeiro nome
        instance.user.first_name = instance.nome.split()[0]

        # Atualizar último nome (se houver mais de uma palavra)
        if len(instance.nome.split()) > 1:
            instance.user.last_name = ' '.join(instance.nome.split()[1:])

        instance.user.save()

    @receiver(post_save, sender=Motorista)
    def atualizar_usuario_motorista(sender, instance, **kwargs):
        if instance.user:
            # Atualizar nome do usuário se o nome do motorista mudou
            if instance.user.first_name != instance.nome.split()[0]:
                instance.user.first_name = instance.nome.split()[0]
                instance.user.save()


class PerfilUsuario(models.Model):
    """Modelo para estender o usuário com informações adicionais"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    motorista = models.OneToOneField('Motorista', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='usuario')
    tipo_usuario = models.CharField(max_length=20,
                                    choices=[('admin', 'Admin'), ('motorista', 'Motorista'), ('cliente', 'Cliente')],
                                    default='cliente')

    def __str__(self):
        return f"Perfil de {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'perfil'):
        instance.perfil.save()

# VEÍCULO -----------------------------

class Veiculo(models.Model):
    STATUS_VEICULO = [
        ('disponivel', 'Disponível'),
        ('em_uso', 'Em uso'),
        ('manutencao', 'Manutenção'),
    ]

    TIPO_VEICULO = [
        ('carro', 'Carro'),
        ('van', 'Van'),
        ('caminhao', 'Caminhão'),
        ('moto', 'Moto'),
    ]

    placa = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_VEICULO)
    capacidade_maxima = models.FloatField()
    km_atual = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_VEICULO, default='disponivel')
    motorista = models.OneToOneField(
        Motorista,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='veiculo_atual'
    )

    def __str__(self):
        return f"{self.placa} - {self.modelo}"

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        ordering = ['placa']



# ROTA -----------------------------------

class Rota(models.Model):
    STATUS_ROTA = [
        ('planejada', 'Planejada'),
        ('em_andamento', 'Em andamento'),
        ('concluida', 'Concluída'),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE, related_name='rotas')
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='rotas')
    data_rota = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_ROTA, default='planejada')
    km_total_estimado = models.IntegerField(default=0)
    tempo_estimado = models.IntegerField(default=0)  # em minutos

    def capacidade_total_utilizada(self):
        """Calcula a capacidade total utilizada pelas entregas desta rota"""
        return sum(e.capacidade_necessaria for e in self.entregas.all())

    def total_entregas(self):
        """Retorna o total de entregas na rota"""
        return self.entregas.count()

    def valor_total_entregas(self):
        """Retorna o valor total das entregas"""
        return sum(e.valor_frete for e in self.entregas.all())

    def pode_adicionar_entrega(self, entrega):
        """Verifica se é possível adicionar uma entrega sem exceder a capacidade"""
        capacidade_atual = self.capacidade_total_utilizada()
        return (capacidade_atual + entrega.capacidade_necessaria) <= self.veiculo.capacidade_maxima

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Rota'
        verbose_name_plural = 'Rotas'
        ordering = ['-data_rota']



# ENTREGA ----------------------------------------

class Entrega(models.Model):
    STATUS_ENTREGA = [
        ('pendente', 'Pendente'),
        ('em_transito', 'Em trânsito'),
        ('entregue', 'Entregue'),
        ('cancelada', 'Cancelada'),
        ('remarcada', 'Remarcada'),
    ]

    codigo_rastreio = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='entregas')

    # Endereços
    endereco_origem = models.CharField(max_length=255)
    cep_origem = models.CharField(max_length=9)
    endereco_destino = models.CharField(max_length=255)
    cep_destino = models.CharField(max_length=9)

    # Status e valores
    status = models.CharField(max_length=20, choices=STATUS_ENTREGA, default='pendente')
    capacidade_necessaria = models.FloatField()
    valor_frete = models.DecimalField(max_digits=10, decimal_places=2)

    # Datas
    data_solicitacao = models.DateField(auto_now_add=True)
    data_entrega_prevista = models.DateField(null=True, blank=True)
    data_entrega_real = models.DateField(null=True, blank=True)

    # Observações
    obs = models.TextField(blank=True, null=True)

    # Relacionamentos
    motorista = models.ForeignKey(
        Motorista,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entregas'
    )

    # IMPORTANTE: Uma entrega pertence a APENAS UMA rota
    rota = models.ForeignKey(
        Rota,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entregas',
        verbose_name='Rota'
    )

    def __str__(self):
        return f"Entrega {self.codigo_rastreio}"

    def pode_ser_adicionada_na_rota(self, rota):
        """Verifica se a entrega pode ser adicionada em uma rota"""
        if self.rota is not None:
            return False  # Já está em uma rota
        return rota.pode_adicionar_entrega(self)

    class Meta:
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'
        ordering = ['-data_solicitacao']