from llama_index.core import Settings
from llama_index.llms.groq import Groq
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner
from dotenv import load_dotenv
import os
import arxiv
import json

# Carrega .env
load_dotenv()



# Configura o modelo da Groq
llm = Groq(model="llama-3.3-70b-versatile", api_key=os.environ.get("GROQ_API_KEY"))

# Função que busca artigos no arXiv
def consulta_artigos(titulo: str) -> str:
    client = arxiv.Client()
    busca = arxiv.Search(
        query=titulo,
        max_results=3,
        sort_by=arxiv.SortCriterion.Relevance
    )
    resultados = [
        f"Titulo: {artigo.title}\n"
        f"Categoria: {artigo.primary_category}\n"
        f"Link: {artigo.entry_id}"
        for artigo in client.results(busca)
    ]
    return "\n\n".join(resultados)

# Registra como ferramenta
consulta_artigos_tool = FunctionTool.from_defaults(fn=consulta_artigos)

# Cria agente
agent_worker = FunctionCallingAgentWorker.from_tools(
    [consulta_artigos_tool],
    verbose=False,
    allow_parallel_tool_calls=False,
    llm=llm
)
agent = AgentRunner(agent_worker)

# Função principal
def executar_consulta(pergunta: str):
    dados= []
    # Extrair o termo de busca da pergunta (exemplo simples para "sobre X")
    termo = pergunta.replace("Me retorne artigos sobre", "").strip()

    # Executa a ferramenta diretamente
    artigos_raw = consulta_artigos(termo)

    # Chamada da LLM
    response = agent.chat(pergunta)
    resposta_llm = response.response.strip()

    # Exibe artigos da ferramenta diretamente
    if artigos_raw:
       
        for bloco in artigos_raw.strip().split("\n\n"):
            linhas = bloco.strip().split("\n")
            if len(linhas) >= 3:
                dados.append({"Titulo":linhas[0].replace('Titulo: ', ''), "Categoria":linhas[0].replace('Titulo: ', ''), "Link":linhas[2].replace('Link: ', '')})
                """
                print(f"Título   : {linhas[0].replace('Titulo: ', '')}")
                print(f"Categoria: {linhas[1].replace('Categoria: ', '')}")
                print(f"Link     : {linhas[2].replace('Link: ', '')}")
                print("-" * 50)"""
                
       
    else:
        print("\n⚠️ Nenhum artigo retornado pela função `consulta_artigos`.")

    
    return json.dumps(dados)
  