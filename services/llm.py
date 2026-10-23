"""Agent conversationnel (Groq) : historique, images (VLM) et appels au LLM."""
import base64
import io

from groq import Groq
from PIL import Image

import config


class ConversationAgent:
    def __init__(self):
        self.groq_client = Groq(api_key=config.GROQ_API_KEY)
        self.conversation_history = [
                {
                    "role": "system",
                    "content": self.read_file(file_path=config.SYSTEM_PROMPT_PATH)
                }
            ]


    @staticmethod
    def read_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()


    def get_conversation_history(self):
        return self.conversation_history[1: ]


    def update_conversation_history(self, role, content):
        self.conversation_history.append(
            {
            "role": role,
            "content": content,
            }
        )


    @staticmethod
    def resize_image(image_bytes):
        # Les tokens dépendent du nombre de pixels : on réduit l'image
        # (en gardant les proportions) et on la recompresse en JPEG.
        image = Image.open(io.BytesIO(image_bytes))
        image.thumbnail((config.MAX_IMAGE_SIZE, config.MAX_IMAGE_SIZE))
        image = image.convert("RGB")

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=config.JPEG_QUALITY)
        return buffer.getvalue()


    def build_content_with_images(self, text, images):
        # images : liste de tuples (type_mime, octets)
        # Pour envoyer des images, "content" devient une liste de morceaux :
        # un morceau texte + un morceau image_url (image encodée en base64)
        content = [{"type": "text", "text": text}]

        for _, image_bytes in images:
            resized_bytes = self.resize_image(image_bytes)
            image_base64 = base64.b64encode(resized_bytes).decode("utf-8")
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                }
            )

        return content


    def history_contains_images(self):
        return any(
            isinstance(message["content"], list)
            for message in self.conversation_history
        )


    def ask_llm(self, text_interaction, images=None):

        if images:
            content = self.build_content_with_images(text_interaction, images)
        else:
            content = text_interaction

        self.update_conversation_history(role="user", content=content)

        # Le modèle texte ne comprend pas les messages contenant des images :
        # dès qu'il y en a une dans l'historique, on utilise le modèle vision.
        if self.history_contains_images():
            model = config.VISION_MODEL
        else:
            model = config.TEXT_MODEL

        response = self.groq_client.chat.completions.create(
            messages=self.conversation_history,
            model=model,
            include_reasoning=False,
        ).choices[0].message.content


        self.update_conversation_history(role="assistant", content=response)
        return response


if __name__ == "__main__":
    agent = ConversationAgent()
    question = input("Pose ta question :\n")
    response = agent.ask_llm(question)
    print("\n")
    print(response)
