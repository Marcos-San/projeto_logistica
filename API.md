# 📡 Documentação da API - LogiTrans

## Visão Geral

API para gerenciar entregas, rotas, motoristas, veículos e clientes. A maioria dos endpoints requer autenticação.

**Base URL**: `http://localhost:8000`

**Autenticação**: Session-based (Django Auth)

**Content-Type**: `application/json` ou `application/x-www-form-urlencoded`

---

## 🔐 Autenticação

### Login

Autentica um usuário no sistema.

- **URL**: `/login/`
- **Método**: `POST`
- **Autenticação**: Não requerida
- **Content-Type**: `application/x-www-form-urlencoded`

**Parâmetros**:
```json
{
  "username": "string (obrigatório)",
  "password": "string (obrigatório)"
}
```

**Exemplo de Request**:
```bash
curl -X POST http://localhost:8000/login/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

**Response** (302 Redirect):
```
Location: /redirecionar-perfil/
Set-Cookie: sessionid=xxx; ...
```

**Códigos de Status**:
- `302 Found`: Login bem-sucedido (redireciona)
- `200 OK`: Falha no login (retorna formulário com erros)

---

### Logout

Remove a sessão do usuário.

- **URL**: `/logout/`
- **Método**: `GET`
- **Autenticação**: Requerida

**Exemplo de Request**:
```bash
curl -X GET http://localhost:8000/logout/ \
  -b "sessionid=xxx"
```

**Response** (302 Redirect):
```
Location: /
```

**Códigos de Status**:
- `302 Found`: Logout bem-sucedido

---

## 📦 Entregas (Deliveries)

### Listar Todas as Entregas

Lista entregas baseado no perfil do usuário.

- **URL**: `/entregas/`
- **Método**: `GET`
- **Autenticação**: Requerida (Admin ou Motorista)
- **Permissões**: 
  - Admin: vê todas as entregas
  - Motorista: vê apenas suas entregas

**Exemplo de Request**:
```bash
curl -X GET http://localhost:8000/entregas/ \
  -b "sessionid=xxx"
```

**Response** (200 OK):
```html
<!-- Retorna página HTML com lista de entregas -->
```

**Códigos de Status**:
- `200 OK`: Lista retornada com sucesso
- `302 Found`: Usuário não autenticado (redireciona para login)
- `403 Forbidden`: Usuário sem permissão

---

### Criar Nova Entrega

Cria uma nova entrega no sistema.

- **URL**: `/entregas/criar/`
- **Método**: `POST`
- **Autenticação**: Requerida (Admin)
- **Content-Type**: `multipart/form-data`

**Parâmetros**:
```json
{
  "codigo_rastreio": "string (obrigatório, único)",
  "cliente": "integer (ID do cliente, obrigatório)",
  "endereco_origem": "string (obrigatório)",
  "cep_origem": "string (formato: 00000-000)",
  "endereco_destino": "string (obrigatório)",
  "cep_destino": "string (formato: 00000-000)",
  "status": "string (pendente|em_transito|entregue|cancelada|remarcada)",
  "capacidade_necessaria": "float (kg, obrigatório, > 0)",
  "valor_frete": "decimal (obrigatório, >= 0)",
  "data_entrega_prevista": "date (YYYY-MM-DD, opcional)",
  "data_entrega_real": "date (YYYY-MM-DD, opcional)",
  "obs": "text (opcional)",
  "motorista": "integer (ID do motorista, opcional)",
  "rota": "integer (ID da rota, opcional)"
}
```

**Exemplo de Request**:
```bash
curl -X POST http://localhost:8000/entregas/criar/ \
  -b "sessionid=xxx" \
  -F "codigo_rastreio=ENT001" \
  -F "cliente=1" \
  -F "endereco_origem=Rua A, 123, São Paulo" \
  -F "cep_origem=01000-000" \
  -F "endereco_destino=Rua B, 456, Rio de Janeiro" \
  -F "cep_destino=20000-000" \
  -F "status=pendente" \
  -F "capacidade_necessaria=50.0" \
  -F "valor_frete=150.00"
