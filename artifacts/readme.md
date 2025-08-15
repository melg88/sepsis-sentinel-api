# 🩺 Diagnóstico Precoce de Sepse com CRISP-DM

Este diretório contém todos os artefatos do projeto acadêmico **"Aplicação do Método CRISP-DM para Diagnóstico Hospitalar Precoce de Sepse"**, desenvolvido como requisito para a disciplina de Inteligência Artificial (IF1017) do Centro de Informática da Universidade Federal de Pernambuco (UFPE).

O projeto realiza uma investigação completa, desde o entendimento do problema e a análise exploratória dos dados até o treinamento, avaliação e seleção de múltiplos modelos de Machine Learning para a predição de sepse em ambiente hospitalar.

---

## 🏗️ Arquitetura do Diretório

````
projeto-sepse-crisp-dm/
├── dataset/                              # Conjunto de dados original utilizado no estudo
│   └── sepsis_data.csv
├── docs/                                 # Artigos acadêmicos do projeto
│   ├── versao_completa.pdf               # Artigo completo com todo o detalhamento metodológico
│   └── versao_resumida.pdf               # Versão resumida de 5 páginas do artigo
├── notebook/                             # Notebook com o código-fonte
│   └── analise_e_treinamento.ipynb       # Código de análise, limpeza, treinamento e avaliação
├── slides/                               # Apresentação final do projeto
│   └── apresentacao.pdf
└── README.md                             # Esta documentação
````
---

## 🚀 Destaques do Projeto

- **Metodologia Robusta:** Aplicação rigorosa de todas as fases do CRISP-DM para guiar o desenvolvimento do projeto.

- **Análise Exploratória Detalhada:** Investigação profunda da qualidade dos dados, tratamento de valores ausentes, análise de correlações e visualizações para extrair insights clínicos.

- **Comparativo de Modelos:** Treinamento e avaliação de diversos algoritmos, incluindo:
  - K-Nearest Neighbors (KNN)
  - Árvore de Decisão
  - Support Vector Machine (SVM)
  - Random Forest
  - Rede Neural (MLP) e Comitê de MLPs
  - Gradient Boosting (XGBoost e LightGBM)
  - Ensemble Híbrido (Stacking)

- **Seleção Baseada em Requisitos Clínicos:** Considerando acurácia, interpretabilidade e sensibilidade (recall).

---

## 📊 Variáveis do Modelo

Após a preparação dos dados, o modelo foi treinado com **16 atributos principais**, selecionados por relevância clínica e preenchimento ≥ 60%.  

**Sinais Vitais:**
- Frequência Cardíaca
- Saturação de Oxigênio
- Temperatura

**Pressão Arterial:**
- Sistólica
- Diastólica
- Média

**Respiração:**
- Frequência Respiratória

**Dados Demográficos:**
- Idade
- Sexo

**Dados Hospitalares:**
- Unidade de Internação (MICU/SICU)
- Tempo Desde Admissão Hospitalar
- Tempo de Internação na UTI

---

## 🔬 Conteúdo do Repositório

- **`/docs`** → Artigo acadêmico completo + versão resumida.
- **`/notebook`** → Notebook `.ipynb` com limpeza, análise, modelagem e avaliação.
- **`/dataset`** → Conjunto de dados brutos.
- **`/slides`** → Apresentação final do projeto.

---

## 📈 Performance do Modelo

**LightGBM (Melhor Performance Geral)**
- Acurácia: **95,1%**
- F1-Score: **0.659**
- AUC-ROC: **0.908**

**Random Forest (Recomendado para Implementação)**
- Acurácia: **95,7%**
- F1-Score: **0.627**
- AUC-ROC: **0.895**


> Apesar da performance ligeiramente superior do LightGBM, o Random Forest foi o recomendado pela sua alta interpretabilidade, robustez e menor custo computacional — fatores cruciais em dados sensíveis de saúde.

---

## 🔧 Tecnologias e Metodologias

- **Metodologia:** CRISP-DM
- **Linguagem:** Python
- **Bibliotecas:** Scikit-learn, XGBoost, LightGBM, Pandas, Matplotlib, Seaborn
- **Ambiente:** Google Colab / Jupyter Notebook

---

## 📝 Licença

MIT License

---

## 👥 Autores

- Allyson Ryan Emiliano da Silva  
- Erick Daniel Alves de Lima  
- Lucas Gabriel de Oliveira Silva  
- Maria Eduarda de Lima Gomes  

**Orientador:** Prof. Flávio Arthur Oliveira dos Santos
