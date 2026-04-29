"""
Módulo de Análise de Riscos de Asteroides
Implementa QP3: Quais são os riscos dos asteroides?
"""

import pandas as pd
import numpy as np

class AnalisadorRiscos:
    """
    Classe para calcular e classificar riscos de impacto de asteroides
    """
    
    # Constantes físicas
    DENSIDADE_MEDIA_ASTEROIDE = 2600  # kg/m³ (rocha típica)
    VELOCIDADE_IMPACTO_MEDIA = 20000  # m/s (velocidade típica de impacto)
    
    # Escalas de referência (baseadas em eventos históricos)
    EVENTOS_HISTORICOS = {
        'Chelyabinsk 2013': {'diametro': 0.020, 'energia_mt': 0.5, 'dano': 'Onda de choque, vidros quebrados'},
        'Tunguska 1908': {'diametro': 0.050, 'energia_mt': 15, 'dano': 'Devastação de 2.000 km²'},
        'Barringer (Arizona)': {'diametro': 0.050, 'energia_mt': 10, 'dano': 'Cratera de 1,2 km'},
        'Chicxulub (Dinossauros)': {'diametro': 10.0, 'energia_mt': 100_000_000, 'dano': 'Extinção em massa'}
    }
    
    @staticmethod
    def calcular_massa(diametro_km):
        """
        Calcula a massa do asteroide assumindo forma esférica
        
        Args:
            diametro_km (float): Diâmetro em quilômetros
            
        Returns:
            float: Massa em kg
        """
        raio_m = (diametro_km * 1000) / 2
        volume_m3 = (4/3) * np.pi * (raio_m ** 3)
        massa_kg = volume_m3 * AnalisadorRiscos.DENSIDADE_MEDIA_ASTEROIDE
        return massa_kg
    
    @staticmethod
    def calcular_energia_impacto(diametro_km, velocidade_kmh):
        """
        Calcula a energia de impacto em megatons de TNT
        
        Fórmula: E = 0.5 * m * v²
        1 megatons TNT = 4.184 × 10^15 joules
        
        Args:
            diametro_km (float): Diâmetro em km
            velocidade_kmh (float): Velocidade em km/h
            
        Returns:
            float: Energia em megatons de TNT
        """
        massa_kg = AnalisadorRiscos.calcular_massa(diametro_km)
        velocidade_ms = velocidade_kmh / 3.6  # Converter km/h para m/s
        
        # Energia cinética em joules
        energia_joules = 0.5 * massa_kg * (velocidade_ms ** 2)
        
        # Converter para megatons TNT
        JOULES_POR_MEGATONS = 4.184e15
        energia_megatons = energia_joules / JOULES_POR_MEGATONS
        
        return energia_megatons
    
    @staticmethod
    def classificar_por_tamanho(diametro_km):
        """
        Classifica o asteroide por categoria de risco baseado no tamanho
        
        Args:
            diametro_km (float): Diâmetro em km
            
        Returns:
            dict: Informações sobre a categoria de risco
        """
        if diametro_km < 0.025:
            return {
                'categoria': 'Meteorito',
                'nivel_risco': 'MÍNIMO',
                'cor': '#00ff00',
                'dano_potencial': 'Queima completamente na atmosfera',
                'area_afetada': 'Nenhuma',
                'frequencia': 'Diária',
                'exemplo_historico': 'Meteoros comuns (estrelas cadentes)'
            }
        elif diametro_km < 0.140:
            return {
                'categoria': 'Impacto Local',
                'nivel_risco': 'BAIXO',
                'cor': '#ffff00',
                'dano_potencial': 'Destruição de área urbana pequena',
                'area_afetada': '~10-50 km²',
                'frequencia': 'A cada 100-1000 anos',
                'exemplo_historico': 'Chelyabinsk (2013) - 20m'
            }
        elif diametro_km < 1.0:
            return {
                'categoria': 'Impacto Regional',
                'nivel_risco': 'MÉDIO',
                'cor': '#ff9900',
                'dano_potencial': 'Devastação de região inteira',
                'area_afetada': '~1.000-10.000 km²',
                'frequencia': 'A cada 1.000-10.000 anos',
                'exemplo_historico': 'Tunguska (1908) - 50m'
            }
        elif diametro_km < 5.0:
            return {
                'categoria': 'Impacto Continental',
                'nivel_risco': 'ALTO',
                'cor': '#ff4444',
                'dano_potencial': 'Devastação de país/continente',
                'area_afetada': '~100.000 km²',
                'frequencia': 'A cada 100.000 anos',
                'exemplo_historico': 'Cratera de Barringer (50.000 anos atrás)'
            }
        else:
            return {
                'categoria': 'Evento de Extinção',
                'nivel_risco': 'CATASTRÓFICO',
                'cor': '#cc0000',
                'dano_potencial': 'Extinção em massa global',
                'area_afetada': 'Global (Terra inteira)',
                'frequencia': 'A cada 100 milhões de anos',
                'exemplo_historico': 'Chicxulub (65 milhões de anos) - 10km'
            }
    
    @staticmethod
    def calcular_raio_destruicao(energia_megatons):
        """
        Estima raio de destruição severa baseado na energia
        
        Fórmula empírica simplificada
        
        Args:
            energia_megatons (float): Energia em megatons
            
        Returns:
            float: Raio de destruição em km
        """
        # Fórmula aproximada: R ≈ 2.2 * E^0.33
        raio_km = 2.2 * (energia_megatons ** 0.33)
        return raio_km
    
    @staticmethod
    def comparar_energia(energia_megatons):
        """
        Compara a energia com eventos conhecidos
        
        Args:
            energia_megatons (float): Energia em megatons
            
        Returns:
            str: Descrição comparativa
        """
        if energia_megatons < 0.001:
            return "Equivalente a fogos de artifício"
        elif energia_megatons < 0.02:
            return f"~{energia_megatons*1000:.1f} toneladas de TNT (explosão pequena)"
        elif energia_megatons < 1:
            return f"~{energia_megatons:.2f} megatons (bomba tática)"
        elif energia_megatons < 50:
            bombas_hiroshima = energia_megatons / 0.015
            return f"~{bombas_hiroshima:.0f}x bomba de Hiroshima"
        elif energia_megatons < 10000:
            return f"~{energia_megatons:.0f} megatons (arsenal nuclear moderno)"
        else:
            return f"~{energia_megatons:,.0f} megatons (evento de extinção)"
    
    @staticmethod
    def analisar_asteroide(row):
        """
        Análise completa de um asteroide
        
        Args:
            row (pd.Series): Linha do DataFrame com dados do asteroide
            
        Returns:
            dict: Análise completa de risco
        """
        diametro = row['diametro_max_km']
        velocidade = row['velocidade_kmh']
        distancia = row['distancia_lunar']
        perigoso_nasa = row['perigoso']
        
        # Cálculos
        massa_kg = AnalisadorRiscos.calcular_massa(diametro)
        energia_mt = AnalisadorRiscos.calcular_energia_impacto(diametro, velocidade)
        raio_destruicao = AnalisadorRiscos.calcular_raio_destruicao(energia_mt)
        classificacao = AnalisadorRiscos.classificar_por_tamanho(diametro)
        comparacao_energia = AnalisadorRiscos.comparar_energia(energia_mt)
        
        # Índice de Risco Próprio (0-100)
        # Ponderação: 40% tamanho, 30% distância, 20% velocidade, 10% NASA
        score_tamanho = min((diametro / 1.0) * 40, 40)  # Normalizado até 1km
        score_distancia = max(30 - (distancia / 10) * 30, 0)  # Quanto mais perto, maior o risco
        score_velocidade = min((velocidade / 100000) * 20, 20)  # Normalizado até 100k km/h
        score_nasa = 10 if perigoso_nasa else 0
        
        indice_risco = score_tamanho + score_distancia + score_velocidade + score_nasa
        
        # Nível de risco por índice
        if indice_risco < 20:
            nivel_indice = "MUITO BAIXO"
            cor_indice = "#00ff00"
        elif indice_risco < 40:
            nivel_indice = "BAIXO"
            cor_indice = "#88ff00"
        elif indice_risco < 60:
            nivel_indice = "MÉDIO"
            cor_indice = "#ffff00"
        elif indice_risco < 80:
            nivel_indice = "ALTO"
            cor_indice = "#ff8800"
        else:
            nivel_indice = "CRÍTICO"
            cor_indice = "#ff0000"
        
        return {
            'nome': row['nome'],
            'massa_kg': massa_kg,
            'energia_megatons': energia_mt,
            'raio_destruicao_km': raio_destruicao,
            'comparacao_energia': comparacao_energia,
            'classificacao': classificacao,
            'indice_risco': round(indice_risco, 1),
            'nivel_indice': nivel_indice,
            'cor_indice': cor_indice,
            'perigoso_nasa': perigoso_nasa
        }
    
    @staticmethod
    def gerar_relatorio_completo(df):
        """
        Gera relatório de análise de riscos para todos os asteroides
        
        Args:
            df (pd.DataFrame): DataFrame com dados dos asteroides
            
        Returns:
            pd.DataFrame: DataFrame com análise de riscos
        """
        analises = []
        
        for _, row in df.iterrows(): # Apesar do iterrows ser considerado lento, não vi necessidade de colocar outro metodo, por conta da quantidade de dados.
            analise = AnalisadorRiscos.analisar_asteroide(row)
            analises.append(analise)
        
        return pd.DataFrame(analises)