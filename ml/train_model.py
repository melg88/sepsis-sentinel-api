"""
Script para treinar o modelo Random Forest para detecção de sepse
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os

def load_and_preprocess_data():
    """Carrega e pré-processa os dados"""
    print("Carregando dados...")
    
    # Carrega o dataset
    df = pd.read_csv('data/dataset_processado.csv')
    
    print(f"Dataset carregado com {len(df)} registros e {len(df.columns)} colunas")
    print(f"Colunas disponíveis: {list(df.columns)}")
    
    # Seleciona as features relevantes para o modelo
    # Usando as colunas que fazem sentido para predição de sepse
    feature_columns = [
        'HR_mean', 'O2Sat_mean', 'Temp_mean', 
        'SBP_mean', 'DBP_mean', 'MAP_mean', 'Resp_mean',
        'Age_mean', 'Gender_mean', 'Unit1_mean', 'Unit2_mean',
        'HospAdmTime_mean', 'ICULOS_mean'
    ]
    
    # Verifica se as colunas existem
    available_features = [col for col in feature_columns if col in df.columns]
    print(f"Features disponíveis: {available_features}")
    
    # Seleciona apenas as features disponíveis
    X = df[available_features].copy()
    y = df['SepsisLabel']
    
    # Remove linhas com valores NaN
    mask = ~(X.isnull().any(axis=1) | y.isnull())
    X = X[mask]
    y = y[mask]
    
    print(f"Dados após limpeza: {len(X)} registros")
    print(f"Distribuição das classes: {y.value_counts().to_dict()}")
    
    return X, y

def train_random_forest(X, y):
    """Treina o modelo Random Forest"""
    print("Treinando modelo Random Forest...")
    
    # Divide os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Inicializa o modelo
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    # Treina o modelo
    rf_model.fit(X_train, y_train)
    
    # Faz predições
    y_pred = rf_model.predict(X_test)
    y_pred_proba = rf_model.predict_proba(X_test)[:, 1]
    
    # Avalia o modelo
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Acurácia: {accuracy:.4f}")
    
    # Cross-validation
    cv_scores = cross_val_score(rf_model, X, y, cv=5)
    print(f"Cross-validation scores: {cv_scores}")
    print(f"CV média: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Relatório de classificação
    print("\nRelatório de Classificação:")
    print(classification_report(y_test, y_pred))
    
    # Matriz de confusão
    print("\nMatriz de Confusão:")
    print(confusion_matrix(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nFeature Importance:")
    print(feature_importance)
    
    return rf_model, X.columns.tolist()

def save_model(model, feature_names):
    """Salva o modelo treinado e as informações das features"""
    print("Salvando modelo...")
    
    # Cria diretório se não existir
    os.makedirs('ml', exist_ok=True)
    
    # Salva o modelo
    joblib.dump(model, 'ml/model.joblib')
    
    # Salva as informações das features
    feature_info = {
        'feature_names': feature_names,
        'feature_importance': dict(zip(feature_names, model.feature_importances_))
    }
    joblib.dump(feature_info, 'ml/feature_info.joblib')
    
    print("Modelo salvo em 'ml/model.joblib'")
    print("Informações das features salvas em 'ml/feature_info.joblib'")

def main():
    """Função principal"""
    print("=== TREINAMENTO DO MODELO DE DETECÇÃO DE SEPSE ===\n")
    
    try:
        # Carrega e pré-processa os dados
        X, y = load_and_preprocess_data()
        
        # Treina o modelo
        model, feature_names = train_random_forest(X, y)
        
        # Salva o modelo
        save_model(model, feature_names)
        
        print("\n✅ Modelo treinado e salvo com sucesso!")
        print(f"Features utilizadas: {feature_names}")
        
    except Exception as e:
        print(f"❌ Erro durante o treinamento: {str(e)}")
        raise

if __name__ == "__main__":
    main()
