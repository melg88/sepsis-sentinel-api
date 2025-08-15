"""
Arquivo de configuração centralizada para o Sepsis Sentinel
"""
import os
from typing import Optional

# -----------------------------------------------------------------------------
# Configurações de Ambiente
# -----------------------------------------------------------------------------

# Detecta se está rodando no Railway
RAILWAY_ENVIRONMENT = os.environ.get("RAILWAY_ENVIRONMENT", "false").lower() == "true"

# -----------------------------------------------------------------------------
# URLs da API
# -----------------------------------------------------------------------------

# Desenvolvimento local
API_BASE_URL_LOCAL = "http://localhost:8000"

# Produção no Railway (será definida via variável de ambiente)
API_BASE_URL_PRODUCTION = os.environ.get("API_URL", "https://seu-api.railway.app")

# URL ativa baseada no ambiente
API_BASE_URL = API_BASE_URL_PRODUCTION if RAILWAY_ENVIRONMENT else API_BASE_URL_LOCAL

# -----------------------------------------------------------------------------
# Configurações do Frontend
# -----------------------------------------------------------------------------

# Configurações do Streamlit
STREAMLIT_CONFIG = {
    "server_port": os.environ.get("PORT", 8501),
    "server_address": "0.0.0.0",
    "server_headless": True,
    "browser_gather_usage_stats": False
}

# -----------------------------------------------------------------------------
# Configurações da API
# -----------------------------------------------------------------------------

# Configurações do FastAPI
FASTAPI_CONFIG = {
    "port": int(os.environ.get("PORT", 8000)),
    "host": "0.0.0.0",
    "reload": not RAILWAY_ENVIRONMENT,  # False em produção
    "workers": 1
}

# -----------------------------------------------------------------------------
# Configurações do Modelo ML
# -----------------------------------------------------------------------------

# Caminhos dos arquivos do modelo
MODEL_PATHS = {
    "model": os.environ.get("MODEL_PATH", "ml/model.joblib"),
    "feature_info": os.environ.get("FEATURE_INFO_PATH", "ml/feature_info.joblib")
}

# -----------------------------------------------------------------------------
# Configurações de Log
# -----------------------------------------------------------------------------

# Nível de log baseado no ambiente
LOG_LEVEL = "INFO" if RAILWAY_ENVIRONMENT else "DEBUG"

# -----------------------------------------------------------------------------
# Funções de Utilidade
# -----------------------------------------------------------------------------

def get_api_url() -> str:
    """Retorna a URL da API baseada no ambiente"""
    return API_BASE_URL

def is_production() -> bool:
    """Verifica se está rodando em produção"""
    return RAILWAY_ENVIRONMENT

def get_model_path() -> str:
    """Retorna o caminho do modelo ML"""
    return MODEL_PATHS["model"]

def get_feature_info_path() -> str:
    """Retorna o caminho das informações das features"""
    return MODEL_PATHS["feature_info"]

# -----------------------------------------------------------------------------
# Configurações de CORS
# -----------------------------------------------------------------------------

# URLs permitidas para CORS
CORS_ORIGINS = [
    "http://localhost:8501",  # Frontend local
    "http://localhost:3000",  # Outros frontends locais
]

# Adiciona URLs de produção se estiver no Railway
if RAILWAY_ENVIRONMENT:
    frontend_url = os.environ.get("FRONTEND_URL", "https://seu-frontend.railway.app")
    CORS_ORIGINS.append(frontend_url)

# -----------------------------------------------------------------------------
# Configurações de Segurança
# -----------------------------------------------------------------------------

# Chave secreta para sessões (em produção, deve ser definida via variável de ambiente)
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

# -----------------------------------------------------------------------------
# Configurações de Banco de Dados (futuro)
# -----------------------------------------------------------------------------

# URL do banco de dados (se necessário no futuro)
DATABASE_URL = os.environ.get("DATABASE_URL", None)

# -----------------------------------------------------------------------------
# Configurações de Cache (futuro)
# -----------------------------------------------------------------------------

# URL do Redis (se necessário no futuro)
REDIS_URL = os.environ.get("REDIS_URL", None)

# -----------------------------------------------------------------------------
# Validação de Configuração
# -----------------------------------------------------------------------------

def validate_config():
    """Valida se todas as configurações necessárias estão presentes"""
    required_vars = []
    
    if RAILWAY_ENVIRONMENT:
        required_vars.extend([
            "API_URL",
            "PORT"
        ])
    
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"⚠️ Variáveis de ambiente faltando: {', '.join(missing_vars)}")
        print("💡 Configure-as no Railway Dashboard > Variables")
        return False
    
    return True

# -----------------------------------------------------------------------------
# Informações de Debug
# -----------------------------------------------------------------------------

def print_config():
    """Imprime a configuração atual para debug"""
    print("🔧 CONFIGURAÇÃO ATUAL:")
    print(f"   Ambiente: {'🚀 Produção (Railway)' if RAILWAY_ENVIRONMENT else '💻 Desenvolvimento Local'}")
    print(f"   API URL: {API_BASE_URL}")
    print(f"   Porta API: {FASTAPI_CONFIG['port']}")
    print(f"   Porta Frontend: {STREAMLIT_CONFIG['server_port']}")
    print(f"   Modelo ML: {get_model_path()}")
    print(f"   Log Level: {LOG_LEVEL}")
    print(f"   CORS Origins: {CORS_ORIGINS}")

if __name__ == "__main__":
    print_config()
    validate_config()
