#!/bin/env python3
import pandas as pd
from sqlalchemy import create_engine

import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams
import string
import copy

threshold = 0.55


def check_dup(str1, str2):
    # check year first episodes first
    # then check similarity
    # less time complex
    # window size 2

    # pre-check number_of_episodes

    '''
    sy1 = str1["start_year"]
    fy1 = str1["finish_year"]
    sy2 = str2["start_year"]
    fy2 = str2["finish_year"]
    '''

    lemmer = nltk.stem.WordNetLemmatizer()  # import WordNet Lemmatizer
    remove_punct_dict = dict((ord(punct), None) for punct in
                             string.punctuation)  # get punctiation symbols as key and None as value in order to remove them using translate later

    def LemTokens(tokens):
        return [lemmer.lemmatize(token, 'v') for token in tokens if
                token not in set(stopwords.words('english'))]  # lemmatize the token if it is not a stopword

    def LemNormalize(text):
        return LemTokens(nltk.word_tokenize(text.lower().translate(
            remove_punct_dict)))  # Remove punctuation, convert to lowercase then tokenize. Return unique values only

    str1Token = LemNormalize(str1)
    str2Token = LemNormalize(str2)
    # print(str1Token)
    str1Token = ' '.join(str1Token)
    str2Token = ' '.join(str2Token)

    def splitch(row):
        t = []
        for token in row:
            token = list(token)
            t += token

        row = copy.deepcopy(t)
        return row

    str1Token = splitch(str1Token)
    str2Token = splitch(str2Token)

    str1ngrams = [u''.join(w) for w in ngrams(str1Token, 3)]
    str2ngrams = [u''.join(w) for w in ngrams(str2Token, 3)]

    def similarity(listA, listB):
        joint = set(listA).intersection(set(listB))  # get the joint
        union = set(listA).union(set(listB))
        if len(union) == 0:
            sim = 0
        else:
            sim = len(joint) / len(union)
        return sim

    return similarity(str1ngrams, str2ngrams)


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
    score = 0
    # score+=(1 if(result1['duration_in_minutes']==result2['duration_in_minutes']) else -3)*(0.05 if((not result1['duration_in_minutes']== None) and (not ['duration_in_minutes']==None)) else 0)
    score += (1 if (result1['number_of_episodes'] == result2['number_of_episodes']) else -3) * (
        0.05 if (not result1['number_of_episodes'] is not None and not ['number_of_episodes'] is None) else 0)
    score += (1 if (result1['start_year'] == result2['start_year']) else -3) * (
        0.05 if (not result1['start_year'] is None and not ['start_year'] is None) else 0)
    score += (1 if (result1['finish_year'] == result2['finish_year']) else -3) * (
        0.05 if (not result1['finish_year'] is None and not ['finish_year'] is None) else 0)
    score += (1 if (result1['season_of_release'] == result2['season_of_release']) else -3) * (
        0.05 if (not result1['season_of_release'] is None and not ['season_of_release'] is None) else 0)
    score += (1 if (result1['number_of_episodes'] == result2['number_of_episodes']) else -3) * (0.05 if (
            (not result1['number_of_episodes'] is None) and (not ['number_of_episodes'] is None)) else 0)
    score += (1 if (result1['season_of_release'] == result2['season_of_release']) else -3) * (0.05 if (
            (not result1['season_of_release'] is None) and (not ['season_of_release'] is None)) else 0)
    return score


def hash(anime_title):
    media_type = anime_title['media_type']
    if media_type is None:
        media_type = ''
    return "".join(list(
        map(lambda word: word[0].lower(), filter(lambda x: len(x) > 0, anime_title['title'].split(' '))))) + media_type


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

    anime_titles.sort_values(by='hash')

    i = 0
    while i < len(anime_titles):
        current_row = anime_titles.iloc[i]
        j = i + 1
        while j < len(anime_titles) and weighted_score(current_row, anime_titles.iloc[j]) > threshold:
            print(current_row['title'], anime_titles.iloc[j]['title'],
                  weighted_score(current_row, anime_titles.iloc[j]))
            current_row = merge(current_row, anime_titles.iloc[j])
            j += 1
        result = result.append(current_row)
        i = j

    result = result.drop('hash', axis=1)
    merge_dependents(engine, result[['id', 'duplicates']].copy())
    result.to_sql('anime_titles_merged', engine, index=False)


if __name__ == '__main__':
    run_data_fusion()
