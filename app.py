import streamlit as st
import re
from io import BytesIO


# =========================================================
# CONFIGURAÇÃO
# =========================================================

st.set_page_config(
    page_title="PrepAI",
    page_icon="💼",
    layout="centered"
)

st.title("💼 PrepAI")
st.subheader("Seu assistente inteligente para processos seletivos")

st.write(
    "Analise seu currículo, compare com uma vaga "
    "e pratique uma entrevista personalizada."
)


# =========================================================
# ESTILO
# =========================================================

st.markdown("""
<style>

.block-container {
    max-width: 900px;
    padding-top: 2rem;
}

h1 {
    text-align: center;
}

h2 {
    margin-top: 25px;
}

.resultado-box {
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #ddd;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def normalizar(texto):
    """
    Deixa o texto em formato mais fácil de analisar.
    """
    texto = texto.lower()

    substituicoes = {
        "á": "a",
        "à": "a",
        "ã": "a",
        "â": "a",
        "é": "e",
        "ê": "e",
        "í": "i",
        "ó": "o",
        "ô": "o",
        "õ": "o",
        "ú": "u",
        "ç": "c"
    }

    for antigo, novo in substituicoes.items():
        texto = texto.replace(antigo, novo)

    return texto


# =========================================================
# LEITURA DE PDF
# =========================================================

def ler_pdf(arquivo):

    try:

        from pypdf import PdfReader

        leitor = PdfReader(arquivo)

        texto = ""

        for pagina in leitor.pages:

            conteudo = pagina.extract_text()

            if conteudo:
                texto += conteudo + "\n"

        return texto.strip()

    except Exception as erro:

        st.error(
            f"Erro ao ler o PDF: {erro}"
        )

        return ""


# =========================================================
# LEITURA DE DOCX
# =========================================================

def ler_docx(arquivo):

    try:

        from docx import Document

        documento = Document(arquivo)

        texto = ""

        for paragrafo in documento.paragraphs:

            if paragrafo.text.strip():

                texto += paragrafo.text + "\n"

        return texto.strip()

    except Exception as erro:

        st.error(
            f"Erro ao ler o DOCX: {erro}"
        )

        return ""


# =========================================================
# EXTRAÇÃO DO CURRÍCULO
# =========================================================

def extrair_curriculo(arquivo):

    nome = arquivo.name.lower()

    if nome.endswith(".pdf"):

        return ler_pdf(arquivo)

    elif nome.endswith(".docx"):

        return ler_docx(arquivo)

    return ""


# =========================================================
# ENCONTRAR SEÇÕES
# =========================================================

def encontrar_secao(texto, palavras):

    linhas = texto.splitlines()

    resultado = []

    encontrou = False

    for linha in linhas:

        linha_limpa = linha.strip()

        if not linha_limpa:
            continue

        linha_normalizada = normalizar(
            linha_limpa
        )

        # identifica o título da seção
        titulo = False

        for palavra in palavras:

            if palavra in linha_normalizada:

                # evita considerar qualquer frase contendo a palavra
                if len(linha_limpa.split()) <= 6:

                    titulo = True
                    break

        if titulo:

            encontrou = True
            continue

        if encontrou:

            # se encontrar outro título conhecido,
            # a seção termina
            possivel_titulo = (
                len(linha_limpa.split()) <= 6
                and linha_limpa.isupper()
            )

            if possivel_titulo:
                break

            resultado.append(linha_limpa)

    return resultado


# =========================================================
# IDENTIFICAÇÃO DOS IDIOMAS
# =========================================================

def identificar_idiomas(texto):

    texto_normalizado = normalizar(texto)

    idiomas = [
        ("Inglês", "ingles"),
        ("Espanhol", "espanhol"),
        ("Francês", "frances"),
        ("Italiano", "italiano"),
        ("Alemão", "alemao"),
        ("Libras", "libras")
    ]

    encontrados = []

    for nome, palavra in idiomas:

        if palavra in texto_normalizado:

            nivel = "Nível não informado"

            if "basico" in texto_normalizado:
                if palavra in texto_normalizado:
                    nivel = "Básico"

            if "intermediario" in texto_normalizado:
                if palavra in texto_normalizado:
                    nivel = "Intermediário"

            if "avancado" in texto_normalizado:
                if palavra in texto_normalizado:
                    nivel = "Avançado"

            if "fluente" in texto_normalizado:
                if palavra in texto_normalizado:
                    nivel = "Fluente"

            encontrados.append(
                f"{nome} - {nivel}"
            )

    return encontrados


# =========================================================
# IDENTIFICAÇÃO DAS COMPETÊNCIAS
# =========================================================

def identificar_competencias(texto):

    texto_normalizado = normalizar(texto)

    competencias = {
        "Excel": ["excel"],
        "Power BI": ["power bi"],
        "Python": ["python"],
        "C++": ["c++"],
        "Java": ["java"],
        "SQL": ["sql"],
        "Comunicação": ["comunicacao"],
        "Trabalho em equipe": [
            "trabalho em equipe",
            "trabalho em grupo"
        ],
        "Liderança": ["lideranca"],
        "Organização": ["organizacao"],
        "Proatividade": ["proatividade"],
        "Gestão de projetos": [
            "gestao de projetos"
        ],
        "Análise de dados": [
            "analise de dados"
        ]
    }

    encontrados = []

    for nome, palavras in competencias.items():

        for palavra in palavras:

            if palavra in texto_normalizado:

                encontrados.append(nome)
                break

    return encontrados


# =========================================================
# IDENTIFICAÇÃO DE CURSOS
# =========================================================

def identificar_cursos(texto):

    linhas = texto.splitlines()

    cursos = []

    dentro = False

    for linha in linhas:

        linha_limpa = linha.strip()

        if not linha_limpa:
            continue

        normalizada = normalizar(
            linha_limpa
        )

        if (
            "cursos" in normalizada
            or "cursos complementares" in normalizada
            or "qualificacoes" in normalizada
            or "certificacoes" in normalizada
        ):

            dentro = True
            continue

        if dentro:

            if (
                "experiencia" in normalizada
                or "formacao" in normalizada
                or "idiomas" in normalizada
                or "competencias" in normalizada
                or "projetos" in normalizada
            ):

                break

            cursos.append(linha_limpa)

    return cursos


# =========================================================
# IDENTIFICAÇÃO DA FORMAÇÃO
# =========================================================

def identificar_formacao(texto):

    palavras = [
        "formacao",
        "formacao academica",
        "educacao"
    ]

    resultado = encontrar_secao(
        texto,
        palavras
    )

    return resultado


# =========================================================
# IDENTIFICAÇÃO DE EXPERIÊNCIAS
# =========================================================

def identificar_experiencias(texto):

    palavras = [
        "experiencia",
        "experiencias profissionais",
        "experiencia profissional"
    ]

    resultado = encontrar_secao(
        texto,
        palavras
    )

    return resultado


# =========================================================
# IDENTIFICAÇÃO DE PROJETOS
# =========================================================

def identificar_projetos(texto):

    palavras = [
        "projetos",
        "projetos academicos",
        "projetos profissionais"
    ]

    resultado = encontrar_secao(
        texto,
        palavras
    )

    return resultado


# =========================================================
# ANÁLISE COMPLETA DO CURRÍCULO
# =========================================================

def analisar_curriculo(texto):

    return {
        "idiomas": identificar_idiomas(texto),
        "competencias": identificar_competencias(texto),
        "cursos": identificar_cursos(texto),
        "formacao": identificar_formacao(texto),
        "experiencias": identificar_experiencias(texto),
        "projetos": identificar_projetos(texto)
    }


# =========================================================
# PALAVRAS IMPORTANTES DA VAGA
# =========================================================

def extrair_requisitos_vaga(vaga):

    texto = normalizar(vaga)

    requisitos = []

    palavras = [
        "excel",
        "power bi",
        "python",
        "sql",
        "ingles",
        "espanhol",
        "comunicacao",
        "organizacao",
        "trabalho em equipe",
        "lideranca",
        "proatividade",
        "engenharia",
        "administracao",
        "producao",
        "gestao",
        "analise de dados",
        "estagio",
        "experiencia"
    ]

    for palavra in palavras:

        if palavra in texto:

            requisitos.append(palavra)

    return requisitos


# =========================================================
# COMPARAÇÃO CURRÍCULO X VAGA
# =========================================================

def comparar_curriculo_vaga(curriculo, vaga):

    curriculo_normalizado = normalizar(
        curriculo
    )

    vaga_normalizada = normalizar(
        vaga
    )

    requisitos = extrair_requisitos_vaga(
        vaga
    )

    encontrados = []
    ausentes = []

    for requisito in requisitos:

        if requisito in curriculo_normalizado:

            encontrados.append(
                requisito
            )

        else:

            ausentes.append(
                requisito
            )

    return encontrados, ausentes


# =========================================================
# GERAR PERGUNTAS
# =========================================================

def gerar_perguntas(curriculo, vaga):

    informacoes = analisar_curriculo(
        curriculo
    )

    perguntas = []

    curriculo_normalizado = normalizar(
        curriculo
    )

    vaga_normalizada = normalizar(
        vaga
    )

    # -----------------------------------------------------
    # 1. FORMAÇÃO
    # -----------------------------------------------------

    if informacoes["formacao"]:

        perguntas.append(
            "Como sua formação acadêmica "
            "se relaciona com os requisitos "
            "desta vaga?"
        )

    else:

        perguntas.append(
            "Conte um pouco sobre sua formação "
            "e como ela contribui para sua "
            "preparação profissional."
        )

    # -----------------------------------------------------
    # 2. EXPERIÊNCIA
    # -----------------------------------------------------

    if informacoes["experiencias"]:

        perguntas.append(
            "Conte sobre uma das suas experiências "
            "profissionais ou acadêmicas e explique "
            "quais conhecimentos adquiridos nela "
            "podem ser aplicados nesta vaga."
        )

    else:

        perguntas.append(
            "Conte sobre uma experiência acadêmica "
            "ou projeto em que você precisou resolver "
            "um problema ou assumir responsabilidades."
        )

    # -----------------------------------------------------
    # 3. IDIOMA
    # -----------------------------------------------------

    if informacoes["idiomas"]:

        idioma = informacoes["idiomas"][0]

        perguntas.append(
            f"Você mencionou no currículo "
            f"{idioma}. Em quais situações "
            f"acadêmicas ou profissionais você "
            f"já utilizou esse idioma?"
        )

    elif "ingles" in vaga_normalizada:

        perguntas.append(
            "A vaga menciona conhecimento em inglês. "
            "Como está seu nível atual e em quais "
            "situações você já utilizou o idioma?"
        )

    else:

        perguntas.append(
            "Conte sobre uma situação em que você "
            "precisou trabalhar em equipe para alcançar "
            "um resultado."
        )

    # -----------------------------------------------------
    # 4. CURSOS / COMPETÊNCIAS
    # -----------------------------------------------------

    if informacoes["cursos"]:

        perguntas.append(
            "Quais dos cursos realizados por você "
            "mais contribuíram para seu desenvolvimento "
            "profissional e como eles podem ajudar "
            "nesta oportunidade?"
        )

    elif informacoes["competencias"]:

        competencia = informacoes["competencias"][0]

        perguntas.append(
            f"Você apresenta conhecimento em "
            f"{competencia}. Conte como desenvolveu "
            f"essa habilidade e como já a utilizou."
        )

    else:

        perguntas.append(
            "Qual é uma habilidade profissional que "
            "você considera um ponto forte e como "
            "ela pode contribuir para esta vaga?"
        )

    # -----------------------------------------------------
    # 5. RELAÇÃO COM A VAGA
    # -----------------------------------------------------

    perguntas.append(
        "Considerando sua formação, experiências "
        "e conhecimentos, por que você acredita "
        "que seu perfil pode contribuir para esta "
        "oportunidade?"
    )

    return perguntas[:5]


# =========================================================
# ANÁLISE DAS RESPOSTAS
# =========================================================

def analisar_respostas(perguntas, respostas):

    resultado = []

    quantidade = len(respostas)

    if quantidade == 0:

        return resultado

    # tamanho médio das respostas
    total_palavras = 0

    for resposta in respostas:

        palavras = resposta.split()

        total_palavras += len(palavras)

    media = total_palavras / quantidade

    # -----------------------------------------------------
    # COMUNICAÇÃO
    # -----------------------------------------------------

    if media >= 35:

        resultado.append(
            "🟢 Comunicação: as respostas apresentam "
            "um nível de detalhamento adequado."
        )

    elif media >= 15:

        resultado.append(
            "🟡 Comunicação: as respostas são objetivas, "
            "mas podem apresentar mais detalhes e exemplos."
        )

    else:

        resultado.append(
            "🟠 Comunicação: algumas respostas estão "
            "muito curtas. Procure explicar melhor "
            "suas experiências."
        )

    # -----------------------------------------------------
    # EXEMPLOS
    # -----------------------------------------------------

    palavras_exemplo = [
        "exemplo",
        "quando",
        "durante",
        "projeto",
        "empresa",
        "estagio",
        "experiencia"
    ]

    encontrou_exemplo = False

    for resposta in respostas:

        resposta_normalizada = normalizar(
            resposta
        )

        for palavra in palavras_exemplo:

            if palavra in resposta_normalizada:

                encontrou_exemplo = True
                break

        if encontrou_exemplo:
            break

    if encontrou_exemplo:

        resultado.append(
            "🟢 Exemplos práticos: o candidato "
            "utilizou situações concretas em suas respostas."
        )

    else:

        resultado.append(
            "🟡 Exemplos práticos: procure utilizar "
            "situações reais da faculdade, trabalho, "
            "projetos ou cursos."
        )

    # -----------------------------------------------------
    # ESTRUTURA
    # -----------------------------------------------------

    resultado.append(
        "🔵 Sugestão: ao responder perguntas de entrevista, "
        "procure explicar a situação, sua ação e o resultado."
    )

    return resultado


# =========================================================
# CURRÍCULO REFORMULADO
# =========================================================

def criar_curriculo_reformulado(
    curriculo,
    informacoes,
    vaga
):

    linhas = []

    linhas.append(
        "# CURRÍCULO PROFISSIONAL"
    )

    linhas.append("")

    # -----------------------------------------------------
    # DADOS ORIGINAIS
    # -----------------------------------------------------

    primeiras_linhas = curriculo.splitlines()

    dados = []

    for linha in primeiras_linhas[:5]:

        if linha.strip():

            dados.append(
                linha.strip()
            )

    if dados:

        linhas.append(
            "## DADOS DO CANDIDATO"
        )

        for item in dados:

            linhas.append(
                item
            )

        linhas.append("")

    # -----------------------------------------------------
    # OBJETIVO
    # -----------------------------------------------------

    linhas.append(
        "## OBJETIVO PROFISSIONAL"
    )

    linhas.append(
        "Buscar uma oportunidade profissional "
        "compatível com minha formação e experiência, "
        "contribuindo para a organização e ampliando "
        "meus conhecimentos."
    )

    linhas.append("")

    # -----------------------------------------------------
    # FORMAÇÃO
    # -----------------------------------------------------

    if informacoes["formacao"]:

        linhas.append(
            "## FORMAÇÃO ACADÊMICA"
        )

        for item in informacoes["formacao"]:

            linhas.append(
                f"- {item}"
            )

        linhas.append("")

    # -----------------------------------------------------
    # EXPERIÊNCIA
    # -----------------------------------------------------

    if informacoes["experiencias"]:

        linhas.append(
            "## EXPERIÊNCIA PROFISSIONAL"
        )

        for item in informacoes["experiencias"]:

            linhas.append(
                f"- {item}"
            )

        linhas.append("")

    # -----------------------------------------------------
    # CURSOS
    # -----------------------------------------------------

    if informacoes["cursos"]:

        linhas.append(
            "## CURSOS E QUALIFICAÇÕES"
        )

        for item in informacoes["cursos"]:

            linhas.append(
                f"- {item}"
            )

        linhas.append("")

    # -----------------------------------------------------
    # IDIOMAS
    # -----------------------------------------------------

    if informacoes["idiomas"]:

        linhas.append(
            "## IDIOMAS"
        )

        for item in informacoes["idiomas"]:

            linhas.append(
                f"- {item}"
            )

        linhas.append("")

    # -----------------------------------------------------
    # COMPETÊNCIAS
    # -----------------------------------------------------

    if informacoes["competencias"]:

        linhas.append(
            "## COMPETÊNCIAS E CONHECIMENTOS"
        )

        for item in informacoes["competencias"]:

            linhas.append(
                f"- {item}"
            )

        linhas.append("")

    # -----------------------------------------------------
    # PROJETOS
    # -----------------------------------------------------

    if informacoes["projetos"]:

        linhas.append(
            "## PROJETOS"
        )

        for item in informacoes["projetos"]:

            linhas.append(
                f"- {item}"
            )

        linhas.append("")

    # -----------------------------------------------------
    # GARANTIA DE PRESERVAÇÃO
    # -----------------------------------------------------

    linhas.append(
        "## OUTRAS INFORMAÇÕES DO CURRÍCULO ORIGINAL"
    )

    linhas.append(
        "As informações abaixo foram preservadas "
        "do currículo original para evitar perda "
        "de dados relevantes:"
    )

    linhas.append("")

    for linha in curriculo.splitlines():

        if linha.strip():

            linhas.append(
                f"- {linha.strip()}"
            )

    return "\n".join(linhas)


# =========================================================
# ESTADO DA SESSÃO
# =========================================================

valores_iniciais = {
    "curriculo": "",
    "vaga": "",
    "informacoes": {},
    "perguntas": [],
    "respostas": [],
    "indice": 0,
    "entrevista_iniciada": False,
    "finalizada": False,
    "resultado": ""
}

for chave, valor in valores_iniciais.items():

    if chave not in st.session_state:

        st.session_state[chave] = valor


# =========================================================
# ETAPA 1 - CURRÍCULO
# =========================================================

st.header("📄 1. Seu currículo")

st.write(
    "Anexe seu currículo em PDF ou DOCX. "
    "Você também pode colar o conteúdo manualmente."
)

arquivo = st.file_uploader(
    "📎 Anexar currículo",
    type=["pdf", "docx"]
)

if arquivo is not None:

    if st.button(
        "📖 Ler currículo anexado",
        use_container_width=True
    ):

        texto = extrair_curriculo(
            arquivo
        )

        if texto.strip():

            st.session_state.curriculo = texto

            st.session_state.informacoes = (
                analisar_curriculo(texto)
            )

            st.success(
                "✅ Currículo lido com sucesso!"
            )

        else:

            st.error(
                "Não foi possível encontrar texto "
                "no arquivo."
            )


st.write("### Ou cole seu currículo")

curriculo_manual = st.text_area(
    "Currículo:",
    height=250,
    placeholder="""
Nome: João Silva

Formação:
Engenharia de Produção - INATEL

Experiência:
Estágio em produção durante 1 ano.

Cursos:
Excel
Power BI

Conhecimentos:
Excel, Power BI e Python.

Idiomas:
Inglês intermediário.
""",
    value=st.session_state.curriculo
)


if curriculo_manual.strip():

    curriculo_atual = curriculo_manual

else:

    curriculo_atual = st.session_state.curriculo


# =========================================================
# MOSTRAR ANÁLISE DO CURRÍCULO
# =========================================================

if curriculo_atual.strip():

    informacoes = analisar_curriculo(
        curriculo_atual
    )

    st.session_state.informacoes = informacoes

    with st.expander(
        "🔎 Informações identificadas no currículo",
        expanded=True
    ):

        if informacoes["formacao"]:

            st.write("### 🎓 Formação")

            for item in informacoes["formacao"]:

                st.write(
                    f"• {item}"
                )

        if informacoes["experiencias"]:

            st.write("### 💼 Experiências")

            for item in informacoes["experiencias"]:

                st.write(
                    f"• {item}"
                )

        if informacoes["cursos"]:

            st.write("### 📚 Cursos")

            for item in informacoes["cursos"]:

                st.write(
                    f"• {item}"
                )

        if informacoes["idiomas"]:

            st.write("### 🌎 Idiomas")

            for item in informacoes["idiomas"]:

                st.write(
                    f"• {item}"
                )

        if informacoes["competencias"]:

            st.write("### 💻 Competências")

            for item in informacoes["competencias"]:

                st.write(
                    f"• {item}"
                )

        if informacoes["projetos"]:

            st.write("### 🚀 Projetos")

            for item in informacoes["projetos"]:

                st.write(
                    f"• {item}"
                )


# =========================================================
# ETAPA 2 - VAGA
# =========================================================

st.header("💼 2. Vaga desejada")

vaga = st.text_area(
    "Cole aqui a descrição da vaga:",
    height=250,
    placeholder="""
Vaga: Estágio em Engenharia de Produção

Requisitos:

- Cursando Engenharia de Produção
- Conhecimento em Excel
- Conhecimento em Power BI
- Boa comunicação
- Organização
- Trabalho em equipe
- Inglês intermediário
"""
)


# =========================================================
# INICIAR ENTREVISTA
# =========================================================

if st.button(
    "🚀 Iniciar entrevista",
    use_container_width=True
):

    if curriculo_atual.strip() == "":

        st.warning(
            "Adicione ou cole seu currículo."
        )

    elif vaga.strip() == "":

        st.warning(
            "Adicione a descrição da vaga."
        )

    else:

        st.session_state.curriculo = (
            curriculo_atual
        )

        st.session_state.vaga = vaga

        informacoes = analisar_curriculo(
            curriculo_atual
        )

        st.session_state.informacoes = (
            informacoes
        )

        perguntas = gerar_perguntas(
            curriculo_atual,
            vaga
        )

        st.session_state.perguntas = perguntas
        st.session_state.respostas = []
        st.session_state.indice = 0
        st.session_state.entrevista_iniciada = True
        st.session_state.finalizada = False
        st.session_state.resultado = ""

        st.rerun()


# =========================================================
# ETAPA 3 - ENTREVISTA
# =========================================================

if st.session_state.entrevista_iniciada:

    indice = st.session_state.indice
    perguntas = st.session_state.perguntas

    if indice < len(perguntas):

        st.divider()

        st.header("🎤 Entrevista personalizada")

        progresso = (
            (indice + 1)
            / len(perguntas)
        )

        st.progress(
            progresso
        )

        st.write(
            f"**Pergunta {indice + 1} "
            f"de {len(perguntas)}**"
        )

        st.info(
            perguntas[indice]
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


# =========================================================
# FINAL DA ENTREVISTA
# =========================================================

if (
    st.session_state.entrevista_iniciada
    and st.session_state.indice
    >= len(st.session_state.perguntas)
    and not st.session_state.finalizada
):

    st.divider()

    st.success(
        "🎉 Você concluiu a entrevista!"
    )

    if st.button(
        "📊 Gerar análise completa",
        use_container_width=True
    ):

        curriculo = (
            st.session_state.curriculo
        )

        vaga = (
            st.session_state.vaga
        )

        informacoes = (
            st.session_state.informacoes
        )

        perguntas = (
            st.session_state.perguntas
        )

        respostas = (
            st.session_state.respostas
        )

        # -------------------------------------------------
        # COMPARAÇÃO
        # -------------------------------------------------

        encontrados, ausentes = (
            comparar_curriculo_vaga(
                curriculo,
                vaga
            )
        )

        # -------------------------------------------------
        # ANÁLISE DAS RESPOSTAS
        # -------------------------------------------------

        analise_respostas = (
            analisar_respostas(
                perguntas,
                respostas
            )
        )

        # -------------------------------------------------
        # CURRÍCULO REFORMULADO
        # -------------------------------------------------

        novo_curriculo = (
            criar_curriculo_reformulado(
                curriculo,
                informacoes,
                vaga
            )
        )

        # -------------------------------------------------
        # RESULTADO
        # -------------------------------------------------

        resultado = ""

        resultado += """
# 📊 ANÁLISE DA ENTREVISTA

"""

        resultado += """
## 1. PONTOS IDENTIFICADOS NAS RESPOSTAS

"""

        for item in analise_respostas:

            resultado += (
                f"- {item}\n"
            )

        resultado += """

## 2. RELAÇÃO ENTRE CURRÍCULO E VAGA

"""

        if encontrados:

            resultado += (
                "### ✅ Requisitos identificados no currículo\n\n"
            )

            for item in encontrados:

                resultado += (
                    f"- {item.title()}\n"
                )

        else:

            resultado += (
                "Nenhum dos requisitos analisados "
                "foi identificado diretamente no currículo.\n"
            )

        if ausentes:

            resultado += (
                "\n### ⚠️ Requisitos que não apareceram claramente\n\n"
            )

            for item in ausentes:

                resultado += (
                    f"- {item.title()}\n"
                )

        resultado += """

## 3. PERGUNTAS E RESPOSTAS

"""

        for i in range(len(perguntas)):

            resultado += (
                f"### Pergunta {i + 1}\n\n"
            )

            resultado += (
                f"**{perguntas[i]}**\n\n"
            )

            resultado += (
                f"**Resposta:** "
                f"{respostas[i]}\n\n"
            )

        resultado += """

## 4. PONTOS A DESENVOLVER

"""

        resultado += """
- Procure utilizar exemplos concretos em suas respostas.
- Relacione suas experiências aos requisitos da vaga.
- Evite respostas muito curtas.
- Explique o que você fez e qual foi o resultado.
- Quando falar sobre uma habilidade, procure apresentar
uma situação em que ela foi utilizada.
"""

        resultado += """

## 5. CURRÍCULO REFORMULADO

"""

        resultado += novo_curriculo

        st.session_state.resultado = resultado
        st.session_state.finalizada = True

        st.rerun()


# =========================================================
# RESULTADO FINAL
# =========================================================

if st.session_state.finalizada:

    st.divider()

    st.header("📊 Resultado da preparação")

    st.markdown(
        st.session_state.resultado
    )

    st.divider()

    st.subheader(
        "📥 Baixar resultado"
    )

    st.download_button(
        "Baixar relatório completo",
        st.session_state.resultado,
        file_name="resultado_prepai.txt",
        mime="text/plain",
        use_container_width=True
    )

    # -----------------------------------------------------
    # NOVA ENTREVISTA
    # -----------------------------------------------------

    if st.button(
        "🔄 Fazer nova entrevista",
        use_container_width=True
    ):

        st.session_state.perguntas = []
        st.session_state.respostas = []
        st.session_state.indice = 0
        st.session_state.entrevista_iniciada = False
        st.session_state.finalizada = False
        st.session_state.resultado = ""

        st.rerun()
