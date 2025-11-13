# Patagonia ESG Corporate Policy Response Analysis (2020-2025)

## Project Overview

This repository contains a comprehensive analysis of Patagonia's corporate responses to ESG regulatory and policy shifts from 2020-2025. The analysis examines changes in target setting, language and tone, announced initiatives, commitment retreats, and impact areas across both U.S. (red vs. blue states) and EU regulatory landscapes.

## Client Deliverables

This project delivers:
1. **Step-by-step analytical framework** for ESG policy response analysis
2. **Comprehensive data extraction** from all annual reports with exact page references
3. **Cleaned and structured datasets** tracking corporate response changes
4. **Quantitative analysis** with visualizations (charts, tables, graphs)
5. **Fact-checked findings** with source citations and page numbers
6. **Python code** for reproducible analysis

## Project Structure

```
Patagonia-Corporate-Policy-Analysis/
├── ANALYTICAL_FRAMEWORK.md          # Complete analytical methodology
├── README.md                         # This file
│
├── Source Documents/
│   ├── Patagonia 2020-2024 Disclosures.zip (extracted)
│   └── Patagonia 2025 pt1-6.pdf
│
├── Python Scripts/
│   ├── run_full_analysis.py          # Master execution script
│   ├── extract_text_with_pages.py    # PDF extraction with page tracking
│   ├── analyze_esg_content.py        # Targeted ESG content extraction
│   └── visualize_findings.py         # Visualization generation
│
├── Output Directories/
│   ├── extracted_data/               # Raw extracted text and page indices
│   ├── analysis_output/              # Structured datasets with findings
│   └── visualizations/               # Charts, graphs, and dashboards
```

## Available Documents

### Years Covered: 2020, 2021, 2024, 2025
**Note:** 2022 and 2023 BCorp reports are not available in the dataset.

**Document Inventory:**
- 2020 BCorp Report
- 2021 BCorp Report
- 2021 Modern Slavery Act Statement
- 2024 BCorp Report
- 2024 Modern Slavery Act Statement
- 2025 Annual Reports (6 parts)

## Quick Start

### Option 1: Run Complete Analysis (Recommended)

Execute the entire analysis pipeline with a single command:

```bash
python run_full_analysis.py
```

This will sequentially run:
1. Text extraction with page number tracking
2. ESG content analysis and data extraction
3. Visualization generation

### Option 2: Run Individual Steps

For more control, run each script separately:

```bash
# Step 1: Extract text from all PDFs
python extract_text_with_pages.py

# Step 2: Analyze ESG content and extract data
python analyze_esg_content.py

# Step 3: Generate visualizations
python visualize_findings.py
```

## Dependencies

The scripts will automatically install required packages:
- pandas
- numpy
- matplotlib
- seaborn
- PyPDF2
- pdfplumber
- openpyxl

To manually install all dependencies:
```bash
pip install pandas numpy matplotlib seaborn PyPDF2 pdfplumber openpyxl
```

## Analysis Dimensions

The analysis examines five key dimensions:

### 1. Target Setting & Goals
- Quantitative sustainability targets
- Timeline commitments (2025, 2030, 2050)
- Scope changes (emissions, waste, renewable energy)
- Science-based targets (SBTi)
- Social and labor goals

### 2. Language & Tone
- Assertive vs. cautious language patterns
- Regulatory compliance terminology
- Activism and advocacy language
- Sentiment analysis
- Word frequency trends

### 3. Announced Initiatives
- New programs and partnerships
- Investment amounts
- Geographic distribution
- Timeline of implementation
- Stakeholder engagement

### 4. Commitment Retreats
- Target modifications or withdrawals
- Initiative discontinuations
- Language softening
- Scope reductions
- Explanatory narratives

### 5. Impact Areas
- Environmental (climate, water, waste, biodiversity)
- Social (labor, human rights, DEI, community)
- Governance (transparency, accountability, ethics)
- Supply chain (traceability, due diligence)

## Geographic Analysis

### U.S. Analysis
- **Blue States:** California, New York, Washington, Oregon, Massachusetts, Colorado, Illinois, Vermont
- **Red States:** Texas, Florida, Tennessee, Oklahoma, Alabama, Mississippi, Louisiana, Arkansas

### EU Analysis
- European Union references
- CSRD compliance language
- EU Taxonomy mentions
- Green Deal alignment

## Output Files

### 1. extracted_data/
- **Individual JSON files:** Complete structured data for each document
- **Individual TXT files:** Plain text with page markers
- **MASTER_PAGE_INDEX.csv:** Searchable index of all pages
- **MASTER_PAGE_INDEX.xlsx:** Excel version with summary sheet
- **extraction_log.json:** Process log

