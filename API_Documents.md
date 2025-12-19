# 📡 Documentação da API REST - LogiTrans

## Visão Geral

O sistema LogiTrans disponibiliza uma **API RESTful completa** desenvolvida com **Django REST Framework (DRF)**, permitindo integração com aplicações externas como:

- **Frontends SPA** (React, Vue, Angular)
- **Aplicativos Mobile** (iOS, Android)
- **Sistemas de terceiros** (ERP, marketplaces, etc.)

A API é **independente do frontend HTML**, seguindo o padrão de **backend desacoplado**.

**Base URL**: `http://127.0.0.1:8000/api/`

**Format**: JSON

---

## 🔑 Autenticação da API

### Métodos de Autenticação

A API utiliza autenticação baseada no sistema padrão do Django com suporte a:

1. **Session Authentication** (para Browsable API)
2. **Token Authentication** (para aplicações externas)

### Login via Browsable API

```
http://127.0.0.1:8000/api-auth/login/
```

**Método**: `POST`  
**Content-Type**: `application/x-www-form-urlencoded`

**Parâmetros**:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

### Autenticação com Token (Opcional)

Se configurado, você pode usar tokens de autenticação:

```bash
# Obter token
curl -X POST http://127.0.0.1:8000/api/token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Resposta
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}

# Usar token nas requisições
curl -X GET http://127.0.0.1:8000/api/entregas/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

⚠️ **Importante**: É necessário estar autenticado para acessar a maioria dos endpoints.

---

## 🔁 Endpoints REST – CRUD Básico

Cada entidade principal possui os métodos HTTP padrão seguindo o padrão REST:

| Entidade | Endpoint | Métodos |
|----------|----------|---------|
| Clientes | `/api/clientes/` | GET, POST |
| Clientes | `/api/clientes/{id}/` | GET, PUT, PATCH, DELETE |
| Motoristas | `/api/motoristas/` | GET, POST |
| Motoristas | `/api/motoristas/{id}/` | GET, PUT, PATCH, DELETE |
| Veículos | `/api/veiculos/` | GET, POST |
| Veículos | `/api/veiculos/{id}/` | GET, PUT, PATCH, DELETE |
| Entregas | `/api/entregas/` | GET, POST |
| Entregas | `/api/entregas/{id}/` | GET, PUT, PATCH, DELETE |
| Rotas | `/api/rotas/` | GET, POST |
| Rotas | `/api/rotas/{id}/` | GET, PUT, PATCH, DELETE |

---

## 👥 API de Clientes

### Listar Clientes

**Endpoint**: `GET /api/clientes/`  
**Autenticação**: Requerida (Admin ou Motorista)

**Exemplo de Request**:
```bash
curl -X GET http://127.0.0.1:8000/api/clientes/ \
  -H "Authorization: Token {seu_token}"
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@email.com",
    "telefone": "(11) 98765-4321"
  },
  {
    "id": 2,
    "nome": "Maria Santos",
    "email": "maria@email.com",
    "telefone": "(11) 91234-5678"
  }
]
```

### Criar Cliente

**Endpoint**: `POST /api/clientes/`  
**Autenticação**: Requerida (Admin)

**Exemplo de Request**:
```bash
curl -X POST http://127.0.0.1:8000/api/clientes/ \
  -H "Authorization: Token {seu_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Pedro Oliveira",
    "email": "pedro@email.com",
    "telefone": "(21) 99876-5432"
  }'
```

**Response** (201 Created):
```json
{
  "id": 3,
  "nome": "Pedro Oliveira",
  "email": "pedro@email.com",
  "telefone": "(21) 99876-5432"
}
```

### Detalhes do Cliente

**Endpoint**: `GET /api/clientes/{id}/`

**Response** (200 OK):
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@email.com",
  "telefone": "(11) 98765-4321"
}
```

### Atualizar Cliente

**Endpoint**: `PUT /api/clientes/{id}/` ou `PATCH /api/clientes/{id}/`

**PUT** - Atualização completa:
```bash
curl -X PUT http://127.0.0.1:8000/api/clientes/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva Santos",
    "email": "joao@email.com",
    "telefone": "(11) 98765-4321"
  }'
```

**PATCH** - Atualização parcial:
```bash
curl -X PATCH http://127.0.0.1:8000/api/clientes/1/ \
  -H "Content-Type: application/json" \
  -d '{"telefone": "(11) 99999-9999"}'
```

### Deletar Cliente

**Endpoint**: `DELETE /api/clientes/{id}/`

**Response** (204 No Content)

