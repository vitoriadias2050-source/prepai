import streamlit as st

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="PrepAI",
    page_icon="💼",
    layout="centered"
)

st.title("💼 PrepAI")
st.subheader("Seu assistente inteligente para processos seletivos")

st.write(
    "Analise seu currículo, prepare-se para uma vaga "
    "e pratique uma entrevista personalizada."
)

# ==========================================
# MODO DE TESTE
# ==========================================

MODO_TESTE = True


# ==========================================
# FUNÇÃO DE IA
# ==========================================

def perguntar_ia(instrucoes):

    # ======================================
    # MODO TESTE
    # ======================================

    if MODO_TESTE:

        # Se estiver pedindo perguntas
        if "Crie exatamente 5 perguntas" in instrucoes:

            return """
1. Conte um pouco sobre sua formação e como ela se relaciona com a vaga.
2. Quais conhecimentos ou habilidades você possui que podem contribuir para essa função?
3. Conte sobre uma experiência em que você precisou trabalhar em equipe.
4. Qual é uma habilidade que você gostaria de desenvolver profissionalmente?
5. Por que você acredita que essa vaga combina com seus objetivos profissionais?
"""

        # Se estiver pedindo análise
        else:

            return """
## 📊 ANÁLISE DA ENTREVISTA

### 1. PONTOS FORTES

O candidato demonstrou interesse pela oportunidade
e apresentou informações relacionadas à sua formação,
experiências e conhecimentos.

Também foi possível observar características
importantes para processos seletivos, como
comunicação, organização e interesse em aprender.

### 2. PONTOS A DESENVOLVER

O candidato pode desenvolver respostas mais detalhadas,
utilizando exemplos concretos de experiências acadêmicas,
profissionais ou projetos realizados.

Também é importante relacionar cada resposta
diretamente aos requisitos da vaga.

### 3. COMPATIBILIDADE COM A VAGA

A compatibilidade deve ser analisada considerando
a formação, os conhecimentos e as experiências
apresentadas pelo candidato.

Os principais pontos de atenção são os requisitos
da vaga que ainda não aparecem claramente no currículo.

### 4. CURRÍCULO REFORMULADO

NOME

OBJETIVO PROFISSIONAL

Buscar uma oportunidade profissional relacionada
à área da vaga desejada, colocando em prática os
conhecimentos adquiridos durante a formação.

RESUMO PROFISSIONAL

Estudante em formação, interessado em desenvolver
experiência profissional e aplicar seus conhecimentos
em um ambiente de trabalho.

FORMAÇÃO

Informações apresentadas no currículo original.

EXPERIÊNCIA

Informações apresentadas no currículo original.

COMPETÊNCIAS

- Organização
- Trabalho em equipe
- Comunicação
- Interesse em aprendizado

IDIOMAS

Informações apresentadas no currículo original.

OUTRAS INFORMAÇÕES RELEVANTES

Informações apresentadas pelo candidato durante
a entrevista.
"""

    # ======================================
    # FUTURA IA REAL
    # ======================================

    return ""


# ==========================================
# VARIÁVEIS DA SESSÃO
# ==========================================

if "perguntas" not in st.session_state:
    st.session_state.perguntas = []

if "respostas" not in st.session_state:
    st.session_state.respostas = []

if "indice" not in st.session_state:
    st.session_state.indice = 0

if "entrevista_iniciada" not in st.session_state:
    st.session_state.entrevista_iniciada = False

if "finalizada" not in st.session_state:
    st.session_state.finalizada = False

if "resultado" not in st.session_state:
    st.session_state.resultado = ""


# ==========================================
# CURRÍCULO
# ==========================================

st.header("📄 1. Seu currículo")

curriculo = st.text_area(
    "Cole seu currículo abaixo:",
    height=250,
    placeholder="""
Exemplo:

Nome: João Silva

Formação:
Engenharia de Produção - INATEL

Experiência:
Estágio em produção durante 1 ano.

Conhecimentos:
Excel, Power BI e Python.

Idiomas:
Inglês intermediário.
"""
)


# ==========================================
# VAGA
# ==========================================

st.header("💼 2. Vaga desejada")

