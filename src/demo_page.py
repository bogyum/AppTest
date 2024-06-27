import streamlit as st
from streamlit_chat import message
import requests
import json

class KoAlpaca_web() :
    def __init__(self):
        self.URL = 'http://127.0.0.1:8000/chat'

    def get_answer(self, message):
        param = {'user_message': message}
        req = requests.post(self.URL, json=param)
        output = json.loads(req.content)
        return output

    def update_log(self, user_message, chatbot_message):
        if 'chat_log' not in st.session_state:
            st.session_state.chat_log = {'user_message': [], 'chatbot_message': []}
        st.session_state.chat_log['chatbot_message'].append(chatbot_message)
        st.session_state.chat_log['user_message'].append(user_message)
        return st.session_state.chat_log

    def chat(self):
        st.title('Chatbot Test')
        st.header('Using KoAlpaca')
        st.subheader('beomi/KoAlpaca-Polyglot-5.8B')
        st.text_input('무엇이든 물어보세요.', key='user_message')

        if user_message := st.session_state['user_message'] :
            answer = self.get_answer(user_message)
            chat_log = self.update_log(user_message, answer)
            chatbot_message = chat_log['chatbot_message'][::-1]
            user_message = chat_log['user_message'][::-1]

            for idx, (bot, user) in enumerate(zip(chatbot_message, user_message)):
                message(bot, key=f"{idx}_bot")
                message(user, key=f"{idx}_user", is_user=True)

if __name__ == '__main__':
    web = KoAlpaca_web()
    web.chat()
        