import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

MODEL_PATH = 'models/modelo_asteroides.joblib'
DATA_PATH = 'data/neo_v2.csv'

def treinar_modelo():
    """
    Treina um modelo de Machine Learning (Random Forest) usando o dataset histórico.
    Objetivo: Prever a probabilidade de um asteroide ser classificado como perigoso (hazardous).
    """
    print("Iniciando treinamento do modelo de Machine Learning...")
    
    if not os.path.exists(DATA_PATH):
        print(f"Erro: Dataset {DATA_PATH} não encontrado.")
        return False

    df = pd.read_csv(DATA_PATH)
    
    # POR QUE ESTAS 4 FEATURES?
    # São as mesmas métricas primárias utilizadas pela NASA para classificar o risco de um NEO:
    # 1. Tamanho estimado (est_diameter_max)
    # 2. Velocidade relativa (relative_velocity)
    # 3. Distância da Terra (miss_distance)
    # 4. Brilho intrínseco/Refletividade (absolute_magnitude)
    features = ['est_diameter_max', 'relative_velocity', 'miss_distance', 'absolute_magnitude']
    target = 'hazardous'
    
    df = df.dropna(subset=features + [target])
    X = df[features]
    y = df[target]

    # POR QUE 80/20?
    # Dividimos os dados para evitar o "vazamento de dados" (data leakage). 
    # O modelo treina com 80% e faz a prova final com 20% de dados que ele nunca viu,
    # garantindo que ele realmente aprendeu padrões, em vez de apenas decorar as respostas (overfitting).
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # POR QUE RANDOM FOREST?
    # O Random Forest funciona como um "comitê de especialistas". Ele cria 100 árvores de decisão 
    # (n_estimators=100) onde cada uma vota se o asteroide é perigoso ou não. A maioria vence.
    # É excelente para dados tabulares, lidando bem com não-linearidades sem precisar de muito ajuste fino.
    modelo = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    modelo.fit(X_train, y_train)

    previsoes = modelo.predict(X_test)
    acuracia = accuracy_score(y_test, previsoes)
    print(f"Modelo treinado com sucesso! Acurácia: {acuracia:.2%}")

    # POR QUE JOBLIB?
    # Salvar (serializar) o modelo em disco evita que o servidor precise retreinar a IA 
    # toda vez que o Streamlit reiniciar. O modelo fica "congelado" e pronto para inferência rápida.
    joblib.dump(modelo, MODEL_PATH)
    print(f"Modelo salvo em {MODEL_PATH}")
    
    return True

def prever_risco_ia(diametro_max, velocidade, distancia, magnitude_absoluta=20.0):
    """
    Carrega o modelo Random Forest em disco e faz a inferência (predict_proba) para um novo objeto.
    """
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
        
        # O predict_proba retorna a probabilidade para [Classe 0 (Seguro), Classe 1 (Perigoso)]
        probabilidade = modelo.predict_proba(dados_novos)[0][1] 
        return probabilidade
        
    except Exception as e:
        print(f"Erro ao fazer inferência no modelo ML: {e}")
        return 0.0

if __name__ == '__main__':
    treinar_modelo()