vaga = st.text_area(
    "Cole aqui a descrição da vaga:",
    height=250,
    placeholder="""
Exemplo:

Vaga: Estágio em Engenharia de Produção

Requisitos:
- Cursando Engenharia de Produção
- Conhecimento em Excel
- Boa comunicação
- Organização
- Trabalho em equipe
"""
)


# ==========================================
# INICIAR ENTREVISTA
# ==========================================

if st.button("🚀 Iniciar entrevista", use_container_width=True):

    if curriculo.strip() == "" or vaga.strip() == "":
        st.warning(
            "Preencha o currículo e a descrição da vaga."
        )

    else:

        instrucoes = f"""
Você é um entrevistador profissional especializado
em processos seletivos.

Analise o currículo:

--- CURRÍCULO ---
{curriculo}

Analise a vaga:

--- VAGA ---
{vaga}

Crie exatamente 5 perguntas para entrevistar esse candidato.

As perguntas devem:

1. Ser relacionadas à vaga.
2. Considerar as experiências do currículo.
3. Identificar conhecimentos do candidato.
4. Identificar possíveis lacunas em relação à vaga.
5. Misturar perguntas comportamentais e profissionais.

Não responda às perguntas.

Retorne apenas as 5 perguntas numeradas.
"""

        resultado = perguntar_ia(instrucoes)

        perguntas = []

        for linha in resultado.split("\n"):

            linha = linha.strip()

            if linha:

                if linha[0].isdigit():

                    pergunta = linha.split(".", 1)[-1].strip()

                    perguntas.append(pergunta)

        st.session_state.perguntas = perguntas
        st.session_state.respostas = []
        st.session_state.indice = 0
        st.session_state.entrevista_iniciada = True
        st.session_state.finalizada = False

        st.rerun()


# ==========================================
# ENTREVISTA
# ==========================================

if st.session_state.entrevista_iniciada:

    indice = st.session_state.indice

    if indice < len(st.session_state.perguntas):

        st.divider()

        st.header("🎤 Entrevista")

        st.write(
            f"Pergunta {indice + 1} "
            f"de {len(st.session_state.perguntas)}"
        )

        st.info(
            st.session_state.perguntas[indice]
        )

        resposta = st.text_area(
            "Digite sua resposta:",
            height=180,
            key=f"resposta_{indice}"
        )

        if st.button(
            "Enviar resposta ➡️",
            use_container_width=True
        ):

            if resposta.strip() == "":
                st.warning(
                    "Digite uma resposta antes de continuar."
                )

            else:

                st.session_state.respostas.append(
                    resposta
                )

                st.session_state.indice += 1

                st.rerun()


# ==========================================
# FINAL DA ENTREVISTA
# ==========================================

if (
    st.session_state.entrevista_iniciada
    and st.session_state.indice >= len(st.session_state.perguntas)
    and not st.session_state.finalizada
):

    st.success(
        "🎉 Você concluiu a entrevista!"
    )

    if st.button(
        "🤖 Analisar entrevista e criar currículo",
        use_container_width=True
    ):

        entrevista = ""

        for i in range(
            len(st.session_state.perguntas)
        ):

            entrevista += f"""
PERGUNTA {i + 1}:

{st.session_state.perguntas[i]}

RESPOSTA:

{st.session_state.respostas[i]}

--------------------------------
"""

        instrucoes = f"""
Você é um especialista em recrutamento.

Analise o currículo original:

--- CURRÍCULO ---
{curriculo}

Analise a vaga:

--- VAGA ---
{vaga}

Analise a entrevista:

--- ENTREVISTA ---
{entrevista}

Agora produza um relatório.

1. PONTOS FORTES
2. PONTOS A DESENVOLVER
3. COMPATIBILIDADE COM A VAGA
4. CURRÍCULO REFORMULADO
"""

        resultado = perguntar_ia(instrucoes)

        st.session_state.resultado = resultado
        st.session_state.finalizada = True

        st.rerun()


# ==========================================
# RESULTADO
# ==========================================

if st.session_state.finalizada:

    st.divider()

    st.header("📊 Resultado")

    st.markdown(
        st.session_state.resultado
    )

    st.download_button(
        "📥 Baixar resultado",
        st.session_state.resultado,
        file_name="resultado_prepai.txt",
        mime="text/plain",
        use_container_width=True
    )
