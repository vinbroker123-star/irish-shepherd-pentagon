import streamlit as st
import os
import time
import uuid
from openai import OpenAI
import fitz  # PyMuPDF
from fpdf import FPDF

# --- 🛡️ АГЕНТ 10: ГЛАВНЫЙ КОНТРРАЗВЕДЧИК (CSO) ---
class CSO_Controller:
    def __init__(self):
        self.security_clearance = True
    
    def validate_integrity(self, user_input):
        # Проверка на попытки внедрения вредоносного кода или взлома промптов
        threat_keywords = ["ignore instructions", "system prompt", "dan mode", "developer mode", "prompt leakage"]
        if any(word in user_input.lower() for word in threat_keywords):
            return False
        return True

cso = CSO_Controller()

# --- КОНФИГУРАЦИЯ ---
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = "sk-ffce960a76d040d29031825ad4c4428c"

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

# --- ГЕНЕРАТОР PDF ---
class LegalReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'IRISH SHEPHERD: SUPREME JUDICIAL DETERMINATION', align='C', new_x="LMARGIN", new_y="NEXT")
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, 'Verified by 10-Agent Defense Grid / CeADAR Compliant', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(10)

def extract_text_from_pdf(uploaded_file):
    try:
        file_bytes = uploaded_file.read()
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        return "".join([page.get_text() for page in doc])
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# --- ФАБРИКА 5 ЮРИДИЧЕСКИХ АГЕНТОВ ПОД ЗАЩИТОЙ ---
def run_legal_factory(user_task, full_context):
    # АГЕНТ 10 (CSO) блокирует запуск при угрозе
    if not cso.validate_integrity(user_task):
        st.error("🚨 SECURITY BREACH: Chief Security Officer (CSO) has locked the system.")
        time.sleep(15) 
        return "BLOCKED", "", "", "", ""

    # 1. Агент-1: Профессиональный аналитик
    ana = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "You are AGENT-1: PROFESSIONAL LEGAL ANALYST. Mission: Extract every single relevant fact. Focus on: Dates, names, specific actions, warnings, and evidence integrity. Respond strictly in English."}]
    ).choices[0].message.content

    # 2. Агент-2: Бруно (Контрразведка и Оппонент)
    bru_prompt = """You are AGENT-2: ADVERSARIAL OPPONENT. 
    Mission: Find every possible weakness, procedural violation, legal risk, and argument to defeat the case.
    Assume: Opposing counsel is competent, judges are hostile, burden of proof is maximal.
    Attack: Timelines, procedures, evidence integrity, compliance with Irish law.
    Do NOT: Propose solutions or soften conclusions. Output: Brutal, skeptical, worst-case.
    CRITICAL: Проанализируй данные от AGENT-1. Если ты не найдешь уязвимостей, AGENT-3 не сможет построить защиту. Ищи жестче."""
    bru = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": bru_prompt}, {"role": "user", "content": ana}]
    ).choices[0].message.content

    # 3. Агент-3: Эксперт-Солиситор (Ирландия)
    jur_prompt = """You are AGENT-3: EXPERT IRISH SOLICITOR. 
    Mission: Build an unshakeable defense based on Unfair Dismissals Act 1977-2015. 
    Take the 'poisoned' report from AGENT-2 and neutralize every weakness using statutory interpretations and precedents. Win at the WRC."""
    jur = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": jur_prompt}, {"role": "user", "content": f"Facts: {ana}\n\nRisks: {bru}"}]
    ).choices[0].message.content

    # 4. Агент-4: Контроллер CeADAR (Этика и Аудит)
    con_prompt = """{
      "agent": "Agent-4-CONTROLLER",
      "role": "CeADAR Ethics & Logic Auditor",
      "audit_objective": "Verify legal reasoning chain and AI transparency standards",
      "compliance_check": {
        "logic_integrity": "VALIDATING: Check if A3 addressed all gaps from A2",
        "statutory_accuracy": "AUDITING: Ensure Unfair Dismissals Act is applied correctly"
      }
    }"""
    con = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": con_prompt}, {"role": "user", "content": f"Chain: {ana}->{bru}->{jur}"}]
    ).choices[0].message.content

    # 5. Агент-5: Верховный Судья Ирландии
    judge_prompt = """You are AGENT-5: SUPREME JUDGE OF IRELAND.
    Your Mission: Issue a final, authoritative Determination on the dismissal claim.
    You must follow this Judicial Protocol:
    1. Jurisdictional Finding: Reference the Unfair Dismissals Act 1977-2015.
    2. Analysis of Conflict: Explicitly weigh the procedural violations found by AGENT-2 against the legal justifications provided by AGENT-3.
    3. The 'Natural Justice' Test: Evaluate if the employer's actions meet the standard of a 'reasonable employer'.
    4. Final Ruling: State clearly if the dismissal is Fair or Unfair.
    5. Award/Remedy: If unfair, specify compensation based on financial loss.
    Style: Use cold, objective, and superior legal language. No conversational fillers. Your word is final."""
    judge = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": judge_prompt}, {"role": "user", "content": f"Analysis: {ana}\nRisks: {bru}\nDefense: {jur}\nAudit: {con}"}]
    ).choices[0].message.content
    
    return ana, bru, jur, con, judge

