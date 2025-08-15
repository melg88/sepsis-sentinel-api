# 🐳 Docker - Sepsis Sentinel

Este guia explica como executar o projeto usando Docker e Docker Compose.

## 🚀 Execução Rápida com Docker

### 1. Usando Docker Compose (Recomendado)

```bash
# Construir e executar todos os serviços
docker-compose up --build

# Executar em background
docker-compose up -d --build

# Parar os serviços
docker-compose down
```

### 2. Usando Docker Individual

```bash
# Construir a imagem da API
docker build -t sepsis-api .

# Executar a API
docker run -p 8000:8000 sepsis-api

# Construir a imagem do Frontend
docker build -f Dockerfile.frontend -t sepsis-frontend .

# Executar o Frontend
docker run -p 8501:8501 sepsis-frontend
```

## 🌐 Acessos

- **API**: http://localhost:8000
- **Frontend**: http://localhost:8501
- **Docs da API**: http://localhost:8000/docs

## 📁 Estrutura Docker

```
├── Dockerfile              # API FastAPI
├── Dockerfile.frontend     # Frontend Streamlit
├── docker-compose.yml      # Orquestração
└── .dockerignore          # Arquivos ignorados
```

## ⚙️ Configurações

### Variáveis de Ambiente

No `docker-compose.yml`:

```yaml
environment:
  - PORT=8000
  - API_BASE_URL=http://api:8000
```

### Volumes

```yaml
volumes:
  - .:/app  # Sincroniza código local com container
```

## 🔧 Desenvolvimento

### Modo Desenvolvimento

```bash
# Com reload automático
docker-compose up --build

# Ver logs
docker-compose logs -f api
docker-compose logs -f frontend
```

### Debug

```bash
# Acessar container da API
docker-compose exec api bash

# Acessar container do Frontend
docker-compose exec frontend bash
```

## 🚨 Solução de Problemas

### Erro: "Port already in use"
```bash
# Verificar portas em uso
netstat -tulpn | grep :8000
netstat -tulpn | grep :8501

# Parar serviços
docker-compose down
```

### Erro: "Build failed"
```bash
# Limpar cache Docker
docker system prune -a

# Reconstruir
docker-compose build --no-cache
```

### Erro: "Model not found"
```bash
# Verificar se o modelo existe
ls -la /..ml/model.joblib

# Treinar modelo se necessário
docker-compose exec api python ml/train_model.py
```

## 📊 Monitoramento

### Logs em Tempo Real
```bash
# Todos os serviços
docker-compose logs -f

# Serviço específico
docker-compose logs -f api
docker-compose logs -f frontend
```

### Status dos Containers
```bash
docker-compose ps
docker stats
```

## 🔄 Atualizações

### Atualizar Código
```bash
# Parar serviços
docker-compose down

# Reconstruir
docker-compose up --build
```

### Atualizar Dependências
```bash
# Editar requirements.txt
# Reconstruir
docker-compose build --no-cache
docker-compose up
```

## 🎯 Casos de Uso

### Desenvolvimento Local
```bash
docker-compose up --build
```

### Testes
```bash
# Executar testes no container
docker-compose exec api python -m pytest

# Executar script de automação
docker-compose exec api python scripts/train_and_deploy.py
```

### Produção
```bash
# Construir imagem de produção
docker build -t sepsis-api:prod .

# Executar em produção
docker run -d -p 8000:8000 --name sepsis-api-prod sepsis-api:prod
```

## 📝 Notas Importantes

1. **Volumes**: O código é sincronizado via volumes para desenvolvimento
2. **Portas**: 8000 (API) e 8501 (Frontend)
3. **Dependências**: Instaladas automaticamente durante o build
4. **Modelo ML**: Deve ser treinado antes ou durante a execução
5. **Logs**: Acessíveis via `docker-compose logs`

## 🆘 Comandos Úteis

```bash
# Limpar tudo
docker-compose down -v --remove-orphans
docker system prune -a

# Verificar imagens
docker images | grep sepsis

# Executar comando específico
docker-compose exec api python ml/train_model.py
docker-compose exec frontend streamlit --version

# Backup do modelo
docker cp sepsis-api:/app/ml/model.joblib ./ml/
```

## 🚀 Próximos Passos

1. ✅ Execute com Docker Compose
2. 🔧 Configure variáveis de ambiente
3. 🧪 Teste todos os endpoints
4. 🚀 Deploy no Railway (sem Docker)
5. 🐳 Configure Docker para produção (opcional)

---

**💡 Dica**: Use Docker Compose para desenvolvimento e Railway para produção!
