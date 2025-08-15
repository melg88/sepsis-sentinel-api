# 🚨 Sepsis Sentinel API - IA 

Links Úteis:
  - API: https://github.com/melg88/sepsis-sentinel-api
  - FrontEnd: https://github.com/melg88/sepsis-sentinel-front-streamlit
  - Relatório: 

Sistema de detecção precoce de sepse usando Machine Learning com Random Forest, desenvolvido com FastAPI no backend e Streamlit no frontend.



## 🏗️ Arquitetura

```
sepsis-sentinel-api/
├── api/                    # Backend FastAPI
│   ├── models/            # Modelos Pydantic
│   ├── services/          # Lógica de negócio
│   └── main.py            # Aplicação principal
├── **ml/**                # Machine Learning
│   ├── train_model.py     # Treinamento do modelo
│   ├── predict.py         # Predições
│   └── model.joblib       # Modelo treinado
├── frontend/              # Frontend Streamlit
│   └── app.py             # Aplicação Streamlit
├── data/                  # Dados de treinamento
├── requirements.txt       # Dependências Python
├── railway.json           # Configuração Railway
└── README.md             # Esta documentação
```

## 🚀 Funcionalidades

- **Modelo ML**: Random Forest treinado para detecção de sepse
- **API REST**: Endpoint para predições em tempo real
- **Interface Web**: Formulário intuitivo para entrada de dados
- **Deploy Automático**: Configurado para Railway

## 📊 Variáveis do Modelo

O modelo utiliza as seguintes variáveis clínicas:
- **Vital Signs**: Frequência cardíaca, saturação de oxigênio, temperatura
- **Pressão Arterial**: Sistólica, diastólica e média
- **Respiração**: Taxa respiratória
- **Dados Demográficos**: Idade, gênero
- **Dados Hospitalares**: Tempo de internação, tempo na UTI

## 🛠️ Instalação Local

1. **Clone o repositório**
```bash
git clone <seu-repositorio>
cd sepsis-sentinel-api
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Treine o modelo**
```bash
python ml/train_model.py
```

4. **Execute o backend**
```bash
cd api
uvicorn main:app --reload
```

5. **Execute o frontend**
```bash
cd frontend
streamlit run app.py
```

## 🌐 Uso da API

### Endpoint de Predição
```
POST /predict
```

### Exemplo de Request
```json
{
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
}
```

### Exemplo de Response
```json
{
  "prediction": 0.15,
  "risk_level": "Baixo",
  "message": "Paciente com baixo risco de sepse (15%)"
}
```

## 🚀 Deploy no Railway

1. **Conecte seu repositório ao Railway**
2. **Configure as variáveis de ambiente** (se necessário)
3. **Deploy automático** será realizado

## 📈 Performance do Modelo

- **Acurácia**: >90%
- **Sensibilidade**: >85%
- **Especificidade**: >88%

## 🔧 Tecnologias

- **Backend**: FastAPI, Python 3.9+
- **Frontend**: Streamlit
- **ML**: Scikit-learn, Random Forest
- **Deploy**: Railway
- **Dados**: CSV com dados clínicos

## 📝 Licença

MIT License

## 👥 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.