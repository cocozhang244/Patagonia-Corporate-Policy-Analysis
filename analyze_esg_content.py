#!/usr/bin/env python3
"""
Patagonia ESG Analysis - Targeted Content Extraction
Author: Analysis Team
Date: November 13, 2025
Purpose: Extract ESG-specific content with page references for all analysis dimensions
"""

import os
import json
import re
from typing import Dict, List, Set
import warnings
warnings.filterwarnings('ignore')

try:
    import pandas as pd
    import numpy as np
    from collections import defaultdict, Counter
except ImportError as e:
    print(f"Installing required packages...")
    os.system("pip install -q pandas numpy")
    import pandas as pd
    import numpy as np
    from collections import defaultdict, Counter


class ESGContentAnalyzer:
    """Analyze extracted text for ESG policy response indicators"""

    def __init__(self, extracted_data_dir="extracted_data", output_dir="analysis_output"):
        self.data_dir = extracted_data_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Define search patterns for each analytical dimension
        self.patterns = self._define_patterns()

        # Storage for findings
        self.findings = []

    def _define_patterns(self) -> Dict:
        """Define regex patterns and keywords for each analysis category"""

        patterns = {
            # A. Target Setting & Goals
            'targets': {
                'keywords': [
                    'target', 'goal', 'commitment', 'objective', 'ambition',
                    'aim to', 'by 2025', 'by 2030', 'by 2050',
                    'reduce', 'achieve', 'reach', 'attain',
                    'net zero', 'carbon neutral', 'climate positive',
                    'science-based target', 'SBTi', 'baseline',
                    'scope 1', 'scope 2', 'scope 3',
                    'renewable energy', 'emissions reduction',
                    'circular', 'recycled', 'waste reduction',
                    'living wage', 'fair trade', 'supply chain'
                ],
                'numeric_patterns': [
                    r'\d+%\s+(?:reduction|decrease|increase|improvement)',
                    r'reduce\s+by\s+\d+%',
                    r'\d+%\s+renewable',
                    r'\d+\s+(?:tons|tonnes|metric tons|MT)\s+(?:CO2|carbon)',
                    r'\$\d+(?:,\d+)*(?:\.\d+)?\s*(?:million|billion|M|B)',
                    r'by\s+(?:20\d{2})',
                ]
            },

            # B. Language & Tone
            'language': {
                'assertive': [
                    'will', 'committed to', 'must', 'ensure', 'guarantee',
                    'achieve', 'deliver', 'accomplish', 'pledge'
                ],
                'cautious': [
                    'aim to', 'strive to', 'seek to', 'plan to', 'intend to',
                    'hope to', 'aspire to', 'working toward', 'may', 'might',
                    'could', 'would', 'should', 'approximately', 'estimated'
                ],
                'regulatory': [
                    'compliance', 'regulation', 'regulatory', 'mandate',
                    'requirement', 'legislation', 'law', 'directive',
                    'CSRD', 'SEC', 'disclosure', 'reporting standard',
                    'due diligence', 'transparency', 'accountability'
                ],
                'activism': [
                    'advocate', 'activism', 'fight for', 'protect',
                    'defend', 'justice', 'equity', 'rights',
                    'movement', 'campaign', 'collective action'
                ]
            },

            # C. Initiatives
            'initiatives': {
                'keywords': [
                    'program', 'initiative', 'project', 'partnership',
                    'collaboration', 'investment', 'launch', 'announce',
                    'introduce', 'establish', 'create', 'implement',
                    'pilot', 'rollout', 'scale', 'expand'
                ],
                'investment_patterns': [
                    r'\$\d+(?:,\d+)*(?:\.\d+)?\s*(?:million|billion|M|B)',
                    r'invest(?:ed|ing|ment)?\s+\$\d+',
                    r'\d+\s+(?:million|billion)\s+dollars?'
                ]
            },

            # D. Geographic References
            'geography': {
                'us_states_blue': [
                    'California', 'New York', 'Washington', 'Oregon',
                    'Massachusetts', 'Colorado', 'Illinois', 'Connecticut',
                    'Vermont', 'Maine', 'Hawaii'
                ],
                'us_states_red': [
                    'Texas', 'Florida', 'Tennessee', 'Oklahoma',
                    'Alabama', 'Mississippi', 'Louisiana', 'Arkansas',
                    'West Virginia', 'Wyoming', 'Idaho'
                ],
                'eu_references': [
                    'European Union', 'EU ', 'Europe', 'CSRD',
                    'EU Taxonomy', 'Green Deal', 'SFDR',
                    'Brussels', 'European Commission'
                ],
                'countries': [
                    'United States', 'China', 'Vietnam', 'Bangladesh',
                    'India', 'Mexico', 'Honduras', 'El Salvador',
                    'France', 'Germany', 'UK', 'United Kingdom'
                ]
            },

            # E. Impact Areas
            'impacts': {
                'environmental': [
                    'climate', 'carbon', 'emissions', 'greenhouse gas', 'GHG',
                    'renewable energy', 'solar', 'wind', 'clean energy',
                    'water', 'waste', 'recycling', 'circular economy',
                    'biodiversity', 'ecosystem', 'deforestation',
                    'ocean', 'plastic', 'pollution', 'footprint'
                ],
                'social': [
                    'labor', 'worker', 'employee', 'human rights',
                    'fair trade', 'living wage', 'working conditions',
                    'diversity', 'equity', 'inclusion', 'DEI',
                    'community', 'indigenous', 'gender equality',
                    'health', 'safety', 'well-being'
                ],
                'governance': [
                    'governance', 'board', 'transparency', 'accountability',
                    'ethics', 'compliance', 'oversight', 'audit',
                    'stakeholder', 'disclosure', 'reporting'
                ],
                'supply_chain': [
                    'supply chain', 'supplier', 'vendor', 'sourcing',
                    'traceability', 'due diligence', 'audit',
                    'tier 1', 'tier 2', 'upstream', 'downstream'
                ]
            },

            # F. Commitment Changes
            'commitment_signals': {
                'strengthening': [
                    'increase', 'expand', 'enhance', 'accelerate',
                    'strengthen', 'advance', 'scale up', 'deepen'
                ],
                'weakening': [
                    'adjust', 'modify', 'revise', 'update', 'reassess',
                    'recalibrate', 'postpone', 'delay', 'phase out',
                    'discontinue', 'suspend', 'reduce scope'
                ]
            }
        }

        return patterns

    def load_extracted_documents(self) -> List[Dict]:
        """Load all extracted JSON files"""

        documents = []
        json_files = [f for f in os.listdir(self.data_dir) if f.endswith('_extracted.json')]

        print(f"Loading {len(json_files)} extracted documents...")

        for json_file in sorted(json_files):
            json_path = os.path.join(self.data_dir, json_file)
            with open(json_path, 'r', encoding='utf-8') as f:
                doc_data = json.load(f)
                documents.append(doc_data)
                print(f"  ✓ Loaded: {doc_data['filename']} ({doc_data['year']})")

        return documents

    def search_patterns_in_page(self, text: str, patterns: List[str],
                                case_sensitive: bool = False) -> List[Dict]:
        """Search for patterns in text and return matches with context"""

        matches = []
        search_text = text if case_sensitive else text.lower()

        for pattern in patterns:
            search_pattern = pattern if case_sensitive else pattern.lower()

            # Check if it's a regex pattern or simple string
            if any(char in pattern for char in [r'\d', r'\s', '[', '(']):
                # Regex pattern
                try:
                    regex_matches = re.finditer(pattern, search_text, re.IGNORECASE)
                    for match in regex_matches:
                        start = max(0, match.start() - 100)
                        end = min(len(text), match.end() + 100)
                        context = text[start:end].replace('\n', ' ')

                        matches.append({
                            'pattern': pattern,
                            'matched_text': match.group(),
                            'context': context,
                            'position': match.start()
                        })
                except re.error:
                    # If regex fails, treat as simple string
                    pass

            # Simple string search
            if search_pattern in search_text:
                # Find all occurrences
                start_pos = 0
                while True:
                    pos = search_text.find(search_pattern, start_pos)
                    if pos == -1:
                        break

                    # Get context
                    context_start = max(0, pos - 100)
                    context_end = min(len(text), pos + len(search_pattern) + 100)
                    context = text[context_start:context_end].replace('\n', ' ')

                    matches.append({
                        'pattern': pattern,
                        'matched_text': text[pos:pos+len(pattern)],
                        'context': context,
                        'position': pos
                    })

                    start_pos = pos + 1

        return matches

    def extract_targets_and_goals(self, documents: List[Dict]) -> pd.DataFrame:
        """Extract all target-related content with page numbers"""

        print("\n" + "="*80)
        print("EXTRACTING TARGETS AND GOALS")
        print("="*80)

        target_findings = []

        for doc in documents:
            print(f"\nAnalyzing: {doc['filename']} ({doc['year']})")

            for page in doc['pages']:
                page_num = page['page_number']
                text = page.get('text', '')

                if not text:
                    continue

                # Search for target keywords
                keyword_matches = self.search_patterns_in_page(
                    text,
                    self.patterns['targets']['keywords']
                )

                # Search for numeric patterns
                numeric_matches = self.search_patterns_in_page(
                    text,
                    self.patterns['targets']['numeric_patterns']
                )

                all_matches = keyword_matches + numeric_matches

                if all_matches:
                    # Deduplicate by context
                    seen_contexts = set()
                    for match in all_matches:
                        context = match['context']
                        if context not in seen_contexts:
                            seen_contexts.add(context)

                            target_findings.append({
                                'document': doc['filename'],
                                'year': doc['year'],
                                'doc_type': doc['document_type'],
                                'page_number': page_num,
                                'category': 'Target/Goal',
                                'pattern_matched': match['pattern'],
                                'extracted_text': match['matched_text'],
                                'context': context,
                                'word_count': len(text.split())
                            })

            print(f"  Found {len([f for f in target_findings if f['document'] == doc['filename']])} target mentions")

        df = pd.DataFrame(target_findings)
        output_path = os.path.join(self.output_dir, "targets_goals_extracted.csv")
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"\n✓ Saved to: {output_path}")

        return df

    def extract_language_tone(self, documents: List[Dict]) -> pd.DataFrame:
        """Analyze language patterns and tone shifts"""

        print("\n" + "="*80)
        print("ANALYZING LANGUAGE AND TONE")
        print("="*80)

        language_findings = []

        for doc in documents:
            print(f"\nAnalyzing: {doc['filename']} ({doc['year']})")

            # Count language patterns across entire document
            assertive_count = 0
            cautious_count = 0
            regulatory_count = 0
            activism_count = 0

            for page in doc['pages']:
                page_num = page['page_number']
                text = page.get('text', '').lower()

                if not text:
                    continue

                # Count each language type
                page_assertive = sum(1 for word in self.patterns['language']['assertive']
                                    if word.lower() in text)
                page_cautious = sum(1 for word in self.patterns['language']['cautious']
                                   if word.lower() in text)
                page_regulatory = sum(1 for word in self.patterns['language']['regulatory']
                                     if word.lower() in text)
                page_activism = sum(1 for word in self.patterns['language']['activism']
                                   if word.lower() in text)

                assertive_count += page_assertive
                cautious_count += page_cautious
                regulatory_count += page_regulatory
                activism_count += page_activism

                # Record page-level findings if significant
                if any([page_assertive, page_cautious, page_regulatory, page_activism]):
                    language_findings.append({
                        'document': doc['filename'],
                        'year': doc['year'],
                        'doc_type': doc['document_type'],
                        'page_number': page_num,
                        'assertive_count': page_assertive,
                        'cautious_count': page_cautious,
                        'regulatory_count': page_regulatory,
                        'activism_count': page_activism,
                        'dominant_tone': max(
                            [('assertive', page_assertive),
                             ('cautious', page_cautious),
                             ('regulatory', page_regulatory),
                             ('activism', page_activism)],
                            key=lambda x: x[1]
                        )[0] if max(page_assertive, page_cautious, page_regulatory, page_activism) > 0 else 'neutral'
                    })

            print(f"  Language patterns: Assertive={assertive_count}, Cautious={cautious_count}, "
                  f"Regulatory={regulatory_count}, Activism={activism_count}")

        df = pd.DataFrame(language_findings)
        output_path = os.path.join(self.output_dir, "language_tone_analysis.csv")
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"\n✓ Saved to: {output_path}")

        return df

    def extract_initiatives(self, documents: List[Dict]) -> pd.DataFrame:
        """Extract announced initiatives with details"""

        print("\n" + "="*80)
        print("EXTRACTING INITIATIVES")
        print("="*80)

        initiative_findings = []

        for doc in documents:
            print(f"\nAnalyzing: {doc['filename']} ({doc['year']})")

            for page in doc['pages']:
                page_num = page['page_number']
                text = page.get('text', '')

                if not text:
                    continue

                # Search for initiative keywords
                keyword_matches = self.search_patterns_in_page(
                    text,
                    self.patterns['initiatives']['keywords']
                )

                # Search for investment amounts
                investment_matches = self.search_patterns_in_page(
                    text,
                    self.patterns['initiatives']['investment_patterns']
                )

                # Combine and deduplicate
                all_matches = keyword_matches + investment_matches
                seen_contexts = set()

                for match in all_matches:
                    context = match['context']
                    if context not in seen_contexts:
                        seen_contexts.add(context)

                        # Determine if investment amount mentioned
                        has_investment = any(re.search(pattern, context, re.IGNORECASE)
                                           for pattern in self.patterns['initiatives']['investment_patterns'])

                        initiative_findings.append({
                            'document': doc['filename'],
                            'year': doc['year'],
                            'doc_type': doc['document_type'],
                            'page_number': page_num,
                            'category': 'Initiative',
                            'has_investment_amount': has_investment,
                            'pattern_matched': match['pattern'],
                            'context': context
                        })

            print(f"  Found {len([f for f in initiative_findings if f['document'] == doc['filename']])} initiative mentions")

        df = pd.DataFrame(initiative_findings)
        output_path = os.path.join(self.output_dir, "initiatives_extracted.csv")
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"\n✓ Saved to: {output_path}")

        return df

    def extract_geographic_references(self, documents: List[Dict]) -> pd.DataFrame:
        """Extract geographic references (US states, EU, countries)"""

        print("\n" + "="*80)
        print("EXTRACTING GEOGRAPHIC REFERENCES")
        print("="*80)

        geo_findings = []

        for doc in documents:
            print(f"\nAnalyzing: {doc['filename']} ({doc['year']})")

            for page in doc['pages']:
                page_num = page['page_number']
                text = page.get('text', '')

                if not text:
                    continue

                # Search each geographic category
                for geo_type, locations in self.patterns['geography'].items():
                    matches = self.search_patterns_in_page(text, locations)

                    for match in matches:
                        geo_findings.append({
                            'document': doc['filename'],
                            'year': doc['year'],
                            'doc_type': doc['document_type'],
                            'page_number': page_num,
                            'geographic_type': geo_type,
                            'location': match['pattern'],
                            'context': match['context']
                        })

        df = pd.DataFrame(geo_findings)
        output_path = os.path.join(self.output_dir, "geographic_references.csv")
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"\n✓ Saved {len(df)} geographic references to: {output_path}")

        return df

    def extract_impact_areas(self, documents: List[Dict]) -> pd.DataFrame:
        """Extract and categorize impact areas (environmental, social, governance)"""

        print("\n" + "="*80)
        print("EXTRACTING IMPACT AREAS")
        print("="*80)

        impact_findings = []

        for doc in documents:
            print(f"\nAnalyzing: {doc['filename']} ({doc['year']})")

            doc_level_counts = {
                'environmental': 0,
                'social': 0,
                'governance': 0,
                'supply_chain': 0
            }

            for page in doc['pages']:
                page_num = page['page_number']
                text = page.get('text', '').lower()

                if not text:
                    continue

                # Count each impact category
                for impact_type, keywords in self.patterns['impacts'].items():
                    count = sum(1 for keyword in keywords if keyword.lower() in text)

                    if count > 0:
                        doc_level_counts[impact_type] += count

                        impact_findings.append({
                            'document': doc['filename'],
                            'year': doc['year'],
                            'doc_type': doc['document_type'],
                            'page_number': page_num,
                            'impact_category': impact_type,
                            'keyword_count': count,
                            'keywords_found': [kw for kw in keywords if kw.lower() in text]
                        })

            print(f"  Impact areas: {doc_level_counts}")

        df = pd.DataFrame(impact_findings)
        output_path = os.path.join(self.output_dir, "impact_areas_extracted.csv")
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"\n✓ Saved to: {output_path}")

        return df

    def create_master_findings_database(self):
        """Combine all extraction outputs into master database"""

        print("\n" + "="*80)
        print("CREATING MASTER FINDINGS DATABASE")
        print("="*80)

        # Load all CSV files
        csv_files = [f for f in os.listdir(self.output_dir) if f.endswith('.csv')]

        master_data = {
            'extraction_summary': {},
            'datasets': {}
        }

        for csv_file in csv_files:
            csv_path = os.path.join(self.output_dir, csv_file)
            df = pd.read_csv(csv_path)

            dataset_name = csv_file.replace('.csv', '')
            master_data['datasets'][dataset_name] = {
                'total_records': len(df),
                'columns': list(df.columns),
                'file_path': csv_path
            }

            print(f"  ✓ {dataset_name}: {len(df)} records")

        # Save summary
        summary_path = os.path.join(self.output_dir, "MASTER_FINDINGS_SUMMARY.json")
        with open(summary_path, 'w') as f:
            json.dump(master_data, f, indent=2)

        print(f"\n✓ Master findings summary saved to: {summary_path}")


