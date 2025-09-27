# 環境変数読み込み用ライブラリのインポート（.envファイルからAPIキーなどを読み込むため）
from dotenv import load_dotenv

"""
Streamlitを使ったWebアプリケーションです。健康と旅行の2つのモードで専門家からのアドバイスを提供します。
- ユーザーは「健康」または「旅行」モードを選択できます。
- 各モードで質問を入力すると、AIが日本語で専門的なアドバイスを返します。
- OpenAIのGPT-4o-miniモデルをLangChain経由で利用しています。
- ユーザーの入力内容とAIの回答を画面に表示します。
- dotenvで環境変数（APIキーなど）を読み込みます。

使用モジュール:
    - streamlit: Web UIの構築
    - langchain_openai: OpenAIの言語モデルとの連携
    - dotenv: 環境変数の読み込み

関数:
    なし（Streamlitアプリとしてトップダウンで実行）

使い方:
    このスクリプトをStreamlitで実行し、Webインターフェースを起動してください。
"""

# .envファイルから環境変数（OpenAI APIキーなど）を読み込み
load_dotenv()

# Streamlitライブラリをインポート（Webアプリケーション用UI作成のため）
import streamlit as st

# アプリケーションのタイトルを画面上部に表示
st.title("Lesson21 Chapter6 提出課題")

# ユーザーが動作モードを選択するためのラジオボタンを表示
# 「健康」または「旅行」から一つを選択可能
selected_item = st.radio(
    "動作モードを選択してください。",
    ["健康", "旅行"]
)

# 視覚的な区切り線を表示
st.divider()

# 選択されたモードに応じて、適切な入力フォームを表示
if selected_item == "健康":
    # 健康モードが選択された場合の入力フォーム
    input_message = st.text_input(label="健康に関して相談したい内容を入力してください。")
else:
    # 旅行モードが選択された場合の入力フォーム
    input_message = st.text_input(label="旅行に関して相談したい内容を入力してください。")

# 「実行」ボタンが押された場合の処理
if st.button("実行"):
    # 視覚的な区切り線を表示
    st.divider()
    
    # ユーザーが入力した内容を画面に表示
    st.write(f"入力された内容: {input_message}")

    # LangChainのOpenAI連携ライブラリをインポート
    from langchain_openai import ChatOpenAI
    # LangChainのメッセージクラスをインポート（システムメッセージとユーザーメッセージ用）
    from langchain.schema import SystemMessage, HumanMessage

    # OpenAIのGPT-4o-miniモデルを初期化
    # temperature=0.5 は回答の一貫性を保つため（ランダム性を最小限に）
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)

    # 選択されたモードに応じてシステムプロンプト（AIの役割設定）を決定
    if selected_item == "健康":
        # 健康モード用のシステムプロンプト設定
        system_prompt = "あなたは健康に関する専門家です。ユーザーの相談に専門的なアドバイスを日本語で提供してください。"
    else:
        # 旅行モード用のシステムプロンプト設定
        system_prompt = "あなたは旅行に関する専門家です。ユーザーの相談に専門的なアドバイスを日本語で提供してください。"

    # AIに送信するメッセージリストを作成
    # SystemMessage: AIの役割や応答方法を指定
    # HumanMessage: ユーザーからの実際の質問内容
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=input_message)
    ]
    
    # OpenAI APIを通じてAIから回答を取得
    result = llm(messages)
    
    # AIが生成した回答内容を画面に表示
    st.write(result.content)
