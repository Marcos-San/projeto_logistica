# core/forms.py
from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from .models import Motorista, Cliente, Veiculo, Entrega, Rota



# FORM MOTORISTA ---------------------------------------------

class MotoristaForm(forms.ModelForm):
    """Formulário para criar/editar motorista"""
    criar_usuario = forms.BooleanField(
        required=False,
        initial=True,
        label='Criar usuário de acesso para o motorista',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='Se marcado, será criado um usuário para o motorista acessar o sistema.'
    )

    email = forms.EmailField(
        required=False,
        label='E-mail (para login)',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'motorista@email.com'
        }),
        help_text='Opcional. Se não informado, será usado um email padrão.'
    )

    class Meta:
        model = Motorista
        fields = ['nome', 'cpf', 'cnh', 'telefone', 'status']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do motorista'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
                'maxlength': '14'
            }),
            'cnh': forms.Select(attrs={
                'class': 'form-control'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),

        }
        labels = {
            'nome': 'Nome Completo',
            'cpf': 'CPF',
            'cnh': 'Categoria CNH',
            'telefone': 'Telefone',
            'status': 'Status',

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se estiver editando, mostrar data de cadastro como informação
        if self.instance and self.instance.pk:
            self.fields['info_data_cadastro'] = forms.CharField(
                required=False,
                disabled=True,
                initial=f"Cadastrado em: {self.instance.data_cadastro.strftime('%d/%m/%Y')}",
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'readonly': 'readonly'
                }),
                label='Data de Cadastro'
            )

    def clean_cpf(self):
        """Validação de CPF"""
        cpf = self.cleaned_data.get('cpf')
        cpf_numeros = ''.join(filter(str.isdigit, cpf))

        if len(cpf_numeros) != 11:
            raise ValidationError('CPF deve conter 11 dígitos.')

        # Verificar se já existe motorista com este CPF
        if Motorista.objects.filter(cpf=cpf).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este CPF já está cadastrado no sistema.')

        # Verificar se já existe usuário com username baseado neste CPF
        username = cpf_numeros
        if User.objects.filter(username=username).exists():
            # Verificar se o usuário já está vinculado a outro motorista
            user = User.objects.get(username=username)
            if hasattr(user, 'motorista_profile') and user.motorista_profile != self.instance:
                raise ValidationError('Este CPF já está vinculado a outro motorista.')

        return cpf

    def save(self, commit=True):
        """Salva o motorista e cria usuário se necessário"""
        motorista = super().save(commit=False)
        criar_usuario = self.cleaned_data.get('criar_usuario')
        email = self.cleaned_data.get('email')

        if commit:
            motorista.save()

            # Criar usuário se solicitado e ainda não existir
            if criar_usuario and not motorista.user:
                user, senha_gerada = motorista.criar_usuario()

                # Atualizar email se fornecido
                if email:
                    user.email = email
                    user.save()

                # Adicionar senha gerada ao contexto
                self.senha_gerada = senha_gerada

        return motorista


class GerenciarAcessoMotoristaForm(forms.Form):
    """Formulário para gerenciar acesso do motorista"""
    ACAO_CHOICES = [
        ('resetar_senha', 'Resetar Senha'),
        ('bloquear_acesso', 'Bloquear Acesso'),
        ('liberar_acesso', 'Liberar Acesso'),
        ('reenviar_credenciais', 'Reenviar Credenciais'),
    ]

    acao = forms.ChoiceField(
        choices=ACAO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Ação'
    )

    email_credenciais = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='E-mail para envio das credenciais',
        help_text='Opcional. Se informado, as credenciais serão enviadas para este email.'
    )


class CriarUsuarioMotoristaForm(forms.Form):
    """Formulário para criar usuário para motorista existente"""
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='E-mail para login',
        help_text='Opcional. Se não informado, será usado um email padrão.'
    )

    enviar_email = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Enviar credenciais por email',
        help_text='Envia as credenciais de acesso por email.'
    )


# FORM CLIENTE ---------------------------------------------

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do cliente'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'cliente@email.com'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
        }
        labels = {
            'nome': 'Nome Completo',
            'email': 'E-mail',
            'telefone': 'Telefone',
        }

    def clean_email(self):
        """Validação de e-mail único"""
        email = self.cleaned_data.get('email')

        # Verificar se já existe (exceto o próprio registro em edição)
        if Cliente.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este e-mail já está cadastrado.')

        return email



# FORM VEÍCULO ---------------------------------------------

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = "__all__"
        widgets = {
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ABC-1234',
                'maxlength': '10'
            }),
            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Fiat Ducato'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'capacidade_maxima': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Capacidade em kg',
                'min': '0',
                'step': '0.01'
            }),
            'km_atual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quilometragem atual',
                'min': '0'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'motorista': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'placa': 'Placa',
            'modelo': 'Modelo',
            'tipo': 'Tipo de Veículo',
            'capacidade_maxima': 'Capacidade Máxima (kg)',
            'km_atual': 'Quilometragem Atual',
            'status': 'Status',
            'motorista': 'Motorista Ativo',
        }

    def clean_placa(self):
        """Validação de placa"""
        placa = self.cleaned_data.get('placa').upper()

        # Verificar se já existe (exceto o próprio registro em edição)
        if Veiculo.objects.filter(placa=placa).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Esta placa já está cadastrada.')

        return placa

    def clean_capacidade_maxima(self):
        """Validação de capacidade"""
        capacidade = self.cleaned_data.get('capacidade_maxima')

        if capacidade <= 0:
            raise ValidationError('Capacidade máxima deve ser maior que zero.')

        return capacidade



