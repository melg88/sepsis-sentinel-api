# 🚀 Início Rápido - Sepsis Sentinel

Este guia te ajudará a executar o projeto em menos de 5 minutos!

## ⚡ Execução Rápida

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Treinar o Modelo
```bash
python ml/train_model.py
```

### 3. Executar a API
```bash
cd api
uvicorn main:app --reload
```

### 4. Executar o Frontend
```bash
cd frontend
streamlit run app.py
```

## 🌐 Acessos

- **API**: http://localhost:8000
- **Docs da API**: http://localhost:8000/docs
- **Frontend**: http://localhost:8501

## 🧪 Teste Rápido

### Via API
```bash
curl -X POST http://localhost:8000/predict \
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

### Via Frontend
1. Abra http://localhost:8501
2. Preencha os dados do paciente
3. Clique em "Fazer Predição"
4. Veja o resultado!

## 📁 Estrutura do Projeto

```
sepsis-sentinel-api/
├── api/                    # Backend FastAPI
├── ml/                     # Machine Learning
├── frontend/               # Interface Streamlit
├── data/                   # Dados de treinamento
├── scripts/                # Scripts de automação
└── docs/                   # Documentação
```

## 🚨 Solução de Problemas

### Erro: "Model not found"
- Execute `python ml/train_model.py` primeiro

### Erro: "Port already in use"
- Use portas diferentes ou pare outros serviços

### Erro: "Module not found"
- Execute `pip install -r requirements.txt`

## 📚 Próximos Passos

1. **Teste local**: Execute os passos acima
2. **Personalize**: Modifique o modelo ou interface
3. **Deploy**: Siga o [DEPLOY.md](DEPLOY.md)
4. **Contribua**: Faça melhorias no código

## 💡 Dicas

- Use o script de automação: `python scripts/train_and_deploy.py`
- Verifique os logs da API para debug
- O frontend salva histórico das predições
- A API tem validação automática dos dados

## 🆘 Precisa de Ajuda?

- 📖 [Documentação Completa](README.md)
- 🚀 [Guia de Deploy](DEPLOY.md)
- 🐛 [Issues do Repositório]
- 💬 [Discord do Railway]

---

**🎯 Objetivo**: Detectar precocemente risco de sepse usando ML
**🔬 Tecnologia**: Random Forest + FastAPI + Streamlit
**🚀 Deploy**: Railway (pronto para produção)