```

**Response** (302 Redirect):
```
Location: /entregas/
Mensagem: Entrega "ENT001" registrada com sucesso!
```

**Validações**:
- `codigo_rastreio` deve ser único
- `capacidade_necessaria` deve ser > 0
- `valor_frete` deve ser >= 0
- Se `rota` for especificada, verifica capacidade disponível

**Códigos de Status**:
- `302 Found`: Entrega criada com sucesso
- `200 OK`: Erro de validação (retorna formulário com erros)
- `403 Forbidden`: Usuário sem permissão

---

### Atualizar Entrega

Atualiza uma entrega existente.

- **URL**: `/entregas/<int:id>/editar/`
- **Método**: `POST`
- **Autenticação**: Requerida
- **Permissões**: 
  - Admin: pode editar qualquer entrega
  - Motorista: pode editar apenas suas entregas

**Parâmetros**: Mesmos da criação

**Exemplo de Request**:
```bash
curl -X POST http://localhost:8000/entregas/1/editar/ \
  -b "sessionid=xxx" \
  -F "status=em_transito" \
  -F "codigo_rastreio=ENT001" \
  -F "cliente=1" \
  -F "endereco_origem=Rua A, 123" \
  -F "cep_origem=01000-000" \
  -F "endereco_destino=Rua B, 456" \
  -F "cep_destino=20000-000" \
  -F "capacidade_necessaria=50.0" \
  -F "valor_frete=150.00"
```

**Response** (302 Redirect):
```
Location: /entregas/
Mensagem: Dados da entrega atualizados com sucesso!
```

**Códigos de Status**:
- `302 Found`: Atualização bem-sucedida
- `200 OK`: Erro de validação
- `403 Forbidden`: Sem permissão para editar esta entrega
- `404 Not Found`: Entrega não encontrada

---

### Deletar Entrega

Remove uma entrega do sistema.

- **URL**: `/entregas/<int:id>/deletar/`
- **Método**: `GET`
- **Autenticação**: Requerida
- **Permissões**: Admin

**Exemplo de Request**:
```bash
curl -X GET http://localhost:8000/entregas/1/deletar/ \
  -b "sessionid=xxx"
```

**Response** (302 Redirect):
```
Location: /entregas/
Mensagem: Entrega "ENT001" deletada com sucesso!
```

**Códigos de Status**:
- `302 Found`: Deleção bem-sucedida
- `403 Forbidden`: Sem permissão
- `404 Not Found`: Entrega não encontrada

---

### Buscar Entrega por Código (Público)

Busca uma entrega pelo código de rastreio.

- **URL**: `/buscar_entrega/`
- **Método**: `GET`
- **Autenticação**: Não requerida (acesso público)

**Query Parameters**:
```
pesquisa: string (código de rastreio)
```

**Exemplo de Request**:
```bash
curl -X GET "http://localhost:8000/buscar_entrega/?pesquisa=ENT001"
```

**Response** (200 OK):
```html
<!-- Retorna página HTML com detalhes da entrega -->
```

**Resposta quando não encontrada**:
```html
<!-- Página com mensagem: Entrega "ENT001" não encontrada! -->
```

**Códigos de Status**:
- `200 OK`: Sempre retorna página (com ou sem resultado)

---

## 🚗 Motoristas

### Listar Motoristas

Lista todos os motoristas (apenas admin).

- **URL**: `/motoristas/`
- **Método**: `GET`
- **Autenticação**: Requerida (Admin)

**Exemplo de Request**:
```bash
curl -X GET http://localhost:8000/motoristas/ \
  -b "sessionid=xxx"
