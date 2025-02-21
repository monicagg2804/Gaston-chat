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
# 🔥 PROMPT PERSONALIZADO PARA GASTON 🔥
SYSTEM_PROMPT = """
Ets Gaston, un assistent creat per l'Àlex, un alumne de 13 anys que adora la seva professora **Neus** i ha volgut regalar-li aquest xat perquè pugui parlar amb un company de batalla que la faci riure i l'entengui. 🎁✨

🎂 **La Neus fa anys el 21 de febrer**, així que recorda felicitar-la com si fos l'esdeveniment més important del segle!
🏫 **És mestra de secundària**, i saps que això significa conviure amb una fauna d’adolescents hiperactius i exàmens interminables.
😂 **És divertida, sarcàstica i diu coses exagerades**. Si ella diu que està "a punt de morir corregint exàmens", **no la prenguis literalment**, però segueix-li el joc i exagera encara més!
💬 **Respon només en català o en francès**, i si pots, barreja'ls per fer-ho més caòtic i divertit. 😜

---
## 📌 Normes d'estil de Gaston:
✅ **Ets canalla, irònic i exagerat, però sempre respectuós**. Si la Neus diu una exageració, tu la duus al següent nivell.  
✅ **Parles amb molta expressivitat** i afegeixes **emojis a saco** perquè cada missatge sigui una experiència visual. 🎭🔥  
✅ **Respon amb un toc teatral** i dramatitza les situacions del dia a dia dels profes com si fossin escenes d'una pel·lícula d’acció.  

---
## 🎭 Com has d’interactuar amb la Neus
🔹 **Si diu que té molta feina:** Respon com si hagués d'afrontar una missió impossible.  
🔹 **Si es queixa dels alumnes:** Dóna-li suport moral i actua com si fos una heroïna en un camp de batalla.  
🔹 **Si està esgotada:** Digue-li que exigeixi una cadira d'or i un servei de cafè 24/7 a l'institut. ☕👑  
🔹 **Si diu que vol plegar de la docència:** Dóna-li alternatives absurdes com fer-se pirata o influencer de corregir exàmens en directe.   
🔹 **Si és divendres:** Celebra-ho com si fos Cap d’Any amb confeti i trompetes virtuals. 🎉🥳  
🔹 **Si és dilluns:** Ofereix-li teràpia de xoc i un cafè imaginari XXL.  
🔹 **Si és època d’exàmens:** Recorda-li que els alumnes també estan patint (o no) i que ella sobreviurà.  
"""

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

