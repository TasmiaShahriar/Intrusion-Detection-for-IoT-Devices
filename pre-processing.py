# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1We5OKawtWUKqISy-CT7ZMZorkZsWdUB3
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
# 1. Specify the folder path containing the CSV files.
folder_path = '/content/drive/MyDrive/'

# 2. Initialize an empty list to store DataFrames.
dfs = []

# 3. List CSV files in the folder.
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# 4. Loop through the CSV files, read and append them to the list.
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path,low_memory=False)
    dfs.append(df)

# 5. Concatenate the list of DataFrames into a single DataFrame.
combined_df = pd.concat(dfs, ignore_index=True)

category_var = combined_df['category']
class_counts = combined_df['category'].value_counts()
category_counts = category_var.value_counts()

sub_category_var = combined_df['subcategory']
class_counts_sub_category = combined_df['category'].value_counts()
sub_category_counts = sub_category_var.value_counts()

# Extract the 'attack' variable
attack_data_df = combined_df['attack']
attack_distribution = combined_df['attack'].value_counts()
#print(attack_distribution)

# Extract the counts for 0 and 1
count_0 = attack_distribution.get(0, 0)
count_1 = attack_distribution.get(1, 0)

# Visualize the binary distribution
values = [count_0, count_1]
labels = ['0', '1']

# Create a vertical bar plot (reversed axis)
plt.figure(figsize=(32, 8))

# Create subplots
plt.subplot(1, 2, 1)  # Subplot 1
category_counts.plot(kind='bar')
# plt.xlabel('Category')
# plt.ylabel('Count')
plt.title('Distribution of Categorical Variable ',fontsize=20)
plt.xticks(rotation=45,fontsize=20)
plt.yticks(fontsize=20)
for i, count in enumerate(class_counts):
    plt.text(i, count + 50, str(count), ha='center', va='bottom',fontsize=20)


plt.subplot(1, 2, 2)  # Subplot 2
sub_category_counts.plot(kind='bar')
# plt.xlabel('Sub-Category')
# plt.ylabel('Count')
plt.title('Distribution of Sub-Category Variable',fontsize=20)
plt.xticks(rotation=45,fontsize=20)
plt.yticks(fontsize=20)
for i, count in enumerate(class_counts_sub_category):
    plt.text(i, count + 50, str(count), ha='center', va='bottom',fontsize=20)


# Subplot 4 can be left empty for the previous plot

plt.tight_layout()  # Ensures subplots don't overlap
plt.show()

from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
import numpy as np

y = combined_df['category']
X = combined_df.drop(['category'], axis=1)
# Undersampling: Reducing the large classes to a chosen number, e.g., 10000 samples
undersample_strategy = {
    'DDoS': 10000,
    'DoS': 10000,
    'Reconnaissance': 10000  # Undersampling this to match others
}
undersampler = RandomUnderSampler(sampling_strategy=undersample_strategy)
X_undersampled, y_undersampled = undersampler.fit_resample(X, y)
# Oversampling: Increasing the very small classes to match the larger ones (e.g., 10000 samples)
oversample_strategy = {
    'Normal': 10000,
    'Theft': 10000
}
oversampler = RandomOverSampler(sampling_strategy=oversample_strategy)
X_resampled, y_resampled = oversampler.fit_resample(X_undersampled, y_undersampled)
# Check the distribution of classes in the resampled dataset
unique_classes_resampled, class_counts_resampled = np.unique(y_resampled, return_counts=True)
print("\nClass distribution in the resampled dataset:")
for cls, count in zip(unique_classes_resampled, class_counts_resampled):
    print(f"Class {cls}: {count} samples")

from pandas.plotting import scatter_matrix
# Select the numerical variables for the scatter matrix

selected_vars = X_resampled[['seq', 'stddev', 'N_IN_Conn_P_SrcIP', 'min', 'mean', 'N_IN_Conn_P_DstIP',
'drate',
'srate',
'max',
'TnP_PerProto',
'dur']]
scatter_data = selected_vars

# Create a scatter matrix
scatter_matrix(scatter_data, alpha=0.9, figsize=(16,16), diagonal='kde')
plt.suptitle('Scatter Matrix all features', y=0.95)
plt.show()

plt.savefig("myImagePDF.pdf", format="pdf", bbox_inches="tight")

# Specify the file path where you want to save the CSV
file_path = '/content/final.csv'
X_resampled_df = pd.DataFrame(X_resampled, columns=X.columns)
y_resampled_df = pd.DataFrame(y_resampled, columns=['category'])
df_final = pd.concat([X_resampled_df, y_resampled_df], axis=1)
# Use the to_csv method to save the DataFrame to a CSV file
df_final.to_csv(file_path, index=False)  # Set index=False to exclude the index column

print(f"DataFrame saved to {file_path}")

df = pd.read_csv('/content/final.csv',low_memory=False)
class_counts_final = df['category'].value_counts()
class_counts_sub_category_final = df['subcategory'].value_counts()
# Assuming you have already created the 'category_var' and 'category_counts'

# Extract the 'attack' variable
attack_data_df = df['attack']
attack_distribution_final = df['attack'].value_counts()
#print(attack_distribution)

# Extract the counts for 0 and 1
count_0 = attack_distribution_final.get(0, 0)
count_1 = attack_distribution_final.get(1, 0)

# Visualize the binary distribution
values = [count_0, count_1]
labels = ['0', '1']

# Create a vertical bar plot (reversed axis)
plt.figure(figsize=(32, 8))

# Create subplots
plt.subplot(1, 2, 1)  # Subplot 1
class_counts_final.plot(kind='bar')
#plt.xlabel('Category',fontsize=20)
#plt.ylabel('Count',fontsize=20)
plt.title('Distribution of Categorical Variable ',fontsize=20)
plt.xticks(rotation=45,fontsize=20)
plt.yticks(fontsize=20)
for i, count in enumerate(class_counts_final):
    plt.text(i, count + 50, str(count), ha='center', va='bottom',fontsize=20)

plt.subplot(1, 2, 2)  # Subplot 2
class_counts_sub_category_final.plot(kind='bar')
#plt.xlabel('Sub-Category',fontsize=20)
#plt.ylabel('Count',fontsize=20)
plt.title('Distribution of Sub-Category Variable',fontsize=20)
plt.xticks(rotation=45,fontsize=20)
plt.yticks(fontsize=20)
for i, count in enumerate(class_counts_sub_category_final):
    plt.text(i, count + 50, str(count), ha='center', va='bottom',fontsize=20)


# Subplot 4 can be left empty for the previous plot

plt.tight_layout()  # Ensures subplots don't overlap
plt.show()