```

**Response** (200 OK):
```html
<!-- Retorna página HTML com lista de motoristas -->
```

**Códigos de Status**:
- `200 OK`: Lista retornada
- `403 Forbidden`: Apenas admin pode acessar

---

### Criar Motorista

Cria um novo motorista com usuário automático.

- **URL**: `/motoristas/criar/`
- **Método**: `POST`
- **Autenticação**: Requerida (Admin)

**Parâmetros**:
```json
{
  "nome": "string (obrigatório)",
  "cpf": "string (11 dígitos, único, obrigatório)",
  "cnh": "string (A|B|C|D|E, obrigatório)",
  "telefone": "string (obrigatório)",
  "status": "string (ativo|inativo|em_rota|disponivel)",
  "criar_usuario": "boolean (padrão: true)",
  "email": "string (opcional, para login)"
}
```

**Exemplo de Request**:
```bash
curl -X POST http://localhost:8000/motoristas/criar/ \
  -b "sessionid=xxx" \
  -F "nome=João Silva" \
  -F "cpf=12345678900" \
  -F "cnh=D" \
  -F "telefone=(11) 98765-4321" \
  -F "status=disponivel" \
  -F "criar_usuario=on" \
  -F "email=joao@email.com"
```

**Response** (302 Redirect):
```
Location: /motoristas/
Mensagem: 
  Motorista cadastrado com sucesso!
  Usuário: 12345678900
  Senha: 1234@Motorista
  Status: Conta ATIVA
```

**Validações**:
- CPF deve ter 11 dígitos
- CPF deve ser único
- Se `criar_usuario=true`, cria usuário automaticamente
  - Username: CPF (apenas números)
  - Senha: gerada automaticamente
  - Adiciona ao grupo "Motoristas"
  - Conta já ativa

**Códigos de Status**:
- `302 Found`: Criação bem-sucedida
- `200 OK`: Erro de validação
- `403 Forbidden`: Apenas admin

---

### Detalhes do Motorista

Exibe detalhes e estatísticas de um motorista.

- **URL**: `/motoristas/<int:id>/`
- **Método**: `GET`
- **Autenticação**: Requerida
- **Permissões**: Admin ou o próprio motorista

**Exemplo de Request**:
```bash
curl -X GET http://localhost:8000/motoristas/1/ \
  -b "sessionid=xxx"
```

**Response** (200 OK):
```html
<!-- Página com:
- Dados do motorista
- Total de entregas
- Entregas pendentes/entregues
- Rotas ativas/concluídas
-->
```

**Códigos de Status**:
- `200 OK`: Detalhes retornados
- `403 Forbidden`: Sem permissão
- `404 Not Found`: Motorista não encontrado

---

### Gerenciar Acesso do Motorista

Gerencia credenciais e acesso ao sistema.

- **URL**: `/motoristas/<int:id>/acesso/`
- **Método**: `POST`
- **Autenticação**: Requerida (Admin)

**Parâmetros**:
```json
{
  "acao": "string (resetar_senha|bloquear_acesso|liberar_acesso|reenviar_credenciais)",
  "email_credenciais": "string (opcional, para envio de email)"
}
```

**Exemplo de Request - Resetar Senha**:
```bash
curl -X POST http://localhost:8000/motoristas/1/acesso/ \
  -b "sessionid=xxx" \
  -F "acao=resetar_senha" \
  -F "email_credenciais=motorista@email.com"
```

**Response** (302 Redirect):
```
Location: /motoristas/1/acesso/
Mensagem: Senha resetada! Nova senha: 5678@Motorista
```

**Ações Disponíveis**:

1. **resetar_senha**:
   - Gera nova senha aleatória
   - Formato: 4 dígitos + "@Motorista"
   - Opcionalmente envia por email

2. **bloquear_acesso**:
   - Define `user.is_active = False`
   - Impede login do motorista

3. **liberar_acesso**:
   - Define `user.is_active = True`
   - Permite login novamente

4. **reenviar_credenciais**:
   - Gera nova senha temporária
   - Envia por email (se fornecido)

**Códigos de Status**:
- `302 Found`: Ação executada com sucesso
- `403 Forbidden`: Apenas admin
- `404 Not Found`: Motorista não encontrado

---

## 🚛 Veículos

### Listar Veículos

Lista veículos baseado no perfil.

- **URL**: `/veiculos/`
- **Método**: `GET`
- **Autenticação**: Requerida
- **Permissões**:
  - Admin: vê todos os veículos

**Exemplo de Request**:
```bash
curl -X GET http://localhost:8000/veiculos/ \
  -b "sessionid=xxx"
