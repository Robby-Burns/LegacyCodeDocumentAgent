"""
PDF Export module for the Legacy Code Documentation Agent.
Converts Markdown documentation to professional PDF reports.
"""

import os
import re
from fpdf import FPDF


class DocumentationPDF(FPDF):
    """Custom PDF class with header and footer."""

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        """Add header to each page."""
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(100, 100, 100)
        # Use effective page width for consistent alignment
        self.cell(0, 10, "Legacy Code Documentation Agent", align="L")
        self.ln(5)
        self.set_draw_color(40, 116, 166)
        # Dynamic line width based on margins
        self.line(self.l_margin, 18, self.w - self.r_margin, 18)
        self.ln(10)

    def footer(self):
        """Add footer with page numbers."""
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def sanitize_text(text: str) -> str:
    """
    Sanitize text to be compatible with Latin-1 (Standard PDF Fonts).
    Replaces unsupported characters (like smart quotes or emojis) to prevent rendering errors.
    """
    # Replace common incompatible characters manually
    replacements = {
        '\u2018': "'", '\u2019': "'",  # Smart quotes
        '\u201c': '"', '\u201d': '"',  # Smart double quotes
        '\u2013': '-', '\u2014': '-',  # Dashes
        '\u2026': '...',  # Ellipsis
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    # robust fallback: encode to latin-1, replacing errors with '?'
    return text.encode('latin-1', 'replace').decode('latin-1')


def clean_markdown(text: str) -> str:
    """Remove Markdown formatting for plain text output."""
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '[CODE BLOCK]', text)
    # Remove inline code
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Remove bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    # Remove italic
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    # Remove headers markdown but keep text
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # Remove horizontal rules
    text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)
    # Remove link formatting
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

    return text


def markdown_to_pdf(markdown_content: str, output_path: str) -> dict:
    """
    Convert Markdown content to a styled PDF.
    """
    result = {
        "success": False,
        "output_path": output_path,
        "error": None
    }

    try:
        pdf = DocumentationPDF()
        pdf.alias_nb_pages()
        pdf.add_page()

        # Calculate Effective Page Width (EPW)
        # Use getattr for compatibility, fallback to calculation if .epw missing
        epw = getattr(pdf, 'epw', pdf.w - 2 * pdf.l_margin)

        # Process the markdown line by line
        lines = markdown_content.split('\n')

        for line in lines:
            # Sanitize line for Latin-1 compatibility
            stripped = sanitize_text(line.strip())

            # Skip empty lines
            if not stripped:
                pdf.ln(3)
                continue

            # Main title (# Header)
            if stripped.startswith('# ') and not stripped.startswith('## '):
                pdf.set_font("Helvetica", "B", 18)
                pdf.set_text_color(26, 82, 118)
                title = stripped[2:]
                pdf.multi_cell(epw, 10, title)  # changed 0 to epw
                pdf.ln(2)
                pdf.set_draw_color(26, 82, 118)
                pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
                pdf.ln(5)
                continue

            # Section headers (## Header)
            if stripped.startswith('## '):
                pdf.ln(5)
                pdf.set_font("Helvetica", "B", 14)
                pdf.set_text_color(40, 116, 166)
                header = stripped[3:]
                pdf.multi_cell(epw, 8, header)  # changed 0 to epw
                pdf.ln(2)
                continue

            # Subsection headers (### Header)
            if stripped.startswith('### '):
                pdf.ln(3)
                pdf.set_font("Helvetica", "B", 12)
                pdf.set_text_color(46, 134, 193)
                header = stripped[4:]
                pdf.multi_cell(epw, 7, header)  # changed 0 to epw
                pdf.ln(1)
                continue

            # Italic text (generated timestamp)
            if stripped.startswith('*') and stripped.endswith('*') and not stripped.startswith('**'):
                pdf.set_font("Helvetica", "I", 10)
                pdf.set_text_color(100, 100, 100)
                text = stripped.strip('*')
                pdf.multi_cell(epw, 6, text)  # changed 0 to epw
                pdf.ln(2)
                continue

            # Horizontal rule
            if stripped.startswith('---'):
                pdf.ln(3)
                pdf.set_draw_color(200, 200, 200)
                pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
                pdf.ln(5)
                continue

            # Bullet points
            if stripped.startswith('- ') or stripped.startswith('* '):
                pdf.set_font("Helvetica", "", 11)
                pdf.set_text_color(51, 51, 51)
                text = "   - " + clean_markdown(stripped[2:])
                pdf.multi_cell(epw, 6, text)  # changed 0 to epw
                continue

            # Table rows - skip separator rows and format data rows
            if '|' in stripped:
                cells = [c.strip() for c in stripped.split('|')]
                cells = [c for c in cells if c]  # Remove empty cells

                # Skip separator rows (|---|---|)
                if cells and all(set(c) <= {'-', ':', ' '} for c in cells):
                    continue

                # Format each cell with length limit
                formatted_cells = []
                for cell in cells:
                    clean_cell = clean_markdown(cell)
                    if len(clean_cell) > 40:
                        clean_cell = clean_cell[:37] + "..."
                    formatted_cells.append(clean_cell)

                # Output as text
                pdf.set_font("Helvetica", "", 9)
                pdf.set_text_color(51, 51, 51)
                row_text = " | ".join(formatted_cells)
                pdf.multi_cell(epw, 5, row_text)  # changed 0 to epw
                continue

            # Regular paragraph
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(51, 51, 51)
            text = clean_markdown(stripped)
            pdf.multi_cell(epw, 6, text)  # changed 0 to epw

        # Save the PDF
        pdf.output(output_path)
        result["success"] = True

    except Exception as e:
        result["error"] = f"PDF generation error: {str(e)}"

    return result


def convert_md_file_to_pdf(md_filepath: str, pdf_filepath: str = None) -> dict:
    """
    Read a Markdown file and convert it to PDF.
    """
    result = {
        "success": False,
        "output_path": None,
        "error": None
    }

    if not os.path.exists(md_filepath):
        result["error"] = f"File not found: {md_filepath}"
        return result

    if pdf_filepath is None:
        pdf_filepath = md_filepath.replace(".md", ".pdf")

    result["output_path"] = pdf_filepath

    try:
        with open(md_filepath, "r", encoding="utf-8") as f:
            markdown_content = f.read()

        pdf_result = markdown_to_pdf(markdown_content, pdf_filepath)

        if pdf_result["success"]:
            result["success"] = True
        else:
            result["error"] = pdf_result["error"]

    except Exception as e:
        result["error"] = f"Error reading file: {str(e)}"

    return result