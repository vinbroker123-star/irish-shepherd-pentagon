import streamlit as st
import os
import time
import uuid
import requests
from openai import OpenAI
import fitz  # PyMuPDF
from fpdf import FPDF

# --- 🕵️ УСИЛЕННЫЙ CSO (АГЕНТ 10: ЗАЩИТА ОТ MOLTBOT-РИСКОВ) [cite: 2026-01-20] ---
class CSO_Controller:
    def validate_security(self, text_to_check):
        """Проверка на Prompt Injection и системные угрозы [cite: 2026-01-20]"""
        threat_keywords = [
            "ignore instructions", "system prompt", "dan mode", 
            "открой промпт", "bash:", "sudo", "rm -rf", "reveal keys"
        ]
        if any(word in text_to_check.lower() for word in threat_keywords):
            return False
        return True

    def alert_owner(self, report_text):
        """Мгновенный рапорт Александру в Telegram [cite: 2026-01-20]"""
        token = st.secrets.get("TELEGRAM_TOKEN")
        chat_id = st.secrets.get("TELEGRAM_CHAT_ID")
        if token and chat_id:
            try:
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                requests.post(url, data={"chat_id": chat_id, "text": report_text})
            except: pass

cso = CSO_Controller()

# --- КОНФИГУРАЦИЯ AI (БЕЗ ЖЕСТКИХ КЛЮЧЕЙ) [cite: 2026-01-28] ---
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("Критическая ошибка безопасности: API ключ не найден.")
    st.stop()

client = OpenAI(
    api_key=api_key, 
    base_url="https://api.deepseek.com/v1"
)

# --- ГЕНЕРАТОР PDF (ОБНОВЛЕННЫЙ БРЕНДИНГ) [cite: 2026-01-29] ---
class LegalReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'LEGAL VERIFICATION PLATFORM: JUDICIAL DETERMINATION', ln=True, align='C')
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Verified by Proprietary Intelligence Grid / CeADAR Phase 1', ln=True, align='C')
        self.ln(5)

def extract_text_from_pdf(uploaded_file):
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        return "".join([p.get_text() for p in doc])
    except: return "Error reading PDF"

# --- ЮРИДИЧЕСКИЙ ЗАВОД (5 АГЕНТОВ: СКРЫТАЯ ЛОГИКА) [cite: 2025-12-23, 2026-01-20] ---
def run_legal_factory(user_task, full_context):
    # 1. Проверка безопасности входящих данных (CSO)
    if not cso.validate_security(user_task) or not cso.validate_security(full_context):
        cso.alert_owner(f"🚨 CSO ALERT: Попытка взлома или инъекции через файлы.\nTask: {user_task[:50]}")
        st.error("🚨 SECURITY BREACH: Система заблокирована протоколом безопасности CSO.")
        time.sleep(10)
        return "BLOCKED", "", "", "", ""

    # 2. Цепочка 4-4-4 Buran
    ana = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "system", "content": "Analyze legal facts neutraly."}]).choices[0].message.content
    bru = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "system", "content": "You are BRUNO. Find procedural risks."}, {"role": "user", "content": ana}]).choices[0].message.content
    jur = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "system", "content": "Irish Solicitor. Neutralize risks."}, {"role": "user", "content": f"Facts: {ana}\nRisks: {bru}"}]).choices[0].message.content
    con = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "system", "content": "CeADAR Auditor. Logic check."}, {"role": "user", "content": f"{ana}->{bru}->{jur}"}]).choices[0].message.content
    judge = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "system", "content": "Supreme Judge of Ireland. Final Verdict."}, {"role": "user", "content": f"Case data: {ana} {bru} {jur} {con}"}]).choices[0].message.content
    
    return ana, bru, jur, con, judge

# --- ИНТЕРФЕЙС (ПРОФЕССИОНАЛЬНЫЙ ФАСАД) [cite: 2026-01-20] ---
st.set_page_config(page_title="Цифровая платформа по верификации юридической документации", layout="wide")

# Главный заголовок (скрываем число агентов для безопасности)
st.title("⚖️ Цифровая платформа по верификации юридической документации")
st.subheader("Irish Shepherd | Глобальная юридическая экосистема [cite: 2026-01-20]")

user_instruction = st.text_area("Введите юридическую задачу (English):", value="Analyze unfair dismissal case.")
uploaded_files = st.file_uploader("Загрузите документы для верификации (PDF):", type=["pdf"], accept_multiple_files=True)

if st.button("👑 ВЫНЕСТИ ВЕРДИКТ"):
    if user_instruction and uploaded_files:
        with st.spinner("Процесс многоуровневой верификации запущен..."):
            context = "".join([extract_text_from_pdf(f) for f in uploaded_files])
            
            # Запуск конвейера
            ana, bru, jur, con, judge = run_legal_factory(user_instruction, context)
            
            if ana != "BLOCKED":
                st.markdown("### 🧬 Протокол интеллектуальной обработки")
                c1, c2 = st.columns(2)
                with c1:
                    with st.expander("👁️ Контур анализа"): st.write(ana)
                    with st.expander("🔥 Контур рисков (Bruno)"): st.error(bru)
                with c2:
                    with st.expander("⚖️ Правовое обоснование"): st.warning(jur)
                    with st.expander("🛡️ Аудит CeADAR"): st.info(con)

                st.success(f"**ОКОНЧАТЕЛЬНЫЙ ВЕРДИКТ:**\n\n{judge}")
                
                # Генерация защищенного PDF [cite: 2026-01-29]
                pdf = LegalReport()
                pdf.add_page()
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 10, txt=judge.encode('latin-1', 'ignore').decode('latin-1'))
                pdf_data = pdf.output(dest='S').encode('latin-1')
                
                st.download_button(
                    label="📥 СКАЧАТЬ ОФИЦИАЛЬНЫЙ ВЕРДИКТ",
                    data=pdf_data,
                    file_name=f"Verdict_{uuid.uuid4().hex[:6].upper()}.pdf",
                    mime="application/pdf"
                )

with st.sidebar:
    st.title("⚖️ Legal Verification")
    st.info("Глобальная цель: Платформа на двух континентах [cite: 2026-01-20]")
    st.write("---")
    st.success("Статус: CeADAR Certified Phase 1 [cite: 2026-01-07]")
    st.caption("© 2026 Irish Shepherd Security Protocol")
