"""
Legacy Code Documentation Agent
Generates professional documentation from SQL, Python, C++, and DAX code files.
"""

import os
import sys
import argparse
from datetime import datetime

# Import local modules
from file_handler import read_code_file, get_code_files_from_folder
from agent import generate_documentation
from pdf_exporter import markdown_to_pdf
from run_logger import log_run, print_summary

# Configuration
OUTPUT_DIR = "output"


def ensure_output_directory():
    """Ensure the output directory exists to prevent write errors."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_documentation(filename: str, documentation: str, export_pdf: bool = False) -> dict:
    """
    Save the generated documentation to a markdown file and optionally PDF.
    """
    ensure_output_directory()

    # Create output filename based on original file
    base_name = os.path.splitext(os.path.basename(filename))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{base_name}_documentation_{timestamp}"

    md_path = os.path.join(OUTPUT_DIR, f"{output_filename}.md")
    pdf_path = os.path.join(OUTPUT_DIR, f"{output_filename}.pdf") if export_pdf else None

    # Build the full markdown content
    full_content = f"# Documentation: {filename}\n\n"
    full_content += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    full_content += "---\n\n"
    full_content += documentation

    # Save Markdown file
    try:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(full_content)
    except IOError as e:
        print(f"❌ Error writing file: {e}")
        return {"md_path": None, "pdf_path": None}

    # Save PDF if requested
    if export_pdf:
        print("   ⏳ Generating PDF...")
        pdf_result = markdown_to_pdf(full_content, pdf_path)
        if not pdf_result["success"]:
            print(f"   ⚠️  PDF error: {pdf_result['error']}")
            pdf_path = None

    return {"md_path": md_path, "pdf_path": pdf_path}


def process_single_file(filepath: str, export_pdf: bool = False) -> dict:
    """
    Process a single code file and generate documentation.
    """
    result = {"success": False, "usage": None}

    # Step 1: Read the file
    print(f"\n📄 Reading: {filepath}")
    file_result = read_code_file(filepath)

    if not file_result["success"]:
        print(f"❌ Error: {file_result['error']}")
        return result

    print(f"✅ Loaded: {file_result['filename']} ({file_result['language']})")

    # Step 2: Generate documentation
    print(f"🤖 Analyzing with AI...")

    doc_result = generate_documentation(
        filename=file_result["filename"],
        language=file_result["language"],
        code_content=file_result["content"]
    )

    if not doc_result["success"]:
        print(f"❌ Error: {doc_result['error']}")
        # Log failed run
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
        return result

    # Step 3: Save to file(s)
    output_paths = save_documentation(
        filename=file_result["filename"],
        documentation=doc_result["documentation"],
        export_pdf=export_pdf
    )

    if not output_paths["md_path"]:
        print(f"❌ Error: Failed to save output files.")
        return result

    print(f"✅ Saved: {output_paths['md_path']}")
    if output_paths["pdf_path"]:
        print(f"✅ PDF:   {output_paths['pdf_path']}")

    # Step 4: Show token usage
    usage = doc_result["usage"]
    print(f"   📊 Tokens: {usage['input_tokens']:,} in / {usage['output_tokens']:,} out")
    print(f"   💰 Cost: ${usage['estimated_cost']:.4f}")

    # Step 5: Log successful run
    log_run(
        filename=file_result["filename"],
        language=file_result["language"],
        model=doc_result["model_used"],
        input_tokens=usage["input_tokens"],
        output_tokens=usage["output_tokens"],
        cost=usage["estimated_cost"],
        output_path=output_paths["md_path"],
        pdf_path=output_paths["pdf_path"],
        success=True
    )

    result["success"] = True
    result["usage"] = usage
    return result


def process_folder(folder_path: str, export_pdf: bool = False) -> dict:
    """
    Process all supported code files in a folder.
    """
    stats = {
        "processed": 0,
        "succeeded": 0,
        "failed": 0,
        "total_input_tokens": 0,
        "total_output_tokens": 0,
        "total_cost": 0.0
    }

    # Get all supported files
    files = get_code_files_from_folder(folder_path)

    if not files:
        print(f"⚠️  No supported code files found in: {folder_path}")
        print("   Supported extensions: .sql, .py, .cpp, .h, .dax, .m")
        return stats

    print(f"📁 Found {len(files)} code file(s) to process:\n")
    for f in files:
        print(f"   • {os.path.basename(f)}")

    print("\n" + "-" * 40)

    # Process each file
    for filepath in files:
        stats["processed"] += 1
        result = process_single_file(filepath, export_pdf=export_pdf)

        if result["success"]:
            stats["succeeded"] += 1
            if result["usage"]:
                stats["total_input_tokens"] += result["usage"]["input_tokens"]
                stats["total_output_tokens"] += result["usage"]["output_tokens"]
                stats["total_cost"] += result["usage"]["estimated_cost"]
        else:
            stats["failed"] += 1

    return stats


def main():
    """Main entry point for the documentation agent."""

    parser = argparse.ArgumentParser(description="Legacy Code Documentation Agent")
    parser.add_argument("path", nargs="?", help="Path to file or folder to document")
    parser.add_argument("--pdf", action="store_true", help="Generate PDF output")
    parser.add_argument("--history", action="store_true", help="Show run history summary")

    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("   LEGACY CODE DOCUMENTATION AGENT")
    print("=" * 60)

    # Check for history flag first
    if args.history:
        print_summary()
        return

    # If no path provided and not asking for history, show help
    if not args.path:
        parser.print_help()
        return

    target_path = args.path

    # Determine if it's a file or folder
    if os.path.isfile(target_path):
        # Single file mode
        print(f"\n📄 Mode: Single File")
        if args.pdf:
            print("   📑 PDF export: Enabled")

        result = process_single_file(target_path, export_pdf=args.pdf)

        print("\n" + "=" * 60)
        print("   COMPLETE!" if result["success"] else "   FAILED!")
        print("=" * 60 + "\n")

    elif os.path.isdir(target_path):
        # Batch folder mode
        print(f"\n📁 Mode: Batch Processing")
        print(f"   Folder: {target_path}")
        if args.pdf:
            print("   📑 PDF export: Enabled")

        stats = process_folder(target_path, export_pdf=args.pdf)

        print("\n" + "=" * 60)
        print("   BATCH COMPLETE!")
        print("-" * 60)
        print(f"   Files processed: {stats['processed']}")
        print(f"   Succeeded:       {stats['succeeded']}")
        print(f"   Failed:          {stats['failed']}")
        print("-" * 60)
        print(f"   📊 Total tokens: {stats['total_input_tokens']:,} in / {stats['total_output_tokens']:,} out")
        print(f"   💰 Total cost:   ${stats['total_cost']:.4f}")
        print("=" * 60 + "\n")

    else:
        print(f"\n❌ Error: Path not found: {target_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()