---

## 🚗 API de Motoristas

### Listar Motoristas

**Endpoint**: `GET /api/motoristas/`  
**Autenticação**: Requerida (Admin)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "nome": "Pedro Santos",
    "cpf": "12345678900",
    "cnh": "D",
    "telefone": "(11) 91234-5678",
    "status": "disponivel",
    "data_cadastro": "2025-01-15",
    "user": {
      "id": 5,
      "username": "12345678900",
      "email": "pedro@logitrans.com",
      "is_active": true
    }
  }
]
```

### Criar Motorista

**Endpoint**: `POST /api/motoristas/`

**Request**:
```json
{
  "nome": "Carlos Souza",
  "cpf": "98765432100",
  "cnh": "E",
  "telefone": "(11) 97777-8888",
  "status": "disponivel",
  "criar_usuario": true,
  "email": "carlos@email.com"
}
```

**Response** (201 Created):
```json
{
  "id": 2,
  "nome": "Carlos Souza",
  "cpf": "98765432100",
  "cnh": "E",
  "telefone": "(11) 97777-8888",
  "status": "disponivel",
  "data_cadastro": "2025-12-19",
  "user": {
    "id": 6,
    "username": "98765432100",
    "email": "carlos@email.com",
    "is_active": true
  },
  "credenciais": {
    "username": "98765432100",
    "senha_temporaria": "5678@Motorista"
  }
}
```

### Entregas do Motorista

**Endpoint**: `GET /api/motoristas/{id}/entregas/`

Lista todas as entregas realizadas por um motorista.

**Response** (200 OK):
```json
{
  "motorista": {
    "id": 1,
    "nome": "Pedro Santos"
  },
  "total_entregas": 15,
  "entregas": [
    {
      "id": 1,
      "codigo_rastreio": "ENT001",
      "cliente": "João Silva",
      "status": "entregue",
      "data_solicitacao": "2025-12-15",
      "valor_frete": "150.00"
    }
  ]
}
```

### Histórico do Motorista

**Endpoint**: `GET /api/motoristas/{id}/historico/`

Retorna histórico completo de entregas do motorista com estatísticas.

**Response** (200 OK):
```json
{
  "motorista": {
    "id": 1,
    "nome": "Pedro Santos",
    "status": "disponivel"
  },
  "estatisticas": {
    "total_entregas": 50,
    "entregas_pendentes": 5,
    "entregas_em_transito": 3,
    "entregas_entregues": 40,
    "entregas_canceladas": 2,
    "taxa_sucesso": "80%",
    "valor_total_transportado": "12500.00"
  },
  "entregas_recentes": [
    {
      "codigo_rastreio": "ENT001",
      "status": "entregue",
      "data_entrega_real": "2025-12-18"
    }
  ]
}
```

### Rotas do Motorista

**Endpoint**: `GET /api/motoristas/{id}/rotas/`

Lista rotas associadas ao motorista.

**Response** (200 OK):
```json
{
  "motorista": "Pedro Santos",
  "total_rotas": 8,
  "rotas": [
    {
      "id": 1,
      "nome": "Rota SP-RJ",
      "data_rota": "2025-12-20",
      "status": "planejada",
      "total_entregas": 5,
      "veiculo": "ABC-1234"
    }
  ]
}
```

### Atribuir Veículo ao Motorista

**Endpoint**: `PUT /api/motoristas/{id}/atribuir-veiculo/`

Vincula um veículo disponível ao motorista.

**Request**:
```json
{
  "veiculo_id": 1
}
```

**Response** (200 OK):
```json
{
  "message": "Veículo ABC-1234 atribuído ao motorista Pedro Santos",
  "motorista": {
    "id": 1,
    "nome": "Pedro Santos"
  },
  "veiculo": {
    "id": 1,
    "placa": "ABC-1234",
    "modelo": "Fiat Ducato"
  }
}
```

### Liberar Veículo do Motorista

**Endpoint**: `PUT /api/motoristas/{id}/liberar-veiculo/`

Remove o veículo do motorista, deixando-o disponível.

**Response** (200 OK):
```json
{
  "message": "Veículo ABC-1234 liberado",
  "veiculo": {
    "id": 1,
    "placa": "ABC-1234",
    "status": "disponivel"
  }
}
```

---

## 🚛 API de Veículos

### Listar Veículos

**Endpoint**: `GET /api/veiculos/`

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "placa": "ABC-1234",
    "modelo": "Fiat Ducato",
    "tipo": "van",
    "capacidade_maxima": 1000.0,
    "km_atual": 50000,
    "status": "disponivel",
    "motorista": {
      "id": 1,
      "nome": "Pedro Santos"
    }
  }
]
```

