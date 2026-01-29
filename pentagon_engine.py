import streamlit as st
import os
from openai import OpenAI
import fitz  # PyMuPDF
from fpdf import FPDF
import uuid

# --- CONFIGURATION (DeepSeek Engine) [cite: 2026-01-20, 2026-01-28] ---
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = "sk-ffce960a76d040d29031825ad4c4428c"

client = OpenAI(
    api_key=api_key, 
    base_url="https://api.deepseek.com/v1"
)

# --- PDF GENERATOR SETUP (fpdf2 standards 2.7.6) [cite: 2026-01-28, 2026-01-29] ---
class LegalReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'IRISH SHEPHERD: OFFICIAL SUPREME VERDICT', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

def extract_text_from_pdf(uploaded_file):
    try:
        file_bytes = uploaded_file.read()
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = "".join([page.get_text() for page in doc])
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# --- 4-4-4 BURAN CHAIN (ANGLO-IRISH LOGIC) [cite: 2025-12-23, 2026-01-20] ---
def run_legal_factory(user_task, full_context):
    # Stage 1: Analyst [cite: 2026-01-05]
    ana = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "You are a Professional Legal Analyst in Ireland. Extract key facts. Respond strictly in English."},
                  {"role": "user", "content": f"Task: {user_task}\n\nDocument Context: {full_context}"}]
    ).choices[0].message.content

    # Stage 2: Bruno (Opponent) [cite: 2025-12-23]
    bru = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "You are Bruno, the Adversary. Find legal weaknesses. Respond strictly in English."},
                  {"role": "user", "content": ana}]
    ).choices[0].message.content

    # Stage 3: Jurist (Irish Law Focus) [cite: 2026-01-20]
    jur = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "You are an Irish Solicitor. Apply the Unfair Dismissals Act 1977. Respond strictly in English."},
                  {"role": "user", "content": f"Facts: {ana}\n\nCounter-arguments: {bru}"}]
    ).choices[0].message.content

    # Stage 4: Controller (CeADAR Ethics) [cite: 2026-01-07]
    con = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "You are the CeADAR Ethics Controller. Verify logic and AI transparency. Respond strictly in English."},
                  {"role": "user", "content": f"Legal Position: {jur}"}]
    ).choices[0].message.content

    # Stage 5: Supreme Judge [cite: 2026-01-20]
    judge = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "You are the Supreme Judge. Issue a final unique determination. Respond strictly in English."},
                  {"role": "user", "content": f"Analysis: {ana}\nRisks: {bru}\nLaw: {jur}\nAudit: {con}"}]
    ).choices[0].message.content
    
    return ana, bru, jur, con, judge

# --- INTERFACE [cite: 2026-01-20] ---
st.set_page_config(page_title="Irish Shepherd OS", layout="wide")
st.title("🐺 Irish Shepherd OS: Global Legal Platform")

st.sidebar.markdown("### 🌍 Expansion Goal")
st.sidebar.info("Two Continents Platform. No human staff. CeADAR Certified [cite: 2026-01-07, 2026-01-20].")

user_instruction = st.text_area("Legal Task/Instruction (In English):", value="Analyze unfair dismissal claim based on the provided document.", height=100)
uploaded_files = st.file_uploader("Upload Legal Cases (PDF):", type=["pdf"], accept_multiple_files=True)

if st.button("👑 SUPREME JUDGE VERDICT"):
    if not user_instruction:
        st.error("Please enter a task!")
    elif not uploaded_files:
        st.error("Please upload at least one PDF!")
    else:
        with st.spinner("Pentagon System is reaching a final verdict..."):
            combined_text = "" # RESET CONTEXT [cite: 2026-01-06]
            for f in uploaded_files:
                combined_text += f"\n--- FILENAME: {f.name} ---\n" + extract_text_from_pdf(f)
            
            ana, bru, jur, con, judge = run_legal_factory(user_instruction, combined_text)
            
            st.markdown("### 🧬 Digital Intelligence Flow")
            c1, c2 = st.columns(2)
            with c1:
                st.error(f"**Agent 2 (Bruno - Opponent):**\n\n{bru}")
            with c2:
                st.warning(f"**Agent 4 (CeADAR Controller):**\n\n{con}")

            st.markdown("---")
            st.header("⚖️ SUPREME JUDGE FINAL DETERMINATION")
            st.success(judge)

            # PDF GENERATION (Modern fpdf2 syntax) [cite: 2026-01-29]
            try:
                pdf = LegalReport()
                pdf.add_page()
                pdf.set_font('Arial', size=11)
                
                case_id = str(uuid.uuid4())[:8].upper()
                pdf.cell(0, 10, f"Case ID: {case_id}", new_x="LMARGIN", new_y="NEXT")
                pdf.cell(0, 10, f"Timestamp: 2026-01-29", new_x="LMARGIN", new_y="NEXT")
                pdf.ln(5)
                
                # ASCII encoding to avoid encoding errors with standard fonts
                clean_text = judge.encode('ascii', 'ignore').decode('ascii')
                pdf.multi_cell(0, 10, text=clean_text)
                
                # FINAL FIX: Convert result to bytes for st.download_button [cite: 2026-01-29]
                pdf_output = bytes(pdf.output())
                
                st.download_button(
                    label="📥 DOWNLOAD OFFICIAL VERDICT (PDF)",
                    data=pdf_output,
                    file_name=f"Verdict_{case_id}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"PDF Generation Error: {e}")
                
   
