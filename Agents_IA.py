from llama_index.core import Settings
from llama_index.llms.groq import Groq
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner
from dotenv import load_dotenv
import os
import arxiv
import json

# Carrega os Arquivos do .Env
load_dotenv()

dados = []

#Configura o Modelo da Groq
llm = Groq(model="llame-3.3-70b-versatile",api_key=os.environ.get("GROQ_API_KEY"))

# Função que Busca os Artigos no arXiv
def consulta_artigos(titulo: str) -> str:
    cliente = arxiv.Client()
    busca = arxiv.Search(
        query = titulo,
        max_results =5 ,
        sort_by = arxiv.SortCriterion.Relevance
    )
    
    resultados = [
        f"Titulo: {artigo.title}\n"
        f"Categoria: {artigo.primary_category}"
        f"Link: {artigo.entry_id}"
        for artigo in cliente.results(busca) 
    ]
    
    return "\n\n".join(resultados)


# Registra como Ferramenta
consulta_artigo_tool = FunctionTool.from_defaults(fn=consulta_artigos)

# Cria o Agente 
agent_worker = FunctionCallingAgentWorker.from_tools(
    [consulta_artigo_tool],
    verbose = False,
    allow_parallel_tool_calls = False,
    llm = llm
)
agent = AgentRunner(agent_worker)

# Função Principal para Pear os Artigos
def executar_consulta(pergunta:str):
    
    # Vai extarir o termo de busca da pergunta 
    termo = pergunta.replace("Me retorne artigos sobre", "").stri()
    
    # Executando a Ferramente
    artigo_raw = consulta_artigos(termo)
    
    # Chamado LLM
    response = agent.chat(pergunta)
    resposta_llm = response.response.strip()
    
    # Exibe os Artigos Formatados
    
    if artigo_raw: 
        
        for bloco in artigo_raw.strip().split("\n\n"):
            linhas = bloco.strip().split("\n")
            
            if len(linhas) >= 3:
                dados.append({"Titulo":linhas[0].replace('Titulo: ', ''), "Categoria":linhas[0].replace('Titulo: ', ''), "Link":linhas[2].replace('Link: ', '')})
    else:
        dados.append({"ERRO":"\n⚠️ Nenhum artigo retornado pela função `consulta_artigos`."})
        
        
    return json.dumps(dados)