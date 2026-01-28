import streamlit as st
import os
from openai import OpenAI
import fitz  # PyMuPDF
from fpdf import FPDF

# --- КОНФИГУРАЦИЯ (DeepSeek Engine через Secrets) [cite: 2026-01-28] ---
try:
    # Пытаемся взять ключ из настроек облака Streamlit [cite: 2026-01-28]
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    # Резервный вариант для локальной работы в Cursor [cite: 2026-01-20]
    api_key = "sk-ffce960a76d040d29031825ad4c4428c"

client = OpenAI(
    api_key=api_key, 
    base_url="https://api.deepseek.com/v1"
)

class LegalReport(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 12)
        self.cell(0, 10, 'Irish Shepherd: Supreme Judge Final Decision', 0, 1, 'C')

def extract_text_from_pdf(uploaded_file):
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        return "".join([page.get_text() for page in doc])
    except Exception as e:
        return f"Ошибка чтения: {str(e)}"

# --- ЦЕПОЧКА 4-4-4 BURAN (5 ЦИФРОВЫХ ДВОЙНИКОВ) [cite: 2026-01-20] ---
def run_legal_factory(user_task, full_context):
    # Этап 1: Аналитик [cite: 2026-01-05]
    ana = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "Этап 1: Ты Аналитик. Собери все факты и даты нарушения."},
                  {"role": "user", "content": f"Задание: {user_task}\nКонтекст: {full_context[:40000]}"}]
    ).choices[0].message.content

    # Этап 2: Бруно (Adversary) [cite: 2025-12-23]
    bru = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "Этап 2: Ты Бруно. Твоя цель — разбить позицию и найти слабые места."},
                  {"role": "user", "content": ana}]
    ).choices[0].message.content

    # Этап 3: Юрист [cite: 2026-01-20]
    jur = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "Этап 3: Ты Юрист. Обоснуй позицию по Unfair Dismissals Act 1977."},
                  {"role": "user", "content": f"Факты: {ana}\nКонтраргументы Бруно: {bru}"}]
    ).choices[0].message.content

    # Этап 4: Контролер (CeADAR) [cite: 2026-01-07]
    con = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "Этап 4: Ты Контролер. Проверь логику и отсутствие людей в штате."},
                  {"role": "user", "content": f"Юридическая позиция: {jur}"}]
    ).choices[0].message.content

    # Этап 5: Верховный Судья [cite: 2026-01-20]
    judge = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "Этап 5: Ты Верховный Судья. Вынеси ОКОНЧАТЕЛЬНЫЙ ВЕРДИКТ."},
                  {"role": "user", "content": f"Анализ: {ana}\nРиски: {bru}\nЗакон: {jur}\nАудит: {con}"}]
    ).choices[0].message.content
    
    return ana, bru, jur, con, judge

# --- ИНТЕРФЕЙС ГЛОБАЛЬНОЙ ПЛАТФОРМЫ [cite: 2026-01-20] ---
st.set_page_config(page_title="Irish Shepherd OS", layout="wide")
st.sidebar.title("🐺 Irish Shepherd OS")
st.sidebar.info("Глобальная цель: Платформа юридических услуг на двух континентах [cite: 2026-01-20]")

user_instruction = st.text_area("Задание для системы:", value="Подготовить жалобу по факту незаконного увольнения", height=100)
uploaded_files = st.file_uploader("Загрузите юридические документы (PDF):", type=["pdf"], accept_multiple_files=True)

# ГЛАВНЫЙ РЫЧАГ УПРАВЛЕНИЯ [cite: 2026-01-20]
if st.button("👑 ВЕРДИКТ ВЕРХОВНОГО СУДЬИ"):
    if not user_instruction:
        st.error("Пожалуйста, введите задание!")
    else:
        with st.spinner("Система Pentagon выносит окончательный вердикт..."):
            combined_text = ""
            if uploaded_files:
                for f in uploaded_files:
                    combined_text += f"\n--- {f.name} ---\n" + extract_text_from_pdf(f)
            
            # Запуск конвейера цифровых двойников [cite: 2026-01-05, 2026-01-20]
            ana, bru, jur, con, judge = run_legal_factory(user_instruction, combined_text)
            
            # Визуализация работы штаба
            st.markdown("### 🧬 Процесс принятия решения")
            col1, col2 = st.columns(2)
            with col1:
                st.error(f"**Агент 2 (Бруно - Оппонент):**\n{bru[:400]}...")
            with col2:
                st.warning(f"**Агент 4 (Контролер CeADAR):**\n{con[:400]}...")

            st.markdown("---")
            st.header("⚖️ ОКОНЧАТЕЛЬНЫЙ ВЕРДИКТ ВЕРХОВНОГО СУДЬИ")
            st.success(judge)

            # Генерация официального PDF-документа
            try:
                pdf = LegalReport()
                pdf.add_page()
                pdf.set_font('helvetica', size=11)
                # Очистка текста для корректной записи в PDF [cite: 2026-01-28]
                clean_text = judge.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(0, 10, txt=clean_text)
                
                pdf_output = pdf.output()
                
                st.download_button(
                    label="📥 СКАЧАТЬ ОФИЦИАЛЬНЫЙ ВЕРДИКТ",
                    data=pdf_output,
                    file_name="Supreme_Verdict_Final.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Ошибка формирования PDF: {e}")
