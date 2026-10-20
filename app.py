import streamlit as st
from llm_agent import ConversationAgent


st.set_page_config(page_title="Jarvis")
st.title("Barbe-Quasar")

# Streamlit relance le script à chaque message : on garde l'agent
# (et son historique) dans session_state pour qu'il ne soit pas recréé.
if "agent" not in st.session_state:
	st.session_state.agent = ConversationAgent()
agent = st.session_state.agent


user_input = st.chat_input(
	"Que veux tu moussaillon ?",
	accept_file=False,
	accept_audio=False
	)

if user_input :
	# met à jour l'historique (question + réponse)
	agent.ask_llm(user_input)

# Affichage de tout l'historique, sans le prompt système (personnage)
for message in agent.conversation_history:
	if message["role"] != "system":
		with st.chat_message(message["role"]):
			st.markdown(message["content"])

# Visualisation de la mémoire de l'agent
with st.sidebar:
	st.header("Mémoire")
	nb_messages = len(agent.conversation_history) - 1
	st.metric("Messages en mémoire", nb_messages)
