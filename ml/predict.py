"""
Módulo para fazer predições usando o modelo treinado
"""
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple

class SepsisPredictor:
    """Classe para predições de sepse usando o modelo treinado"""
    
    def __init__(self, model_path: str = 'ml/model.joblib', 
                 feature_info_path: str = 'ml/feature_info.joblib'):
        """Inicializa o preditor carregando o modelo e informações das features"""
        try:
            self.model = joblib.load(model_path)
            self.feature_info = joblib.load(feature_info_path)
            self.feature_names = self.feature_info['feature_names']
            print(f"Modelo carregado com sucesso. Features: {self.feature_names}")
        except Exception as e:
            raise Exception(f"Erro ao carregar modelo: {str(e)}")
    
    def preprocess_input(self, input_data: Dict[str, Any]) -> np.ndarray:
        """Pré-processa os dados de entrada para o formato esperado pelo modelo"""
        # Mapeia os nomes das features de entrada para as features do modelo
        feature_mapping = {
            'hr': 'HR_mean',
            'o2sat': 'O2Sat_mean', 
            'temp': 'Temp_mean',
            'sbp': 'SBP_mean',
            'dbp': 'DBP_mean',
            'map': 'MAP_mean',
            'resp': 'Resp_mean',
            'age': 'Age_mean',
            'gender': 'Gender_mean',
            'unit1': 'Unit1_mean',
            'unit2': 'Unit2_mean',
            'hosp_adm_time': 'HospAdmTime_mean',
            'iculos': 'ICULOS_mean'
        }
        
        # Cria um array com as features na ordem correta
        features = []
        for feature_name in self.feature_names:
            # Encontra a chave correspondente no input_data
            input_key = None
            for key, value in feature_mapping.items():
                if value == feature_name:
                    input_key = key
                    break
            
            if input_key and input_key in input_data:
                features.append(input_data[input_key])
            else:
                # Valor padrão se a feature não for fornecida
                features.append(0.0)
        
        return np.array(features).reshape(1, -1)
    
    def predict(self, input_data: Dict[str, Any]) -> Tuple[float, str, str]:
        """
        Faz a predição de risco de sepse
        
        Args:
            input_data: Dicionário com os dados do paciente
            
        Returns:
            Tuple com (probabilidade, nível_risco, mensagem)
        """
        try:
            # Pré-processa os dados
            X = self.preprocess_input(input_data)
            
            # Faz a predição
            prediction_proba = self.model.predict_proba(X)[0, 1]
            
            # Determina o nível de risco
            risk_level, message = self._get_risk_level(prediction_proba)
            
            return prediction_proba, risk_level, message
            
        except Exception as e:
            raise Exception(f"Erro durante predição: {str(e)}")
    
    def _get_risk_level(self, probability: float) -> Tuple[str, str]:
        """Determina o nível de risco baseado na probabilidade"""
        if probability < 0.2:
            return "Baixo", f"Paciente com baixo risco de sepse ({probability:.1%})"
        elif probability < 0.5:
            return "Moderado", f"Paciente com risco moderado de sepse ({probability:.1%})"
        elif probability < 0.8:
            return "Alto", f"Paciente com alto risco de sepse ({probability:.1%})"
        else:
            return "Crítico", f"Paciente com risco crítico de sepse ({probability:.1%})"
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Retorna a importância das features"""
        return self.feature_info['feature_importance']
    
    def get_available_features(self) -> list:
        """Retorna a lista de features disponíveis"""
        return self.feature_names.copy()

def predict_sepsis(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função de conveniência para fazer predições
    
    Args:
        input_data: Dicionário com os dados do paciente
        
    Returns:
        Dicionário com o resultado da predição
    """
    try:
        predictor = SepsisPredictor()
        probability, risk_level, message = predictor.predict(input_data)
        
        return {
            "prediction": round(probability, 4),
            "risk_level": risk_level,
            "message": message,
            "success": True
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "prediction": 0.0,
            "risk_level": "Erro",
            "message": "Erro durante predição"
        }

# Exemplo de uso
if __name__ == "__main__":
    # Dados de exemplo
    sample_data = {
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
    
    try:
        result = predict_sepsis(sample_data)
        print("Resultado da predição:")
        print(f"Probabilidade: {result['prediction']:.1%}")
        print(f"Nível de risco: {result['risk_level']}")
        print(f"Mensagem: {result['message']}")
    except Exception as e:
        print(f"Erro: {e}")
