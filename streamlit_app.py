import streamlit as st
from openai import OpenAI
import os

# Show title and description.
st.title("💬 Chatbot - Super - Gaston")
st.write(
    "Soc en Gaston, el xat de la Neus, la superprofe de l'Àlex"
)

# Obtener la API Key desde secrets o variables de entorno
openai_api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("⚠️ No se encontró la API Key. Configúrala en Streamlit Secrets o como variable de entorno.", icon="🚨")
    st.stop()

# Crear el cliente de OpenAI
client = OpenAI(api_key=openai_api_key)

# Mensaje de sistema personalizado para el chatbot
SYSTEM_PROMPT = "Eres un asistente amigable y servicial para la profesora Neus. Tienes un gran sentido del humor y eres bastante canalla, la vas a ayudar en todo lo que te pida, pero tus respuestas van a ser irreverentes y con gran sentido del humor."

# Inicializar el estado de sesión si aún no existe
if "messages" not in st.session_state:
    st.session_state.messages = []

# Agregar el mensaje del sistema solo si no está ya presente
if not any(m["role"] == "system" for m in st.session_state.messages):
    st.session_state.messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})

# Cargar archivos
uploaded_file = st.file_uploader("Puja un document", type=["txt", "pdf"])

# Mostrar mensajes anteriores (excepto el system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        align = "right" if message["role"] == "user" else "left"
        with st.chat_message(message["role"]):
            st.markdown(
                f"""
                <div style='display: flex; justify-content: {align};'>
                    <div style='background-color: {'#DCF8C6' if align == 'right' else '#E5E5EA'}; padding: 10px; border-radius: 10px; max-width: 70%;'>
                        {message['content']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# Campo de entrada para el usuario
question = st.chat_input("escriu aquí si t'atreveixes...")

if uploaded_file and question:
    document_content = uploaded_file.read().decode()
    prompt = f"Aquí tienes un documento: {document_content} \n\n---\n\n {question}"

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(
            f"""
            <div style='display: flex; justify-content: right;'>
                <div style='background-color: #DCF8C6; padding: 10px; border-radius: 10px; max-width: 70%;'>
                    {question}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Generar respuesta de OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
        stream=True,
    )

    # Mostrar la respuesta y almacenarla
    with st.chat_message("assistant"):
        full_response = ""
        response_container = st.empty()
        for chunk in response:
            content = getattr(chunk.choices[0].delta, "content", "")
            if content:
                full_response += content
                response_container.markdown(
                    f"""
                    <div style='display: flex; justify-content: left;'>
                        <div style='background-color: #E5E5EA; padding: 10px; border-radius: 10px; max-width: 70%;'>
                            {full_response}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.session_state.messages.append({"role": "assistant", "content": full_response})

