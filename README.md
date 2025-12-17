# Sistema de Gerenciamento de Logística e Entregas

📋 Descrição do Sistema 
Sistema completo de gerenciamento de logística desenvolvido em Django para empresas regionais que realizam entregas para diversos clientes (e-commerce, farmácias, restaurantes). 
O sistema permite o controle total de entregas, motoristas, veículos e rotas otimizadas.

Funcionalidades Principais -

* Autenticação e Autorização: Sistema com dois perfis (Administrador e Motorista) com permissões diferenciadas 
* Gestão de Entregas: Cadastro, acompanhamento e atualização de status de entregas
* Gestão de Motoristas: Controle completo de motoristas com criação automática de usuários
* Gestão de Veículos: Gerenciamento de frota com controle de capacidade e quilometragem 
* Gestão de Rotas: Organização de entregas em rotas otimizadas com validação de capacidade

---
# 🛠 Tecnologias Utilizadas

* Python 3.13 
* Django 5.0 
* Frontend: HTML5, CSS3, Bootstrap 5
* Django REST Framework para API 
* SQLite como banco de dados
* Autenticação: Django Authentication System

---
# 📦 Instalação

### Pré-requisitos

* Python 3.10 ou superior
* asgiref==3.11.0
* Django==5.2.8
* django-crispy-forms==2.5
* sqlparse==0.5.3
* tzdata==2025.2
* rest-framework
* crispy_bootstrap4
* crispy_bootstrap5



### Passo 1: Clonar o Repositório

```
git clone https://github.com/Marcos-San/projeto_logistica.git
cd projeto_logistica
```

### Passo 2: Criar Ambiente Virtual

```
python -m venv venv
venv\Scripts\activate
```

### Passo 3: Instalar Dependências

```
pip install -r requirements.txt
```

---
# 🗄️ Configuração do banco de dados

### Criar as tabelas do banco de dados
```
python manage.py makemigrations
python manage.py migrate
```

---
# 👤 Como Criar Usuário Admin

```
python manage.py createsuperuser
```

Será solicitado:
- **Username**: admin (ou nome desejado)
- **Email**: admin@email.com
- **Password**: (senha forte)
- **Password confirmation**: (repetir senha)

---
## 🚀 Como Rodar o Servidor

### Desenvolvimento

```bash
# Rodar servidor de desenvolvimento
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000/`

---

## 💡 Testar a API e  Exemplos de Uso Básico

### Endpoints Principais
### Acessando pelo Navegador

#### 1. Acesso Público - Rastreamento

```bash
# Acessar página de busca de entregas
http://127.0.0.1:8000/buscar_entrega/

# Buscar entrega específica (substitua ENT001 pelo código real)
http://127.0.0.1:8000//buscar_entrega/?pesquisa=ENT001
```
#### 2. **Dashboard Principal**

```bash
# Página inicial do sistema
http://127.0.0.1:8000/

# Dashboard admin (requer login)
http://127.0.0.1:8000/dashboard/
```

#### 3. **Listar Entregas**
```bash
# Via navegador (requer autenticação)
http://localhost:8000/entregas/
```

#### 4. **Admin Django**
```bash
# Acessar painel administrativo
http://localhost:8000/admin/
```

### 🧪 Testar o Sistema / Uso Básico

- Criar clientes

- Criar motoristas (usuário é criado automaticamente)

- Criar veículos

- Criar entregas

- Criar rotas e associar entregas

- Rastrear entrega pelo código de rastreio


---

## 🔐 Perfis de Usuário

### Administrador
- **Acesso**: Total ao sistema
- **Permissões**: CRUD completo em todas as entidades
- **Login**: Via admin Django ou interface web
- **Dashboard**: Estatísticas gerais do sistema

### Motorista
- **Acesso**: Visualização e edição limitada
- **Permissões**: 
  - Ver suas próprias entregas
  - Editar status de suas entregas
  - Ver suas rotas
  - Editar seu próprio perfil
- **Login**: Via interface web com CPF e senha
- **Dashboard**: Estatísticas pessoais

### Cliente
- **Acesso**: Rastreamento público
- **Permissões**: Consultar entregas por código
- **Login**: Não requerido para rastreamento

---

## 📁 Estrutura do Projeto

```
logitrans/
│
├── projeto_logistica/          # Configurações do projeto
│   ├── __init__.py
│   ├── settings.py            # Configurações principais
│   ├── urls.py                # URLs principais
│   └── wsgi.py                # WSGI application
│
├── logistica/                  # App principal
│   ├── migrations/            # Migrações do banco
│   ├── templates/log/         # Templates HTML
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── list_entrega.html
│   │   └── ...
│   ├── static/log/            # Arquivos estáticos
│   │   └── style.css
│   ├── __init__.py
│   ├── admin.py               # Configuração Django Admin
│   ├── apps.py
│   ├── models.py              # Modelos de dados
│   ├── views.py               # Views (Controllers)
│   ├── urls.py                # URLs do app
│   ├── forms.py               # Formulários
│   ├── permissions.py         # Sistema de permissões
│   ├── middleware.py          # Middlewares customizados
│   └── context_processors.py # Context processors
│
├── db.sqlite3                 # Banco de dados SQLite
├── manage.py                  # Script de gerenciamento Django
└── requirements.txt           # Dependências do projeto
```

---

## 🐛 Solução de Problemas Comuns

### Erro: "No module named 'crispy_forms'"
```bash
pip install django-crispy-forms crispy-bootstrap5
```

### Erro: "relation does not exist"
```bash
python manage.py makemigrations
python manage.py migrate
```
---

## 🎯 Próximas Funcionalidades

- [ ] Aplicativo mobile para motoristas
- [ ] Integração com sistemas de GPS
- [ ] Relatórios em PDF
- [ ] Notificações por email/SMS
 
---

**Versão**: 1.0.0  
**Última Atualização**: Dezembro 2025
