"""
Legacy Code Documentation Agent - Streamlit Web Interface
A user-friendly UI for generating documentation from legacy code.
"""

import streamlit as st
import os
import tempfile
from datetime import datetime

# Import local modules
from file_handler import read_code_file, EXTENSION_MAP, get_code_files_from_folder
from agent import generate_documentation
from pdf_exporter import markdown_to_pdf
from run_logger import log_run, get_summary

# Configuration
SAMPLE_DIR = "sample_files"
OUTPUT_DIR = "output"

# Page configuration
st.set_page_config(
    page_title="Legacy Code Documentation Agent",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1a5276;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2874a6;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if "documentation" not in st.session_state:
        st.session_state.documentation = None
    if "doc_result" not in st.session_state:
        st.session_state.doc_result = None
    if "file_info" not in st.session_state:
        st.session_state.file_info = None
    if "selected_sample" not in st.session_state:
        st.session_state.selected_sample = None


def save_uploaded_file(uploaded_file) -> str:
    """Save uploaded file to temp directory and return path."""
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def generate_pdf_bytes(markdown_content: str) -> bytes:
    """Generate PDF and return as bytes for download."""
    temp_dir = tempfile.mkdtemp()
    pdf_path = os.path.join(temp_dir, "documentation.pdf")

    result = markdown_to_pdf(markdown_content, pdf_path)

    if result["success"]:
        with open(pdf_path, "rb") as f:
            return f.read()
    return None


def display_metrics():
    """Display run history metrics in the sidebar."""
    summary = get_summary()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Usage Statistics")

    col1, col2 = st.sidebar.columns(2)
    col1.metric("Total Runs", summary["total_runs"])

    success_rate = 0
    if summary["total_runs"] > 0:
        success_rate = (summary['successful_runs'] / summary['total_runs']) * 100

    col2.metric("Success Rate", f"{success_rate:.0f}%")

    st.sidebar.metric("Total Cost", f"${summary['total_cost_usd']:.4f}")

    if summary["by_language"]:
        st.sidebar.markdown("#### By Language:")
        for lang, data in summary["by_language"].items():
            st.sidebar.text(f"  {lang}: {data['count']} files")


def get_sample_files():
    """Get list of files from sample directory."""
    if not os.path.exists(SAMPLE_DIR):
        return []
    return [f for f in os.listdir(SAMPLE_DIR) if os.path.isfile(os.path.join(SAMPLE_DIR, f))]


def process_single_file_ui(file_result: dict, include_pdf: bool) -> dict:
    """Process a single file and return the result."""
    doc_result = generate_documentation(
        filename=file_result["filename"],
        language=file_result["language"],
        code_content=file_result["content"]
    )

    if not doc_result["success"]:
        log_run(
            filename=file_result["filename"],
            language=file_result["language"],
            model=doc_result.get("model_used", "Unknown"),
            input_tokens=0,
            output_tokens=0,
            cost=0.0,
            output_path="",
            success=False,
            error=doc_result["error"]
        )
        return doc_result

    # Build full markdown
    full_content = f"# Documentation: {file_result['filename']}\n\n"
    full_content += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    full_content += "---\n\n"
    full_content += doc_result["documentation"]

    doc_result["full_content"] = full_content

    # Log successful run
    log_run(
        filename=file_result["filename"],
        language=file_result["language"],
        model=doc_result["model_used"],
        input_tokens=doc_result["usage"]["input_tokens"],
        output_tokens=doc_result["usage"]["output_tokens"],
        cost=doc_result["usage"]["estimated_cost"],
        output_path="streamlit_ui",
        pdf_path="streamlit_ui" if include_pdf else None,
        success=True
    )

    return doc_result


def main():
    """Main Streamlit application."""
    init_session_state()

    # Header
    st.markdown('<p class="main-header">📄 Legacy Code Documentation Agent</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Generate professional documentation from your legacy code files</p>',
                unsafe_allow_html=True)

    # --- SIDEBAR ---
    st.sidebar.image("https://img.icons8.com/color/96/000000/source-code.png", width=80)

    # 1. Quick Start (Sample Files)
    st.sidebar.markdown("### 🚀 Quick Start")
    sample_files = get_sample_files()
    if sample_files:
        selected_sample = st.sidebar.selectbox(
            "Load a sample file:",
            [""] + sample_files,
            index=0
        )
        if selected_sample:
            st.session_state.selected_sample = os.path.join(SAMPLE_DIR, selected_sample)
        else:
            st.session_state.selected_sample = None
    else:
        st.sidebar.info(f"Create a '{SAMPLE_DIR}' folder to add samples.")

    st.sidebar.markdown("---")

    # 2. Settings / Info
    st.sidebar.markdown("### Settings")
    supported_types = list(EXTENSION_MAP.keys())
    st.sidebar.markdown("**Supported Files:**")
    st.sidebar.markdown(", ".join([f"`{ext}`" for ext in supported_types]))

    # 3. Metrics
    display_metrics()

    # --- MAIN CONTENT ---
    tab1, tab2, tab3 = st.tabs(["📤 Generate Documentation", "📜 View History", "ℹ️ About"])

    with tab1:
        st.markdown("### Select Source Code")

        # Choose input mode
        input_mode = st.radio(
            "Choose input method:",
            ["📄 Single File", "📁 Batch Folder"],
            horizontal=True
        )

        st.markdown("---")

        if input_mode == "📄 Single File":
            # --- SINGLE FILE MODE ---
            uploaded_file = st.file_uploader(
                "Upload a file",
                type=[ext.replace(".", "") for ext in supported_types],
                label_visibility="collapsed"
            )

            target_path = None
            target_filename = None

            if uploaded_file:
                target_path = save_uploaded_file(uploaded_file)
                target_filename = uploaded_file.name
                st.info(f"📂 Using uploaded file: **{target_filename}**")
            elif st.session_state.selected_sample:
                target_path = st.session_state.selected_sample
                target_filename = os.path.basename(target_path)
                st.info(f"🧪 Using sample file: **{target_filename}**")
            else:
                st.info("👆 Upload a file above OR select a sample from the sidebar to begin.")

            if target_path:
                file_result = read_code_file(target_path)

                if file_result["success"]:
                    with st.expander("👀 View Source Code Preview", expanded=False):
                        st.code(file_result["content"], language=file_result["language"].lower())

                    col1, col2, col3 = st.columns([1, 1, 2])

                    with col1:
                        generate_btn = st.button("🚀 Generate Documentation", type="primary", use_container_width=True)

                    with col2:
                        include_pdf = st.checkbox("Include PDF", value=True)

                    if generate_btn:
                        st.session_state.file_info = file_result

                        with st.spinner("🤖 AI is analyzing your code... (this may take 15-30 seconds)"):
                            doc_result = process_single_file_ui(file_result, include_pdf)

                        if not doc_result["success"]:
                            st.error(f"❌ Error generating documentation: {doc_result['error']}")
                        else:
                            st.session_state.doc_result = doc_result
                            st.session_state.documentation = doc_result["full_content"]
                            st.success("✅ Documentation generated successfully!")
                else:
                    st.error(f"❌ Error reading file: {file_result['error']}")

                # Display results if available
                if st.session_state.documentation and st.session_state.file_info:
                    st.markdown("---")
                    st.markdown("### 📋 Generated Documentation")

                    if st.session_state.doc_result:
                        usage = st.session_state.doc_result["usage"]
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Model", st.session_state.doc_result["model_used"])
                        col2.metric("Input Tokens", f"{usage['input_tokens']:,}")
                        col3.metric("Output Tokens", f"{usage['output_tokens']:,}")
                        col4.metric("Cost", f"${usage['estimated_cost']:.4f}")

                    st.markdown("#### Download Options:")
                    d_col1, d_col2, d_col3 = st.columns([1, 1, 2])

                    with d_col1:
                        st.download_button(
                            label="📥 Download Markdown",
                            data=st.session_state.documentation,
                            file_name=f"{st.session_state.file_info['filename']}_documentation.md",
                            mime="text/markdown",
                            use_container_width=True
                        )

                    with d_col2:
                        with st.spinner("Preparing PDF..."):
                            pdf_bytes = generate_pdf_bytes(st.session_state.documentation)

                        if pdf_bytes:
                            st.download_button(
                                label="📥 Download PDF",
                                data=pdf_bytes,
                                file_name=f"{st.session_state.file_info['filename']}_documentation.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                        else:
                            st.warning("PDF generation failed")

                    st.markdown("#### Preview:")
                    with st.container():
                        st.markdown(st.session_state.documentation)

        else:
            # --- BATCH FOLDER MODE ---
            st.markdown("### 📁 Batch Process Folder")
            st.info("Enter a folder path to process all supported code files at once.")

            folder_path = st.text_input(
                "Folder path:",
                placeholder=r"C:\Projects\SQL_Scripts  or  ./test_code",
                help="Enter the full path to a folder containing code files"
            )

            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                batch_btn = st.button("🚀 Process All Files", type="primary", use_container_width=True)

            with col2:
                batch_pdf = st.checkbox("Include PDFs", value=True, key="batch_pdf")

            if batch_btn:
                if not folder_path:
                    st.warning("⚠️ Please enter a folder path.")
                elif not os.path.isdir(folder_path):
                    st.error(f"❌ Folder not found: {folder_path}")
                else:
                    files = get_code_files_from_folder(folder_path)

                    if not files:
                        st.warning("⚠️ No supported code files found in this folder.")
                        st.info(f"Supported extensions: {', '.join(supported_types)}")
                    else:
                        st.success(f"📁 Found **{len(files)}** code file(s) to process")

                        with st.expander("📋 Files to process", expanded=False):
                            for f in files:
                                st.text(f"  • {os.path.basename(f)}")

                        # Progress tracking
                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        # Stats
                        stats = {
                            "processed": 0,
                            "succeeded": 0,
                            "failed": 0,
                            "total_input_tokens": 0,
                            "total_output_tokens": 0,
                            "total_cost": 0.0
                        }

                        results_container = st.container()

                        # Ensure output directory exists
                        os.makedirs(OUTPUT_DIR, exist_ok=True)

                        for i, filepath in enumerate(files):
                            filename = os.path.basename(filepath)
                            status_text.text(f"🤖 Processing: {filename} ({i + 1}/{len(files)})")

                            file_result = read_code_file(filepath)

                            if not file_result["success"]:
                                with results_container:
                                    st.error(f"❌ {filename}: {file_result['error']}")
                                stats["failed"] += 1
                            else:
                                doc_result = generate_documentation(
                                    filename=file_result["filename"],
                                    language=file_result["language"],
                                    code_content=file_result["content"]
                                )

                                if not doc_result["success"]:
                                    with results_container:
                                        st.error(f"❌ {filename}: {doc_result['error']}")
                                    stats["failed"] += 1

                                    log_run(
                                        filename=filename,
                                        language=file_result["language"],
                                        model=doc_result.get("model_used", "Unknown"),
                                        input_tokens=0,
                                        output_tokens=0,
                                        cost=0.0,
                                        output_path="",
                                        success=False,
                                        error=doc_result["error"]
                                    )
                                else:
                                    # Build content
                                    full_content = f"# Documentation: {filename}\n\n"
                                    full_content += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
                                    full_content += "---\n\n"
                                    full_content += doc_result["documentation"]

                                    # Save files
                                    base_name = os.path.splitext(filename)[0]
                                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                                    md_path = os.path.join(OUTPUT_DIR, f"{base_name}_documentation_{timestamp}.md")
                                    with open(md_path, "w", encoding="utf-8") as f:
                                        f.write(full_content)

                                    pdf_path = None
                                    if batch_pdf:
                                        pdf_path = os.path.join(OUTPUT_DIR,
                                                                f"{base_name}_documentation_{timestamp}.pdf")
                                        markdown_to_pdf(full_content, pdf_path)

                                    # Update stats
                                    stats["succeeded"] += 1
                                    stats["total_input_tokens"] += doc_result["usage"]["input_tokens"]
                                    stats["total_output_tokens"] += doc_result["usage"]["output_tokens"]
                                    stats["total_cost"] += doc_result["usage"]["estimated_cost"]

                                    log_run(
                                        filename=filename,
                                        language=file_result["language"],
                                        model=doc_result["model_used"],
                                        input_tokens=doc_result["usage"]["input_tokens"],
                                        output_tokens=doc_result["usage"]["output_tokens"],
                                        cost=doc_result["usage"]["estimated_cost"],
                                        output_path=md_path,
                                        pdf_path=pdf_path,
                                        success=True
                                    )

                                    with results_container:
                                        st.success(f"✅ {filename} — ${doc_result['usage']['estimated_cost']:.4f}")

                            stats["processed"] += 1
                            progress_bar.progress((i + 1) / len(files))

                        status_text.text("✅ Batch processing complete!")

                        # Final summary
                        st.markdown("---")
                        st.markdown("### 📊 Batch Summary")

                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Processed", stats["processed"])
                        col2.metric("Succeeded", stats["succeeded"])
                        col3.metric("Failed", stats["failed"])
                        col4.metric("Total Cost", f"${stats['total_cost']:.4f}")

                        col1, col2 = st.columns(2)
                        col1.metric("Input Tokens", f"{stats['total_input_tokens']:,}")
                        col2.metric("Output Tokens", f"{stats['total_output_tokens']:,}")

                        st.info(f"📂 Output files saved to: `{os.path.abspath(OUTPUT_DIR)}`")

    with tab2:
        st.markdown("### 📜 Run History")

        summary = get_summary()

        if summary["total_runs"] == 0:
            st.info("No runs recorded yet. Generate some documentation to see history!")
        else:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Runs", summary["total_runs"])
            col2.metric("Successful", summary["successful_runs"])
            col3.metric("Failed", summary["failed_runs"])
            col4.metric("Total Cost", f"${summary['total_cost_usd']:.4f}")

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### By Language")
                for lang, data in summary["by_language"].items():
                    st.markdown(f"- **{lang}**: {data['count']} files (${data['cost']:.4f})")

            with col2:
                st.markdown("#### By Model")
                for model, data in summary["by_model"].items():
                    st.markdown(f"- **{model}**: {data['count']} runs (${data['cost']:.4f})")

            st.markdown("---")
            st.markdown("#### 📊 Excel Report")
            st.info("Full run history is available in `run_history.xlsx` in your project folder.")

    with tab3:
        st.markdown("### ℹ️ About This Tool")

        st.markdown("""
        **Legacy Code Documentation Agent** is an AI-powered tool that automatically 
        generates professional documentation from your legacy code files.

        #### Features:
        - 🔍 **Multi-language support**: SQL, Python, C++, DAX
        - 🏦 **Credit Union domain knowledge**: Understands Member, Loans, Shares terminology
        - 📊 **7-section reports**: Overview, Business Logic, Inputs, Outputs, Dependencies, Data Relationships, Best Practices
        - 📄 **Multiple formats**: Markdown and PDF export
        - 💰 **Cost tracking**: Monitor token usage and API costs
        - 📁 **Batch processing**: Process entire folders at once

        #### Supported File Types:
        """)

        for ext, lang in EXTENSION_MAP.items():
            st.markdown(f"- `{ext}` → {lang}")

        st.markdown("""
        ---
        *Built with ❤️ for Credit Union IT teams*
        """)


if __name__ == "__main__":
    main()