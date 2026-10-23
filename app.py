"""Interface Streamlit. Aucun appel réseau ici : tout passe par services/."""
import base64

import streamlit as st

from services.llm import ConversationAgent
from services import stt


class UserInterface:
    def __init__(self):
        st.set_page_config(page_title="Jarvis")
        st.title("Barbe-Quasar")
        self.conversation_agent_object = self.get_persistant_conversation_agent()

    def get_persistant_conversation_agent(self):
        # Streamlit relance le script à chaque interaction : on garde l'agent
        # (et son historique) dans session_state pour qu'il ne soit pas recréé.
        if "conversation_agent_object" not in st.session_state:
            st.session_state.conversation_agent_object = ConversationAgent()
        return st.session_state.conversation_agent_object

    def show_message_content(self, content):
        # Un message texte est une chaîne, un message avec images est une liste de morceaux
        if isinstance(content, str):
            st.markdown(content)
            return

        for part in content:
            if part["type"] == "text":
                st.markdown(part["text"])
            elif part["type"] == "image_url":
                image_base64 = part["image_url"]["url"].split(",", 1)[1]
                st.image(base64.b64decode(image_base64))

    def show_discussion_history(self):
        for message in self.conversation_agent_object.get_conversation_history():
            with st.chat_message(message["role"]):
                self.show_message_content(message["content"])

    def show_sidebar(self):
        with st.sidebar:
            st.header("Mémoire")
            st.metric(
                "Messages en mémoire",
                len(self.conversation_agent_object.get_conversation_history()),
            )

    def run(self):
        user_input = st.chat_input(
            "Que veux tu moussaillon ?",
            accept_file="multiple",
            file_type=["png", "jpg", "jpeg"],
            accept_audio=True,
        )

        if user_input:
            text = user_input.text
            images = [(file.type, file.getvalue()) for file in user_input.files]

            # Vocal sans texte : on transcrit l'audio et on s'en sert comme question
            if not text and user_input.audio:
                try:
                    with st.spinner("Transcription du vocal..."):
                        text = stt.transcribe_audio(user_input.audio)
                except NotImplementedError:
                    st.warning("La saisie vocale n'est pas encore disponible.")

            # Image envoyée sans question : on en demande une description
            if images and not text:
                text = "Décris cette image."

            if text:
                self.conversation_agent_object.ask_llm(text, images)

        self.show_discussion_history()
        self.show_sidebar()


if __name__ == "__main__":
    UserInterface().run()
