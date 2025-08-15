from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import uvicorn
import os

from api.models.sepsis import SepsisInput, SepsisResponse, HealthCheck, ErrorResponse
from api.services.sepsis_service import sepsis_service

# Configuração da aplicação
app = FastAPI(
    title="Sepsis Sentinel API",
    description="API para detecção precoce de sepse usando Machine Learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("🚀 Iniciando Sepsis Sentinel API...")
    print(f"📊 Status do modelo: {'✅ Carregado' if sepsis_service.model_loaded else '❌ Não carregado'}")

@app.get("/", tags=["Root"])
async def root():
    """Endpoint raiz"""
    return {
        "message": "Sepsis Sentinel API",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthCheck, tags=["Health"])
async def health_check():
    service_status = sepsis_service.get_health_status()
    
    return HealthCheck(
        status=service_status["status"],
        timestamp=service_status["timestamp"],
        ml_model_loaded=service_status["ml_model_loaded"],
        version="1.0.0"
    )

@app.get("/model/info", tags=["Model"])
async def get_model_info():
    """Retorna informações sobre o modelo ML"""
    return sepsis_service.get_model_info()

@app.post("/predict", response_model=SepsisResponse, tags=["Prediction"])
async def predict_sepsis(input_data: SepsisInput):
    """
    Faz predição de risco de sepse para um paciente
    
    - **hr**: Frequência cardíaca (bpm)
    - **o2sat**: Saturação de oxigênio (%)
    - **temp**: Temperatura corporal (°C)
    - **sbp**: Pressão sistólica (mmHg)
    - **dbp**: Pressão diastólica (mmHg)
    - **map**: Pressão arterial média (mmHg)
    - **resp**: Taxa respiratória (rpm)
    - **age**: Idade (anos)
    - **gender**: Gênero (0=Feminino, 1=Masculino)
    - **unit1**: Unidade 1 (0=Não, 1=Sim)
    - **unit2**: Unidade 2 (0=Não, 1=Sim)
    - **hosp_adm_time**: Tempo de internação (horas)
    - **iculos**: Tempo na UTI (horas)
    """
    try:
        # Valida os dados de entrada
        validation_result = sepsis_service.validate_input_data(input_data.dict())
        if not validation_result["valid"]:
            raise HTTPException(
                status_code=400, 
                detail=validation_result["message"]
            )
        
        # Faz a predição
        result = sepsis_service.predict_sepsis_risk(input_data.dict())
        
        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=result["error"]
            )
        
        return SepsisResponse(
            prediction=result["prediction"],
            risk_level=result["risk_level"],
            message=result["message"],
            success=result["success"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Erro interno do servidor",
            detail=str(exc),
            timestamp=datetime.now().isoformat()
        ).dict()
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler para exceções HTTP"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            timestamp=datetime.now().isoformat()
        ).dict()
    )

if __name__ == "__main__":
    # Configuração para deploy no Railway
    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Desabilita reload em produção
    )