### 2. analysis_output/
- **targets_goals_extracted.csv:** All target and goal mentions with page numbers
- **language_tone_analysis.csv:** Language pattern analysis by page
- **initiatives_extracted.csv:** All announced initiatives with context
- **geographic_references.csv:** Geographic mentions (US/EU/states/countries)
- **impact_areas_extracted.csv:** ESG impact area keyword analysis
- **MASTER_FINDINGS_SUMMARY.json:** Summary of all datasets

### 3. visualizations/
- **language_tone_analysis.png:** Language evolution trends
- **targets_goals_analysis.png:** Target setting patterns
- **geographic_distribution.png:** Geographic focus analysis
- **impact_areas_analysis.png:** ESG impact area trends
- **initiatives_analysis.png:** Initiative timeline
- **EXECUTIVE_DASHBOARD.png:** Single-page summary dashboard

## Using the Outputs

### For Quality Checks and Cross-References

All extracted data includes **exact page numbers** for verification:

1. **MASTER_PAGE_INDEX.xlsx:** Quick lookup of content by page
2. **CSV files in analysis_output/:** Each finding includes:
   - Document name
   - Year
   - Page number
   - Extracted text
   - Context (surrounding text)

### For Client Presentations

1. **Visualizations:** Ready-to-use charts and graphs
2. **EXECUTIVE_DASHBOARD.png:** High-level summary
3. **CSV files:** Import into Excel/PowerPoint for custom tables

### For Deep Analysis

1. **JSON files:** Complete document structure for programmatic analysis
2. **TXT files:** Full text for manual review with page markers
3. **ANALYTICAL_FRAMEWORK.md:** Methodology and interpretation guidance

## Methodology Highlights

### Page Number Preservation
- All extractions maintain source page numbers
- Every finding is traceable to original document
- Cross-referencing enabled for quality assurance

### Multi-Method Extraction
- Primary: pdfplumber (handles complex layouts)
- Fallback: PyPDF2 (alternative extraction)
- Table detection and extraction
- Text quality validation

### Comprehensive Pattern Matching
- Keyword searches (case-insensitive)
- Regular expression patterns for numeric targets
- Contextual extraction (surrounding text captured)
- Deduplication to avoid over-counting

### Quantitative Rigor
- Year-over-year trend analysis
- Percentage change calculations
- Statistical aggregations
- Multi-dimensional comparisons

## Key Research Questions Addressed

1. How have Patagonia's quantitative ESG targets changed from 2020 to 2025?
2. What language shifts indicate policy response or strategic repositioning?
3. Are there observable commitment retreats correlating with policy events?
4. How does approach differ between U.S. red states, blue states, and EU markets?
5. What initiatives have been sustained vs. discontinued?
6. How has tone evolved in response to anti-ESG sentiment?
7. What impact areas have received increased vs. decreased emphasis?
8. How transparent is Patagonia about methodology changes?

## Data Quality & Limitations

### Strengths
- Complete page number tracking for all findings
- Multi-dimensional analysis approach
- Reproducible methodology
- Fact-checkable with source citations

### Limitations
- Missing 2022 and 2023 BCorp reports (data gap)
- Automated extraction may miss context-dependent nuances
- Pattern matching captures keywords but may miss implicit meanings
- Manual review recommended for critical findings

## Validation & Fact-Checking

### Recommended Process
1. Review MASTER_PAGE_INDEX.xlsx for data completeness
2. Spot-check extracted findings against source PDFs using page numbers
3. Validate quantitative targets with original documents
4. Cross-reference geographic claims with source context
5. Verify trend interpretations against raw data

### Page Reference Format
All findings include:
- **Document:** Filename of source PDF
- **Year:** Report year
- **Page Number:** Exact page where finding appears
- **Context:** Surrounding text for validation

## Contact & Support

For questions about methodology, data interpretation, or analysis extensions:
- Review ANALYTICAL_FRAMEWORK.md for detailed methodology
- Check extraction_log.json for processing details
- Examine MASTER_FINDINGS_SUMMARY.json for dataset overview

## License & Usage

This analysis is prepared for client deliverable purposes. All source documents are property of Patagonia. Analysis methodology and code are provided for transparency and reproducibility.

---

**Analysis Date:** November 13, 2025
**Document Coverage:** 2020, 2021, 2024, 2025
**Total Pages Analyzed:** [Generated after execution]
**Total Findings Extracted:** [Generated after execution]
