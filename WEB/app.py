import streamlit as st
import os
from openai import OpenAI
import fitz  # PyMuPDF
from fpdf import FPDF

# --- КОНФИГУРАЦИЯ (DeepSeek Engine через Secrets) [cite: 2026-01-28] ---
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = "sk-ffce960a76d040d29031825ad4c4428c"

client = OpenAI(
    api_key=api_key, 
    base_url="https://api.deepseek.com/v1"
)

class LegalReport(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 12)
        # НОВОЕ НАЗВАНИЕ В PDF
        self.cell(0, 10, 'Legal Verification Platform: Final Decision', 0, 1, 'C')

def extract_text_from_pdf(uploaded_file):
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        return "".join([page.get_text() for page in doc])
    except Exception as e:
        return f"Ошибка чтения: {str(e)}"

# --- ЦЕПОЧКА 4-4-4 BURAN (ЛОГИКА СОХРАНЕНА) [cite: 2026-01-20] ---
def run_legal_factory(user_task, full_context):
    # Этап 1: Аналитик
    ana = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "Этап 1: Ты Аналитик. Собери все факты и даты нарушения."},
                  {"role": "user", "content": f"Задание: {user_task}\nКонтекст: {full_context[:40000]}"}]
    ).choices[0].message.content

    # Этап 2: Бруно (Adversary) [cite: 2025-12-23]
    bru = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "Этап 2: Ты Оппонент. Найди слабые места в позиции."},
                  {"role": "user", "content": ana}]
    ).choices[0].message.content

    # Этап 3: Юрист
    jur = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "Этап 3: Ты Юрист. Обоснуй позицию по закону."},
                  {"role": "user", "content": f"Факты: {ana}\nКонтраргументы: {bru}"}]
    ).choices[0].message.content

    # Этап 4: Контролер (CeADAR) [cite: 2026-01-07]
    con = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "Этап 4: Ты Контролер. Проверь логику системы."},
                  {"role": "user", "content": f"Юридическая позиция: {jur}"}]
    ).choices[0].message.content

    # Этап 5: Верховный Судья [cite: 2026-01-20]
    judge = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "Этап 5: Ты Верховный Судья. Вынеси ОКОНЧАТЕЛЬНЫЙ ВЕРДИКТ."},
                  {"role": "user", "content": f"Анализ: {ana}\nРиски: {bru}\nЗакон: {jur}\nАудит: {con}"}]
    ).choices[0].message.content
    
    return ana, bru, jur, con, judge

# --- ИНТЕРФЕЙС ОБНОВЛЕННОЙ ПЛАТФОРМЫ ---
# НОВОЕ НАЗВАНИЕ ЗДЕСЬ
st.set_page_config(page_title="Цифровая платформа по верификации юридической документации", layout="wide")

with st.sidebar:
    st.title("⚖️ Legal Verification")
    st.info("Глобальная платформа юридических услуг [cite: 2026-01-20]")
    st.write("---")
    st.success("Статус: CeADAR Certified [cite: 2026-01-07]")

st.title("⚖️ Цифровая платформа по верификации юридической документации")

user_instruction = st.text_area("Задание для верификации:", value="Подготовить жалобу по факту незаконного увольнения", height=100)
uploaded_files = st.file_uploader("Загрузите юридические документы (PDF):", type=["pdf"], accept_multiple_files=True)

if st.button("👑 ПОЛУЧИТЬ ЮРИДИЧЕСКИЙ ВЕРДИКТ"):
    if not user_instruction:
        st.error("Пожалуйста, введите задание!")
    else:
        with st.spinner("Интеллектуальный контур проводит верификацию..."):
            combined_text = ""
            if uploaded_files:
                for f in uploaded_files:
                    combined_text += f"\n--- {f.name} ---\n" + extract_text_from_pdf(f)
            
            # Запуск конвейера (10 агентов работают внутри этой функции скрытно)
            ana, bru, jur, con, judge = run_legal_factory(user_instruction, combined_text)
            
            st.markdown("### 🧬 Протокол обработки данных")
            col1, col2 = st.columns(2)
            with col1:
                st.error(f"**Контур анализа рисков:**\n{bru[:400]}...")
            with col2:
                st.warning(f"**Контур соответствия стандартам:**\n{con[:400]}...")

            st.markdown("---")
            st.header("⚖️ ОКОНЧАТЕЛЬНЫЙ ВЕРДИКТ СИСТЕМЫ")
            st.success(judge)

            # PDF генерация
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
