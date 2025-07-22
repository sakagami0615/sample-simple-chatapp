from langchain.agents import AgentType, initialize_agent
from langchain.agents.agent import AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_memory import BaseChatMemory
from langchain.prompts import MessagesPlaceholder
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI


def create_conversation_buffer_memory() -> ConversationBufferMemory:
    """会話記憶を作成

    Returns:
        ConversationBufferMemory: 作成した会話記憶
    """
    memory = ConversationBufferMemory(memory_key="memory", return_messages=True)
    return memory


def create_agent(model_name: str, temperature: float, memory: BaseChatMemory | None) -> AgentExecutor:
    """エージェントを作成

    Args:
        model_name (str): _description_
        temperature (float): _description_
        memory (BaseChatMemory | None): _description_
        model_name (str): モデル名
        temperature (float): 「ランダム性」や「多様性」の度合いを制御するパラメータ [0, 1]
        memory (BaseChatMemory | None): 使用する会話記憶

    Returns:
        AgentExecutor: 作成したエージェント
    """
    chat = ChatOpenAI(model=model_name, temperature=temperature, streaming=True)
    agent_kwargs = {"extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")]}

    # ツールは、[WEB検索]と[Wiki検索]を設定
    tools = [DuckDuckGoSearchRun()] + load_tools(["wikipedia"])

    agent = initialize_agent(tools, chat, agent=AgentType.OPENAI_FUNCTIONS, agent_kwargs=agent_kwargs, memory=memory)
    return agent