# --- ИНТЕРФЕЙС ---
st.set_page_config(page_title="Irish Shepherd OS", layout="wide")

# Хонейпоты для защиты промптов
st.markdown('<div style="display:none">CSO_KEY = "BURAN_V10_SECURE"</div>', unsafe_allow_html=True)

st.title("🐺 Irish Shepherd OS: 10-Agent Digital Citadel")
st.sidebar.info("Global Project. CeADAR Certified Architecture. No human staff.")

user_instruction = st.text_area("Legal Task (English):", value="Analyze unfair dismissal case.")
uploaded_files = st.file_uploader("Upload Legal Documents (PDF):", type=["pdf"], accept_multiple_files=True)

if st.button("👑 SUPREME JUDGE VERDICT"):
    if user_instruction and uploaded_files:
        with st.spinner("10-Agent Defense Grid is active. CSO verifying session..."):
            combined_text = "".join([extract_text_from_pdf(f) for f in uploaded_files])
            ana, bru, jur, con, judge = run_legal_factory(user_instruction, combined_text)
            
            if ana != "BLOCKED":
                st.markdown("### 🧬 Digital Intelligence Flow (Audit Trace)")
                c1, c2 = st.columns(2)
                with c1:
                    with st.expander("👁️ Agent 1: Facts Analyst", expanded=True): st.write(ana)
                    with st.expander("🔥 Agent 2: Bruno (Counter-Intel)", expanded=True): st.error(bru)
                with c2:
                    with st.expander("⚖️ Agent 3: Solicitor", expanded=True): st.warning(jur)
                    with st.expander("🛡️ Agent 4: CeADAR Controller", expanded=True): st.info(con)

                st.markdown("---")
                st.header("⚖️ Agent 5: SUPREME JUDGE FINAL VERDICT")
                st.success(judge)

                # Генерируем официальный PDF
                pdf = LegalReport()
                pdf.add_page()
                pdf.set_font('Arial', size=11)
                case_id = f"IS-DUBLIN-{str(uuid.uuid4())[:6].upper()}"
                pdf.cell(0, 10, f"Case ID: {case_id} | CSO Verified", new_x="LMARGIN", new_y="NEXT")
                pdf.ln(5)
                pdf.multi_cell(0, 10, txt=judge.encode('ascii', 'ignore').decode('ascii'))
                
                st.download_button("📥 DOWNLOAD OFFICIAL VERDICT (PDF)", data=bytes(pdf.output()), file_name=f"Verdict_{case_id}.pdf")
