#!/usr/bin/env python3
"""
PDF to Markdown Converter
Converts PDF files to markdown format while preserving structure and formatting.
"""

import pdfplumber
import re
import sys
import os
from pathlib import Path

def clean_text(text):
    """Clean and format text for markdown"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Handle common special characters
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    
    return text

def extract_text_with_formatting(pdf_path):
    """Extract text from PDF with basic formatting detection"""
    markdown_content = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            markdown_content.append(f"# DM4340 减速电机技术文档\n\n")
            markdown_content.append(f"*文档页数: {total_pages}*\n\n")
            markdown_content.append("---\n\n")
            
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract text
                text = page.extract_text()
                if text:
                    # Clean the text
                    cleaned_text = clean_text(text)
                    
                    # Add page header
                    markdown_content.append(f"## 第 {page_num} 页\n\n")
                    
                    # Split into paragraphs and format
                    paragraphs = cleaned_text.split('\n\n')
                    for paragraph in paragraphs:
                        if paragraph.strip():
                            # Check if it might be a heading (all caps, shorter text)
                            if len(paragraph.strip()) < 100 and paragraph.strip().isupper():
                                markdown_content.append(f"### {paragraph.strip()}\n\n")
                            else:
                                markdown_content.append(f"{paragraph.strip()}\n\n")
                    
                    markdown_content.append("---\n\n")
                
                # Extract tables if present
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        if table and any(any(cell for cell in row if cell) for row in table):
                            markdown_content.append("### 表格数据\n\n")
                            markdown_content.append("| " + " | ".join(str(cell) if cell else "" for cell in table[0]) + " |\n")
                            markdown_content.append("| " + " | ".join("---" for _ in table[0]) + " |\n")
                            for row in table[1:]:
                                markdown_content.append("| " + " | ".join(str(cell) if cell else "" for cell in row) + " |\n")
                            markdown_content.append("\n")
    
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None
    
    return "".join(markdown_content)

def pdf_to_markdown(pdf_path, output_path=None):
    """Convert PDF to markdown file"""
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file '{pdf_path}' not found.")
        return False
    
    # Generate output path if not provided
    if output_path is None:
        pdf_name = Path(pdf_path).stem
        output_path = f"{pdf_name}.md"
    
    # Extract content
    markdown_content = extract_text_with_formatting(pdf_path)
    
    if markdown_content is None:
        return False
    
    # Write to file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"Successfully converted '{pdf_path}' to '{output_path}'")
        return True
    except Exception as e:
        print(f"Error writing markdown file: {e}")
        return False

if __name__ == "__main__":
    pdf_path = "2D图纸/DM4340 减速电机20240116.PDF"
    output_path = "DM4340_减速电机技术文档.md"
    
    success = pdf_to_markdown(pdf_path, output_path)
    if success:
        print("Conversion completed successfully!")
    else:
        print("Conversion failed!") 