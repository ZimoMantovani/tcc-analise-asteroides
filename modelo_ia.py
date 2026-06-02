import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

MODEL_PATH = 'modelo_asteroides.joblib'
DATA_PATH = 'neo_v2.csv'

def treinar_modelo():
    """
    Treina o modelo de Machine Learning usando o dataset histórico da NASA.
    O modelo prevê se um asteroide é perigoso (hazardous).
    """
    print("Iniciando treinamento do modelo IA...")
    
    if not os.path.exists(DATA_PATH):
        print(f"Erro: Dataset {DATA_PATH} não encontrado.")
        return False

    # Carregar dados
    df = pd.read_csv(DATA_PATH)
    
    # Selecionar as features (características) e o target (alvo)
    features = ['est_diameter_max', 'relative_velocity', 'miss_distance', 'absolute_magnitude']
    target = 'hazardous'
    
    # Remover valores nulos, se houver
    df = df.dropna(subset=features + [target])
    
    X = df[features]
    y = df[target]

    # Dividir os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Inicializar e treinar o classificador Random Forest
    # Limitando a profundidade para manter o modelo rápido e leve
    modelo = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    modelo.fit(X_train, y_train)

    # Avaliar o modelo (opcional, apenas para log)
    previsoes = modelo.predict(X_test)
    acuracia = accuracy_score(y_test, previsoes)
    print(f"Modelo treinado com sucesso! Acurácia: {acuracia:.2%}")

    # Salvar o modelo em disco para não precisar treinar toda vez
    joblib.dump(modelo, MODEL_PATH)
    print(f"Modelo salvo em {MODEL_PATH}")
    
    return True

def prever_risco_ia(diametro_max, velocidade, distancia, magnitude_absoluta=20.0):
    """
    Usa o modelo treinado para prever a probabilidade de risco de um novo asteroide.
    """
    # Se o modelo não existe, treina primeiro
    if not os.path.exists(MODEL_PATH):
        treinar_modelo()
        
    try:
        modelo = joblib.load(MODEL_PATH)
        
        # O DataFrame precisa ter as mesmas colunas usadas no treino
        dados_novos = pd.DataFrame([{
            'est_diameter_max': diametro_max,
            'relative_velocity': velocidade,
            'miss_distance': distancia,
            'absolute_magnitude': magnitude_absoluta # Usamos um valor médio caso não tenhamos o real
        }])
        
        # predict_proba retorna a probabilidade [chance_falso, chance_verdadeiro]
        probabilidade = modelo.predict_proba(dados_novos)[0][1] # Pega a chance de ser 'hazardous' (True)
        return probabilidade
        
    except Exception as e:
        print(f"Erro ao fazer previsão com IA: {e}")
        return 0.0

if __name__ == '__main__':
    # Quando o arquivo é rodado diretamente, ele apenas treina o modelo.
    treinar_modelo()
