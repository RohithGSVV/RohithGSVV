import os
import re
import json
from collections import defaultdict
import matplotlib.pyplot as plt

tech_categories = {
    'Data Science': ['numpy', 'pandas', 'matplotlib', 'scipy', 'sklearn'],
    'Machine Learning': ['keras', 'tensorflow', 'pytorch', 'scikit-learn'],
    'Web Development': ['flask', 'django', 'selenium'],
}

def extract_libraries(filepath):
    with open(filepath, 'r') as file:
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

def categorize_libraries(libs):
    category_counts = defaultdict(int)
    for lib in libs:
        for category, library_list in tech_categories.items():
            if lib in library_list:
                category_counts[category] += 1
                break
    return category_counts

def generate_pie_chart(counts, filename='add-ons/pie_chart.png'):
    labels = counts.keys()
    sizes = counts.values()
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.savefig(filename)

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
