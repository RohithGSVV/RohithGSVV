import os
import re
import json
from collections import defaultdict
import matplotlib.pyplot as plt

tech_categories = {
    'Data Science': ['numpy', 'pandas', 'matplotlib', 'scipy', 'seaborn', 'statsmodels', 'resample', 'ParameterGrid', 'CoherenceModel', 'Dictionary', 'Sparse2Corpus'],
    'Machine Learning': ['keras', 'tensorflow', 'pytorch', 'sklearn', 'lightgbm', 'xgboost', 'CountVectorizer', 'LatentDirichletAllocation', 'GridSearchCV', 'BaseEstimator', 'KNNImputer'],
    'Deep Learning': ['tensorflow', 'keras', 'pytorch', 'fastai'],
    'Natural Language Processing': ['nltk', 'spacy', 'gensim', 'transformers', 'stopwords', 'WordNetLemmatizer', 'word_tokenize', 'sent_tokenize'],
    'Computer Vision': ['opencv', 'pillow', 'scikit-image'],
    'Web Development': ['flask', 'django', 'selenium', 'fastapi', 'tornado'],
    'Automation': ['selenium', 'pyautogui', 'scrapy', 'os', 'time'],
    'Data Visualization': ['matplotlib', 'seaborn', 'plotly', 'bokeh', 'ggplot', 'wordcloud'],
    'API Development': ['flask-restful', 'django-rest-framework', 'fastapi'],
    'Network Programming': ['socket', 'scapy', 'twisted'],
    'Game Development': ['pygame', 'panda3d', 'arcade'],
    'Desktop Application Development': ['tkinter', 'pyqt', 'wxpython'],
    'Programming Fundamentals': ['re', 'string', 'unicodedata', 'ast'],
    'Big Data': ['bigquery'],
    'Topic Modeling and Text Analysis': ['bertopic', 'LatentDirichletAllocation', 'CoherenceModel', 'CountVectorizer']
}

def extract_libraries(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as file:
            data = json.load(file)
            libraries = []
            for cell in data.get('cells', []):
                if cell['cell_type'] == 'code':
                    code = ''.join(cell['source'])
                    matches = re.findall(r'import (\w+)|from (\w+) import', code)
                    for match in matches:
                        lib = match[0] if match[0] else match[1]
                        libraries.append(lib)
            return libraries
    except UnicodeDecodeError as e:
        print(f"Error reading {filepath}: {e}")
        return []

def categorize_libraries(libs):
    category_counts = defaultdict(int)
    for lib in libs:
        found = False
        for category, library_list in tech_categories.items():
            if lib in library_list:
                category_counts[category] += 1
                found = True
        if not found:
            category_counts['Other'] += 1
    return category_counts

def generate_pie_chart(counts, filename='add-ons/pie_chart.png'):
    labels = counts.keys()
    sizes = counts.values()
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6', '#c4e17f', '#76d7c4', '#f7c6c7', '#f7c6c7', '#d1f2a5']
    explode = (0.1,) * len(labels)

    plt.figure(figsize=(10, 8))
    plt.gcf().set_facecolor('#333333')
    plt.rcParams.update({
        "text.color": "white",
        "axes.facecolor": "#333333",
        "axes.edgecolor": "white",
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "figure.facecolor": "#333333",
        "figure.edgecolor": "#333333",
        "savefig.facecolor": "#333333",
        "savefig.edgecolor": "#333333"
    })

    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, pctdistance=0.85, textprops={'color':"white"})

    plt.axis('equal')
    plt.title('Technology Usage Distribution', pad=20, color='white')
    plt.savefig(filename, transparent=True)

def main():
    all_libs = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.ipynb'):
                filepath = os.path.join(root, file)
                all_libs.extend(extract_libraries(filepath))

    category_counts = categorize_libraries(all_libs)
    generate_pie_chart(category_counts)

if __name__ == '__main__':
    main()
