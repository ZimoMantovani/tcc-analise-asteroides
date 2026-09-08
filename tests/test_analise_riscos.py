"""
Testes do AnalisadorRiscos (src/analise_riscos.py).

Por que só esse módulo tem testes automatizados por enquanto: é o único
que faz cálculo puro (fórmulas físicas), sem depender de banco de dados,
da API da NASA ou do Streamlit — dá pra testar isolado, rápido e sem
precisar de nenhuma infraestrutura rodando.

Rodar com: pytest
(o pytest.ini na raiz já garante que o pacote src/ é encontrado)
"""

import pandas as pd
import pytest

from src.analise_riscos import AnalisadorRiscos


# ---------------------------------------------------------------------------
# calcular_massa
# ---------------------------------------------------------------------------

class TestCalcularMassa:

    def test_diametro_zero_resulta_em_massa_zero(self):
        assert AnalisadorRiscos.calcular_massa(0) == 0

    def test_dobrar_o_diametro_multiplica_a_massa_por_oito(self):
        # Volume de uma esfera escala com o cubo do raio (V ∝ r³).
        # Se o diâmetro dobra, o raio dobra, e o volume (logo a massa,
        # já que a densidade é constante) deve multiplicar por 2³ = 8.
        massa_1 = AnalisadorRiscos.calcular_massa(1.0)
        massa_2 = AnalisadorRiscos.calcular_massa(2.0)
        assert massa_2 == pytest.approx(massa_1 * 8, rel=1e-9)

    def test_valor_conhecido_para_1km_de_diametro(self):
        # raio = 500 m -> volume = (4/3)*pi*500^3 ≈ 523.598.775,6 m³
        # massa = volume * 2600 kg/m³ ≈ 1,3614 x 10^12 kg
        massa = AnalisadorRiscos.calcular_massa(1.0)
        assert massa == pytest.approx(1.3613568e12, rel=1e-4)


# ---------------------------------------------------------------------------
# calcular_energia_impacto
# ---------------------------------------------------------------------------

class TestCalcularEnergiaImpacto:

    def test_diametro_zero_resulta_em_energia_zero(self):
        assert AnalisadorRiscos.calcular_energia_impacto(0, 50000) == 0

    def test_dobrar_a_velocidade_multiplica_a_energia_por_quatro(self):
        # Energia cinética: E = 0.5 * m * v² -> escala com o QUADRADO da velocidade.
        energia_1 = AnalisadorRiscos.calcular_energia_impacto(1.0, 20000)
        energia_2 = AnalisadorRiscos.calcular_energia_impacto(1.0, 40000)
        assert energia_2 == pytest.approx(energia_1 * 4, rel=1e-9)

    def test_energia_e_sempre_positiva(self):
        assert AnalisadorRiscos.calcular_energia_impacto(0.5, 30000) > 0


# ---------------------------------------------------------------------------
# classificar_por_tamanho
# ---------------------------------------------------------------------------

class TestClassificarPorTamanho:

    @pytest.mark.parametrize("diametro_km, categoria_esperada", [
        (0.001, "Meteorito"),
        (0.024, "Meteorito"),          # último valor antes da fronteira dos 0.025
        (0.025, "Impacto Local"),      # exatamente na fronteira -> já muda de categoria
        (0.139, "Impacto Local"),
        (0.140, "Impacto Regional"),
        (0.999, "Impacto Regional"),
        (1.000, "Impacto Continental"),
        (4.999, "Impacto Continental"),
        (5.000, "Evento de Extinção"),
        (12.0, "Evento de Extinção"),
    ])
    def test_fronteiras_de_categoria(self, diametro_km, categoria_esperada):
        resultado = AnalisadorRiscos.classificar_por_tamanho(diametro_km)
        assert resultado["categoria"] == categoria_esperada

    def test_retorno_tem_todas_as_chaves_esperadas(self):
        resultado = AnalisadorRiscos.classificar_por_tamanho(0.5)
        chaves_esperadas = {
            "categoria", "nivel_risco", "cor", "dano_potencial",
            "area_afetada", "frequencia", "exemplo_historico",
        }
        assert chaves_esperadas.issubset(resultado.keys())


# ---------------------------------------------------------------------------
# calcular_raio_destruicao
# ---------------------------------------------------------------------------

