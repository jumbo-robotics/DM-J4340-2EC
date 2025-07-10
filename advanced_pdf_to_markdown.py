#!/usr/bin/env python3
"""
Advanced PDF to Markdown Converter
Converts PDF files to markdown format with improved formatting and structure detection.
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
    
    # Remove excessive whitespace but preserve line breaks
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    # Handle common special characters
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    
    return text.strip()

def detect_heading(text, font_sizes=None):
    """Detect if text might be a heading based on content and formatting"""
    if not text or len(text.strip()) < 2:
        return False
    
    # Check for common heading patterns
    text_upper = text.strip().upper()
    
    # All caps text is likely a heading
    if text_upper == text.strip() and len(text.strip()) < 50:
        return True
    
    # Check for numbered headings
    if re.match(r'^\d+\.?\s+[A-Z]', text.strip()):
        return True
    
    # Check for common heading keywords
    heading_keywords = ['规格', '参数', '技术', '尺寸', '说明', '要求', '标准', '型号', '名称']
    for keyword in heading_keywords:
        if keyword in text:
            return True
    
    return False

def format_table(table_data):
    """Format table data as markdown table"""
    if not table_data or not any(any(cell for cell in row if cell) for row in table_data):
        return ""
    
    # Filter out empty rows
    filtered_table = []
    for row in table_data:
        if any(cell for cell in row if cell):
            filtered_table.append(row)
    
    if not filtered_table:
        return ""
    
    markdown_table = []
    
    # Create header
    header = "| " + " | ".join(str(cell) if cell else "" for cell in filtered_table[0]) + " |"
    markdown_table.append(header)
    
    # Create separator
    separator = "| " + " | ".join("---" for _ in filtered_table[0]) + " |"
    markdown_table.append(separator)
    
    # Add data rows
    for row in filtered_table[1:]:
        row_text = "| " + " | ".join(str(cell) if cell else "" for cell in row) + " |"
        markdown_table.append(row_text)
    
    return "\n".join(markdown_table)

def extract_text_with_advanced_formatting(pdf_path):
    """Extract text from PDF with advanced formatting detection"""
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
                            # Check if it might be a heading
                            if detect_heading(paragraph.strip()):
                                markdown_content.append(f"### {paragraph.strip()}\n\n")
                            else:
                                markdown_content.append(f"{paragraph.strip()}\n\n")
                    
                    markdown_content.append("---\n\n")
                
                # Extract tables if present
                tables = page.extract_tables()
                if tables:
                    for i, table in enumerate(tables):
                        if table and any(any(cell for cell in row if cell) for row in table):
                            markdown_content.append(f"### 表格 {i+1}\n\n")
                            table_markdown = format_table(table)
                            if table_markdown:
                                markdown_content.append(table_markdown)
                                markdown_content.append("\n\n")
    
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None
    
    return "".join(markdown_content)

def pdf_to_markdown_advanced(pdf_path, output_path=None):
    """Convert PDF to markdown file with advanced formatting"""
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file '{pdf_path}' not found.")
        return False
    
    # Generate output path if not provided
    if output_path is None:
        pdf_name = Path(pdf_path).stem
        output_path = f"{pdf_name}_advanced.md"
    
    # Extract content
    markdown_content = extract_text_with_advanced_formatting(pdf_path)
    
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
    output_path = "DM4340_减速电机技术文档_advanced.md"
    
    success = pdf_to_markdown_advanced(pdf_path, output_path)
    if success:
        print("Advanced conversion completed successfully!")
    else:
        print("Advanced conversion failed!") 