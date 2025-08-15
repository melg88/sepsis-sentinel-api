# 🚀 Guia de Deploy no Railway

Este guia explica como fazer o deploy da aplicação Sepsis Sentinel no Railway.

## 📋 Pré-requisitos

1. **Conta no Railway**: [railway.app](https://railway.app)
2. **Repositório Git**: Código deve estar em um repositório GitHub/GitLab
3. **Modelo Treinado**: Execute `python ml/train_model.py` antes do deploy

## 🔧 Preparação Local

### 1. Treinar o Modelo

```bash
# Instale as dependências
pip install -r requirements.txt

# Treine o modelo
python ml/train_model.py
```

### 2. Testar Localmente

```bash
# Terminal 1: Backend
cd api
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
streamlit run app.py
```

### 3. Verificar Arquivos de Deploy

Certifique-se de que os seguintes arquivos existem:
- ✅ `railway.json`
- ✅ `Procfile`
- ✅ `runtime.txt`
- ✅ `requirements.txt`
- ✅ `ml/model.joblib` (após treinamento)

## 🚀 Deploy no Railway

### Opção 1: Deploy via GitHub (Recomendado)

1. **Faça commit e push do código**
```bash
git add .
git commit -m "Preparando para deploy no Railway"
git push origin main
```

2. **Acesse o Railway**
   - Vá para [railway.app](https://railway.app)
   - Faça login com sua conta GitHub

3. **Crie um novo projeto**
   - Clique em "New Project"
   - Selecione "Deploy from GitHub repo"

4. **Conecte o repositório**
   - Selecione seu repositório
   - Escolha a branch (geralmente `main`)

5. **Configure o projeto**
   - Nome: `sepsis-sentinel-api`
   - Framework: `Python`
   - Build Command: Deixe vazio (usará o Procfile)
   - Start Command: Deixe vazio (usará o Procfile)

6. **Deploy automático**
   - O Railway detectará automaticamente que é uma aplicação Python
   - Usará o `Procfile` para iniciar a aplicação
   - O deploy será iniciado automaticamente

### Opção 2: Deploy via Railway CLI

1. **Instale o Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Faça login**
```bash
railway login
```

3. **Deploy**
```bash
railway up
```

## ⚙️ Configurações do Railway

### Variáveis de Ambiente (Opcional)

Se necessário, configure estas variáveis no Railway:

```bash
# No dashboard do Railway > Variables
PORT=8000
ENVIRONMENT=production
```

### Domínio Personalizado

1. No dashboard do Railway, vá para "Settings"
2. Clique em "Domains"
3. Adicione seu domínio personalizado

## 🔍 Verificação do Deploy

### 1. Endpoints da API

Após o deploy, teste os endpoints:

```bash
# Health check
curl https://seu-app.railway.app/health

# Documentação
https://seu-app.railway.app/docs

# Predição (exemplo)
curl -X POST https://seu-app.railway.app/predict \
  -H "Content-Type: application/json" \
  -d '{
    "hr": 95,
    "o2sat": 98,
    "temp": 37.2,
    "sbp": 120,
    "dbp": 80,
    "map": 93,
    "resp": 18,
    "age": 45,
    "gender": 1,
    "unit1": 1,
    "unit2": 0,
    "hosp_adm_time": 24,
    "iculos": 48
  }'
```

### 2. Logs

No dashboard do Railway:
- Vá para "Deployments"
- Clique no deployment mais recente
- Verifique os logs para identificar possíveis erros

## 🐛 Troubleshooting

### Erro: "Module not found"

**Sintoma**: Erro de importação no deploy
**Solução**: Verifique se o `requirements.txt` está correto

### Erro: "Port already in use"

**Sintoma**: Aplicação não inicia
**Solução**: O Railway define a porta automaticamente via variável `$PORT`

### Erro: "Model not found"

**Sintoma**: API retorna erro sobre modelo não carregado
**Solução**: Verifique se `ml/model.joblib` foi commitado

### Erro: "Build failed"

**Sintoma**: Deploy falha na construção
**Solução**: 
1. Verifique os logs de build
2. Confirme que `runtime.txt` especifica uma versão Python válida
3. Verifique se todas as dependências estão em `requirements.txt`

## 📊 Monitoramento

### Métricas do Railway

- **Uptime**: Disponível no dashboard
- **Logs**: Acesso em tempo real
- **Deployments**: Histórico de deploys

### Health Checks

Configure health checks externos para monitorar:
- Endpoint `/health`
- Endpoint `/`
- Tempo de resposta da API

## 🔄 Deploy Contínuo

### GitHub Actions (Opcional)

Crie `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Railway
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        uses: railway/deploy@v1
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
```

## 📝 Notas Importantes

1. **Modelo ML**: Deve ser treinado antes do deploy
2. **Arquivos Grandes**: O modelo `.joblib` pode ser grande, mas é necessário
3. **Dependências**: Todas as dependências devem estar em `requirements.txt`
4. **Porta**: Use `$PORT` (Railway define automaticamente)
5. **Logs**: Sempre verifique os logs em caso de erro

## 🎯 Próximos Passos

Após o deploy bem-sucedido:

1. ✅ Teste todos os endpoints
2. ✅ Configure domínio personalizado (se necessário)
3. ✅ Configure monitoramento
4. ✅ Atualize o frontend com a URL da API em produção
5. ✅ Teste o frontend com a API em produção

## 📞 Suporte

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Issues**: Abra uma issue no repositório
- **Discord**: [Railway Discord](https://discord.gg/railway)