### Veículos Disponíveis

**Endpoint**: `GET /api/veiculos/disponiveis/`

Lista apenas veículos com status "disponivel".

**Response** (200 OK):
```json
[
  {
    "id": 2,
    "placa": "XYZ-5678",
    "modelo": "Mercedes Sprinter",
    "tipo": "van",
    "capacidade_maxima": 1500.0,
    "status": "disponivel"
  }
]
```

### Rotas do Veículo

**Endpoint**: `GET /api/veiculos/{id}/rotas/`

Lista rotas realizadas com determinado veículo.

**Response** (200 OK):
```json
{
  "veiculo": {
    "placa": "ABC-1234",
    "modelo": "Fiat Ducato"
  },
  "total_rotas": 12,
  "rotas": [
    {
      "id": 1,
      "nome": "Rota SP-RJ",
      "data_rota": "2025-12-20",
      "motorista": "Pedro Santos",
      "km_total_estimado": 450
    }
  ]
}
```

### Histórico do Veículo

**Endpoint**: `GET /api/veiculos/{id}/historico/`

Retorna histórico de uso e quilometragem do veículo.

**Response** (200 OK):
```json
{
  "veiculo": {
    "placa": "ABC-1234",
    "modelo": "Fiat Ducato",
    "km_atual": 50000
  },
  "estatisticas": {
    "total_rotas": 12,
    "km_total_percorrido": 5400,
    "entregas_realizadas": 45,
    "ultima_manutencao": "2025-11-15",
    "proxima_manutencao_estimada": "2026-02-15"
  },
  "historico_rotas": [
    {
      "data": "2025-12-15",
      "nome": "Rota SP-RJ",
      "km_percorrido": 450
    }
  ]
}
```

---

## 📦 API de Entregas

### Listar Entregas

**Endpoint**: `GET /api/entregas/`

**Query Parameters**:
- `status`: Filtrar por status (pendente, em_transito, entregue, cancelada)
- `motorista`: Filtrar por ID do motorista
- `rota`: Filtrar por ID da rota
- `cliente`: Filtrar por ID do cliente

**Exemplo**:
```bash
GET /api/entregas/?status=pendente&motorista=1
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "codigo_rastreio": "ENT001",
    "cliente": {
      "id": 1,
      "nome": "João Silva"
    },
    "motorista": {
      "id": 1,
      "nome": "Pedro Santos"
    },
    "rota": {
      "id": 1,
      "nome": "Rota SP-RJ"
    },
    "endereco_origem": "Rua A, 123, São Paulo - SP",
    "cep_origem": "01000-000",
    "endereco_destino": "Rua B, 456, Rio de Janeiro - RJ",
    "cep_destino": "20000-000",
    "status": "pendente",
    "capacidade_necessaria": 50.0,
    "valor_frete": "150.00",
    "data_solicitacao": "2025-12-15",
    "data_entrega_prevista": "2025-12-20",
    "obs": "Entregar no período da manhã"
  }
]
```

### Criar Entrega

**Endpoint**: `POST /api/entregas/`

**Request**:
```json
{
  "codigo_rastreio": "ENT002",
  "cliente": 1,
  "motorista": 1,
  "endereco_origem": "Av. Paulista, 1000, São Paulo - SP",
  "cep_origem": "01310-000",
  "endereco_destino": "Av. Atlântica, 2000, Rio de Janeiro - RJ",
  "cep_destino": "22010-000",
  "status": "pendente",
  "capacidade_necessaria": 75.0,
  "valor_frete": 200.00,
  "data_entrega_prevista": "2025-12-22",
  "obs": "Frágil - manusear com cuidado"
}
```

**Response** (201 Created):
```json
{
  "id": 2,
  "codigo_rastreio": "ENT002",
  "cliente": {
    "id": 1,
    "nome": "João Silva"
  },
  "status": "pendente",
  "data_solicitacao": "2025-12-19"
}
```

### Atribuir Motorista à Entrega

**Endpoint**: `POST /api/entregas/{id}/atribuir-motorista/`

**Request**:
```json
{
  "motorista_id": 1
}
```

**Response** (200 OK):
```json
{
  "message": "Motorista Pedro Santos atribuído à entrega ENT002",
  "entrega": {
    "id": 2,
    "codigo_rastreio": "ENT002",
    "motorista": {
      "id": 1,
      "nome": "Pedro Santos"
    }
  }
}
```