# FORM ENTREGA ---------------------------------------------

class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = "__all__"
        widgets = {
            'codigo_rastreio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ENT001',
                'maxlength': '20'
            }),
            'cliente': forms.Select(attrs={
                'class': 'form-control'
            }),
            'endereco_origem': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço completo de origem'
            }),
            'cep_origem': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000-000',
                'maxlength': '9'
            }),
            'endereco_destino': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço completo de destino'
            }),
            'cep_destino': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000-000',
                'maxlength': '9'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'capacidade_necessaria': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Peso em kg',
                'min': '0',
                'step': '0.01'
            }),
            'valor_frete': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'min': '0',
                'step': '0.01'
            }),
            'data_entrega_prevista': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'data_entrega_real': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'obs': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações sobre a entrega'
            }),
            'motorista': forms.Select(attrs={
                'class': 'form-control'
            }),
            'rota': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'codigo_rastreio': 'Código de Rastreio',
            'cliente': 'Cliente',
            'endereco_origem': 'Endereço de Origem',
            'cep_origem': 'CEP de Origem',
            'endereco_destino': 'Endereço de Destino',
            'cep_destino': 'CEP de Destino',
            'status': 'Status',
            'capacidade_necessaria': 'Capacidade Necessária (kg)',
            'valor_frete': 'Valor do Frete (R$)',
            'data_entrega_prevista': 'Data de Entrega Prevista',
            'data_entrega_real': 'Data de Entrega Real',
            'obs': 'Observações',
            'motorista': 'Motorista',
            'rota': 'Rota',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas rotas ativas para seleção
        self.fields['rota'].queryset = Rota.objects.filter(
            status__in=['planejada', 'em_andamento']
        ).order_by('-data_rota')

        # Adicionar opção vazia
        self.fields['rota'].empty_label = "Sem rota (adicionar depois)"
        self.fields['motorista'].empty_label = "Sem motorista"

    def clean_codigo_rastreio(self):
        """Validação de código único"""
        codigo = self.cleaned_data.get('codigo_rastreio').upper()

        # Verificar se já existe (exceto o próprio registro em edição)
        if Entrega.objects.filter(codigo_rastreio=codigo).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este código de rastreio já existe.')

        return codigo

    def clean_capacidade_necessaria(self):
        """Validação de capacidade"""
        capacidade = self.cleaned_data.get('capacidade_necessaria')

        if capacidade <= 0:
            raise ValidationError('Capacidade necessária deve ser maior que zero.')

        return capacidade

    def clean_valor_frete(self):
        """Validação de valor"""
        valor = self.cleaned_data.get('valor_frete')

        if valor < 0:
            raise ValidationError('Valor do frete não pode ser negativo.')

        return valor

    def clean(self):
        """Validações gerais"""
        cleaned_data = super().clean()
        rota = cleaned_data.get('rota')
        capacidade_necessaria = cleaned_data.get('capacidade_necessaria')

        # Se uma rota foi selecionada, verificar capacidade
        if rota and capacidade_necessaria:
            # Se for uma nova entrega ou mudando de rota
            if not self.instance.pk or self.instance.rota != rota:
                capacidade_atual = rota.capacidade_total_utilizada()
                capacidade_disponivel = rota.veiculo.capacidade_maxima - capacidade_atual

                if capacidade_necessaria > capacidade_disponivel:
                    raise ValidationError(
                        f'Capacidade excedida! A rota "{rota.nome}" tem apenas '
                        f'{capacidade_disponivel}kg disponíveis, mas a entrega precisa de '
                        f'{capacidade_necessaria}kg.'
                    )

        return cleaned_data



# FORM ROTA ---------------------------------------------

class RotaForm(forms.ModelForm):
    class Meta:
        model = Rota
        fields = "__all__"
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da rota'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição da rota'
            }),
            'motorista': forms.Select(attrs={
                'class': 'form-control'
            }),
            'veiculo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'data_rota': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'km_total_estimado': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quilometragem estimada',
                'min': '0'
            }),
            'tempo_estimado': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tempo em minutos',
                'min': '0'
            }),
        }
        labels = {
            'nome': 'Nome da Rota',
            'descricao': 'Descrição',
            'motorista': 'Motorista',
            'veiculo': 'Veículo',
            'data_rota': 'Data da Rota',
            'status': 'Status',
            'km_total_estimado': 'KM Total Estimado',
            'tempo_estimado': 'Tempo Estimado (minutos)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas motoristas e veículos disponíveis (para novas rotas)
        if not self.instance.pk:
            self.fields['motorista'].queryset = Motorista.objects.filter(
                status='disponivel'
            )
            self.fields['veiculo'].queryset = Veiculo.objects.filter(
                status='disponivel'
            )

    def clean(self):
        """Validações gerais"""
        cleaned_data = super().clean()
        motorista = cleaned_data.get('motorista')
        veiculo = cleaned_data.get('veiculo')

        # Para novas rotas, verificar disponibilidade
        if not self.instance.pk:
            if motorista and motorista.status != 'disponivel':
                raise ValidationError(
                    f'O motorista "{motorista.nome}" não está disponível. '
                    f'Status atual: {motorista.get_status_display()}'
                )

            if veiculo and veiculo.status != 'disponivel':
                raise ValidationError(
                    f'O veículo "{veiculo.placa}" não está disponível. '
                    f'Status atual: {veiculo.get_status_display()}'
                )

        return cleaned_data