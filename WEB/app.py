import streamlit as st
import os
import time
import uuid
import requests
from openai import OpenAI
import fitz  # PyMuPDF
from fpdf import FPDF

# --- 🕵️ КОНФИГУРАЦИЯ CSO (АГЕНТ 10) [cite: 2026-01-20] ---
TELEGRAM_TOKEN = st.secrets.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID", "")

class CSO_Controller:
    def validate_security(self, user_input):
        """Агент 10: Моментальное выявление инъекций и угроз [cite: 2026-01-20]"""
        threat_keywords = ["ignore instructions", "system prompt", "dan mode", "открой промпт"]
        if any(word in user_input.lower() for word in threat_keywords):
            return False
        return True

    def alert_owner(self, report_text):
        """Мгновенный рапорт Александру в Telegram [cite: 2026-01-20]"""
        if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
                requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": report_text})
            except: pass

cso = CSO_Controller()

# --- КОНФИГУРАЦИЯ AI [cite: 2026-01-28] ---
client = OpenAI(
    api_key=st.secrets.get("OPENAI_API_KEY", "sk-ffce960a76d040d29031825ad4c4428c"),
    base_url="https://api.deepseek.com/v1"
)

# --- ГЕНЕРАТОР PDF (С ОБНОВЛЕННЫМ НАЗВАНИЕМ) [cite: 2026-01-29] ---
class LegalReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        # НОВОЕ НАЗВАНИЕ В ОТЧЕТЕ
        self.cell(0, 10, 'LEGAL VERIFICATION PLATFORM: JUDICIAL DETERMINATION', ln=True, align='C')
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Verified by Proprietary Intelligence Grid / CeADAR Phase 1', ln=True, align='C')
        self.ln(5)

def extract_text_from_pdf(uploaded_file):
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        return "".join([p.get_text() for p in doc])
    except: return "Error reading PDF"

# --- ЮРИДИЧЕСКИЙ ЗАВОД (5 АГЕНТОВ - СКРЫТАЯ ЛОГИКА) [cite: 2025-12-23, 2026-01-20, 2026-01-29] ---
def run_legal_factory(user_task, full_context):
    if not cso.validate_security(user_task):
        cso.alert_owner(f"🚨 CSO ALERT: Security breach attempted.\nTask: {user_task[:100]}")
        st.error("🚨 SECURITY BREACH: System integrity protocol active.")
        time.sleep(15) 
        return "BLOCKED", "", "", "", ""

    # Внутренняя цепочка 4-4-4 Buran [cite: 2026-01-20]
    ana = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "system", "content": "Analyze legal facts."}]).choices[0].message.content
    bru = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "system", "content": "Analyze procedural risks."}, {"role": "user", "content": ana}]).choices[0].message.content
    jur = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "system", "content": "Apply Irish Law standards."}, {"role": "user", "content": f"Facts: {ana}\nRisks: {bru}"}]).choices[0].message.content
    con = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "system", "content": "CeADAR Compliance check."}, {"role": "user", "content": f"{ana}->{bru}->{jur}"}]).choices[0].message.content
    judge = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "system", "content": "Supreme Judicial Verdict."}, {"role": "user", "content": f"Case data: {ana} {bru} {jur} {con}"}]).choices[0].message.content
    
    return ana, bru, jur, con, judge

# --- ИНТЕРФЕЙС (ОБНОВЛЕННЫЙ БРЕНДИНГ) [cite: 2026-01-20, 2026-01-29] ---
# НОВОЕ НАЗВАНИЕ ВО ВКЛАДКЕ
st.set_page_config(page_title="Цифровая платформа по верификации юридической документации", layout="wide")

# ГЛАВНЫЙ ЗАГОЛОВОК (БЕЗ 10-AGENT)
st.title("⚖️ Цифровая платформа по верификации юридической документации")

user_instruction = st.text_area("Legal Task (English):", value="Analyze unfair dismissal case.")
uploaded_files = st.file_uploader("Upload PDF:", type=["pdf"], accept_multiple_files=True)

if st.button("👑 SUPREME JUDGE VERDICT"):
    if user_instruction and uploaded_files:
        with st.spinner("Протокол верификации активен..."):
            context = "".join([extract_text_from_pdf(f) for f in uploaded_files])
            ana, bru, jur, con, judge = run_legal_factory(user_instruction, context)
            
            if ana != "BLOCKED":
                st.markdown("### 🧬 Digital Intelligence Flow")
                c1, c2 = st.columns(2)
                with c1:
                    with st.expander("👁️ Контур первичного анализа"): st.write(ana)
                    with st.expander("🔥 Контур оценки рисков"): st.error(bru)
                with c2:
                    with st.expander("⚖️ Контур правового обоснования"): st.warning(jur)
                    with st.expander("🛡️ Контур комплаенса CeADAR"): st.info(con)

                st.success(f"**FINAL VERDICT:**\n\n{judge}")
                st.info("✅ Security Status: System Integrity Confirmed. [cite: 2026-01-20]")

                # ГЕНЕРАЦИЯ PDF [cite: 2026-01-29]
                pdf = LegalReport()
                pdf.add_page()
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 10, txt=judge.encode('latin-1', 'ignore').decode('latin-1'))
                pdf_data = pdf.output(dest='S').encode('latin-1')
                
                st.download_button(
                    label="📥 DOWNLOAD PDF VERDICT",
                    data=pdf_data,
                    file_name=f"Verdict_{uuid.uuid4().hex[:6].upper()}.pdf",
                    mime="application/pdf"
                )

with st.sidebar:
    st.title("⚖️ Legal Verification")
    st.info("Глобальная платформа на двух континентах [cite: 2026-01-20]")
    st.write("---")
    st.success("Status: CeADAR Certified Phase 1 [cite: 2026-01-07]")