```

**Response** (200 OK):
```html
<!-- Lista de veículos -->
```

**Códigos de Status**:
- `200 OK`: Lista retornada
- `403 Forbidden`: Sem permissão

---

### Criar Veículo

Cria um novo veículo.

- **URL**: `/veiculos/criar/`
- **Método**: `POST`
- **Autenticação**: Requerida (Admin)

**Parâmetros**:
```json
{
  "placa": "string (única, obrigatória)",
  "modelo": "string (obrigatório)",
  "tipo": "string (carro|van|caminhao|moto)",
  "capacidade_maxima": "float (kg, obrigatório, > 0)",
  "km_atual": "integer (obrigatório, >= 0)",
  "status": "string (disponivel|em_uso|manutencao)",
  "motorista": "integer (ID do motorista, opcional)"
}
```

**Exemplo de Request**:
```bash
curl -X POST http://localhost:8000/veiculos/criar/ \
  -b "sessionid=xxx" \
  -F "placa=ABC-1234" \
  -F "modelo=Fiat Ducato" \
  -F "tipo=van" \
  -F "capacidade_maxima=1000.0" \
  -F "km_atual=50000" \
  -F "status=disponivel"
```

**Response** (302 Redirect):
```
Location: /veiculos/
Mensagem: Veículo cadastrado com sucesso!
```

**Validações**:
- Placa deve ser única
- Capacidade máxima deve ser > 0

**Códigos de Status**:
- `302 Found`: Criação bem-sucedida
- `200 OK`: Erro de validação
- `403 Forbidden`: Apenas admin

---

## 🗺️ Rotas (Routes)

### Listar Rotas

Lista rotas baseado no perfil.

- **URL**: `/rotas/`
- **Método**: `GET`
- **Autenticação**: Requerida
- **Permissões**:
  - Admin: vê todas as rotas
  - Motorista: vê apenas suas rotas

**Exemplo de Request**:
```bash
curl -X GET http://localhost:8000/rotas/ \
  -b "sessionid=xxx"
```

**Response** (200 OK):
```html
<!-- Lista de rotas -->
```

**Códigos de Status**:
- `200 OK`: Lista retornada
- `403 Forbidden`: Sem permissão

---

### Criar Rota

Cria uma nova rota.

- **URL**: `/rotas/criar/`
- **Método**: `POST`
- **Autenticação**: Requerida (Admin)

**Parâmetros**:
```json
{
  "nome": "string (obrigatório)",
  "descricao": "text (opcional)",
  "motorista": "integer (ID, obrigatório, status='disponivel')",
  "veiculo": "integer (ID, obrigatório, status='disponivel')",
  "data_rota": "date (YYYY-MM-DD, obrigatório)",
  "status": "string (planejada|em_andamento|concluida)",
  "km_total_estimado": "integer (obrigatório, >= 0)",
  "tempo_estimado": "integer (minutos, obrigatório, >= 0)"
}
```

**Exemplo de Request**:
```bash
curl -X POST http://localhost:8000/rotas/criar/ \
  -b "sessionid=xxx" \
  -F "nome=Rota SP-RJ" \
  -F "descricao=Entregas São Paulo - Rio de Janeiro" \
  -F "motorista=1" \
  -F "veiculo=1" \
  -F "data_rota=2025-12-20" \
  -F "status=planejada" \
  -F "km_total_estimado=450" \
  -F "tempo_estimado=360"
```

**Response** (302 Redirect):
```
Location: /rotas/
Mensagem: Rota "Rota SP-RJ" registrada com sucesso!
```

**Efeitos Colaterais**:
- Atualiza `veiculo.status` para "em_uso"
- Atualiza `motorista.status` para "em_rota"

**Validações**:
- Motorista deve estar com status "disponivel"
- Veículo deve estar com status "disponivel"

**Códigos de Status**:
- `302 Found`: Criação bem-sucedida
- `200 OK`: Erro de validação
- `403 Forbidden`: Apenas admin

---

### Listar Entregas da Rota

Lista todas as entregas de uma rota específica.

- **URL**: `/rotas/<int:rota_id>/entregas/`
- **Método**: `GET`
- **Autenticação**: Requerida
- **Permissões**: Admin ou motorista da rota

**Exemplo de Request**:
```bash
curl -X GET http://localhost:8000/rotas/1/entregas/ \
  -b "sessionid=xxx"
