#!/bin/env python3
import pandas as pd
from sqlalchemy import create_engine

import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams
import string

threshold = 0.5

def compute_ngrams(value):
    # import WordNet Lemmatizer
    lemmer = nltk.stem.WordNetLemmatizer()
    # get punctuation symbols as key and None as value in order to remove them using translate later
    remove_punct_dict = dict((ord(punct), None) for punct in
                             string.punctuation)  

    def LemTokens(tokens):
        # lemmatize the token if it is not a stopword
        return [lemmer.lemmatize(token, 'v') for token in tokens 
                    if token not in set(stopwords.words('english'))]

    def LemNormalize(text):
        # Remove punctuation, convert to lowercase then tokenize. Return unique values only
        return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

    tokens = LemNormalize(value)
    joined = ' '.join(tokens)
    return [''.join(list(kgram)) for kgram in ngrams(list(joined), 3)]


def set_similarity(listA, listB):
    joint = set(listA).intersection(set(listB))  # get the joint
    union = set(listA).union(set(listB))
    if len(union) == 0:
        sim = 0
    else:
        sim = len(joint) / len(union)
    return sim


def check_dup(left, right):
    left_ngrams = compute_ngrams(left)
    right_ngrams = compute_ngrams(right)

    return set_similarity(left_ngrams, right_ngrams)


def merge(row_a, row_b):
    if row_a['synopsis']:
        if row_b['synopsis']:
            row_b['synopsis'] += row_a['synopsis']
        else:
            row_b['synopsis'] = row_a['synopsis']

    row_b['duplicates'] = row_b['duplicates'] + row_a['duplicates']

    if not row_b['score']:
        row_b['score'] = row_a['score']
    if row_b['score'] and row_a['score']:
        row_b['score'] = (row_a['score'] + row_b['score']) / 2

    # prefer merge_target information over delete, where present
    if not row_b['duration_in_minutes']:
        row_b['duration_in_minutes'] = row_a['duration_in_minutes']
    if not row_b['number_of_episodes']:
        row_b['number_of_episodes'] = row_a['number_of_episodes']
    if not row_b['media_type']:
        row_b['media_type'] = row_a['media_type']

    if not row_b['scored_by']:
        row_b['scored_by'] = row_a['scored_by']

    if not row_b['popularity']:
        row_b['popularity'] = row_a['popularity']
    if not row_b['source']:
        row_b['source'] = row_a['source']
    if not row_b['start_year']:
        row_b['start_year'] = row_a['start_year']
    if not row_b['finish_year']:
        row_b['finish_year'] = row_a['finish_year']
    if not row_b['season_of_release']:
        row_b['season_of_release'] = row_a['season_of_release']
    if not row_b['esrb_rating']:
        row_b['esrb_rating'] = row_a['esrb_rating']
    if not row_b['broadcast_time']:
        row_b['broadcast_time'] = row_a['broadcast_time']

    return row_b


def weighted_score(result1, result2):
    score = check_dup(result1['title'], result2['title'])
    score += (1 if (result1['media_type'] == result2['media_type']) else -3) * (
        0.05 if (not result1['media_type'] is None and not ['media_type'] is None) else 0)
    # score+=(1 if(result1['duration_in_minutes']==result2['duration_in_minutes']) else -3)*(0.05 if((not result1['duration_in_minutes']== None) and (not ['duration_in_minutes']==None)) else 0)
    score += (1 if (result1['number_of_episodes'] == result2['number_of_episodes']) else -3) * (
        0.05 if (not result1['number_of_episodes'] is not None and not ['number_of_episodes'] is None) else 0)
    return score


def hash(anime_title):
    media_type = anime_title['media_type']
    if media_type is None:
        media_type = ''
    # return "".join(list(
    #     map(lambda word: word[0].lower(), filter(lambda x: len(x) > 0, anime_title['title'].split(' '))))) + media_type
    return anime_title['title'] + media_type


def merge_dependent(table, engine, anime_titles_merged):
    anime_titles_genres = pd.read_sql_query('select * from result.' + table, engine)
    result = anime_titles_merged.explode('duplicates') \
        .rename(columns={"duplicates": "anime_title_id"}) \
        .merge(anime_titles_genres, on='anime_title_id') \
        .drop('anime_title_id', axis=1)

    result.to_sql(table + '_merged', engine, index=False)


def merge_dependents(engine, anime_titles_merged):
    merge_dependent("anime_titles_content_warnings", engine, anime_titles_merged)
    merge_dependent("anime_titles_genres", engine, anime_titles_merged)
    merge_dependent("anime_titles_producers", engine, anime_titles_merged)
    merge_dependent("anime_titles_studios", engine, anime_titles_merged)


def run_data_fusion():
    result = pd.DataFrame()
    engine = create_engine('postgresql://postgres:password@localhost:5432/integrated_system')
    # anime_titles = pd.read_sql_query('select * from result.anime_titles where title = \'Z/X: Ignition\'', engine)
    anime_titles = pd.read_sql_query('select * from result.anime_titles', engine)
    anime_titles['hash'] = anime_titles.apply(lambda row: hash(row), axis=1)
    anime_titles['duplicates'] = anime_titles.apply(lambda row: [row['id']], axis=1)
    anime_titles = anime_titles.sort_values(by='hash')

    i = 0
    while i < len(anime_titles):
        current_row = anime_titles.iloc[i]
        j = i + 1
        while j < len(anime_titles) and weighted_score(current_row, anime_titles.iloc[j]) > threshold:
            print(current_row['title'], anime_titles.iloc[j]['title'],
                  weighted_score(current_row, anime_titles.iloc[j]))
            current_row = merge(current_row, anime_titles.iloc[j])
            j += 1
        # result = pd.concat([result, current_row])
        result = result.append(current_row)
        i = j

    result = result.drop('hash', axis=1)
    merge_dependents(engine, result[['id', 'duplicates']].copy())
    result.to_sql('anime_titles_merged', engine, index=False)


if __name__ == '__main__':

    # download nltk modules
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("wordnet")
    nltk.download("omw-1.4")

    run_data_fusion()
