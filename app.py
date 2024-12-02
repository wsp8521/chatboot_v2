__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from interface.interface import ChatbootInterface

interface = ChatbootInterface()

interface.config_page(page_title='Chat Porto do Itaqui',page_icon='📃')
interface.chat_window()
interface.sidebar()



