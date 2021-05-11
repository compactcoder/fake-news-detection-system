# Importing required libraries
import pandas as pd
from sklearn.utils import shuffle
from data_cleaning import clean_words,clean_fake_text,clean_fake_title,clean_true_text


def get_features(true_dataset_path, fake_dataset_path):

    # Reading dataset
    df_true = pd.read_csv(true_dataset_path)
    df_fake = pd.read_csv(fake_dataset_path)

    # Cleaning True text Data
    df_true["text"] = df_true["text"].apply(clean_true_text)

    # Cleaning Fake text Data
    df_fake["text"] = df_fake["text"].apply(clean_fake_text)
    df_fake["title"] = df_fake["title"].apply(clean_fake_title)

    # Labeling news
    df_true['label'] = 1
    df_fake['label'] = 0

    # Merging both True and Fake news dataset
    df_merge = pd.concat([df_fake, df_true], axis=0)
    df_merge.reset_index(drop=True, inplace=True)

    # Checking for blank rows (text column)
    blank_rows = []
    for index, text in df_merge['text'].iteritems():
        if text.isspace():
            blank_rows.append(index)

    # Removing blank rows
    df_merge.drop(index=blank_rows, axis=0, inplace=True)

    # Adding title and text column into single column total
    df_merge['total'] = df_merge["title"] + df_merge['text']

    # Assigning to new data-frame 'df' after removing unnecessary features
    df = df_merge.drop({"title", "text", "subject", "date"}, axis=1)

    # Shuffling data
    df = shuffle(df)

    # Resetting Index
    df.reset_index(drop=True, inplace=True)

    # Cleaning text Data
    df['total'] = df['total'].apply(clean_words)

    # Returning pre-processed dataframe
    return df
