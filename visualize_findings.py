#!/usr/bin/env python3
"""
Patagonia ESG Analysis - Data Visualization
Author: Analysis Team
Date: November 13, 2025
Purpose: Generate comprehensive visualizations of ESG policy response trends
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
except ImportError as e:
    print("Installing required packages...")
    os.system("pip install -q pandas numpy matplotlib seaborn")
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from datetime import datetime


class ESGVisualizer:
    """Create visualizations for Patagonia ESG analysis"""

    def __init__(self, analysis_dir="analysis_output", viz_dir="visualizations"):
        self.analysis_dir = analysis_dir
        self.viz_dir = viz_dir
        os.makedirs(viz_dir, exist_ok=True)

        # Set visualization style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
        self.colors = {
            '2020': '#1f77b4',
            '2021': '#ff7f0e',
            '2024': '#2ca02c',
            '2025': '#d62728'
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

    def plot_language_tone_trends(self, df: pd.DataFrame):
        """Visualize language and tone patterns over time"""

        if df.empty:
            print("  ⚠ No language data to visualize")
            return

        print("\nGenerating language & tone visualizations...")

        # Aggregate by year
        tone_by_year = df.groupby('year').agg({
            'assertive_count': 'sum',
            'cautious_count': 'sum',
            'regulatory_count': 'sum',
            'activism_count': 'sum'
        }).reset_index()

        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Patagonia ESG Language & Tone Evolution (2020-2025)',
                     fontsize=16, fontweight='bold', y=0.995)

        # 1. Stacked bar chart of all tone types
        ax1 = axes[0, 0]
        tone_columns = ['assertive_count', 'cautious_count', 'regulatory_count', 'activism_count']
        tone_by_year.plot(x='year', y=tone_columns, kind='bar', stacked=True, ax=ax1)
        ax1.set_title('Language Distribution by Year (Stacked)', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Year', fontsize=11)
        ax1.set_ylabel('Frequency Count', fontsize=11)
        ax1.legend(['Assertive', 'Cautious', 'Regulatory', 'Activism'],
                   loc='upper left', fontsize=9)
        ax1.grid(axis='y', alpha=0.3)

        # 2. Line chart showing trends
        ax2 = axes[0, 1]
        for col in tone_columns:
            label = col.replace('_count', '').title()
            ax2.plot(tone_by_year['year'], tone_by_year[col],
                    marker='o', linewidth=2, markersize=8, label=label)
        ax2.set_title('Language Trend Lines', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Year', fontsize=11)
        ax2.set_ylabel('Frequency Count', fontsize=11)
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3)

        # 3. Assertive vs Cautious ratio
        ax3 = axes[1, 0]
        tone_by_year['assertive_ratio'] = (
            tone_by_year['assertive_count'] /
            (tone_by_year['assertive_count'] + tone_by_year['cautious_count'] + 1)
        ) * 100
        bars = ax3.bar(tone_by_year['year'].astype(str), tone_by_year['assertive_ratio'],
                      color=['#2ca02c' if x > 50 else '#d62728' for x in tone_by_year['assertive_ratio']])
        ax3.axhline(y=50, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax3.set_title('Assertiveness Ratio (Higher = More Assertive)', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Year', fontsize=11)
        ax3.set_ylabel('Assertive %', fontsize=11)
        ax3.set_ylim(0, 100)
        ax3.grid(axis='y', alpha=0.3)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=9)

        # 4. Dominant tone distribution
        ax4 = axes[1, 1]
        if 'dominant_tone' in df.columns:
            tone_counts = df['dominant_tone'].value_counts()
            colors_pie = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
            ax4.pie(tone_counts.values, labels=tone_counts.index, autopct='%1.1f%%',
                   colors=colors_pie, startangle=90)
            ax4.set_title('Overall Dominant Tone Distribution', fontsize=12, fontweight='bold')

        plt.tight_layout()
        output_path = os.path.join(self.viz_dir, 'language_tone_analysis.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Saved: {output_path}")

    def plot_target_mentions_over_time(self, df: pd.DataFrame):
        """Visualize target and goal mentions over time"""

        if df.empty:
            print("  ⚠ No target data to visualize")
            return

        print("\nGenerating target & goals visualizations...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Patagonia ESG Targets & Goals Evolution (2020-2025)',
                     fontsize=16, fontweight='bold', y=0.995)

        # 1. Total mentions by year
        ax1 = axes[0, 0]
        mentions_by_year = df.groupby('year').size()
        bars = ax1.bar(mentions_by_year.index.astype(str), mentions_by_year.values,
                      color=[self.colors.get(str(y), '#888888') for y in mentions_by_year.index])
        ax1.set_title('Target/Goal Mentions by Year', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Year', fontsize=11)
        ax1.set_ylabel('Number of Mentions', fontsize=11)
        ax1.grid(axis='y', alpha=0.3)

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=10)

        # 2. Mentions by document type
        ax2 = axes[0, 1]
        if 'doc_type' in df.columns:
            doc_type_counts = df.groupby(['year', 'doc_type']).size().unstack(fill_value=0)
            doc_type_counts.plot(kind='bar', ax=ax2, width=0.8)
            ax2.set_title('Targets by Document Type', fontsize=12, fontweight='bold')
            ax2.set_xlabel('Year', fontsize=11)
            ax2.set_ylabel('Number of Mentions', fontsize=11)
            ax2.legend(fontsize=9, loc='best')
            ax2.grid(axis='y', alpha=0.3)
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

        # 3. Average page density (mentions per page)
        ax3 = axes[1, 0]
        if 'page_number' in df.columns:
            page_density = df.groupby('year').agg({
                'page_number': lambda x: len(x) / x.nunique() if x.nunique() > 0 else 0
            }).reset_index()
            page_density.columns = ['year', 'mentions_per_page']
            bars = ax3.bar(page_density['year'].astype(str), page_density['mentions_per_page'],
                          color=[self.colors.get(str(y), '#888888') for y in page_density['year']])
            ax3.set_title('Target Mention Density (Mentions per Page)', fontsize=12, fontweight='bold')
            ax3.set_xlabel('Year', fontsize=11)
            ax3.set_ylabel('Mentions per Page', fontsize=11)
            ax3.grid(axis='y', alpha=0.3)

            for bar in bars:
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.2f}', ha='center', va='bottom', fontsize=9)

        # 4. Word cloud style - most common patterns
        ax4 = axes[1, 1]
        if 'pattern_matched' in df.columns:
            pattern_counts = df['pattern_matched'].value_counts().head(15)
            y_pos = np.arange(len(pattern_counts))
            ax4.barh(y_pos, pattern_counts.values, color='steelblue')
            ax4.set_yticks(y_pos)
            ax4.set_yticklabels(pattern_counts.index, fontsize=8)
            ax4.invert_yaxis()
            ax4.set_title('Top 15 Most Common Target Patterns', fontsize=12, fontweight='bold')
            ax4.set_xlabel('Frequency', fontsize=11)
            ax4.grid(axis='x', alpha=0.3)

        plt.tight_layout()
        output_path = os.path.join(self.viz_dir, 'targets_goals_analysis.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Saved: {output_path}")

    def plot_geographic_distribution(self, df: pd.DataFrame):
        """Visualize geographic focus and distribution"""

        if df.empty:
            print("  ⚠ No geographic data to visualize")
            return

        print("\nGenerating geographic distribution visualizations...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Patagonia Geographic Focus Analysis (2020-2025)',
                     fontsize=16, fontweight='bold', y=0.995)

        # 1. Geographic type distribution over time
        ax1 = axes[0, 0]
        geo_by_year = df.groupby(['year', 'geographic_type']).size().unstack(fill_value=0)
        geo_by_year.plot(kind='bar', ax=ax1, width=0.8)
        ax1.set_title('Geographic References by Type and Year', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Year', fontsize=11)
        ax1.set_ylabel('Number of References', fontsize=11)
        ax1.legend(fontsize=9, loc='best')
        ax1.grid(axis='y', alpha=0.3)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

        # 2. US Red vs Blue states comparison
        ax2 = axes[0, 1]
        us_states = df[df['geographic_type'].isin(['us_states_red', 'us_states_blue'])]
        if not us_states.empty:
            state_comparison = us_states.groupby(['year', 'geographic_type']).size().unstack(fill_value=0)
            state_comparison.plot(kind='bar', ax=ax2, color=['#d62728', '#1f77b4'], width=0.7)
            ax2.set_title('US Red States vs Blue States References', fontsize=12, fontweight='bold')
            ax2.set_xlabel('Year', fontsize=11)
            ax2.set_ylabel('Number of References', fontsize=11)
            ax2.legend(['Red States', 'Blue States'], fontsize=10)
            ax2.grid(axis='y', alpha=0.3)
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

        # 3. EU vs US references
        ax3 = axes[1, 0]
        us_eu = df.copy()
        us_eu['region'] = us_eu['geographic_type'].apply(
            lambda x: 'EU' if 'eu' in str(x).lower() else ('US' if 'us' in str(x).lower() else 'Other')
        )
        region_by_year = us_eu.groupby(['year', 'region']).size().unstack(fill_value=0)
        region_by_year.plot(kind='line', ax=ax3, marker='o', linewidth=2, markersize=8)
        ax3.set_title('US vs EU References Over Time', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Year', fontsize=11)
        ax3.set_ylabel('Number of References', fontsize=11)
        ax3.legend(fontsize=10)
        ax3.grid(True, alpha=0.3)

        # 4. Top countries mentioned
        ax4 = axes[1, 1]
        countries = df[df['geographic_type'] == 'countries']
        if not countries.empty:
            top_countries = countries['location'].value_counts().head(10)
            y_pos = np.arange(len(top_countries))
            ax4.barh(y_pos, top_countries.values, color='teal')
            ax4.set_yticks(y_pos)
            ax4.set_yticklabels(top_countries.index, fontsize=9)
            ax4.invert_yaxis()
            ax4.set_title('Top 10 Countries Mentioned', fontsize=12, fontweight='bold')
            ax4.set_xlabel('Frequency', fontsize=11)
            ax4.grid(axis='x', alpha=0.3)

        plt.tight_layout()
        output_path = os.path.join(self.viz_dir, 'geographic_distribution.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Saved: {output_path}")

    def plot_impact_areas(self, df: pd.DataFrame):
        """Visualize ESG impact area focus"""

        if df.empty:
            print("  ⚠ No impact area data to visualize")
            return

        print("\nGenerating impact areas visualizations...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Patagonia ESG Impact Areas Analysis (2020-2025)',
                     fontsize=16, fontweight='bold', y=0.995)

        # 1. Impact category trends over time
        ax1 = axes[0, 0]
        impact_by_year = df.groupby(['year', 'impact_category'])['keyword_count'].sum().unstack(fill_value=0)
        impact_by_year.plot(kind='area', ax=ax1, alpha=0.7, stacked=True)
        ax1.set_title('Impact Area Focus Over Time (Stacked Area)', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Year', fontsize=11)
        ax1.set_ylabel('Keyword Mentions', fontsize=11)
        ax1.legend(fontsize=9, loc='upper left')
        ax1.grid(True, alpha=0.3)

        # 2. Impact category comparison
        ax2 = axes[0, 1]
        impact_totals = df.groupby('impact_category')['keyword_count'].sum().sort_values(ascending=False)
        colors_impact = ['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728']
        ax2.bar(range(len(impact_totals)), impact_totals.values, color=colors_impact)
        ax2.set_xticks(range(len(impact_totals)))
        ax2.set_xticklabels(impact_totals.index, rotation=45, ha='right', fontsize=10)
        ax2.set_title('Total Impact Area Mentions (All Years)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Total Keyword Mentions', fontsize=11)
        ax2.grid(axis='y', alpha=0.3)

        # Add value labels
        for i, v in enumerate(impact_totals.values):
            ax2.text(i, v, f'{int(v)}', ha='center', va='bottom', fontsize=9)

        # 3. Year-over-year change
        ax3 = axes[1, 0]
        if len(impact_by_year) > 1:
            # Calculate percentage change from first to last year
            years = sorted(impact_by_year.index)
            first_year = years[0]
            last_year = years[-1]

            pct_change = ((impact_by_year.loc[last_year] - impact_by_year.loc[first_year]) /
                         (impact_by_year.loc[first_year] + 1) * 100)

            colors_change = ['#2ca02c' if x > 0 else '#d62728' for x in pct_change.values]
            bars = ax3.bar(range(len(pct_change)), pct_change.values, color=colors_change)
            ax3.set_xticks(range(len(pct_change)))
            ax3.set_xticklabels(pct_change.index, rotation=45, ha='right', fontsize=10)
            ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
            ax3.set_title(f'Impact Area Change: {first_year} to {last_year}', fontsize=12, fontweight='bold')
            ax3.set_ylabel('Percentage Change (%)', fontsize=11)
            ax3.grid(axis='y', alpha=0.3)

            # Add value labels
            for bar in bars:
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}%', ha='center',
                        va='bottom' if height > 0 else 'top', fontsize=9)

        # 4. Heatmap of impact areas by year
        ax4 = axes[1, 1]
        pivot_data = df.pivot_table(values='keyword_count', index='impact_category',
                                    columns='year', aggfunc='sum', fill_value=0)
        sns.heatmap(pivot_data, annot=True, fmt='g', cmap='YlOrRd', ax=ax4,
                   cbar_kws={'label': 'Keyword Count'})
        ax4.set_title('Impact Areas Heatmap by Year', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Year', fontsize=11)
        ax4.set_ylabel('Impact Category', fontsize=11)

        plt.tight_layout()
        output_path = os.path.join(self.viz_dir, 'impact_areas_analysis.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Saved: {output_path}")

    def plot_initiatives_timeline(self, df: pd.DataFrame):
        """Visualize initiatives announced over time"""

        if df.empty:
            print("  ⚠ No initiatives data to visualize")
            return

        print("\nGenerating initiatives visualizations...")

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Patagonia Initiatives & Programs Analysis (2020-2025)',
                     fontsize=16, fontweight='bold', y=0.995)

        # 1. Total initiatives by year
        ax1 = axes[0, 0]
        initiatives_by_year = df.groupby('year').size()
        bars = ax1.bar(initiatives_by_year.index.astype(str), initiatives_by_year.values,
                      color=[self.colors.get(str(y), '#888888') for y in initiatives_by_year.index])
        ax1.set_title('Initiative Mentions by Year', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Year', fontsize=11)
        ax1.set_ylabel('Number of Mentions', fontsize=11)
        ax1.grid(axis='y', alpha=0.3)

        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=10)

        # 2. Initiatives with vs without investment amounts
        ax2 = axes[0, 1]
        if 'has_investment_amount' in df.columns:
            investment_split = df.groupby(['year', 'has_investment_amount']).size().unstack(fill_value=0)
            investment_split.plot(kind='bar', ax=ax2, color=['#ff7f0e', '#2ca02c'], width=0.7)
            ax2.set_title('Initiatives with Investment Amounts', fontsize=12, fontweight='bold')
            ax2.set_xlabel('Year', fontsize=11)
            ax2.set_ylabel('Number of Initiatives', fontsize=11)
            ax2.legend(['No Amount', 'With Amount'], fontsize=10)
            ax2.grid(axis='y', alpha=0.3)
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

        # 3. Cumulative initiatives over time
        ax3 = axes[1, 0]
        cumulative = initiatives_by_year.cumsum()
        ax3.plot(cumulative.index.astype(str), cumulative.values,
                marker='o', linewidth=3, markersize=10, color='#2ca02c')
        ax3.fill_between(range(len(cumulative)), cumulative.values, alpha=0.3, color='#2ca02c')
        ax3.set_title('Cumulative Initiatives Announced', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Year', fontsize=11)
        ax3.set_ylabel('Cumulative Count', fontsize=11)
        ax3.grid(True, alpha=0.3)

        # Add value labels
        for i, (year, value) in enumerate(zip(cumulative.index.astype(str), cumulative.values)):
            ax3.text(i, value, f'{int(value)}', ha='center', va='bottom', fontsize=10)

        # 4. Most common initiative patterns
        ax4 = axes[1, 1]
        if 'pattern_matched' in df.columns:
            pattern_counts = df['pattern_matched'].value_counts().head(12)
            y_pos = np.arange(len(pattern_counts))
            ax4.barh(y_pos, pattern_counts.values, color='darkorange')
            ax4.set_yticks(y_pos)
            ax4.set_yticklabels(pattern_counts.index, fontsize=9)
            ax4.invert_yaxis()
            ax4.set_title('Top Initiative Keywords', fontsize=12, fontweight='bold')
            ax4.set_xlabel('Frequency', fontsize=11)
            ax4.grid(axis='x', alpha=0.3)

        plt.tight_layout()
        output_path = os.path.join(self.viz_dir, 'initiatives_analysis.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Saved: {output_path}")

    def create_executive_dashboard(self, data: dict):
        """Create a single-page executive summary dashboard"""

        print("\nGenerating executive dashboard...")

        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

        fig.suptitle('Patagonia ESG Policy Response: Executive Dashboard (2020-2025)',
                     fontsize=18, fontweight='bold', y=0.98)

        # 1. Overall data availability
        ax1 = fig.add_subplot(gs[0, 0])
        data_counts = {k: len(v) for k, v in data.items() if not v.empty}
        ax1.bar(range(len(data_counts)), data_counts.values(), color='steelblue')
        ax1.set_xticks(range(len(data_counts)))
        ax1.set_xticklabels([k.title() for k in data_counts.keys()], rotation=45, ha='right')
        ax1.set_title('Data Extraction Summary', fontweight='bold')
        ax1.set_ylabel('Records Extracted')
        ax1.grid(axis='y', alpha=0.3)

        # 2. Language tone summary
        ax2 = fig.add_subplot(gs[0, 1])
        if not data['language'].empty:
            lang_df = data['language']
            tone_totals = {
                'Assertive': lang_df['assertive_count'].sum(),
                'Cautious': lang_df['cautious_count'].sum(),
                'Regulatory': lang_df['regulatory_count'].sum(),
                'Activism': lang_df['activism_count'].sum()
            }
            ax2.pie(tone_totals.values(), labels=tone_totals.keys(), autopct='%1.1f%%',
                   startangle=90, colors=['#2ca02c', '#ff7f0e', '#1f77b4', '#d62728'])
            ax2.set_title('Overall Language Distribution', fontweight='bold')

        # 3. Geographic focus
        ax3 = fig.add_subplot(gs[0, 2])
        if not data['geography'].empty:
            geo_df = data['geography']
            geo_totals = geo_df['geographic_type'].value_counts().head(5)
            ax3.barh(range(len(geo_totals)), geo_totals.values, color='teal')
            ax3.set_yticks(range(len(geo_totals)))
            ax3.set_yticklabels(geo_totals.index)
            ax3.invert_yaxis()
            ax3.set_title('Top Geographic References', fontweight='bold')
            ax3.set_xlabel('Count')
            ax3.grid(axis='x', alpha=0.3)

        # 4. Targets over time
        ax4 = fig.add_subplot(gs[1, :2])
        if not data['targets'].empty:
            targets_by_year = data['targets'].groupby('year').size()
            ax4.plot(targets_by_year.index, targets_by_year.values,
                    marker='o', linewidth=3, markersize=10, color='#d62728')
            ax4.fill_between(targets_by_year.index, targets_by_year.values, alpha=0.3, color='#d62728')
            ax4.set_title('Target & Goal Mentions Over Time', fontweight='bold', fontsize=12)
            ax4.set_xlabel('Year')
            ax4.set_ylabel('Number of Mentions')
            ax4.grid(True, alpha=0.3)

        # 5. Impact areas
        ax5 = fig.add_subplot(gs[1, 2])
        if not data['impacts'].empty:
            impact_totals = data['impacts'].groupby('impact_category')['keyword_count'].sum()
            ax5.bar(range(len(impact_totals)), impact_totals.values,
                   color=['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728'])
            ax5.set_xticks(range(len(impact_totals)))
            ax5.set_xticklabels(impact_totals.index, rotation=45, ha='right')
            ax5.set_title('Impact Area Focus', fontweight='bold')
            ax5.set_ylabel('Keyword Count')
            ax5.grid(axis='y', alpha=0.3)

        # 6. Initiatives timeline
        ax6 = fig.add_subplot(gs[2, :])
        if not data['initiatives'].empty:
            init_by_year = data['initiatives'].groupby('year').size()
            ax6.bar(init_by_year.index.astype(str), init_by_year.values,
                   color=[self.colors.get(str(y), '#888888') for y in init_by_year.index])
            ax6.set_title('Initiatives & Programs Announced by Year', fontweight='bold', fontsize=12)
            ax6.set_xlabel('Year')
            ax6.set_ylabel('Number of Initiatives')
            ax6.grid(axis='y', alpha=0.3)

            for i, (year, count) in enumerate(zip(init_by_year.index.astype(str), init_by_year.values)):
                ax6.text(i, count, f'{int(count)}', ha='center', va='bottom', fontsize=11)

        # Add timestamp
        fig.text(0.99, 0.01, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                ha='right', va='bottom', fontsize=8, style='italic')

        output_path = os.path.join(self.viz_dir, 'EXECUTIVE_DASHBOARD.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Saved: {output_path}")


def main():
    """Main visualization process"""

    print("="*80)
    print("PATAGONIA ESG ANALYSIS - VISUALIZATION GENERATION")
    print("="*80)

    # Initialize visualizer
    viz = ESGVisualizer(analysis_dir="analysis_output", viz_dir="visualizations")

    # Load analysis data
    data = viz.load_analysis_data()

    if all(df.empty for df in data.values()):
        print("\n❌ ERROR: No analysis data found!")
        print("Please run analyze_esg_content.py first.")
        return

    # Generate all visualizations
    print("\n" + "="*80)
    print("GENERATING VISUALIZATIONS")
    print("="*80)

    viz.plot_language_tone_trends(data['language'])
    viz.plot_target_mentions_over_time(data['targets'])
    viz.plot_geographic_distribution(data['geography'])
    viz.plot_impact_areas(data['impacts'])
    viz.plot_initiatives_timeline(data['initiatives'])
    viz.create_executive_dashboard(data)

    print("\n" + "="*80)
    print("VISUALIZATION COMPLETE")
    print("="*80)
    print(f"Output directory: {viz.viz_dir}/")
    print("\nGenerated visualizations:")
    print("  - language_tone_analysis.png")
    print("  - targets_goals_analysis.png")
    print("  - geographic_distribution.png")
    print("  - impact_areas_analysis.png")
    print("  - initiatives_analysis.png")
    print("  - EXECUTIVE_DASHBOARD.png")
    print("="*80)


if __name__ == "__main__":
    main()
