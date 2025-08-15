from setuptools import setup, find_packages
import os

# Lê o arquivo requirements.txt
def read_requirements():
    requirements = []
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line)
    return requirements

# Lê o README.md para a descrição longa
def read_readme():
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    return "Sistema de Detecção Precoce de Sepse usando Machine Learning"

setup(
    name="sepsis-sentinel",
    version="1.0.0",
    description="Sistema de Detecção Precoce de Sepse usando Machine Learning",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    
    # Informações do autor
    author="Sepsis Sentinel Team",
    author_email="contato@sepsis-sentinel.com",
    url="https://github.com/seu-usuario/sepsis-sentinel-api",
    
    # Classificações
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    
    # Palavras-chave
    keywords=[
        "sepsis", "machine learning", "healthcare", "medical", 
        "random forest", "fastapi", "streamlit", "prediction",
        "clinical", "hospital", "icu", "vital signs"
    ],
    
    # Pacotes Python encontrados automaticamente
    packages=find_packages(),
    
    # Dependências
    install_requires=read_requirements(),
    
    # Dependências extras para desenvolvimento
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "pre-commit>=2.20.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "myst-parser>=0.18.0",
        ],
        "docker": [
            "docker>=6.0.0",
            "docker-compose>=1.29.0",
        ],
    },
    
    # Scripts de linha de comando
    entry_points={
        "console_scripts": [
            "sepsis-train=ml.train_model:main",
            "sepsis-api=api.main:main",
            "sepsis-frontend=frontend.app:main",
        ],
    },
    
    # Dados não-Python incluídos no pacote
    package_data={
        "ml": ["*.joblib", "*.pkl"],
        "api": ["*.yaml", "*.yml"],
        "frontend": ["*.toml", "*.css"],
    },
    
    # Dados incluídos no pacote
    include_package_data=True,
    
    # Python 3.9+ requerido
    python_requires=">=3.9",
    
    # URLs do projeto
    project_urls={
        "Bug Reports": "https://github.com/seu-usuario/sepsis-sentinel-api/issues",
        "Source": "https://github.com/seu-usuario/sepsis-sentinel-api",
        "Documentation": "https://sepsis-sentinel.readthedocs.io/",
        "Changelog": "https://github.com/seu-usuario/sepsis-sentinel-api/blob/main/CHANGELOG.md",
    },
    
    # Configurações específicas
    zip_safe=False,  # Não compactar em ZIP (para desenvolvimento)
    
    # Metadados adicionais
    platforms=["any"],
    license="MIT",
)