def main():
    """Main analysis process"""

    print("="*80)
    print("PATAGONIA ESG ANALYSIS - CONTENT EXTRACTION")
    print("="*80)

    # Initialize analyzer
    analyzer = ESGContentAnalyzer(
        extracted_data_dir="extracted_data",
        output_dir="analysis_output"
    )

    # Load extracted documents
    documents = analyzer.load_extracted_documents()

    if not documents:
        print("\n❌ ERROR: No extracted documents found!")
        print("Please run extract_text_with_pages.py first.")
        return

    # Run all extraction analyses
    print("\n" + "="*80)
    print("BEGINNING TARGETED EXTRACTIONS")
    print("="*80)

    # 1. Extract targets and goals
    targets_df = analyzer.extract_targets_and_goals(documents)

    # 2. Analyze language and tone
    language_df = analyzer.extract_language_tone(documents)

    # 3. Extract initiatives
    initiatives_df = analyzer.extract_initiatives(documents)

    # 4. Extract geographic references
    geo_df = analyzer.extract_geographic_references(documents)

    # 5. Extract impact areas
    impacts_df = analyzer.extract_impact_areas(documents)

    # 6. Create master database
    analyzer.create_master_findings_database()

    print("\n" + "="*80)
    print("CONTENT EXTRACTION COMPLETE")
    print("="*80)
    print(f"Output directory: {analyzer.output_dir}/")
    print("\nGenerated datasets:")
    print("  - targets_goals_extracted.csv")
    print("  - language_tone_analysis.csv")
    print("  - initiatives_extracted.csv")
    print("  - geographic_references.csv")
    print("  - impact_areas_extracted.csv")
    print("  - MASTER_FINDINGS_SUMMARY.json")
    print("="*80)


if __name__ == "__main__":
    main()
