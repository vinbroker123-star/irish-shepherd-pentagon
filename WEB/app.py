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
        # Название в официальном отчете
        self.cell(0, 10, 'Legal Verification Platform: Final Verdict', 0, 1, 'C')

def extract_text_from_pdf(uploaded_file):
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        return "".join([page.get_text() for page in doc])
    except Exception as e:
        return f"Ошибка чтения: {str(e)}"

# --- ЦЕПОЧКА 4-4-4 BURAN (РАЗВЕРНУТАЯ ЛОГИКА 5 ДВОЙНИКОВ) [cite: 2026-01-20] ---
def run_legal_factory(user_task, full_context):
    # Этап 1: Аналитик [cite: 2026-01-05]
    ana = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "Этап 1: Ты Аналитик. Собери все факты и даты нарушения."},
                  {"role": "user", "content": f"Задание: {user_task}\nКонтекст: {full_context[:40000]}"}]
    ).choices[0].message.content

    # Этап 2: Бруно (Adversary/Оппонент) [cite: 2025-12-23]
    bru = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "Этап 2: Ты Оппонент. Твоя цель — разбить позицию и найти слабые места."},
                  {"role": "user", "content": ana}]
    ).choices[0].message.content

    # Этап 3: Юрист [cite: 2026-01-20]
    jur = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "Этап 3: Ты Юрист. Обоснуй позицию по Unfair Dismissals Act 1977."},
                  {"role": "user", "content": f"Факты: {ana}\nКонтраргументы: {bru}"}]
    ).choices[0].message.content

    # Этап 4: Контролер (CeADAR Compliance) [cite: 2026-01-07]
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

# --- ИНТЕРФЕЙС ПЛАТФОРМЫ [cite: 2026-01-20] ---
# НОВОЕ НАЗВАНИЕ В КОНФИГУРАЦИИ
st.set_page_config(page_title="Цифровая платформа по верификации юридической документации", layout="wide")

# Боковая панель
with st.sidebar:
    st.title("⚖️ Legal Verification")
    st.info("Глобальная цель: Платформа юридических услуг на двух континентах [cite: 2026-01-20]")
    st.write("---")
    st.success("Статус: CeADAR Certified [cite: 2026-01-07]")
    st.caption("Архитектура: 4-4-4 Buran")

# Главный заголовок страницы
st.title("⚖️ Цифровая платформа по верификации юридической документации")

user_instruction = st.text_area("Задание для системы:", value="Подготовить жалобу по факту незаконного увольнения", height=100)
uploaded_files = st.file_uploader("Загрузите юридические документы (PDF):", type=["pdf"], accept_multiple_files=True)

# ГЛАВНЫЙ РЫЧАГ УПРАВЛЕНИЯ
if st.button("👑 ПОЛУЧИТЬ ЮРИДИЧЕСКИЙ ВЕРДИКТ"):
    if not user_instruction:
        st.error("Пожалуйста, введите задание!")
    else:
        with st.spinner("Интеллектуальный контур проводит верификацию..."):
            combined_text = ""
            if uploaded_files:
                for f in uploaded_files:
                    combined_text += f"\n--- {f.name} ---\n" + extract_text_from_pdf(f)
            
            # Запуск конвейера цифровых двойников
            ana, bru, jur, con, judge = run_legal_factory(user_instruction, combined_text)
            
            # Визуализация работы штаба
            st.markdown("### 🧬 Протокол обработки данных")
            col1, col2 = st.columns(2)
            with col1:
                st.error(f"**Контур анализа рисков (Бруно):**\n{bru[:400]}...")
            with col2:
                st.warning(f"**Контур соответствия стандартам (CeADAR):**\n{con[:400]}...")

            st.markdown("---")
            st.header("⚖️ ОКОНЧАТЕЛЬНЫЙ ВЕРДИКТ СИСТЕМЫ")
            st.success(judge)

            # Генерация PDF
            try:
                pdf = LegalReport()
                pdf.add_page()
                pdf.set_font('helvetica', size=11)
                clean_text = judge.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(0, 10, txt=clean_text)
                pdf_output = pdf.output()
                
                st.download_button(
                    label="📥 СКАЧАТЬ ОФИЦИАЛЬНЫЙ ВЕРДИКТ",
                    data=pdf_output,
                    file_name="Legal_Verdict_Final.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Ошибка формирования PDF: {e}")

st.write("---")
st.caption("© 2026 Irish Shepherd. Проприетарный протокол верификации юридических данных.")
