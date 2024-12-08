'''__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')'''
from interface.chatboot_interface import ChatbootInterface
import streamlit as st



st.set_page_config(page_title="Chat Porto do Itaqui", page_icon='📃')


interface = ChatbootInterface(model_apenai=True)
interface.sidebar()
interface.chat_window()