```

**Response** (200 OK):
```html
<!-- Página com:
- Informações da rota
- Lista de entregas
- Estatísticas (capacidade, valor total)
- Formulário para adicionar entregas
-->
```

**Códigos de Status**:
- `200 OK`: Lista retornada
- `403 Forbidden`: Sem permissão para ver esta rota
- `404 Not Found`: Rota não encontrada

---

### Adicionar Entrega à Rota

Adiciona uma entrega existente a uma rota.

- **URL**: `/rotas/<int:rota_id>/adicionar-entrega/`
- **Método**: `POST`
- **Autenticação**: Requerida (Admin)

**Parâmetros**:
```json
{
  "entrega_id": "integer (ID da entrega, obrigatório)"
}
```

**Exemplo de Request**:
```bash
curl -X POST http://localhost:8000/rotas/1/adicionar-entrega/ \
  -b "sessionid=xxx" \
  -F "entrega_id=5"
```

**Response** (302 Redirect):
```
Location: /rotas/1/entregas/
Mensagem: Entrega "ENT005" adicionada à rota com sucesso!
```

**Validações**:
- Entrega não pode já estar em outra rota
- Capacidade da rota não pode ser excedida
  - `capacidade_usada + capacidade_entrega <= capacidade_veiculo`

**Possíveis Erros**:
- "A entrega já está em outra rota!"
- "Capacidade excedida! A entrega precisa de X kg, mas só há Y kg disponíveis."

**Códigos de Status**:
- `302 Found`: Adição bem-sucedida
- `302 Found`: Erro de validação (com mensagem de erro)
- `403 Forbidden`: Apenas admin
- `404 Not Found`: Rota ou entrega não encontrada

---

### Remover Entrega da Rota

Remove uma entrega de sua rota.

- **URL**: `/entregas/<int:entrega_id>/remover-rota/`
- **Método**: `GET`
- **Autenticação**: Requerida
- **Permissões**: Admin 

**Exemplo de Request**:
```bash
curl -X GET http://localhost:8000/entregas/5/remover-rota/ \
  -b "sessionid=xxx"
```

**Response** (302 Redirect):
```
Location: /rotas/1/entregas/  (ou /entregas/ se não havia rota)
Mensagem: Entrega "ENT005" removida da rota com sucesso!
```

**Códigos de Status**:
- `302 Found`: Remoção bem-sucedida
- `403 Forbidden`: Sem permissão
- `404 Not Found`: Entrega não encontrada

---

## 👥 Clientes (Clients)

### Listar Clientes

Lista todos os clientes.

- **URL**: `/clientes/`
- **Método**: `GET`
- **Autenticação**: Requerida (Admin)

**Exemplo de Request**:
```bash
curl -X GET http://localhost:8000/clientes/ \
  -b "sessionid=xxx"
```

**Response** (200 OK):
```html
<!-- Lista de clientes -->
```

**Códigos de Status**:
- `200 OK`: Lista retornada
- `403 Forbidden`: Sem permissão

---

### Criar Cliente

Cria um novo cliente.

- **URL**: `/clientes/criar/`
- **Método**: `POST`
- **Autenticação**: Requerida (Admin)

**Parâmetros**:
```json
{
  "nome": "string (obrigatório)",
  "email": "string (único, obrigatório)",
  "telefone": "string (obrigatório)"
}
```

**Exemplo de Request**:
```bash
curl -X POST http://localhost:8000/clientes/criar/ \
  -b "sessionid=xxx" \
  -F "nome=Maria Santos" \
  -F "email=maria@email.com" \
  -F "telefone=(11) 91234-5678"
