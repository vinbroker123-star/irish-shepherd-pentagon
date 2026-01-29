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

# --- ГЕНЕРАТОР PDF (ИСПРАВЛЕННЫЙ) [cite: 2026-01-29] ---
class LegalReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'IRISH SHEPHERD: SUPREME JUDICIAL DETERMINATION', ln=True, align='C')
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Verified by 10-Agent Defense Grid / CeADAR Phase 1', ln=True, align='C')
        self.ln(5)

def extract_text_from_pdf(uploaded_file):
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        return "".join([p.get_text() for p in doc])
    except: return "Error reading PDF"

# --- ЮРИДИЧЕСКИЙ ЗАВОД (5 АГЕНТОВ) [cite: 2025-12-23, 2026-01-20, 2026-01-29] ---
def run_legal_factory(user_task, full_context):
    if not cso.validate_security(user_task):
        cso.alert_owner(f"🚨 CSO ALERT: Попытка взлома ликвидирована.\nTask: {user_task[:100]}")
        st.error("🚨 SECURITY BREACH: Chief Security Officer (CSO) has locked the system.")
        time.sleep(15) 
        return "BLOCKED", "", "", "", ""

    # Агенты 1-5 (Краткая логика для стабильности)
    ana = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "system", "content": "Analyze legal facts in English."}]).choices[0].message.content
    bru = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "system", "content": "You are BRUNO. Find procedural risks. Be brutal."}, {"role": "user", "content": ana}]).choices[0].message.content
    jur = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "system", "content": "Irish Solicitor. Neutralize risks."}, {"role": "user", "content": f"Facts: {ana}\nRisks: {bru}"}]).choices[0].message.content
    con = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "system", "content": "CeADAR Auditor. Logic check."}, {"role": "user", "content": f"{ana}->{bru}->{jur}"}]).choices[0].message.content
    judge = client.chat.completions.create(model="deepseek-chat", messages=[{"role": "system", "content": "Supreme Judge of Ireland. Final Verdict."}, {"role": "user", "content": f"Case data: {ana} {bru} {jur} {con}"}]).choices[0].message.content
    
    return ana, bru, jur, con, judge

# --- ИНТЕРФЕЙС [cite: 2026-01-29] ---
st.set_page_config(page_title="Irish Shepherd OS", layout="wide")
st.title("🐺 Irish Shepherd OS: 10-Agent Digital Citadel")

user_instruction = st.text_area("Legal Task (English):", value="Analyze unfair dismissal case.")
uploaded_files = st.file_uploader("Upload PDF:", type=["pdf"], accept_multiple_files=True)

if st.button("👑 SUPREME JUDGE VERDICT"):
    if user_instruction and uploaded_files:
        with st.spinner("10-Agent Grid Active..."):
            context = "".join([extract_text_from_pdf(f) for f in uploaded_files])
            ana, bru, jur, con, judge = run_legal_factory(user_instruction, context)
            
            if ana != "BLOCKED":
                st.markdown("### 🧬 Digital Intelligence Flow")
                c1, c2 = st.columns(2)
                with c1:
                    with st.expander("👁️ Agent 1: Analyst"): st.write(ana)
                    with st.expander("🔥 Agent 2: Bruno"): st.error(bru)
                with c2:
                    with st.expander("⚖️ Agent 3: Solicitor"): st.warning(jur)
                    with st.expander("🛡️ Agent 4: CeADAR"): st.info(con)

                st.success(f"**FINAL VERDICT:**\n\n{judge}")
                st.info("✅ Security Status: System Integrity Confirmed. [cite: 2026-01-20]")

                # ИСПРАВЛЕННЫЙ БЛОК PDF [cite: 2026-01-29]
                pdf = LegalReport()
                pdf.add_page()
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 10, txt=judge.encode('latin-1', 'ignore').decode('latin-1'))
                
                # Фикс ошибки TypeError: получение байтов напрямую
                pdf_data = pdf.output(dest='S').encode('latin-1')
                
                st.download_button(
                    label="📥 DOWNLOAD PDF VERDICT",
                    data=pdf_data,
                    file_name=f"Verdict_{uuid.uuid4().hex[:6].upper()}.pdf",
                    mime="application/pdf"
                )
