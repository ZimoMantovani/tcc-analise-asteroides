import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import json
import os

MODEL_PATH = 'models/modelo_asteroides.joblib'
METRICS_PATH = 'models/metricas_modelo.json'
DATA_PATH = 'data/neo_v2.csv'

def treinar_modelo():
    """
    Treina o modelo com Validação Cruzada Estratificada e salva as métricas
    para serem consumidas pelo front-end (Model Card).
    """
    print("Iniciando treinamento avançado do modelo ML...")
    
    if not os.path.exists(DATA_PATH):
        print(f"Erro: Dataset {DATA_PATH} não encontrado.")
        return False

    df = pd.read_csv(DATA_PATH)
    features = ['est_diameter_max', 'relative_velocity', 'miss_distance', 'absolute_magnitude']
    target = 'hazardous'
    
    df = df.dropna(subset=features + [target])
    X = df[features]
    y = df[target].astype(bool) # Garantir que o target seja booleano

    # 1. Tratamento do Desbalanceamento
    # A classe 'True' (perigoso) recebe um peso ~9x maior automaticamente
    rf_config = {
        'n_estimators': 100,
        'max_depth': 10,
        'class_weight': 'balanced', 
        'random_state': 42,
        'n_jobs': -1
    }

    # 2. Validação Cruzada Estratificada (Rigor Acadêmico)
    # Garante que a proporção de 9.7% seja mantida em todas as divisões de teste
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    modelo_cv = RandomForestClassifier(**rf_config)
    
    print("Executando Validação Cruzada (5-folds)...")
    previsoes_cv = cross_val_predict(modelo_cv, X, y, cv=skf)
    
    # 3. Extração das Métricas Reais
    report = classification_report(y, previsoes_cv, output_dict=True)
    cm = confusion_matrix(y, previsoes_cv)

    # 4. Treinamento do Modelo Final (para produção)
    modelo_final = RandomForestClassifier(**rf_config)
    modelo_final.fit(X, y)
    
    # Capturando a importância de cada variável nas decisões da rede
    importancias = {
        features[i]: float(modelo_final.feature_importances_[i]) 
        for i in range(len(features))
    }

    # 5. Empacotamento de Dados para o Streamlit (Model Card)
    metricas = {
        "precisao_perigosos": report['True']['precision'],
        "recall_perigosos": report['True']['recall'],
        "f1_perigosos": report['True']['f1-score'],
        "acuracia_geral": report['accuracy'],
        "matriz_confusao": cm.tolist(),
        "importancia_features": importancias
    }
    
    os.makedirs('models', exist_ok=True)
    with open(METRICS_PATH, 'w') as f:
        json.dump(metricas, f)
        
    joblib.dump(modelo_final, MODEL_PATH)
    print("✅ Treinamento concluído. Modelo e métricas salvos com sucesso!")
    
    return True

def prever_risco_ia(diametro_max, velocidade, distancia, magnitude_absoluta=20.0):
    """ Faz a inferência usando o modelo Random Forest em disco. """
    if not os.path.exists(MODEL_PATH):
        treinar_modelo()
        
    try:
        modelo = joblib.load(MODEL_PATH)
        dados_novos = pd.DataFrame([{
            'est_diameter_max': diametro_max,
            'relative_velocity': velocidade,
            'miss_distance': distancia,
            'absolute_magnitude': magnitude_absoluta 
        }])
        
        probabilidade = modelo.predict_proba(dados_novos)[0][1] 
        return probabilidade
        
    except Exception as e:
        print(f"Erro ao fazer inferência no modelo ML: {e}")
        return 0.0

if __name__ == '__main__':
    treinar_modelo()