import streamlit as st
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

from llm.agent import create_agent, create_conversation_buffer_memory
from llm.datatype import ModelInfo
from setting import LOGGER, TITLE


def select_model() -> ModelInfo:
    """使用するモデル選択

    Returns:
        ModelInfo: 選択したモデル情報
    """
    model_name = st.sidebar.radio("Model:", ("gpt-3.5-turbo", "gpt-4"))
    temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
    LOGGER.debug(f"select model info (model: {model_name}, model: {temperature})")
    return ModelInfo(model_name, temperature)


def update_model(model_info: ModelInfo) -> None:
    """モデル(エージェント)の更新処理

    [初回時のモデル新規作成]と[モデル情報が変更された際にエージェントを更新]する処理を担う。

    Args:
        model_info (ModelInfo): モデル情報
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "memory" not in st.session_state:
        st.session_state.memory = create_conversation_buffer_memory()
    if "latest_model_info" not in st.session_state:
        st.session_state.latest_model_info = model_info

    # 会話履歴削除ボタン
    clear_button = st.sidebar.button("Clear Conversation History", key="clear")

    # 新規エージェント作成
    if "agent" not in st.session_state:
        LOGGER.info("Create agent")
        st.session_state.agent = create_agent(model_info.model_name, model_info.temperature, st.session_state.memory)
    else:
        # モデル情報が変更された場合、エージェント再作成(記憶はそのまま)
        if st.session_state.latest_model_info != model_info:
            LOGGER.info("Update agent")
            # モデル情報も差し替える
            st.session_state.latest_model_info = model_info
            st.session_state.agent = create_agent(
                model_info.model_name, model_info.temperature, st.session_state.memory
            )

        # 会話履歴削除ボタンが押された場合、会話履歴を削除してエージェントを再作成(記憶も初期化)
        if clear_button:
            LOGGER.info("Clear message & update agent")
            st.session_state.messages = []
            st.session_state.memory = create_conversation_buffer_memory()
            st.session_state.agent = create_agent(
                st.session_state.latest_model_info.model_name,
                st.session_state.latest_model_info.temperature,
                st.session_state.memory,
            )


def render_chat_history() -> None:
    """会話履歴の表示"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def chat_process(prompt: str) -> None:
    """チャット処理

    Args:
        prompt (str): ユーザ入力内容
    """
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 回答はストリーミング表示する
        callback = StreamlitCallbackHandler(st.container())
        response = st.session_state.agent.invoke(
            {"input": prompt}, {"callbacks": [callback]}
        )
        st.markdown(response["output"])

    st.session_state.messages.append({"role": "assistant", "content": response["output"]})


def main() -> None:
    """メイン処理"""
    st.title(TITLE)

    model_info = select_model()
    update_model(model_info)
    render_chat_history()

    prompt = st.chat_input("What is up?")
    if prompt:
        chat_process(prompt)


if __name__ == "__main__":
    main()
