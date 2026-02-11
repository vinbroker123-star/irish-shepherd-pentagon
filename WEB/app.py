import streamlit as st
import google.generativeai as genai
from docx import Document
from PyPDF2 import PdfReader
import json
import os

# --- ГЛОБАЛЬНЫЕ НАСТРОЙКИ ---
st.set_page_config(page_title="BURAN | MAS v2.8 MVP Ready", layout="wide")
DB_FILE = "knowledge_base.json"

# --- ПОДДЕРЖКА МОДЕЛИ GEMINI 2.5 FLASH ---
genai.configure(api_key="AIzaSyAPo1AMLqHooGteWwFhNmuaanHrMuNQkxs") 
model = genai.GenerativeModel('gemini-2.5-flash')

# --- ФУНКЦИИ БД ---
def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_db():
    if os.path.exists(DB_FILE) and os.path.getsize(DB_FILE) > 0:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# --- ИНИЦИАЛИЗАЦИЯ (ИСПРАВЛЕНИЕ ОШИБКИ СО СКРИНА 71) ---
if "vector_db" not in st.session_state: st.session_state.vector_db = load_db()
if "step" not in st.session_state: st.session_state.step = 3 # Начинаем с реализации, если QA пройден

# Расширяем до 5 этапов (1.Архитектор, 2.БА, 3.Программист, 4.QA, 5.MVP Release)
AGENTS = ["Архитектор Систем", "Бизнес-Аналитик", "Старший Программист", "QA Верификатор", "MVP Release"]

# --- САЙДБАР ---
st.sidebar.header("🕹️ Управление этапами")
# Исправлено: max_value теперь 5
st.session_state.step = st.sidebar.number_input("Текущий этап:", 1, 5, value=st.session_state.step)

st.sidebar.divider()
st.sidebar.header("📚 Энциклопедия")
for item in st.session_state.vector_db:
    st.sidebar.success(f"✅ {item['title']}")

# --- ИНТЕРФЕЙС ---
agent = AGENTS[st.session_state.step - 1]
st.title(f"🚜 {agent}")

# Логика генерации (Шаг 4 и 5 вашего плана)
if st.button(f"🚀 Сформировать работу: {agent}"):
    context = "\n".join([f"{i['title']}: {i['content']}" for i in st.session_state.vector_db])
    
    if agent == "Старший Программист":
        prompt = f"""Ты Старший Программист. Твоя задача - реализовать MVP Sprint 1-4.
        Основывайся на Архитектуре v1.3 и Master Spec: {context}
        Учти жесткие требования QA (Golden Datasets, Evidence-first).
        ВЫДАЙ: Структуру файлов проекта, логику Auth, Case CRUD и Pipeline загрузки."""
    elif agent == "QA Верификатор":
        prompt = f"Выдай Test Plan, Golden Datasets (5 шт) и Gate Checklists на основе: {context}"
    
    with st.spinner("Gemini 2.5 Flash анализирует базу знаний..."):
        response = model.generate_content(prompt)
        st.session_state.last_res = response.text
        st.markdown(st.session_state.last_res)

# Фиксация
if "last_res" in st.session_state:
    if st.button(f"🧊 FIX AS FACT ({agent})"):
        st.session_state.vector_db.append({"title": f"{agent} Baseline", "content": st.session_state.last_res})
        save_db(st.session_state.vector_db)
        st.session_state.step += 1
        st.rerun()