"""
Serviço para gerenciar predições de sepse
"""
import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional

# Adiciona o diretório raiz ao path para importar o módulo ml
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from ml.predict import SepsisPredictor, predict_sepsis
    MODEL_AVAILABLE = True
except Exception as e:
    print(f"Aviso: Modelo ML não disponível: {e}")
    MODEL_AVAILABLE = False

class SepsisService:
    """Serviço para gerenciar predições de sepse"""
    
    def __init__(self):
        """Inicializa o serviço"""
        self.predictor: Optional[SepsisPredictor] = None
        self.model_loaded = False
        
        if MODEL_AVAILABLE:
            try:
                self.predictor = SepsisPredictor()
                self.model_loaded = True
                print("✅ Serviço de sepse inicializado com sucesso")
            except Exception as e:
                print(f"❌ Erro ao inicializar serviço: {e}")
                self.model_loaded = False
    
    def predict_sepsis_risk(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Faz predição de risco de sepse para um paciente
        
        Args:
            patient_data: Dados clínicos do paciente
            
        Returns:
            Resultado da predição
        """
        if not self.model_loaded:
            return {
                "success": False,
                "error": "Modelo ML não está disponível",
                "prediction": 0.0,
                "risk_level": "Erro",
                "message": "Serviço temporariamente indisponível"
            }
        
        try:
            # Faz a predição usando o módulo ML
            result = predict_sepsis(patient_data)
            
            # Adiciona timestamp
            result["timestamp"] = datetime.now().isoformat()
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "prediction": 0.0,
                "risk_level": "Erro",
                "message": f"Erro durante predição: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Retorna o status de saúde do serviço"""
        return {
            "status": "healthy" if self.model_loaded else "unhealthy",
            "ml_model_loaded": self.model_loaded,
            "timestamp": datetime.now().isoformat(),
            "service": "SepsisService"
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o modelo"""
        if not self.model_loaded or not self.predictor:
            return {
                "available": False,
                "error": "Modelo não carregado"
            }
        
        try:
            return {
                "available": True,
                "features": self.predictor.get_available_features(),
                "feature_importance": self.predictor.get_feature_importance()
            }
        except Exception as e:
            return {
                "available": False,
                "error": str(e)
            }
    
    def validate_input_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida os dados de entrada do paciente
        
        Args:
            data: Dados a serem validados
            
        Returns:
            Resultado da validação
        """
        required_fields = [
            'hr', 'o2sat', 'temp', 'sbp', 'dbp', 'map', 
            'resp', 'age', 'gender', 'unit1', 'unit2', 
            'hosp_adm_time', 'iculos'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return {
                "valid": False,
                "missing_fields": missing_fields,
                "message": f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"
            }
        
        # Validações básicas de range
        validation_errors = []
        
        if 'hr' in data and (data['hr'] < 40 or data['hr'] > 200):
            validation_errors.append("Frequência cardíaca deve estar entre 40-200 bpm")
        
        if 'o2sat' in data and (data['o2sat'] < 0 or data['o2sat'] > 100):
            validation_errors.append("Saturação de oxigênio deve estar entre 0-100%")
        
        if 'temp' in data and (data['temp'] < 35 or data['temp'] > 42):
            validation_errors.append("Temperatura deve estar entre 35-42°C")
        
        if 'age' in data and (data['age'] < 0 or data['age'] > 150):
            validation_errors.append("Idade deve estar entre 0-150 anos")
        
        if validation_errors:
            return {
                "valid": False,
                "validation_errors": validation_errors,
                "message": "Dados fora dos ranges fisiológicos aceitáveis"
            }
        
        return {
            "valid": True,
            "message": "Dados validados com sucesso"
        }

# Instância global do serviço
sepsis_service = SepsisService()
