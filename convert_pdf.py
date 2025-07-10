#!/usr/bin/env python3
"""
Simple PDF to Markdown Converter
Usage: python convert_pdf.py <input_pdf> [output_md]
"""

import pdfplumber
import re
import sys
import os
from pathlib import Path

def pdf_to_markdown_simple(pdf_path, output_path=None):
    """Simple PDF to markdown conversion"""
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file '{pdf_path}' not found.")
        return False
    
    # Generate output path if not provided
    if output_path is None:
        pdf_name = Path(pdf_path).stem
        output_path = f"{pdf_name}.md"
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            markdown_content = []
            markdown_content.append(f"# {Path(pdf_path).stem}\n\n")
            markdown_content.append(f"*Converted from PDF - {len(pdf.pages)} pages*\n\n")
            markdown_content.append("---\n\n")
            
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    markdown_content.append(f"## Page {page_num}\n\n")
                    markdown_content.append(f"{text.strip()}\n\n")
                    markdown_content.append("---\n\n")
                
                # Add tables if present
                tables = page.extract_tables()
                if tables:
                    for i, table in enumerate(tables):
                        if table and any(any(cell for cell in row if cell) for row in table):
                            markdown_content.append(f"### Table {i+1}\n\n")
                            # Simple table formatting
                            for row in table:
                                if any(cell for cell in row if cell):
                                    row_text = "| " + " | ".join(str(cell) if cell else "" for cell in row) + " |"
                                    markdown_content.append(row_text + "\n")
                            markdown_content.append("\n")
            
            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("".join(markdown_content))
            
            print(f"Successfully converted '{pdf_path}' to '{output_path}'")
            return True
            
    except Exception as e:
        print(f"Error converting PDF: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_pdf.py <input_pdf> [output_md]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = pdf_to_markdown_simple(pdf_path, output_path)
    if success:
        print("Conversion completed successfully!")
    else:
        print("Conversion failed!")
        sys.exit(1) 