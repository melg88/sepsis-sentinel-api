"""
Modelos Pydantic para a API de detecção de sepse
"""
from pydantic import BaseModel, Field, validator
from typing import Optional

class SepsisInput(BaseModel):
    """Modelo para dados de entrada do paciente"""
    
    # Sinais vitais
    hr: float = Field(..., ge=0, le=300, description="Frequência cardíaca (bpm)")
    o2sat: float = Field(..., ge=0, le=100, description="Saturação de oxigênio (%)")
    temp: float = Field(..., ge=30, le=45, description="Temperatura corporal (°C)")
    
    # Pressão arterial
    sbp: float = Field(..., ge=0, le=300, description="Pressão sistólica (mmHg)")
    dbp: float = Field(..., ge=0, le=200, description="Pressão diastólica (mmHg)")
    map: float = Field(..., ge=0, le=200, description="Pressão arterial média (mmHg)")
    
    # Respiração
    resp: float = Field(..., ge=0, le=100, description="Taxa respiratória (rpm)")
    
    # Dados demográficos
    age: float = Field(..., ge=0, le=150, description="Idade (anos)")
    gender: int = Field(..., ge=0, le=1, description="Gênero (0=Feminino, 1=Masculino)")
    
    # Dados hospitalares
    unit1: int = Field(..., ge=0, le=1, description="Unidade 1 (0=Não, 1=Sim)")
    unit2: int = Field(..., ge=0, le=1, description="Unidade 2 (0=Não, 1=Sim)")
    hosp_adm_time: float = Field(..., ge=0, description="Tempo de internação (horas)")
    iculos: float = Field(..., ge=0, description="Tempo na UTI (horas)")
    
    @validator('map')
    def validate_map(cls, v, values):
        """Valida se MAP está dentro do range esperado baseado em SBP e DBP"""
        if 'sbp' in values and 'dbp' in values:
            sbp = values['sbp']
            dbp = values['dbp']
            expected_map = (sbp + 2 * dbp) / 3
            if abs(v - expected_map) > 20:
                raise ValueError(f"MAP deve estar próximo de {(sbp + 2 * dbp) / 3:.1f}")
        return v
    
    @validator('temp')
    def validate_temp(cls, v):
        """Valida se a temperatura está em um range fisiológico"""
        if v < 35 or v > 42:
            raise ValueError("Temperatura deve estar entre 35°C e 42°C")
        return v
    
    @validator('hr')
    def validate_hr(cls, v):
        """Valida se a frequência cardíaca está em um range fisiológico"""
        if v < 40 or v > 200:
            raise ValueError("Frequência cardíaca deve estar entre 40 e 200 bpm")
        return v

class SepsisResponse(BaseModel):
    """Modelo para resposta da predição de sepse"""
    
    prediction: float = Field(..., ge=0, le=1, description="Probabilidade de sepse (0-1)")
    risk_level: str = Field(..., description="Nível de risco (Baixo/Moderado/Alto/Crítico)")
    message: str = Field(..., description="Mensagem descritiva do resultado")
    success: bool = Field(..., description="Indica se a predição foi bem-sucedida")
    error: Optional[str] = Field(None, description="Mensagem de erro, se houver")

class HealthCheck(BaseModel):
    """Modelo para verificação de saúde da API"""
    
    status: str = Field(..., description="Status da API")
    timestamp: str = Field(..., description="Timestamp da verificação")
    model_loaded: bool = Field(..., description="Indica se o modelo ML está carregado")
    version: str = Field(..., description="Versão da API")

class ErrorResponse(BaseModel):
    """Modelo para respostas de erro"""
    
    error: str = Field(..., description="Descrição do erro")
    detail: Optional[str] = Field(None, description="Detalhes adicionais do erro")
    timestamp: str = Field(..., description="Timestamp do erro")