### Rastrear Entrega (Público)

**Endpoint**: `GET /api/entregas/rastrear/{codigo}/`  
**Autenticação**: Não requerida

**Response** (200 OK):
```json
{
  "codigo_rastreio": "ENT001",
  "status": "em_transito",
  "cliente": "João Silva",
  "data_solicitacao": "2025-12-15",
  "data_entrega_prevista": "2025-12-20",
  "endereco_destino": "Rua B, 456, Rio de Janeiro - RJ",
  "historico_status": [
    {
      "status": "pendente",
      "data": "2025-12-15"
    },
    {
      "status": "em_transito",
      "data": "2025-12-19"
    }
  ]
}
```

---

## 🗺️ API de Rotas

### Listar Rotas

**Endpoint**: `GET /api/rotas/`

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "nome": "Rota SP-RJ",
    "descricao": "Entregas de São Paulo para Rio de Janeiro",
    "motorista": {
      "id": 1,
      "nome": "Pedro Santos"
    },
    "veiculo": {
      "id": 1,
      "placa": "ABC-1234",
      "modelo": "Fiat Ducato"
    },
    "data_rota": "2025-12-20",
    "status": "planejada",
    "km_total_estimado": 450,
    "tempo_estimado": 360,
    "total_entregas": 5,
    "capacidade_utilizada": 250.0,
    "capacidade_disponivel": 750.0
  }
]
```

### Criar Rota

**Endpoint**: `POST /api/rotas/`

**Request**:
```json
{
  "nome": "Rota SP-Campinas",
  "descricao": "Entregas para região de Campinas",
  "motorista": 1,
  "veiculo": 1,
  "data_rota": "2025-12-21",
  "status": "planejada",
  "km_total_estimado": 100,
  "tempo_estimado": 120
}
```

**Response** (201 Created):
```json
{
  "id": 2,
  "nome": "Rota SP-Campinas",
  "motorista": {
    "id": 1,
    "nome": "Pedro Santos",
    "status": "em_rota"
  },
  "veiculo": {
    "id": 1,
    "placa": "ABC-1234",
    "status": "em_uso"
  },
  "status": "planejada"
}
```

### Entregas da Rota

**Endpoint**: `GET /api/rotas/{id}/entregas/`

Lista entregas associadas a uma rota.

**Response** (200 OK):
```json
{
  "rota": {
    "id": 1,
    "nome": "Rota SP-RJ",
    "status": "planejada"
  },
  "total_entregas": 5,
  "entregas": [
    {
      "id": 1,
      "codigo_rastreio": "ENT001",
      "cliente": "João Silva",
      "endereco_destino": "Rua B, 456, Rio de Janeiro",
      "status": "pendente",
      "capacidade_necessaria": 50.0
    }
  ]
}
```

### Adicionar Entrega à Rota

**Endpoint**: `POST /api/rotas/{id}/entregas/`

**Request**:
```json
{
  "entrega_id": 3
}
```

**Validações**:
- Entrega não pode já estar em outra rota
- Capacidade da rota não pode ser excedida

**Response** (200 OK):
```json
{
  "message": "Entrega ENT003 adicionada à rota",
  "rota": {
    "id": 1,
    "total_entregas": 6,
    "capacidade_utilizada": 300.0,
    "capacidade_disponivel": 700.0
  }
}
```

**Response** (400 Bad Request) - Capacidade excedida:
```json
{
  "error": "Capacidade excedida",
  "detalhes": {
    "capacidade_necessaria": 200.0,
    "capacidade_disponivel": 150.0,
    "capacidade_veiculo": 1000.0,
    "capacidade_utilizada": 850.0
  }
}
```

### Remover Entrega da Rota

**Endpoint**: `DELETE /api/rotas/{id}/entregas/{entrega_id}/`

**Response** (200 OK):
```json
{
  "message": "Entrega ENT003 removida da rota",
  "rota": {
    "id": 1,
    "total_entregas": 5,
    "capacidade_utilizada": 250.0,
    "capacidade_disponivel": 750.0
  }
}
```

### Capacidade da Rota

**Endpoint**: `GET /api/rotas/{id}/capacidade/`

Retorna informações detalhadas sobre capacidade.

**Response** (200 OK):
```json
{
  "rota": {
    "id": 1,
    "nome": "Rota SP-RJ"
  },
  "veiculo": {
    "placa": "ABC-1234",
    "capacidade_maxima": 1000.0
  },
  "capacidade": {
    "total": 1000.0,
    "utilizada": 250.0,
    "disponivel": 750.0,
    "percentual_utilizado": 25.0
  },
  "entregas": [
    {
      "codigo_rastreio": "ENT001",
      "capacidade": 50.0
    },
    {
      "codigo_rastreio": "ENT002",
      "capacidade": 75.0
    }
  ]
}
```

---

## 📊 Endpoint de Composição (Dashboard Completo)

### Dashboard da Rota

**Endpoint**: `GET /api/rotas/{id}/dashboard/`

Retorna dados completos para dashboards e aplicações mobile.

**Response** (200 OK):
```json
{
  "rota": {
    "id": 1,
    "nome": "Rota SP-RJ",
    "descricao": "Entregas de São Paulo para Rio de Janeiro",
    "data_rota": "2025-12-20",
    "status": "em_andamento",
    "km_total_estimado": 450,
    "tempo_estimado": 360
  },
  "motorista": {
    "id": 1,
    "nome": "Pedro Santos",
    "cpf": "123.456.789-00",
    "telefone": "(11) 91234-5678",
    "cnh": "D",
    "status": "em_rota"
  },
  "veiculo": {
    "id": 1,
    "placa": "ABC-1234",
    "modelo": "Fiat Ducato",
    "tipo": "van",
    "capacidade_maxima": 1000.0,
    "km_atual": 50000,
    "status": "em_uso"
  },
  "capacidade": {
    "total": 1000.0,
    "utilizada": 250.0,
    "disponivel": 750.0,
    "percentual_utilizado": 25.0
  },
  "entregas": [
    {
      "id": 1,
      "codigo_rastreio": "ENT001",
      "cliente": {
        "nome": "João Silva",
        "telefone": "(11) 98765-4321"
      },
      "endereco_destino": "Rua B, 456, Rio de Janeiro - RJ",
      "cep_destino": "20000-000",
      "status": "em_transito",
      "capacidade_necessaria": 50.0,
      "valor_frete": "150.00",
      "data_entrega_prevista": "2025-12-20",
      "obs": "Entregar no período da manhã"
    },
    {
      "id": 2,
      "codigo_rastreio": "ENT002",
      "cliente": {
        "nome": "Maria Santos",
        "telefone": "(11) 91234-5678"
      },
      "endereco_destino": "Av. Atlântica, 2000, Rio de Janeiro - RJ",
      "cep_destino": "22010-000",
      "status": "pendente",
      "capacidade_necessaria": 75.0,
      "valor_frete": "200.00",
      "data_entrega_prevista": "2025-12-20"
    }
  ],
  "estatisticas": {
    "total_entregas": 5,
    "entregas_pendentes": 2,
    "entregas_em_transito": 2,
    "entregas_entregues": 1,
    "valor_total": "725.00"
  }
}
```

📌 **Ideal para**: Dashboards administrativos, aplicativos mobile, painéis de controle em tempo real.

---

## 🔐 Permissões da API

As permissões seguem as regras definidas em `permissions.py`:

| Perfil | Acesso | Endpoints Permitidos |
|--------|--------|----------------------|
| **Administrador** | Acesso total (CRUD completo) | Todos os endpoints |
| **Motorista** | Acesso restrito | - Ver/editar suas próprias entregas<br>- Ver suas rotas<br>- Ver seu histórico<br>- Ver veículos associados |
| **Cliente/Público** | Apenas leitura pública | - Rastreamento de entregas<br>- Consulta pública |

### Exemplos de Restrições

```python
# Motorista só vê suas entregas
GET /api/entregas/  # Filtra automaticamente por motorista logado

# Motorista não pode deletar entregas de outros
DELETE /api/entregas/{id}/  # 403 Forbidden se não for sua entrega

# Apenas admin pode criar motoristas
POST /api/motoristas/  # 403 Forbidden para não-admin
```

---

## 📝 Códigos de Status HTTP

| Código | Significado | Uso |
|--------|-------------|-----|
| 200 OK | Sucesso | GET, PUT, PATCH bem-sucedidos |
| 201 Created | Recurso criado | POST bem-sucedido |
| 204 No Content | Sucesso sem conteúdo | DELETE bem-sucedido |
| 400 Bad Request | Dados inválidos | Validação falhou |
| 401 Unauthorized | Não autenticado | Token/sessão inválidos |
| 403 Forbidden | Sem permissão | Usuário sem acesso ao recurso |
| 404 Not Found | Não encontrado | Recurso não existe |
| 500 Internal Server Error | Erro no servidor | Erro não tratado |

---
