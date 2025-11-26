Legacy Code Documentation Agent 📄

🤖An AI-powered tool designed to automatically generate professional, readable documentation from legacy code files. Built with Python and Streamlit, this agent understands complex logic in SQL, Python, C++, and DAX and converts it into structured Markdown reports and PDF documents.

🚀 FeaturesMulti-Language Support: Analyzes Python, SQL, C++, and DAX files.Streamlit 

Web Interface: User-friendly drag-and-drop UI for single files or batch processing.PDF 

Export: Automatically converts generated documentation into formatted PDFs.Batch Processing: Point the agent at a folder to document every file inside it automatically.Cost & Token 

Tracking: Logs every run to run_history.xlsx (Excel) and .jsonl to track API costs and token usage.Domain 

Awareness: Optimized for IT contexts (Credit Unions, Finance, Data Warehousing).

🛠️ InstallationClone the repository:git clone [https://github.com/Robby-Burns/LegacyCodeDocumentAgent.git](https://github.com/Robby-Burns/LegacyCodeDocumentAgent.git)
cd LegacyCodeDocumentAgent
Create a virtual environment (Recommended):python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:pip install -r requirements.txt
Set up your API Key:Create a .env file in the root directory.Add your OpenAI (or compatible provider) key:OPENAI_API_KEY=sk-your-key-here

▶️ UsageRun the Web InterfaceTo launch the interactive dashboard:streamlit run streamlit_app.py
Run via Command Line (Optional)If you prefer using the terminal without the UI:# Process a single file
python main.py sample_files/monthly_revenue_report.sql --pdf

# Process an entire folder
python main.py ./my_legacy_code_folder --pdf

# View run history
python main.py --history
## 📂 Project Structure

* `app.py`: The main Streamlit web interface.
* `main.py`: Command-line interface and batch processing logic.
* `agent.py`: Core logic for interacting with the AI model.
* `prompts.py`: Stores the system prompts and AI instructions.
* `pdf_exporter.py`: Handles conversion of Markdown to PDF.
* `run_logger.py`: Manages logging to Excel and JSONL.
* `file_handler.py`: Utilities for reading code files.
* `sample_files/`: Contains legacy code examples for testing.
* `output/`: Generated Markdown and PDF files are saved here.
