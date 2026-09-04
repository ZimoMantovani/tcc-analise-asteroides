class GeradorCuriosidades:
    """
    Simula uma IA Generativa para fins educacionais.
    Gera textos descritivos baseados nos dados físicos do asteroide.
    """
    
    @staticmethod
    def comparar_tamanho(diametro_km):
        metros = diametro_km * 1000
        if metros < 2:
            return "aproximadamente do tamanho de uma bicicleta."
        elif metros < 10:
            return "do tamanho de um ônibus escolar."
        elif metros < 30:
            return "equivalente a uma casa de dois andares."
        elif metros < 50:
            return "do tamanho da Torre de Pisa."
        elif metros < 100:
            return "similar ao tamanho do Big Ben ou da Estátua da Liberdade."
        elif metros < 300:
            return "comparável ao tamanho do navio Titanic."
        elif metros < 500:
            return "quase do tamanho do Empire State Building."
        elif metros < 1000:
            return "gigante, com o tamanho próximo ao do edifício Burj Khalifa."
        elif metros < 5000:
            return "colossal, equivalente a uma montanha inteira voando pelo espaço."
        else:
            return "catastrófico, com dimensões similares a uma cidade inteira."

    @staticmethod
    def comparar_velocidade(velocidade_kmh):
        if velocidade_kmh < 1000:
            return "viajando um pouco mais rápido que um avião comercial."
        elif velocidade_kmh < 5000:
            return "se movendo na velocidade de um caça supersônico."
        elif velocidade_kmh < 20000:
            return "voando a uma velocidade incrível, mais rápido que um foguete espacial moderno."
        elif velocidade_kmh < 50000:
            return "cortando o espaço vazio cerca de 15 vezes mais rápido que a bala de um rifle."
        elif velocidade_kmh < 100000:
            return "viajando a uma velocidade hipersônica assustadora, rápido o suficiente para dar a volta na Terra em menos de uma hora."
        else:
            return "se movendo a uma velocidade inimaginável, uma das coisas mais rápidas do sistema solar."

    @staticmethod
    def gerar_fatos_educacionais(nome, diametro_km, velocidade_kmh, distancia_lunar, score_ia):
        """
        Gera um parágrafo educacional usando as métricas.
        """
        texto_tamanho = GeradorCuriosidades.comparar_tamanho(diametro_km)
        texto_vel = GeradorCuriosidades.comparar_velocidade(velocidade_kmh)
        
        # Formatando a probabilidade calculada pela nossa IA local
        chance_perigo = score_ia * 100
        
        texto = f"**💡 Análise de {nome}**\n\n"
        texto += f"Imagine um objeto que é {texto_tamanho} Ele está {texto_vel} ({velocidade_kmh:,.0f} km/h).\n\n"
        
        texto += "🔭 **Perspectiva de Distância:**\n"
        if distancia_lunar < 1:
            texto += f"Isso é extremamente perto! Ele vai passar a uma distância {distancia_lunar:.2f} vezes a distância da Terra até a Lua. Em termos astronômicos, isso é um 'raspão'.\n\n"
        elif distancia_lunar < 5:
            texto += f"Ele vai passar relativamente perto, a {distancia_lunar:.1f} distâncias lunares de nós. É um lembrete constante de como a vizinhança cósmica da Terra é movimentada.\n\n"
        else:
            texto += f"Fique tranquilo, ele vai passar a uma distância segura de {distancia_lunar:.1f} vezes a distância até a Lua.\n\n"
            
        texto += "**Veredito final (Machine Learning):**\n"
        texto += f"Foi analizado os dados históricos de mais de 90 mil asteroides registrados pela NASA. Com base nisso, "
        
        if chance_perigo < 10:
            texto += f"ela calculou apenas **{chance_perigo:.1f}% de probabilidade** deste asteroide ser classificado como um perigo real. Podemos dormir em paz!"
        elif chance_perigo < 50:
            texto += f"ela indica que existe uma **probabilidade moderada ({chance_perigo:.1f}%)** de perigo. Astrônomos o mantêm sob observação."
        else:
            texto += f"ela emite um **ALERTA com {chance_perigo:.1f}% de probabilidade** de risco. Asteroides com este perfil exigem monitoramento rigoroso das agências espaciais!"
            
        return texto