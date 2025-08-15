#!/usr/bin/env python3
"""
Script para automatizar o treinamento do modelo e preparação para deploy
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Executa um comando e mostra o progresso"""
    print(f"\n🔄 {description}...")
    print(f"Comando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} concluído com sucesso!")
        if result.stdout:
            print("Saída:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}:")
        print(f"Erro: {e.stderr}")
        return False

def check_requirements():
    """Verifica se os requisitos estão instalados"""
    print("🔍 Verificando requisitos...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'streamlit', 'pandas', 
        'numpy', 'scikit-learn', 'joblib', 'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️ Pacotes faltando: {', '.join(missing_packages)}")
        print("Instalando dependências...")
        
        if not run_command("pip install -r requirements.txt", "Instalação de dependências"):
            print("❌ Falha na instalação das dependências")
            return False
    
    return True

def train_model():
    """Treina o modelo ML"""
    print("\n🤖 Iniciando treinamento do modelo...")
    
    # Verifica se o dataset existe
    dataset_path = Path("data/dataset_processado (1).csv")
    if not dataset_path.exists():
        print(f"❌ Dataset não encontrado em {dataset_path}")
        return False
    
    # Executa o treinamento
    if not run_command("python ml/train_model.py", "Treinamento do modelo"):
        return False
    
    # Verifica se o modelo foi criado
    model_path = Path("ml/model.joblib")
    if not model_path.exists():
        print("❌ Modelo não foi criado")
        return False
    
    print(f"✅ Modelo salvo em {model_path}")
    return True

def test_api():
    """Testa a API localmente"""
    print("\n🧪 Testando API...")
    
    # Inicia a API em background
    print("Iniciando API em background...")
    api_process = subprocess.Popen(
        ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Aguarda a API inicializar
    import time
    time.sleep(5)
    
    try:
        # Testa endpoint de saúde
        import requests
        response = requests.get("http://localhost:8000/health", timeout=10)
        
        if response.status_code == 200:
            print("✅ API funcionando corretamente")
            health_data = response.json()
            print(f"Status: {health_data.get('status')}")
            print(f"Modelo carregado: {health_data.get('model_loaded')}")
        else:
            print(f"❌ API retornou status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar API: {e}")
        return False
    finally:
        # Para a API
        api_process.terminate()
        api_process.wait()
    
    return True

def test_frontend():
    """Testa o frontend localmente"""
    print("\n🌐 Testando frontend...")
    
    # Verifica se o arquivo existe
    frontend_path = Path("frontend/app.py")
    if not frontend_path.exists():
        print(f"❌ Frontend não encontrado em {frontend_path}")
        return False
    
    print("✅ Frontend encontrado")
    print("💡 Para testar o frontend, execute: streamlit run frontend/app.py")
    return True

def prepare_deploy():
    """Prepara arquivos para deploy"""
    print("\n🚀 Preparando para deploy...")
    
    # Verifica arquivos essenciais
    essential_files = [
        "railway.json",
        "Procfile", 
        "runtime.txt",
        "requirements.txt",
        "api/main.py",
        "ml/model.joblib"
    ]
    
    missing_files = []
    for file_path in essential_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Arquivos faltando para deploy: {', '.join(missing_files)}")
        return False
    
    print("✅ Todos os arquivos de deploy estão presentes")
    
    # Cria arquivo de status
    deploy_status = {
        "deploy_ready": True,
        "timestamp": str(Path().cwd()),
        "model_trained": Path("ml/model.joblib").exists(),
        "api_ready": Path("api/main.py").exists(),
        "frontend_ready": Path("frontend/app.py").exists()
    }
    
    print("\n📋 Status do Deploy:")
    for key, value in deploy_status.items():
        status_icon = "✅" if value else "❌"
        print(f"{status_icon} {key}: {value}")
    
    return True

def main():
    """Função principal"""
    print("🚀 SEPSSIS SENTINEL - AUTOMAÇÃO DE TREINAMENTO E DEPLOY")
    print("=" * 60)
    
    # Verifica requisitos
    if not check_requirements():
        print("❌ Falha na verificação de requisitos")
        return False
    
    # Treina o modelo
    if not train_model():
        print("❌ Falha no treinamento do modelo")
        return False
    
    # Testa a API
    if not test_api():
        print("❌ Falha no teste da API")
        return False
    
    # Testa o frontend
    if not test_frontend():
        print("❌ Falha no teste do frontend")
        return False
    
    # Prepara deploy
    if not prepare_deploy():
        print("❌ Falha na preparação do deploy")
        return False
    
    print("\n🎉 TODOS OS TESTES PASSARAM!")
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. ✅ Modelo treinado e salvo")
    print("2. ✅ API testada e funcionando")
    print("3. ✅ Frontend verificado")
    print("4. ✅ Arquivos de deploy prontos")
    print("\n🚀 Para fazer deploy no Railway:")
    print("1. Faça commit e push para o repositório")
    print("2. Conecte o repositório ao Railway")
    print("3. Deploy automático será realizado")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
