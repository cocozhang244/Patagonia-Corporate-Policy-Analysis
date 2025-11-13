#!/usr/bin/env python3
"""
Patagonia ESG Analysis - PDF Text Extraction with Page Number Tracking
Author: Analysis Team
Date: November 13, 2025
Purpose: Extract text from all Patagonia reports while preserving page numbers for citation
"""

import os
import json
import re
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

try:
    import PyPDF2
    import pdfplumber
    from pathlib import Path
    import pandas as pd
except ImportError as e:
    print(f"Missing required library: {e}")
    print("Installing required packages...")
    os.system("pip install -q PyPDF2 pdfplumber pandas openpyxl")
    import PyPDF2
    import pdfplumber
    from pathlib import Path
    import pandas as pd


class PatagoniaTextExtractor:
    """Extract text from Patagonia PDFs with precise page number tracking"""

    def __init__(self, output_dir="extracted_data"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.extraction_log = []

    def extract_with_pdfplumber(self, pdf_path: str) -> List[Dict]:
        """
        Extract text using pdfplumber (better for complex layouts)
        Returns: List of dicts with page_number, text, and metadata
        """
        pages_data = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                print(f"  Processing {total_pages} pages...")

                for page_num, page in enumerate(pdf.pages, start=1):
                    try:
                        # Extract text
                        text = page.extract_text() or ""

                        # Extract tables if present
                        tables = page.extract_tables()

                        # Get page dimensions
                        width = page.width
                        height = page.height

                        page_data = {
                            'page_number': page_num,
                            'text': text.strip(),
                            'char_count': len(text),
                            'word_count': len(text.split()),
                            'has_tables': len(tables) > 0,
                            'table_count': len(tables),
                            'tables': tables if tables else [],
                            'page_width': width,
                            'page_height': height
                        }

                        pages_data.append(page_data)

                        if page_num % 10 == 0:
                            print(f"    Processed {page_num}/{total_pages} pages...")

                    except Exception as e:
                        print(f"    Warning: Error on page {page_num}: {str(e)}")
                        pages_data.append({
                            'page_number': page_num,
                            'text': '',
                            'error': str(e)
                        })

        except Exception as e:
            print(f"  Error opening PDF: {str(e)}")
            return []

        return pages_data

    def extract_with_pypdf2(self, pdf_path: str) -> List[Dict]:
        """
        Fallback extraction using PyPDF2
        Returns: List of dicts with page_number and text
        """
        pages_data = []

        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                total_pages = len(reader.pages)
                print(f"  Processing {total_pages} pages with PyPDF2...")

                for page_num in range(total_pages):
                    try:
                        page = reader.pages[page_num]
                        text = page.extract_text() or ""

                        page_data = {
                            'page_number': page_num + 1,
                            'text': text.strip(),
                            'char_count': len(text),
                            'word_count': len(text.split())
                        }

                        pages_data.append(page_data)

                    except Exception as e:
                        print(f"    Warning: Error on page {page_num + 1}: {str(e)}")
                        pages_data.append({
                            'page_number': page_num + 1,
                            'text': '',
                            'error': str(e)
                        })

        except Exception as e:
            print(f"  Error with PyPDF2: {str(e)}")
            return []

        return pages_data

    def process_pdf(self, pdf_path: str, doc_year: str, doc_type: str) -> Dict:
        """
        Process a single PDF file and extract all content
        """
        filename = os.path.basename(pdf_path)
        print(f"\nProcessing: {filename}")
        print(f"  Year: {doc_year}, Type: {doc_type}")

        # Try pdfplumber first (more robust)
        pages_data = self.extract_with_pdfplumber(pdf_path)

        # Fallback to PyPDF2 if pdfplumber fails
        if not pages_data:
            print("  Trying alternative extraction method...")
            pages_data = self.extract_with_pypdf2(pdf_path)

        if not pages_data:
            print(f"  ERROR: Failed to extract any content from {filename}")
            return None

        # Calculate statistics
        total_chars = sum(p.get('char_count', 0) for p in pages_data)
        total_words = sum(p.get('word_count', 0) for p in pages_data)
        pages_with_content = sum(1 for p in pages_data if p.get('text', ''))

        document_data = {
            'filename': filename,
            'filepath': pdf_path,
            'year': doc_year,
            'document_type': doc_type,
            'total_pages': len(pages_data),
            'pages_with_content': pages_with_content,
            'total_characters': total_chars,
            'total_words': total_words,
            'pages': pages_data
        }

        print(f"  ✓ Extracted {len(pages_data)} pages, {total_words:,} words")

        # Save individual document JSON
        safe_filename = filename.replace('.pdf', '').replace(' ', '_')
        json_path = os.path.join(self.output_dir, f"{safe_filename}_{doc_year}_extracted.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(document_data, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Saved to: {json_path}")

        # Save as plain text with page markers
        txt_path = os.path.join(self.output_dir, f"{safe_filename}_{doc_year}_text.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(f"DOCUMENT: {filename}\n")
            f.write(f"YEAR: {doc_year}\n")
            f.write(f"TYPE: {doc_type}\n")
            f.write(f"TOTAL PAGES: {len(pages_data)}\n")
            f.write("=" * 80 + "\n\n")

            for page in pages_data:
                f.write(f"\n{'='*80}\n")
                f.write(f"PAGE {page['page_number']}\n")
                f.write(f"{'='*80}\n\n")
                f.write(page.get('text', '[No text extracted]'))
                f.write("\n\n")
        print(f"  ✓ Saved text to: {txt_path}")

        self.extraction_log.append({
            'filename': filename,
            'year': doc_year,
            'type': doc_type,
            'status': 'success',
            'pages': len(pages_data),
            'words': total_words
        })

        return document_data

    def create_master_index(self, all_documents: List[Dict]):
        """Create a master index of all extracted documents"""

        index_data = []

        for doc in all_documents:
            if doc is None:
                continue

            for page in doc['pages']:
                index_data.append({
                    'document': doc['filename'],
                    'year': doc['year'],
                    'document_type': doc['document_type'],
                    'page_number': page['page_number'],
                    'word_count': page.get('word_count', 0),
                    'has_tables': page.get('has_tables', False),
                    'text_preview': page.get('text', '')[:200] + '...' if len(page.get('text', '')) > 200 else page.get('text', '')
                })

        # Save as CSV
        df = pd.DataFrame(index_data)
        csv_path = os.path.join(self.output_dir, "MASTER_PAGE_INDEX.csv")
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"\n✓ Master index saved to: {csv_path}")
        print(f"  Total entries: {len(df)}")

        # Save as Excel with formatting
        excel_path = os.path.join(self.output_dir, "MASTER_PAGE_INDEX.xlsx")
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Page Index', index=False)

            # Summary sheet
            summary_df = df.groupby(['year', 'document_type']).agg({
                'page_number': 'count',
                'word_count': 'sum'
            }).reset_index()
            summary_df.columns = ['Year', 'Document Type', 'Total Pages', 'Total Words']
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

        print(f"✓ Master index Excel saved to: {excel_path}")

        return df

    def save_extraction_log(self):
        """Save extraction process log"""
        log_path = os.path.join(self.output_dir, "extraction_log.json")
        with open(log_path, 'w') as f:
            json.dump(self.extraction_log, f, indent=2)
        print(f"\n✓ Extraction log saved to: {log_path}")


def main():
    """Main extraction process"""

    print("="*80)
    print("PATAGONIA ESG ANALYSIS - TEXT EXTRACTION WITH PAGE TRACKING")
    print("="*80)

    # Initialize extractor
    extractor = PatagoniaTextExtractor(output_dir="extracted_data")

    # Define all documents to process
    documents = [
        # Extracted from zip files
        {
            'path': 'extracted_reports/Patagonia 2021 Disclosures/PAT_2020_BCorp_Report-REV-100125.pdf',
            'year': '2020',
            'type': 'BCorp Report'
        },
        {
            'path': 'extracted_reports/Patagonia 2022 Disclosures/PAT_2021_BCorp_Report-REV-100125.pdf',
            'year': '2021',
            'type': 'BCorp Report'
        },
        {
            'path': 'extracted_reports/Patagonia 2021 Disclosures/PAT_2021_LegalDocuments-ModernSlaveryAct-012423.pdf',
            'year': '2021',
            'type': 'Modern Slavery Act'
        },
        {
            'path': 'extracted_reports/Patagonia 2024 Disclosures/PAT_2024_BCorp_Report-V2-100125.pdf',
            'year': '2024',
            'type': 'BCorp Report'
        },
        {
            'path': 'extracted_reports/Patagonia 2024 Disclosures/PAT_2024_LegalDocuments-ModernSlaveryAct-060324.pdf',
            'year': '2024',
            'type': 'Modern Slavery Act'
        },
        # 2025 reports
        {
            'path': 'Patagonia 2025 pt1.pdf',
            'year': '2025',
            'type': 'Annual Report Part 1'
        },
        {
            'path': 'Patagonia 2025 pt2.pdf',
            'year': '2025',
            'type': 'Annual Report Part 2'
        },
        {
            'path': 'Patagonia 2025 pt3.pdf',
            'year': '2025',
            'type': 'Annual Report Part 3'
        },
        {
            'path': 'Patagonia 2025 pt4.pdf',
            'year': '2025',
            'type': 'Annual Report Part 4'
        },
        {
            'path': 'Patagonia 2025 pt5.pdf',
            'year': '2025',
            'type': 'Annual Report Part 5'
        },
        {
            'path': 'Patagonia pt6.pdf',
            'year': '2025',
            'type': 'Annual Report Part 6'
        }
    ]

    # Process all documents
    all_documents = []
    for doc_info in documents:
        if os.path.exists(doc_info['path']):
            doc_data = extractor.process_pdf(
                doc_info['path'],
                doc_info['year'],
                doc_info['type']
            )
            if doc_data:
                all_documents.append(doc_data)
        else:
            print(f"\n⚠ WARNING: File not found: {doc_info['path']}")
            extractor.extraction_log.append({
                'filename': os.path.basename(doc_info['path']),
                'year': doc_info['year'],
                'type': doc_info['type'],
                'status': 'file_not_found'
            })

    # Create master index
    print("\n" + "="*80)
    print("CREATING MASTER INDEX")
    print("="*80)
    extractor.create_master_index(all_documents)

    # Save log
    extractor.save_extraction_log()

    # Print summary
    print("\n" + "="*80)
    print("EXTRACTION COMPLETE")
    print("="*80)
    print(f"Documents processed: {len(all_documents)}")
    print(f"Total pages extracted: {sum(doc['total_pages'] for doc in all_documents)}")
    print(f"Total words extracted: {sum(doc['total_words'] for doc in all_documents):,}")
    print(f"\nOutput directory: {extractor.output_dir}/")
    print("\nGenerated files:")
    print("  - Individual JSON files for each document")
    print("  - Individual TXT files for each document")
    print("  - MASTER_PAGE_INDEX.csv (searchable page index)")
    print("  - MASTER_PAGE_INDEX.xlsx (Excel with summary)")
    print("  - extraction_log.json (process log)")
    print("="*80)


if __name__ == "__main__":
    main()
