import random

class GeradorInsights:
    """
    Módulo de Natural Language Generation (NLG) Baseado em Regras.
    Gera resumos interpretativos usando variação determinística (seed baseada no ID do objeto)
    para evitar textos repetitivos sem a necessidade de LLMs externas.
    """
    
    @staticmethod
    def comparar_tamanho(diametro_km, id_neo):
        # A seed garante que o mesmo asteroide SEMPRE retorne a mesma frase,
        # mas asteroides diferentes variem o texto, dando sensação de dinamicidade.
        random.seed(str(id_neo))
        metros = diametro_km * 1000
        
        if metros < 2:
            opcoes = [
                "aproximadamente do tamanho de uma bicicleta.",
                "com dimensões similares a um pequeno eletrodoméstico.",
                "tão pequeno que caberia na caçamba de uma caminhonete."
            ]
        elif metros < 10:
            opcoes = [
                "do tamanho de um micro-ônibus.",
                "equivalente ao tamanho de um elefante adulto.",
                "com o comprimento aproximado de um carro de luxo alongado."
            ]
        elif metros < 30:
            opcoes = [
                "equivalente a uma casa de dois andares.",
                "do tamanho de uma quadra de basquete.",
                "similar ao comprimento de um vagão de trem."
            ]
        elif metros < 50:
            opcoes = [
                "do tamanho da Torre de Pisa.",
                "equivalente a um prédio de 15 andares.",
                "com dimensões que rivalizam com o Cristo Redentor."
            ]
        elif metros < 100:
            opcoes = [
                "similar ao tamanho do Big Ben em Londres.",
                "da mesma escala que a Estátua da Liberdade.",
                "gigante, cobrindo a área de um campo de futebol profissional."
            ]
        elif metros < 300:
            opcoes = [
                "comparável ao tamanho do lendário navio Titanic.",
                "do tamanho de três quarteirões inteiros.",
                "vasto o suficiente para cobrir o estádio do Maracanã."
            ]
        elif metros < 500:
            opcoes = [
                "quase do tamanho do Empire State Building.",
                "equivalente à altura das Torres Petronas.",
                "um colosso de rocha do tamanho de uma ponte suspensa."
            ]
        elif metros < 1000:
            opcoes = [
                "gigante, com o tamanho próximo ao do edifício Burj Khalifa.",
                "equivalente a uma montanha de porte médio voando pelo espaço.",
                "uma estrutura rochosa colossal, quase com um quilômetro de ponta a ponta."
            ]
        elif metros < 5000:
            opcoes = [
                "colossal, com volume suficiente para cobrir uma cidade pequena.",
                "uma montanha inteira vagando pelo sistema solar.",
                "uma ameaça de escala continental, visível a vastas distâncias."
            ]
        else:
            opcoes = [
                "catastrófico, com dimensões similares a uma metrópole inteira.",
                "um evento de extinção em potencial, do tamanho de uma província.",
                "um leviatã cósmico, grande o suficiente para alterar a geografia da Terra."
            ]
        return random.choice(opcoes)

    @staticmethod
    def gerar_resumo_nlg(nome, id_neo, diametro_km, velocidade_kmh, distancia_lunar):
        """
        Gera o parágrafo explicativo focando apenas nos dados físicos e contexto.
        A predição de ML foi separada para a interface.
        """
        texto_tamanho = GeradorInsights.comparar_tamanho(diametro_km, id_neo)
        
        texto = f"**Análise de {nome}:**\n\n"
        texto += f"Detectamos uma estrutura rochosa {texto_tamanho} O objeto se desloca pelo vácuo a impressionantes **{velocidade_kmh:,.0f} km/h**.\n\n"
        
        texto += "🔭 **Perspectiva de Interceptação:**\n"
        if distancia_lunar < 1:
            texto += f"Atenção extrema: a trajetória prevê uma passagem a apenas **{distancia_lunar:.2f} distâncias lunares**. Em escala astronômica, isso é considerado um 'raspão' na órbita terrestre.\n"
        elif distancia_lunar < 5:
            texto += f"O objeto passará a **{distancia_lunar:.1f} vezes** a distância entre a Terra e a Lua. É um lembrete próximo da alta atividade orbital na nossa vizinhança cósmica.\n"
        else:
            texto += f"A rota atual indica uma passagem segura a **{distancia_lunar:.1f} distâncias lunares**, mantendo uma margem de segurança confortável em relação ao nosso planeta.\n"
            
        return texto