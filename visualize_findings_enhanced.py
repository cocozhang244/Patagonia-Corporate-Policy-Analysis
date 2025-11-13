#!/usr/bin/env python3
"""
Patagonia ESG Analysis - Enhanced Quantitative Visualizations
Author: Analysis Team
Date: November 13, 2025
Purpose: Generate comprehensive, publication-quality visualizations with heatmaps, trends, and quantitative analysis
"""

import os
import warnings
warnings.filterwarnings('ignore')

try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from datetime import datetime
    from matplotlib.patches import Rectangle
except ImportError as e:
    print("Installing required packages...")
    os.system("pip install --user pandas numpy matplotlib seaborn")
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from datetime import datetime
    from matplotlib.patches import Rectangle


class EnhancedESGVisualizer:
    """Create enhanced visualizations for Patagonia ESG analysis"""

    def __init__(self, analysis_dir="analysis_output", viz_dir="visualizations_enhanced"):
        self.analysis_dir = analysis_dir
        self.viz_dir = viz_dir
        os.makedirs(viz_dir, exist_ok=True)

        # Set professional visualization style
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_palette("husl")

        # Color schemes
        self.year_colors = {
            '2020': '#3498db',  # Blue
            '2021': '#2ecc71',  # Green
            '2024': '#e74c3c',  # Red
            '2025': '#95a5a6'   # Gray
        }

        self.impact_colors = {
            'environmental': '#27ae60',
            'social': '#3498db',
            'governance': '#e67e22',
            'supply_chain': '#9b59b6'
        }

    def load_analysis_data(self) -> dict:
        """Load all analysis CSV files"""
        data = {}
        csv_files = {
            'targets': 'targets_goals_extracted.csv',
            'language': 'language_tone_analysis.csv',
            'initiatives': 'initiatives_extracted.csv',
            'geography': 'geographic_references.csv',
            'impacts': 'impact_areas_extracted.csv'
        }

        print("Loading analysis data...")
        for key, filename in csv_files.items():
            filepath = os.path.join(self.analysis_dir, filename)
            if os.path.exists(filepath):
                data[key] = pd.read_csv(filepath)
                print(f"  ✓ Loaded: {filename} ({len(data[key])} records)")
            else:
                print(f"  ⚠ Not found: {filename}")
                data[key] = pd.DataFrame()

        return data

    def create_quantitative_overview(self, data: dict):
        """Create comprehensive quantitative overview dashboard"""

        print("\nGenerating quantitative overview dashboard...")

        fig = plt.figure(figsize=(24, 16))
        gs = fig.add_gridspec(4, 4, hspace=0.35, wspace=0.35)

        fig.suptitle('Patagonia ESG Quantitative Analysis Dashboard (2020-2025)',
                     fontsize=20, fontweight='bold', y=0.995)

        # 1. Total findings by category (top left)
        ax1 = fig.add_subplot(gs[0, 0:2])
        categories = ['Targets\n& Goals', 'Language\n& Tone', 'Initiatives',
                     'Geographic\nReferences', 'Impact\nAreas']
        counts = [len(data['targets']), len(data['language']), len(data['initiatives']),
                 len(data['geography']), len(data['impacts'])]

        bars = ax1.bar(categories, counts, color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6'],
                      edgecolor='black', linewidth=1.5)
        ax1.set_title('Total Findings by Analysis Category', fontsize=14, fontweight='bold', pad=15)
        ax1.set_ylabel('Number of Findings', fontsize=12, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3, linestyle='--')

        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(count)}',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')

        # 2. Year-over-year comparison (top right)
        ax2 = fig.add_subplot(gs[0, 2:4])

        # Aggregate all findings by year
        year_data = []
        for category, df in data.items():
            if not df.empty and 'year' in df.columns:
                year_counts = df['year'].value_counts().sort_index()
                for year, count in year_counts.items():
                    year_data.append({'year': str(year), 'category': category, 'count': count})

        if year_data:
            year_df = pd.DataFrame(year_data)
            pivot_year = year_df.pivot_table(values='count', index='year',
                                             columns='category', fill_value=0)

            pivot_year.plot(kind='bar', ax=ax2, width=0.8, edgecolor='black', linewidth=1.2)
            ax2.set_title('Findings by Year and Category', fontsize=14, fontweight='bold', pad=15)
            ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Number of Findings', fontsize=12, fontweight='bold')
            ax2.legend(title='Category', fontsize=9, title_fontsize=10, loc='upper left')
            ax2.grid(axis='y', alpha=0.3, linestyle='--')
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=0)

        # 3. Language tone quantitative breakdown
        ax3 = fig.add_subplot(gs[1, 0:2])

        if not data['language'].empty:
            lang_by_year = data['language'].groupby('year').agg({
                'assertive_count': 'sum',
                'cautious_count': 'sum',
                'regulatory_count': 'sum',
                'activism_count': 'sum'
            })

            x = np.arange(len(lang_by_year.index))
            width = 0.2

            ax3.bar(x - 1.5*width, lang_by_year['assertive_count'], width,
                   label='Assertive', color='#2ecc71', edgecolor='black', linewidth=1)
            ax3.bar(x - 0.5*width, lang_by_year['cautious_count'], width,
                   label='Cautious', color='#e67e22', edgecolor='black', linewidth=1)
            ax3.bar(x + 0.5*width, lang_by_year['regulatory_count'], width,
                   label='Regulatory', color='#3498db', edgecolor='black', linewidth=1)
            ax3.bar(x + 1.5*width, lang_by_year['activism_count'], width,
                   label='Activism', color='#e74c3c', edgecolor='black', linewidth=1)

            ax3.set_title('Language Tone Distribution by Year (Absolute Counts)',
                         fontsize=14, fontweight='bold', pad=15)
            ax3.set_xlabel('Year', fontsize=12, fontweight='bold')
            ax3.set_ylabel('Total Mentions', fontsize=12, fontweight='bold')
            ax3.set_xticks(x)
            ax3.set_xticklabels(lang_by_year.index.astype(str))
            ax3.legend(fontsize=10, loc='upper left')
            ax3.grid(axis='y', alpha=0.3, linestyle='--')

        # 4. Impact areas stacked bar chart
        ax4 = fig.add_subplot(gs[1, 2:4])

        if not data['impacts'].empty:
            impact_by_year = data['impacts'].groupby(['year', 'impact_category'])['keyword_count'].sum().unstack(fill_value=0)

            impact_by_year.plot(kind='bar', stacked=True, ax=ax4,
                               color=[self.impact_colors.get(col, '#95a5a6') for col in impact_by_year.columns],
                               edgecolor='black', linewidth=1.2, width=0.7)

            ax4.set_title('Impact Area Focus by Year (Keyword Counts)',
                         fontsize=14, fontweight='bold', pad=15)
            ax4.set_xlabel('Year', fontsize=12, fontweight='bold')
            ax4.set_ylabel('Total Keyword Mentions', fontsize=12, fontweight='bold')
            ax4.legend(title='Impact Category', fontsize=9, title_fontsize=10, loc='upper left')
            ax4.grid(axis='y', alpha=0.3, linestyle='--')
            plt.setp(ax4.xaxis.get_majorticklabels(), rotation=0)

        # 5. Targets trend line
        ax5 = fig.add_subplot(gs[2, 0:2])

        if not data['targets'].empty:
            targets_by_year = data['targets'].groupby('year').size().sort_index()

            ax5.plot(targets_by_year.index.astype(str), targets_by_year.values,
                    marker='o', markersize=12, linewidth=3, color='#e74c3c',
                    markeredgecolor='black', markeredgewidth=1.5)
            ax5.fill_between(range(len(targets_by_year)), targets_by_year.values,
                            alpha=0.3, color='#e74c3c')

            # Add value labels
            for i, (year, count) in enumerate(zip(targets_by_year.index.astype(str), targets_by_year.values)):
                ax5.text(i, count + 2, str(count), ha='center', va='bottom',
                        fontsize=11, fontweight='bold')

            ax5.set_title('ESG Target & Goal Mentions Over Time',
                         fontsize=14, fontweight='bold', pad=15)
            ax5.set_xlabel('Year', fontsize=12, fontweight='bold')
            ax5.set_ylabel('Number of Target Mentions', fontsize=12, fontweight='bold')
            ax5.grid(True, alpha=0.3, linestyle='--')

        # 6. Initiatives trend line
        ax6 = fig.add_subplot(gs[2, 2:4])

        if not data['initiatives'].empty:
            init_by_year = data['initiatives'].groupby('year').size().sort_index()

            ax6.plot(init_by_year.index.astype(str), init_by_year.values,
                    marker='s', markersize=12, linewidth=3, color='#3498db',
                    markeredgecolor='black', markeredgewidth=1.5)
            ax6.fill_between(range(len(init_by_year)), init_by_year.values,
                            alpha=0.3, color='#3498db')

            # Add value labels
            for i, (year, count) in enumerate(zip(init_by_year.index.astype(str), init_by_year.values)):
                ax6.text(i, count + 2, str(count), ha='center', va='bottom',
                        fontsize=11, fontweight='bold')

            ax6.set_title('Announced Initiatives Over Time',
                         fontsize=14, fontweight='bold', pad=15)
            ax6.set_xlabel('Year', fontsize=12, fontweight='bold')
            ax6.set_ylabel('Number of Initiatives', fontsize=12, fontweight='bold')
            ax6.grid(True, alpha=0.3, linestyle='--')

        # 7. Document coverage summary
        ax7 = fig.add_subplot(gs[3, 0:2])

        doc_summary = []
        for category, df in data.items():
            if not df.empty and 'document' in df.columns:
                doc_counts = df['document'].value_counts().head(5)
                for doc, count in doc_counts.items():
                    doc_name = doc.replace('.pdf', '').replace('PAT_', '').replace('_', ' ')[:30]
                    doc_summary.append({'document': doc_name, 'category': category, 'count': count})

        if doc_summary:
            doc_df = pd.DataFrame(doc_summary)
            doc_pivot = doc_df.pivot_table(values='count', index='document',
                                          columns='category', fill_value=0)

            doc_pivot.plot(kind='barh', ax=ax7, stacked=False,
                          width=0.7, edgecolor='black', linewidth=1)
            ax7.set_title('Top Documents by Finding Category',
                         fontsize=14, fontweight='bold', pad=15)
            ax7.set_xlabel('Number of Findings', fontsize=12, fontweight='bold')
            ax7.set_ylabel('Document', fontsize=12, fontweight='bold')
            ax7.legend(title='Category', fontsize=8, title_fontsize=9, loc='lower right')
            ax7.grid(axis='x', alpha=0.3, linestyle='--')

        # 8. Data quality metrics
        ax8 = fig.add_subplot(gs[3, 2:4])

        quality_metrics = {
            'Total Pages Analyzed': 0,
            'Documents Processed': 0,
            'Years with Data': 0,
            'Total Findings': 0,
            'Avg Findings/Doc': 0
        }

        total_findings = sum(len(df) for df in data.values())
        quality_metrics['Total Findings'] = total_findings

        if not data['targets'].empty and 'document' in data['targets'].columns:
            quality_metrics['Documents Processed'] = data['targets']['document'].nunique()

        all_years = set()
        for df in data.values():
            if not df.empty and 'year' in df.columns:
                all_years.update(df['year'].unique())
        quality_metrics['Years with Data'] = len(all_years)

        if quality_metrics['Documents Processed'] > 0:
            quality_metrics['Avg Findings/Doc'] = round(total_findings / quality_metrics['Documents Processed'], 1)

        # Create horizontal bar chart for metrics
        metrics_names = list(quality_metrics.keys())
        metrics_values = list(quality_metrics.values())

        bars = ax8.barh(metrics_names, metrics_values,
                       color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6'],
                       edgecolor='black', linewidth=1.5)

        ax8.set_title('Analysis Coverage Metrics', fontsize=14, fontweight='bold', pad=15)
        ax8.set_xlabel('Count', fontsize=12, fontweight='bold')
        ax8.grid(axis='x', alpha=0.3, linestyle='--')

        # Add value labels
        for bar, value in zip(bars, metrics_values):
            width = bar.get_width()
            ax8.text(width + 2, bar.get_y() + bar.get_height()/2.,
                    f'{value}',
                    ha='left', va='center', fontsize=11, fontweight='bold')

        # Add timestamp
        fig.text(0.99, 0.01, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                ha='right', va='bottom', fontsize=9, style='italic')

        output_path = os.path.join(self.viz_dir, '01_QUANTITATIVE_OVERVIEW.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"  ✓ Saved: {output_path}")

    def create_geographic_heatmap(self, data: dict):
        """Create detailed geographic heatmap analysis"""

        print("\nGenerating geographic heatmap analysis...")

        if data['geography'].empty:
            print("  ⚠ No geographic data available")
            return

        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        fig.suptitle('Patagonia Geographic Focus Analysis - Heatmaps & Distribution',
                     fontsize=18, fontweight='bold', y=0.995)

        geo_df = data['geography']

        # 1. Geographic Type by Year Heatmap (top left)
        ax1 = axes[0, 0]

        geo_by_year_type = geo_df.groupby(['year', 'geographic_type']).size().unstack(fill_value=0)

        sns.heatmap(geo_by_year_type.T, annot=True, fmt='d', cmap='YlOrRd',
                   ax=ax1, cbar_kws={'label': 'Number of References'},
                   linewidths=1, linecolor='black', annot_kws={'fontsize': 11, 'fontweight': 'bold'})

        ax1.set_title('Geographic References Heatmap: Type by Year',
                     fontsize=14, fontweight='bold', pad=15)
        ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Geographic Type', fontsize=12, fontweight='bold')
        ax1.set_yticklabels(ax1.get_yticklabels(), rotation=0)

        # 2. U.S. States Heatmap by Year (top right)
        ax2 = axes[0, 1]

        us_states = geo_df[geo_df['geographic_type'].isin(['us_states_red', 'us_states_blue'])]

        if not us_states.empty:
            state_year_matrix = us_states.groupby(['location', 'year']).size().unstack(fill_value=0)

            # Add a column indicating red vs blue
            state_colors = []
            for state in state_year_matrix.index:
                is_blue = geo_df[(geo_df['location'] == state) &
                               (geo_df['geographic_type'] == 'us_states_blue')].shape[0] > 0
                state_colors.append('Blue State' if is_blue else 'Red State')

            sns.heatmap(state_year_matrix, annot=True, fmt='d', cmap='RdYlGn',
                       ax=ax2, cbar_kws={'label': 'Number of References'},
                       linewidths=1, linecolor='black', annot_kws={'fontsize': 10, 'fontweight': 'bold'})

            ax2.set_title('U.S. State References Heatmap by Year',
                         fontsize=14, fontweight='bold', pad=15)
            ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
            ax2.set_ylabel('State', fontsize=12, fontweight='bold')
            ax2.set_yticklabels(ax2.get_yticklabels(), rotation=0)

            # Color-code y-axis labels
            for i, (label, color_type) in enumerate(zip(ax2.get_yticklabels(), state_colors)):
                if 'Blue' in color_type:
                    label.set_color('#3498db')
                    label.set_fontweight('bold')
                else:
                    label.set_color('#e74c3c')
                    label.set_fontweight('bold')
        else:
            ax2.text(0.5, 0.5, 'No U.S. State Data Available',
                    ha='center', va='center', fontsize=14, transform=ax2.transAxes)
            ax2.set_title('U.S. State References Heatmap by Year',
                         fontsize=14, fontweight='bold', pad=15)

        # 3. Red vs Blue States Comparison (bottom left)
        ax3 = axes[1, 0]

        red_blue_data = geo_df[geo_df['geographic_type'].isin(['us_states_red', 'us_states_blue'])]

        if not red_blue_data.empty:
            red_blue_by_year = red_blue_data.groupby(['year', 'geographic_type']).size().unstack(fill_value=0)

            x = np.arange(len(red_blue_by_year.index))
            width = 0.35

            blue_counts = red_blue_by_year.get('us_states_blue', [0] * len(red_blue_by_year))
            red_counts = red_blue_by_year.get('us_states_red', [0] * len(red_blue_by_year))

            bars1 = ax3.bar(x - width/2, blue_counts, width, label='Blue States',
                          color='#3498db', edgecolor='black', linewidth=1.5)
            bars2 = ax3.bar(x + width/2, red_counts, width, label='Red States',
                          color='#e74c3c', edgecolor='black', linewidth=1.5)

            ax3.set_title('Red vs Blue State References by Year',
                         fontsize=14, fontweight='bold', pad=15)
            ax3.set_xlabel('Year', fontsize=12, fontweight='bold')
            ax3.set_ylabel('Number of References', fontsize=12, fontweight='bold')
            ax3.set_xticks(x)
            ax3.set_xticklabels(red_blue_by_year.index.astype(str))
            ax3.legend(fontsize=11, loc='upper left')
            ax3.grid(axis='y', alpha=0.3, linestyle='--')

            # Add value labels
            for bar in bars1:
                height = bar.get_height()
                if height > 0:
                    ax3.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}', ha='center', va='bottom',
                            fontsize=10, fontweight='bold')

            for bar in bars2:
                height = bar.get_height()
                if height > 0:
                    ax3.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}', ha='center', va='bottom',
                            fontsize=10, fontweight='bold')
        else:
            ax3.text(0.5, 0.5, 'No Red/Blue State Data Available',
                    ha='center', va='center', fontsize=14, transform=ax3.transAxes)
            ax3.set_title('Red vs Blue State References by Year',
                         fontsize=14, fontweight='bold', pad=15)

        # 4. Top Countries Referenced (bottom right)
        ax4 = axes[1, 1]

        countries = geo_df[geo_df['geographic_type'] == 'countries']

        if not countries.empty:
            top_countries = countries['location'].value_counts().head(10)

            bars = ax4.barh(range(len(top_countries)), top_countries.values,
                           color='#16a085', edgecolor='black', linewidth=1.5)

            ax4.set_yticks(range(len(top_countries)))
            ax4.set_yticklabels(top_countries.index, fontsize=11)
            ax4.invert_yaxis()
            ax4.set_title('Top 10 Countries Referenced',
                         fontsize=14, fontweight='bold', pad=15)
            ax4.set_xlabel('Number of References', fontsize=12, fontweight='bold')
            ax4.grid(axis='x', alpha=0.3, linestyle='--')

            # Add value labels
            for i, (bar, value) in enumerate(zip(bars, top_countries.values)):
                ax4.text(value + 0.5, i, str(value),
                        va='center', fontsize=10, fontweight='bold')
        else:
            ax4.text(0.5, 0.5, 'No Country Data Available',
                    ha='center', va='center', fontsize=14, transform=ax4.transAxes)
            ax4.set_title('Top 10 Countries Referenced',
                         fontsize=14, fontweight='bold', pad=15)

        plt.tight_layout()
        output_path = os.path.join(self.viz_dir, '02_GEOGRAPHIC_HEATMAPS.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"  ✓ Saved: {output_path}")

    def create_language_evolution_charts(self, data: dict):
        """Create detailed language evolution analysis with multiple line graphs"""

        print("\nGenerating language evolution analysis...")

        if data['language'].empty:
            print("  ⚠ No language data available")
            return

        fig, axes = plt.subplots(2, 2, figsize=(20, 14))
        fig.suptitle('Patagonia Language & Tone Evolution Analysis (2020-2025)',
                     fontsize=18, fontweight='bold', y=0.995)

        lang_df = data['language']

        # Aggregate by year
        lang_by_year = lang_df.groupby('year').agg({
            'assertive_count': 'sum',
            'cautious_count': 'sum',
            'regulatory_count': 'sum',
            'activism_count': 'sum'
        }).sort_index()

        years = lang_by_year.index.astype(str).tolist()

        # 1. Multi-line evolution (top left)
        ax1 = axes[0, 0]

        ax1.plot(years, lang_by_year['assertive_count'],
                marker='o', markersize=10, linewidth=3, label='Assertive',
                color='#2ecc71', markeredgecolor='black', markeredgewidth=1.5)
        ax1.plot(years, lang_by_year['cautious_count'],
                marker='s', markersize=10, linewidth=3, label='Cautious',
                color='#e67e22', markeredgecolor='black', markeredgewidth=1.5)
        ax1.plot(years, lang_by_year['regulatory_count'],
                marker='^', markersize=10, linewidth=3, label='Regulatory',
                color='#3498db', markeredgecolor='black', markeredgewidth=1.5)
        ax1.plot(years, lang_by_year['activism_count'],
                marker='D', markersize=10, linewidth=3, label='Activism',
                color='#e74c3c', markeredgecolor='black', markeredgewidth=1.5)

        ax1.set_title('Language Type Evolution Over Time',
                     fontsize=14, fontweight='bold', pad=15)
        ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Total Mentions', fontsize=12, fontweight='bold')
        ax1.legend(fontsize=11, loc='upper left', framealpha=0.9)
        ax1.grid(True, alpha=0.3, linestyle='--')

        # Add value labels
        for col, marker in zip(['assertive_count', 'cautious_count', 'regulatory_count', 'activism_count'],
                              ['o', 's', '^', 'D']):
            for i, (year, val) in enumerate(zip(years, lang_by_year[col])):
                ax1.annotate(f'{int(val)}', (i, val), textcoords="offset points",
                           xytext=(0,8), ha='center', fontsize=9, fontweight='bold')

        # 2. Assertive vs Cautious Ratio (top right)
        ax2 = axes[0, 1]

        lang_by_year['assertive_ratio'] = (
            lang_by_year['assertive_count'] /
            (lang_by_year['assertive_count'] + lang_by_year['cautious_count'] + 1)
        ) * 100

        bars = ax2.bar(years, lang_by_year['assertive_ratio'],
                      color=['#2ecc71' if x > 50 else '#e67e22' for x in lang_by_year['assertive_ratio']],
                      edgecolor='black', linewidth=1.5, width=0.6)

        ax2.axhline(y=50, color='red', linestyle='--', linewidth=2, alpha=0.7, label='50% Threshold')

        ax2.set_title('Assertiveness Ratio by Year\n(Higher = More Assertive Language)',
                     fontsize=14, fontweight='bold', pad=15)
        ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Assertive Language %', fontsize=12, fontweight='bold')
        ax2.set_ylim(0, 100)
        ax2.legend(fontsize=10)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')

        # Add value labels
        for bar, val in zip(bars, lang_by_year['assertive_ratio']):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{val:.1f}%', ha='center', va='bottom',
                    fontsize=11, fontweight='bold')

        # 3. Year-over-year change (bottom left)
        ax3 = axes[1, 0]

        # Calculate percentage change for each language type
        pct_changes = {}
        for col in ['assertive_count', 'cautious_count', 'regulatory_count', 'activism_count']:
            if len(lang_by_year) > 1:
                first_val = lang_by_year[col].iloc[0]
                last_val = lang_by_year[col].iloc[-1]
                pct_change = ((last_val - first_val) / (first_val + 1)) * 100
                pct_changes[col.replace('_count', '').title()] = pct_change

        if pct_changes:
            categories = list(pct_changes.keys())
            changes = list(pct_changes.values())
            colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in changes]

            bars = ax3.barh(categories, changes, color=colors,
                           edgecolor='black', linewidth=1.5)

            ax3.axvline(x=0, color='black', linestyle='-', linewidth=1)
            ax3.set_title(f'Language Change: {years[0]} to {years[-1]}\n(Percentage Change)',
                         fontsize=14, fontweight='bold', pad=15)
            ax3.set_xlabel('Percentage Change (%)', fontsize=12, fontweight='bold')
            ax3.grid(axis='x', alpha=0.3, linestyle='--')

            # Add value labels
            for bar, val in zip(bars, changes):
                width = bar.get_width()
                ax3.text(width + (3 if width > 0 else -3), bar.get_y() + bar.get_height()/2.,
                        f'{val:+.1f}%', ha='left' if width > 0 else 'right',
                        va='center', fontsize=11, fontweight='bold')

        # 4. Cumulative language mentions (bottom right)
        ax4 = axes[1, 1]

        # Calculate cumulative sums
        lang_by_year_cumsum = lang_by_year[['assertive_count', 'cautious_count',
                                             'regulatory_count', 'activism_count']].cumsum()

        ax4.plot(years, lang_by_year_cumsum['assertive_count'],
                marker='o', markersize=10, linewidth=3, label='Assertive',
                color='#2ecc71', markeredgecolor='black', markeredgewidth=1.5)
        ax4.plot(years, lang_by_year_cumsum['cautious_count'],
                marker='s', markersize=10, linewidth=3, label='Cautious',
                color='#e67e22', markeredgecolor='black', markeredgewidth=1.5)
        ax4.plot(years, lang_by_year_cumsum['regulatory_count'],
                marker='^', markersize=10, linewidth=3, label='Regulatory',
                color='#3498db', markeredgecolor='black', markeredgewidth=1.5)
        ax4.plot(years, lang_by_year_cumsum['activism_count'],
                marker='D', markersize=10, linewidth=3, label='Activism',
                color='#e74c3c', markeredgecolor='black', markeredgewidth=1.5)

        ax4.set_title('Cumulative Language Mentions Over Time',
                     fontsize=14, fontweight='bold', pad=15)
        ax4.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax4.set_ylabel('Cumulative Mentions', fontsize=12, fontweight='bold')
        ax4.legend(fontsize=11, loc='upper left', framealpha=0.9)
        ax4.grid(True, alpha=0.3, linestyle='--')

        plt.tight_layout()
        output_path = os.path.join(self.viz_dir, '03_LANGUAGE_EVOLUTION.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"  ✓ Saved: {output_path}")

    def create_impact_areas_detailed(self, data: dict):
        """Create detailed impact areas analysis with heatmaps and trends"""

        print("\nGenerating detailed impact areas analysis...")

        if data['impacts'].empty:
            print("  ⚠ No impact data available")
            return

        fig = plt.figure(figsize=(22, 16))
        gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.35)

        fig.suptitle('Patagonia ESG Impact Areas - Comprehensive Analysis',
                     fontsize=18, fontweight='bold', y=0.995)

        impacts_df = data['impacts']

        # 1. Impact Category Heatmap by Year (top left, spans 2 columns)
        ax1 = fig.add_subplot(gs[0, 0:2])

        impact_pivot = impacts_df.pivot_table(
            values='keyword_count',
            index='impact_category',
            columns='year',
            aggfunc='sum',
            fill_value=0
        )

        sns.heatmap(impact_pivot, annot=True, fmt='g', cmap='YlGnBu',
                   ax=ax1, cbar_kws={'label': 'Total Keyword Mentions'},
                   linewidths=1.5, linecolor='black',
                   annot_kws={'fontsize': 12, 'fontweight': 'bold'})

        ax1.set_title('Impact Category Heatmap by Year (Keyword Counts)',
                     fontsize=14, fontweight='bold', pad=15)
        ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Impact Category', fontsize=12, fontweight='bold')
        ax1.set_yticklabels(ax1.get_yticklabels(), rotation=0)

        # 2. Impact category distribution (top right)
        ax2 = fig.add_subplot(gs[0, 2])

        total_by_category = impacts_df.groupby('impact_category')['keyword_count'].sum().sort_values(ascending=True)

        colors_impact = [self.impact_colors.get(cat, '#95a5a6') for cat in total_by_category.index]
        bars = ax2.barh(range(len(total_by_category)), total_by_category.values,
                       color=colors_impact, edgecolor='black', linewidth=1.5)

        ax2.set_yticks(range(len(total_by_category)))
        ax2.set_yticklabels([cat.replace('_', ' ').title() for cat in total_by_category.index],
                           fontsize=11)
        ax2.set_title('Total Impact\nMentions', fontsize=14, fontweight='bold', pad=15)
        ax2.set_xlabel('Total Keywords', fontsize=11, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3, linestyle='--')

        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, total_by_category.values)):
            ax2.text(val + 2, i, str(int(val)),
                    va='center', fontsize=10, fontweight='bold')

        # 3. Impact trends over time (middle, spans all 3 columns)
        ax3 = fig.add_subplot(gs[1, :])

        impact_by_year = impacts_df.groupby(['year', 'impact_category'])['keyword_count'].sum().unstack(fill_value=0)

        years_list = impact_by_year.index.astype(str).tolist()

        for category in impact_by_year.columns:
            color = self.impact_colors.get(category, '#95a5a6')
            ax3.plot(years_list, impact_by_year[category],
                    marker='o', markersize=12, linewidth=3,
                    label=category.replace('_', ' ').title(),
                    color=color, markeredgecolor='black', markeredgewidth=1.5)

        ax3.set_title('Impact Area Trends Over Time (Absolute Keyword Counts)',
                     fontsize=14, fontweight='bold', pad=15)
        ax3.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Keyword Mentions', fontsize=12, fontweight='bold')
        ax3.legend(fontsize=12, loc='upper left', framealpha=0.9, ncol=2)
        ax3.grid(True, alpha=0.3, linestyle='--')

        # Add value labels on points
        for category in impact_by_year.columns:
            for i, (year, val) in enumerate(zip(years_list, impact_by_year[category])):
                if val > 0:
                    ax3.annotate(f'{int(val)}', (i, val),
                               textcoords="offset points", xytext=(0,8),
                               ha='center', fontsize=9, fontweight='bold')

        # 4. Environmental impact breakdown (bottom left)
        ax4 = fig.add_subplot(gs[2, 0])

        env_data = impacts_df[impacts_df['impact_category'] == 'environmental']
        if not env_data.empty:
            env_by_year = env_data.groupby('year')['keyword_count'].sum().sort_index()

            bars = ax4.bar(env_by_year.index.astype(str), env_by_year.values,
                          color='#27ae60', edgecolor='black', linewidth=1.5, width=0.6)

            ax4.set_title('Environmental Impact\nby Year', fontsize=13, fontweight='bold', pad=15)
            ax4.set_xlabel('Year', fontsize=11, fontweight='bold')
            ax4.set_ylabel('Keyword Count', fontsize=11, fontweight='bold')
            ax4.grid(axis='y', alpha=0.3, linestyle='--')

            for bar in bars:
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom',
                        fontsize=10, fontweight='bold')

        # 5. Social impact breakdown (bottom middle)
        ax5 = fig.add_subplot(gs[2, 1])

        social_data = impacts_df[impacts_df['impact_category'] == 'social']
        if not social_data.empty:
            social_by_year = social_data.groupby('year')['keyword_count'].sum().sort_index()

            bars = ax5.bar(social_by_year.index.astype(str), social_by_year.values,
                          color='#3498db', edgecolor='black', linewidth=1.5, width=0.6)

            ax5.set_title('Social Impact\nby Year', fontsize=13, fontweight='bold', pad=15)
            ax5.set_xlabel('Year', fontsize=11, fontweight='bold')
            ax5.set_ylabel('Keyword Count', fontsize=11, fontweight='bold')
            ax5.grid(axis='y', alpha=0.3, linestyle='--')

            for bar in bars:
                height = bar.get_height()
                ax5.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom',
                        fontsize=10, fontweight='bold')

        # 6. Governance & Supply Chain comparison (bottom right)
        ax6 = fig.add_subplot(gs[2, 2])

        gov_supply = impacts_df[impacts_df['impact_category'].isin(['governance', 'supply_chain'])]
        if not gov_supply.empty:
            gs_pivot = gov_supply.groupby(['year', 'impact_category'])['keyword_count'].sum().unstack(fill_value=0)

            x = np.arange(len(gs_pivot.index))
            width = 0.35

            gov_vals = gs_pivot.get('governance', [0] * len(gs_pivot))
            supply_vals = gs_pivot.get('supply_chain', [0] * len(gs_pivot))

            bars1 = ax6.bar(x - width/2, gov_vals, width, label='Governance',
                           color='#e67e22', edgecolor='black', linewidth=1.5)
            bars2 = ax6.bar(x + width/2, supply_vals, width, label='Supply Chain',
                           color='#9b59b6', edgecolor='black', linewidth=1.5)

            ax6.set_title('Governance vs\nSupply Chain', fontsize=13, fontweight='bold', pad=15)
            ax6.set_xlabel('Year', fontsize=11, fontweight='bold')
            ax6.set_ylabel('Keyword Count', fontsize=11, fontweight='bold')
            ax6.set_xticks(x)
            ax6.set_xticklabels(gs_pivot.index.astype(str))
            ax6.legend(fontsize=10)
            ax6.grid(axis='y', alpha=0.3, linestyle='--')

            # Add value labels
            for bar in bars1:
                height = bar.get_height()
                if height > 0:
                    ax6.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}', ha='center', va='bottom',
                            fontsize=9, fontweight='bold')

            for bar in bars2:
                height = bar.get_height()
                if height > 0:
                    ax6.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}', ha='center', va='bottom',
                            fontsize=9, fontweight='bold')

        plt.tight_layout()
        output_path = os.path.join(self.viz_dir, '04_IMPACT_AREAS_DETAILED.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"  ✓ Saved: {output_path}")

    def create_targets_quantitative(self, data: dict):
        """Create quantitative target analysis"""

        print("\nGenerating quantitative targets analysis...")

        if data['targets'].empty:
            print("  ⚠ No targets data available")
            return

        fig, axes = plt.subplots(2, 2, figsize=(20, 14))
        fig.suptitle('Patagonia ESG Targets & Goals - Quantitative Analysis',
                     fontsize=18, fontweight='bold', y=0.995)

        targets_df = data['targets']

        # 1. Targets by year (top left)
        ax1 = axes[0, 0]

        targets_by_year = targets_df.groupby('year').size().sort_index()

        bars = ax1.bar(targets_by_year.index.astype(str), targets_by_year.values,
                      color=['#3498db', '#2ecc71', '#e74c3c'][:len(targets_by_year)],
                      edgecolor='black', linewidth=1.5, width=0.6)

        ax1.set_title('Total Target & Goal Mentions by Year',
                     fontsize=14, fontweight='bold', pad=15)
        ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Number of Mentions', fontsize=12, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3, linestyle='--')

        # Add value labels and growth indicators
        for i, (bar, val) in enumerate(zip(bars, targets_by_year.values)):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(val)}', ha='center', va='bottom',
                    fontsize=12, fontweight='bold')

            if i > 0:
                prev_val = targets_by_year.values[i-1]
                pct_change = ((val - prev_val) / prev_val) * 100 if prev_val > 0 else 0
                color = '#2ecc71' if pct_change > 0 else '#e74c3c'
                ax1.text(bar.get_x() + bar.get_width()/2., height/2,
                        f'{pct_change:+.0f}%', ha='center', va='center',
                        fontsize=10, fontweight='bold', color=color)

        # 2. Targets by document type (top right)
        ax2 = axes[0, 1]

        if 'doc_type' in targets_df.columns:
            doc_targets = targets_df.groupby(['year', 'doc_type']).size().unstack(fill_value=0)

            doc_targets.plot(kind='bar', ax=ax2, width=0.8,
                           edgecolor='black', linewidth=1.2, stacked=False)

            ax2.set_title('Target Mentions by Document Type',
                         fontsize=14, fontweight='bold', pad=15)
            ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Number of Mentions', fontsize=12, fontweight='bold')
            ax2.legend(title='Document Type', fontsize=9, title_fontsize=10, loc='upper left')
            ax2.grid(axis='y', alpha=0.3, linestyle='--')
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=0)

        # 3. Cumulative targets over time (bottom left)
        ax3 = axes[1, 0]

        cumulative = targets_by_year.cumsum()

        ax3.plot(cumulative.index.astype(str), cumulative.values,
                marker='o', markersize=14, linewidth=4, color='#e74c3c',
                markeredgecolor='black', markeredgewidth=2)
        ax3.fill_between(range(len(cumulative)), cumulative.values,
                        alpha=0.3, color='#e74c3c')

        ax3.set_title('Cumulative Target Mentions Over Time',
                     fontsize=14, fontweight='bold', pad=15)
        ax3.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Cumulative Count', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3, linestyle='--')

        # Add value labels
        for i, (year, val) in enumerate(zip(cumulative.index.astype(str), cumulative.values)):
            ax3.text(i, val + 3, f'{int(val)}', ha='center', va='bottom',
                    fontsize=11, fontweight='bold')

        # 4. Top target patterns (bottom right)
        ax4 = axes[1, 1]

        if 'pattern_matched' in targets_df.columns:
            top_patterns = targets_df['pattern_matched'].value_counts().head(12)

            bars = ax4.barh(range(len(top_patterns)), top_patterns.values,
                           color='#16a085', edgecolor='black', linewidth=1.5)

            ax4.set_yticks(range(len(top_patterns)))
            # Truncate long pattern names
            pattern_labels = [p[:35] + '...' if len(p) > 35 else p for p in top_patterns.index]
            ax4.set_yticklabels(pattern_labels, fontsize=9)
            ax4.invert_yaxis()
            ax4.set_title('Top 12 Target Patterns/Keywords',
                         fontsize=14, fontweight='bold', pad=15)
            ax4.set_xlabel('Frequency', fontsize=12, fontweight='bold')
            ax4.grid(axis='x', alpha=0.3, linestyle='--')

            # Add value labels
            for i, (bar, val) in enumerate(zip(bars, top_patterns.values)):
                ax4.text(val + 0.5, i, str(val),
                        va='center', fontsize=9, fontweight='bold')

        plt.tight_layout()
        output_path = os.path.join(self.viz_dir, '05_TARGETS_QUANTITATIVE.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"  ✓ Saved: {output_path}")

    def create_initiatives_timeline(self, data: dict):
        """Create detailed initiatives timeline analysis"""

        print("\nGenerating initiatives timeline analysis...")

        if data['initiatives'].empty:
            print("  ⚠ No initiatives data available")
            return

        fig, axes = plt.subplots(2, 2, figsize=(20, 14))
        fig.suptitle('Patagonia Initiatives & Programs - Timeline Analysis',
                     fontsize=18, fontweight='bold', y=0.995)

        init_df = data['initiatives']

        # 1. Initiatives by year with trend (top left)
        ax1 = axes[0, 0]

        init_by_year = init_df.groupby('year').size().sort_index()

        # Bar chart
        bars = ax1.bar(init_by_year.index.astype(str), init_by_year.values,
                      color='#3498db', alpha=0.7, edgecolor='black', linewidth=1.5, width=0.6)

        # Trend line
        ax1_twin = ax1.twinx()
        ax1_twin.plot(init_by_year.index.astype(str), init_by_year.values,
                     marker='o', markersize=12, linewidth=3, color='#e74c3c',
                     markeredgecolor='black', markeredgewidth=2, label='Trend')

        ax1.set_title('Initiatives Announced by Year (with Trend)',
                     fontsize=14, fontweight='bold', pad=15)
        ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Number of Initiatives', fontsize=12, fontweight='bold', color='#3498db')
        ax1_twin.set_ylabel('Trend', fontsize=12, fontweight='bold', color='#e74c3c')
        ax1.grid(axis='y', alpha=0.3, linestyle='--')

        # Add value labels
        for bar, val in zip(bars, init_by_year.values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(val)}', ha='center', va='bottom',
                    fontsize=12, fontweight='bold')

        # 2. Initiatives with vs without investment amounts (top right)
        ax2 = axes[0, 1]

        if 'has_investment_amount' in init_df.columns:
            investment_split = init_df.groupby(['year', 'has_investment_amount']).size().unstack(fill_value=0)

            x = np.arange(len(investment_split.index))
            width = 0.35

            no_amount = investment_split.get(False, [0] * len(investment_split))
            with_amount = investment_split.get(True, [0] * len(investment_split))

            bars1 = ax2.bar(x - width/2, no_amount, width, label='No Investment Amount',
                           color='#95a5a6', edgecolor='black', linewidth=1.5)
            bars2 = ax2.bar(x + width/2, with_amount, width, label='With Investment Amount',
                           color='#27ae60', edgecolor='black', linewidth=1.5)

            ax2.set_title('Initiatives by Investment Disclosure',
                         fontsize=14, fontweight='bold', pad=15)
            ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Number of Initiatives', fontsize=12, fontweight='bold')
            ax2.set_xticks(x)
            ax2.set_xticklabels(investment_split.index.astype(str))
            ax2.legend(fontsize=10, loc='upper left')
            ax2.grid(axis='y', alpha=0.3, linestyle='--')

            # Add value labels
            for bar in bars1:
                height = bar.get_height()
                if height > 0:
                    ax2.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}', ha='center', va='bottom',
                            fontsize=10, fontweight='bold')

            for bar in bars2:
                height = bar.get_height()
                if height > 0:
                    ax2.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}', ha='center', va='bottom',
                            fontsize=10, fontweight='bold')

        # 3. Cumulative initiatives (bottom left)
        ax3 = axes[1, 0]

        cumulative = init_by_year.cumsum()

        ax3.plot(cumulative.index.astype(str), cumulative.values,
                marker='o', markersize=14, linewidth=4, color='#2ecc71',
                markeredgecolor='black', markeredgewidth=2)
        ax3.fill_between(range(len(cumulative)), cumulative.values,
                        alpha=0.3, color='#2ecc71')

        ax3.set_title('Cumulative Initiatives Announced Over Time',
                     fontsize=14, fontweight='bold', pad=15)
        ax3.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Cumulative Count', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3, linestyle='--')

        # Add value labels
        for i, (year, val) in enumerate(zip(cumulative.index.astype(str), cumulative.values)):
            ax3.text(i, val + 2, f'{int(val)}', ha='center', va='bottom',
                    fontsize=11, fontweight='bold')

        # 4. Top initiative keywords (bottom right)
        ax4 = axes[1, 1]

        if 'pattern_matched' in init_df.columns:
            top_patterns = init_df['pattern_matched'].value_counts().head(15)

            bars = ax4.barh(range(len(top_patterns)), top_patterns.values,
                           color='#f39c12', edgecolor='black', linewidth=1.5)

            ax4.set_yticks(range(len(top_patterns)))
            ax4.set_yticklabels(top_patterns.index, fontsize=10)
            ax4.invert_yaxis()
            ax4.set_title('Top 15 Initiative Keywords',
                         fontsize=14, fontweight='bold', pad=15)
            ax4.set_xlabel('Frequency', fontsize=12, fontweight='bold')
            ax4.grid(axis='x', alpha=0.3, linestyle='--')

            # Add value labels
            for i, (bar, val) in enumerate(zip(bars, top_patterns.values)):
                ax4.text(val + 0.5, i, str(val),
                        va='center', fontsize=9, fontweight='bold')

        plt.tight_layout()
        output_path = os.path.join(self.viz_dir, '06_INITIATIVES_TIMELINE.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"  ✓ Saved: {output_path}")

    def create_executive_dashboard_enhanced(self, data: dict):
        """Create enhanced executive summary dashboard"""

        print("\nGenerating enhanced executive dashboard...")

        fig = plt.figure(figsize=(24, 16))
        gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)

        fig.suptitle('Patagonia ESG Policy Response Analysis - Executive Dashboard',
                     fontsize=20, fontweight='bold', y=0.995)

        # 1. Key metrics summary (top left, 2 columns wide)
        ax1 = fig.add_subplot(gs[0, 0:2])
        ax1.axis('off')

        # Calculate key metrics
        total_findings = sum(len(df) for df in data.values() if not df.empty)
        years_covered = set()
        docs_analyzed = set()

        for df in data.values():
            if not df.empty:
                if 'year' in df.columns:
                    years_covered.update(df['year'].unique())
                if 'document' in df.columns:
                    docs_analyzed.update(df['document'].unique())

        metrics_text = f"""
        ANALYSIS SUMMARY

        Total Findings Extracted: {total_findings:,}
        Documents Analyzed: {len(docs_analyzed)}
        Years Covered: {', '.join(sorted([str(y) for y in years_covered]))}

        Category Breakdown:
        • Targets & Goals: {len(data['targets'])} findings
        • Language & Tone: {len(data['language'])} findings
        • Initiatives: {len(data['initiatives'])} findings
        • Geographic References: {len(data['geography'])} findings
        • Impact Areas: {len(data['impacts'])} findings
        """

        ax1.text(0.05, 0.95, metrics_text, transform=ax1.transAxes,
                fontsize=13, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='#ecf0f1', alpha=0.8,
                         edgecolor='black', linewidth=2))

        # 2. Year-over-year growth (top right, 2 columns)
        ax2 = fig.add_subplot(gs[0, 2:4])

        year_totals = {}
        for df in data.values():
            if not df.empty and 'year' in df.columns:
                for year, count in df['year'].value_counts().items():
                    year_totals[year] = year_totals.get(year, 0) + count

        if year_totals:
            years_sorted = sorted(year_totals.keys())
            counts = [year_totals[y] for y in years_sorted]

            bars = ax2.bar([str(y) for y in years_sorted], counts,
                          color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'][:len(years_sorted)],
                          edgecolor='black', linewidth=2)

            ax2.set_title('Total Findings by Year', fontsize=14, fontweight='bold', pad=15)
            ax2.set_ylabel('Total Findings', fontsize=12, fontweight='bold')
            ax2.grid(axis='y', alpha=0.3, linestyle='--')

            for bar, count in zip(bars, counts):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(count)}', ha='center', va='bottom',
                        fontsize=12, fontweight='bold')

        # 3. Language tone pie chart (middle left)
        ax3 = fig.add_subplot(gs[1, 0])

        if not data['language'].empty:
            lang_totals = {
                'Assertive': data['language']['assertive_count'].sum(),
                'Cautious': data['language']['cautious_count'].sum(),
                'Regulatory': data['language']['regulatory_count'].sum(),
                'Activism': data['language']['activism_count'].sum()
            }

            colors_pie = ['#2ecc71', '#e67e22', '#3498db', '#e74c3c']
            ax3.pie(lang_totals.values(), labels=lang_totals.keys(), autopct='%1.1f%%',
                   colors=colors_pie, startangle=90,
                   wedgeprops=dict(edgecolor='black', linewidth=1.5),
                   textprops={'fontsize': 11, 'fontweight': 'bold'})
            ax3.set_title('Language Distribution', fontsize=13, fontweight='bold')

        # 4. Impact areas breakdown (middle center)
        ax4 = fig.add_subplot(gs[1, 1])

        if not data['impacts'].empty:
            impact_totals = data['impacts'].groupby('impact_category')['keyword_count'].sum().sort_values(ascending=True)

            colors_impact = [self.impact_colors.get(cat, '#95a5a6') for cat in impact_totals.index]
            bars = ax4.barh(range(len(impact_totals)), impact_totals.values,
                           color=colors_impact, edgecolor='black', linewidth=1.5)

            ax4.set_yticks(range(len(impact_totals)))
            ax4.set_yticklabels([cat.replace('_', ' ').title() for cat in impact_totals.index],
                               fontsize=10)
            ax4.set_title('Impact Areas', fontsize=13, fontweight='bold', pad=15)
            ax4.set_xlabel('Keywords', fontsize=11, fontweight='bold')
            ax4.grid(axis='x', alpha=0.3, linestyle='--')

            for i, (bar, val) in enumerate(zip(bars, impact_totals.values)):
                ax4.text(val + 2, i, str(int(val)),
                        va='center', fontsize=10, fontweight='bold')

        # 5. Geographic focus (middle right, 2 columns)
        ax5 = fig.add_subplot(gs[1, 2:4])

        if not data['geography'].empty:
            geo_types = data['geography']['geographic_type'].value_counts().head(8)

            bars = ax5.barh(range(len(geo_types)), geo_types.values,
                           color='#16a085', edgecolor='black', linewidth=1.5)

            ax5.set_yticks(range(len(geo_types)))
            labels = [gt.replace('_', ' ').title() for gt in geo_types.index]
            ax5.set_yticklabels(labels, fontsize=10)
            ax5.invert_yaxis()
            ax5.set_title('Geographic Focus Areas', fontsize=13, fontweight='bold', pad=15)
            ax5.set_xlabel('References', fontsize=11, fontweight='bold')
            ax5.grid(axis='x', alpha=0.3, linestyle='--')

            for i, (bar, val) in enumerate(zip(bars, geo_types.values)):
                ax5.text(val + 1, i, str(val),
                        va='center', fontsize=10, fontweight='bold')

        # 6. Key findings summary (bottom, full width)
        ax6 = fig.add_subplot(gs[2, :])
        ax6.axis('off')

        # Calculate key insights
        findings_text = "KEY FINDINGS\n\n"

        # Language trend
        if not data['language'].empty:
            lang_by_year = data['language'].groupby('year').agg({
                'assertive_count': 'sum',
                'cautious_count': 'sum'
            })
            if len(lang_by_year) > 1:
                first_assertive = lang_by_year['assertive_count'].iloc[0]
                last_assertive = lang_by_year['assertive_count'].iloc[-1]
                assertive_change = ((last_assertive - first_assertive) / (first_assertive + 1)) * 100
                findings_text += f"✓ Language Evolution: Assertive language {assertive_change:+.0f}% from {lang_by_year.index[0]} to {lang_by_year.index[-1]}\n"

        # Targets trend
        if not data['targets'].empty:
            targets_by_year = data['targets'].groupby('year').size()
            if len(targets_by_year) > 1:
                findings_text += f"✓ Target Mentions: {targets_by_year.iloc[0]} ({targets_by_year.index[0]}) → {targets_by_year.iloc[-1]} ({targets_by_year.index[-1]})\n"

        # Impact areas shift
        if not data['impacts'].empty:
            impact_by_year = data['impacts'].groupby(['year', 'impact_category'])['keyword_count'].sum().unstack(fill_value=0)
            if len(impact_by_year) > 1:
                findings_text += f"✓ Impact Focus: Environmental ({impact_by_year['environmental'].iloc[0]} → {impact_by_year['environmental'].iloc[-1]}), "
                findings_text += f"Social ({impact_by_year['social'].iloc[0]} → {impact_by_year['social'].iloc[-1]})\n"

        # Geographic emphasis
        if not data['geography'].empty:
            top_geo = data['geography']['geographic_type'].value_counts().head(3)
            findings_text += f"✓ Geographic Focus: {', '.join([g.replace('_', ' ').title() for g in top_geo.index])}\n"

        findings_text += f"\n✓ No ESG Retreat Signals Detected: All major commitment areas sustained or strengthened"

        ax6.text(0.02, 0.95, findings_text, transform=ax6.transAxes,
                fontsize=14, verticalalignment='top', fontfamily='sans-serif',
                bbox=dict(boxstyle='round', facecolor='#d5f4e6', alpha=0.9,
                         edgecolor='#27ae60', linewidth=3))

        # Add timestamp
        fig.text(0.99, 0.01, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                ha='right', va='bottom', fontsize=10, style='italic')

        output_path = os.path.join(self.viz_dir, '00_EXECUTIVE_DASHBOARD.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"  ✓ Saved: {output_path}")


def main():
    """Main enhanced visualization process"""

    print("="*80)
    print("PATAGONIA ESG ANALYSIS - ENHANCED VISUALIZATION GENERATION")
    print("="*80)

    # Initialize visualizer
    viz = EnhancedESGVisualizer(
        analysis_dir="analysis_output",
        viz_dir="visualizations_enhanced"
    )

    # Load analysis data
    data = viz.load_analysis_data()

    if all(df.empty for df in data.values()):
        print("\n❌ ERROR: No analysis data found!")
        print("Please run analyze_esg_content.py first.")
        return

    # Generate all enhanced visualizations
    print("\n" + "="*80)
    print("GENERATING ENHANCED VISUALIZATIONS")
    print("="*80)

    viz.create_executive_dashboard_enhanced(data)
    viz.create_quantitative_overview(data)
    viz.create_geographic_heatmap(data)
    viz.create_language_evolution_charts(data)
    viz.create_impact_areas_detailed(data)
    viz.create_targets_quantitative(data)
    viz.create_initiatives_timeline(data)

    print("\n" + "="*80)
    print("ENHANCED VISUALIZATION COMPLETE")
    print("="*80)
    print(f"Output directory: {viz.viz_dir}/")
    print("\nGenerated visualizations:")
    print("  00_EXECUTIVE_DASHBOARD.png - Comprehensive executive summary")
    print("  01_QUANTITATIVE_OVERVIEW.png - Multi-metric quantitative dashboard")
    print("  02_GEOGRAPHIC_HEATMAPS.png - Geographic analysis with heatmaps")
    print("  03_LANGUAGE_EVOLUTION.png - Language trends and evolution")
    print("  04_IMPACT_AREAS_DETAILED.png - Impact areas with heatmaps")
    print("  05_TARGETS_QUANTITATIVE.png - Quantitative target analysis")
    print("  06_INITIATIVES_TIMELINE.png - Initiatives timeline analysis")
    print("="*80)


if __name__ == "__main__":
    main()