```

**Response** (302 Redirect):
```
Location: /clientes/
Mensagem: Cliente cadastrado com sucesso!
```

**Validações**:
- Email deve ser único

**Códigos de Status**:
- `302 Found`: Criação bem-sucedida
- `200 OK`: Erro de validação (email duplicado)
- `403 Forbidden`: Apenas admin

---

## 📊 Códigos de Status HTTP

| Código | Significado | Uso no LogiTrans |
|--------|-------------|------------------|
| 200 OK | Requisição bem-sucedida | Páginas HTML renderizadas |
| 302 Found | Redirecionamento | Após criar/editar/deletar recursos |
| 400 Bad Request | Dados inválidos | Validação de formulário falhou |
| 403 Forbidden | Acesso negado | Usuário sem permissão |
| 404 Not Found | Recurso não encontrado | ID inválido |
| 500 Internal Server Error | Erro no servidor | Erro não tratado |

---

## 🔒 Sistema de Permissões

### Níveis de Acesso

| Ação | Admin | Motorista | Cliente |
|------|-------|-----------|---------|
| Ver todas entregas | ✅ | ❌ (só suas) | ❌ |
| Criar entrega | ✅ | ❌ | ❌ |
| Editar entrega | ✅ | ✅ (só suas) | ❌ |
| Deletar entrega | ✅ | ❌ | ❌ |
| Ver motoristas | ✅ | ❌ (só próprio perfil) | ❌ |
| Criar motorista | ✅ | ❌ | ❌ |
| Ver veículos | ✅ | ❌ | ❌ |
| Criar veículo | ✅ | ❌ | ❌ |
| Ver rotas | ✅ | ✅ (só suas) | ❌ |
| Criar rota | ✅ | ❌ | ❌ |
| Ver clientes | ✅ | ❌ | ❌ |
| Criar cliente | ✅ | ❌ | ❌ |
| Rastrear entrega | ✅ | ✅ | ✅ (público) |

---

## 📝 Exemplos Completos de Fluxo

### Fluxo 1: Criar Entrega Completa

```bash
# 1. Login como admin
curl -c cookies.txt -X POST http://localhost:8000/login/ \
  -d "username=admin&password=admin123"

# 2. Criar cliente
curl -b cookies.txt -X POST http://localhost:8000/clientes/criar/ \
  -F "nome=João Silva" \
  -F "email=joao@email.com" \
  -F "telefone=(11) 98765-4321"

# 3. Criar motorista
curl -b cookies.txt -X POST http://localhost:8000/motoristas/criar/ \
  -F "nome=Pedro Santos" \
  -F "cpf=12345678900" \
  -F "cnh=D" \
  -F "telefone=(11) 91234-5678" \
  -F "status=disponivel" \
  -F "criar_usuario=on"

# 4. Criar veículo
curl -b cookies.txt -X POST http://localhost:8000/veiculos/criar/ \
  -F "placa=ABC-1234" \
  -F "modelo=Fiat Ducato" \
  -F "tipo=van" \
  -F "capacidade_maxima=1000" \
  -F "km_atual=50000" \
  -F "status=disponivel"

# 5. Criar rota
curl -b cookies.txt -X POST http://localhost:8000/rotas/criar/ \
  -F "nome=Rota SP-RJ" \
  -F "motorista=1" \
  -F "veiculo=1" \
  -F "data_rota=2025-12-20" \
  -F "status=planejada" \
  -F "km_total_estimado=450" \
  -F "tempo_estimado=360"

# 6. Criar entrega
curl -b cookies.txt -X POST http://localhost:8000/entregas/criar/ \
  -F "codigo_rastreio=ENT001" \
  -F "cliente=1" \
  -F "motorista=1" \
  -F "endereco_origem=Rua A, 123, São Paulo" \
  -F "cep_origem=01000-000" \
  -F "endereco_destino=Rua B, 456, Rio de Janeiro" \
  -F "cep_destino=20000-000" \
  -F "status=pendente" \
  -F "capacidade_necessaria=50" \
  -F "valor_frete=150.00"

# 7. Adicionar entrega à rota
curl -b cookies.txt -X POST http://localhost:8000/rotas/1/adicionar-entrega/ \
  -F "entrega_id=1"

# 8. Rastrear entrega (sem autenticação)
curl -X GET "http://localhost:8000/buscar_entrega/?pesquisa=ENT001"
```

---
