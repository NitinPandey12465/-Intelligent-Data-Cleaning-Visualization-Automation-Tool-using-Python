# -Intelligent-Data-Cleaning-Visualization-Automation-Tool-using-Python
# Auto Dataset Cleaner & Visualizer

This project is a Python-based algorithm that automates the process of data cleaning, preprocessing, and visualization for structured datasets (CSV or Excel). It is designed to make exploratory data analysis (EDA) intuitive, customizable, and efficient—especially for non-technical users or fast prototyping.

## Features

- **File Compatibility**: Supports `.csv`, `.xlsx`, and `.xls` file formats.
- **Data Cleaning**:
  - Column name normalization (lowercased, hyphenated, cleaned of symbols)
  - Duplicate row detection and removal
  - Null value handling with user-defined options (mean, sum, 0, custom string)
  - Data type parsing (automatic datetime conversion)
  - Rating and percentage column transformation
  - Outlier detection using Z-score and IQR methods
- **Visualization**:
  - Supports multiple graph types: histogram, bar, pie, line, boxplot
  - Allows user to select column(s) and graph type(s) interactively
  - Includes relational visualizations between categorical and numerical columns (bar, box, violin)
  - Plots can be displayed and optionally saved as `.png` files
- **User Interaction**:
  - Step-by-step prompts for filling nulls and generating plots
  - Final option to export the cleaned dataset as `.csv` or `.xlsx`

## Requirements

- Python 3.x
- pandas
- numpy
- seaborn
- matplotlib
- plotly
- scipy
- openpyxl (for saving Excel files)

Install requirements using:

```bash
pip install pandas numpy matplotlib seaborn plotly scipy openpyxl