class TestCalcularRaioDestruicao:

    def test_energia_zero_resulta_em_raio_zero(self):
        assert AnalisadorRiscos.calcular_raio_destruicao(0) == 0

    def test_valor_conhecido_para_1_megaton(self):
        # R = 2.2 * E^0.33 -> para E=1, R = 2.2 * 1 = 2.2
        assert AnalisadorRiscos.calcular_raio_destruicao(1) == pytest.approx(2.2)

    def test_raio_cresce_com_a_energia(self):
        raio_pequeno = AnalisadorRiscos.calcular_raio_destruicao(1)
        raio_grande = AnalisadorRiscos.calcular_raio_destruicao(1000)
        assert raio_grande > raio_pequeno


# ---------------------------------------------------------------------------
# comparar_energia
# ---------------------------------------------------------------------------

class TestCompararEnergia:

    @pytest.mark.parametrize("energia_mt, trecho_esperado", [
        (0.0001, "fogos de artifício"),
        (0.01, "toneladas de TNT"),
        (0.5, "bomba tática"),
        (10, "bomba de Hiroshima"),
        (5000, "arsenal nuclear"),
        (50_000_000, "extinção"),
    ])
    def test_faixas_retornam_descricao_esperada(self, energia_mt, trecho_esperado):
        resultado = AnalisadorRiscos.comparar_energia(energia_mt)
        assert trecho_esperado in resultado


# ---------------------------------------------------------------------------
# analisar_asteroide (fluxo completo — combina todos os cálculos acima)
# ---------------------------------------------------------------------------

class TestAnalisarAsteroide:

    def test_asteroide_de_alto_risco(self):
        # Grande, rápido, passando perto e já sinalizado pela NASA como perigoso.
        # Score esperado: tamanho=40 (teto) + distância=15 + velocidade=10 + nasa=10 = 75 -> "ALTO"
        row = pd.Series({
            "nome": "TesteAltoRisco",
            "diametro_max_km": 2.0,
            "velocidade_kmh": 50000,
            "distancia_lunar": 5,
            "perigoso": True,
        })
        resultado = AnalisadorRiscos.analisar_asteroide(row)

        assert resultado["indice_risco"] == pytest.approx(75.0)
        assert resultado["nivel_indice"] == "ALTO"
        assert resultado["perigoso_nasa"] is True
        # A massa retornada deve bater com o cálculo isolado (sem duplicar lógica)
        assert resultado["massa_kg"] == AnalisadorRiscos.calcular_massa(2.0)

    def test_asteroide_de_baixo_risco(self):
        # Pequeno, lento, passando longe e não sinalizado pela NASA.
        # Score esperado: tamanho=0.4 + distância=0 + velocidade=0.2 + nasa=0 = 0.6 -> "MUITO BAIXO"
        row = pd.Series({
            "nome": "TesteBaixoRisco",
            "diametro_max_km": 0.01,
            "velocidade_kmh": 1000,
            "distancia_lunar": 50,
            "perigoso": False,
        })
        resultado = AnalisadorRiscos.analisar_asteroide(row)

        assert resultado["indice_risco"] == pytest.approx(0.6)
        assert resultado["nivel_indice"] == "MUITO BAIXO"
        assert resultado["perigoso_nasa"] is False

    def test_retorno_tem_todas_as_chaves_esperadas(self):
        row = pd.Series({
            "nome": "TesteGenerico",
            "diametro_max_km": 0.3,
            "velocidade_kmh": 20000,
            "distancia_lunar": 20,
            "perigoso": False,
        })
        resultado = AnalisadorRiscos.analisar_asteroide(row)
        chaves_esperadas = {
            "nome", "massa_kg", "energia_megatons", "raio_destruicao_km",
            "comparacao_energia", "classificacao", "indice_risco",
            "nivel_indice", "cor_indice", "perigoso_nasa",
        }
        assert chaves_esperadas.issubset(resultado.keys())


# ---------------------------------------------------------------------------
# gerar_relatorio_completo (aplica analisar_asteroide numa lista de asteroides)
# ---------------------------------------------------------------------------

class TestGerarRelatorioCompleto:

    def test_gera_uma_linha_por_asteroide_de_entrada(self):
        df_entrada = pd.DataFrame([
            {"nome": "A", "diametro_max_km": 0.5, "velocidade_kmh": 30000,
             "distancia_lunar": 10, "perigoso": False},
            {"nome": "B", "diametro_max_km": 1.5, "velocidade_kmh": 60000,
             "distancia_lunar": 2, "perigoso": True},
        ])

        relatorio = AnalisadorRiscos.gerar_relatorio_completo(df_entrada)

        assert len(relatorio) == 2
        assert list(relatorio["nome"]) == ["A", "B"]
        assert "indice_risco" in relatorio.columns
