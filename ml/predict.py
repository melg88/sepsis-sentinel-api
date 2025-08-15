import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple

class SepsisPredictor:
    
    def __init__(self, model_path: str = 'ml/model.joblib', 
                 feature_info_path: str = 'ml/feature_info.joblib'):
        try:
            self.model = joblib.load(model_path)
            self.feature_info = joblib.load(feature_info_path)
            self.feature_names = self.feature_info['feature_names']
            print(f"Modelo carregado com sucesso. Features: {self.feature_names}")
        except Exception as e:
            raise Exception(f"Erro ao carregar modelo: {str(e)}")
    
    def preprocess_input(self, input_data: Dict[str, Any]) -> np.ndarray:
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
        

        features = []
        for feature_name in self.feature_names:
            input_key = None
            for key, value in feature_mapping.items():
                if value == feature_name:
                    input_key = key
                    break
            
            if input_key and input_key in input_data:
                features.append(input_data[input_key])
            else:
                features.append(0.0)
        
        return np.array(features).reshape(1, -1)
    
    def predict(self, input_data: Dict[str, Any]) -> Tuple[float, str, str]:
        try:
            X = self.preprocess_input(input_data)
            
            prediction_proba = self.model.predict_proba(X)[0, 1]
            
            risk_level, message = self._get_risk_level(prediction_proba)
            
            return prediction_proba, risk_level, message
            
        except Exception as e:
            raise Exception(f"Erro durante predição: {str(e)}")
    
    def _get_risk_level(self, probability: float) -> Tuple[str, str]:
        if probability < 0.2:
            return "Baixo", f"Paciente com baixo risco de sepse ({probability:.1%})"
        elif probability < 0.5:
            return "Moderado", f"Paciente com risco moderado de sepse ({probability:.1%})"
        elif probability < 0.8:
            return "Alto", f"Paciente com alto risco de sepse ({probability:.1%})"
        else:
            return "Crítico", f"Paciente com risco crítico de sepse ({probability:.1%})"
    
    def get_feature_importance(self) -> Dict[str, float]:
        return self.feature_info['feature_importance']
    
    def get_available_features(self) -> list:
        return self.feature_names.copy()

def predict_sepsis(input_data: Dict[str, Any]) -> Dict[str, Any]:
    #teste ok
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
