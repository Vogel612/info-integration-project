#!/bin/env python3

import psycopg
from psycopg.rows import dict_row

import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams
import string
import copy
from queue import Queue

debug = False
threshold=0.55

def check_dup(str1,str2):
    #check year first episodes first
    #then check similarity
    #less time complex
    #window size 2
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
    #print(str1Token)
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
        if (len(union)==0):
            sim = 0
        else:
            sim = len(joint) / len(union)
        return sim
    return similarity(str1ngrams,str2ngrams)

def merge(delete, merge_target):
    if delete['synopsis']:
        if merge_target['synopsis']:
            merge_target['synopsis'] += delete['synopsis']
        else:
            merge_target['synopsis'] = delete['synopsis']

    if not merge_target['score']:
        merge_target['score'] = delete['score']
    elif not delete['score']:
        # compute merged score as arithmetic mean (not sure how well that works for more than two duplicates?)
        merge_target['score'] = (delete['score'] + merge_target['score']) / 2

    # prefer merge_target information over delete, where present
    if not merge_target['duration_in_minutes']:
        merge_target['duration_in_minutes'] = delete['duration_in_minutes']
    if not merge_target['number_of_episodes']:
        merge_target['number_of_episodes'] = delete['number_of_episodes']
    if not merge_target['media_type']:
        merge_target['media_type'] = delete['media_type']

    if not merge_target['scored_by']:
        merge_target['scored_by'] = delete['scored_by']

    if not merge_target['popularity']:
        merge_target['popularity'] = delete['popularity']
    if not merge_target['source']:
        merge_target['source'] = delete['source']
    if not merge_target['start_year']:
        merge_target['start_year'] = delete['start_year']
    if not merge_target['finish_year']:
        merge_target['finish_year'] = delete['finish_year']
    if not merge_target['season_of_release']:
        merge_target['season_of_release'] = delete['season_of_release']
    if not merge_target['esrb_rating']:
        merge_target['esrb_rating'] = delete['esrb_rating']
    if not merge_target['broadcast_time']:
        merge_target['broadcast_time'] = delete['broadcast_time']

    return merge_target

def find_dup_update():

    with psycopg.connect("host=127.0.0.1 dbname=integrated_system user=postgres password=password", row_factory=dict_row) as conn:
        with conn.cursor() as cursor, conn.cursor() as update:
            cursor.execute("""SELECT * FROM result.anime_titles ORDER BY title DESC""")

            #1 sorted neighborhood
            first = True

            for row in cursor:
                #window size = 2
                if(first):
                    title2 = row['title']
                    id2 = row['id']
                    first = False
                else:
                    title1 = title2
                    id1 = id2
                    title2 = row['title']
                    id2 = row['id']
                    check_dup(title1,title2)
                    sim = check_dup(title1, title2)

                    update.execute("SELECT * FROM result.anime_titles WHERE id = %s",([id1]))
                    result1 = update.fetchone()

                    update.execute("SELECT * FROM result.anime_titles WHERE id = %s", ([id2]))
                    # many records' year = None, thus only consider num_episodes
                    result2 = update.fetchone()

                    #weighted similarity
                    # TODO: Extract into separate method :D
                    sim+=(1 if(result1['duration_in_minutes']==result2['duration_in_minutes']) else -1)*(0.05 if((not result1['duration_in_minutes']== None) and (not ['duration_in_minutes']==None)) else 0)
                    sim += (1 if (result1['number_of_episodes'] == result2['number_of_episodes']) else -1) * (0.05 if ((not result1['number_of_episodes'] == None) and (not ['number_of_episodes']==None)) else 0)
                    sim+=(1 if(result1['start_year']==result2['start_year']) else -1)*(0.05 if((not result1['start_year']== None) and (not ['start_year']==None)) else 0)
                    sim += (1 if (result1['finish_year'] == result2['finish_year']) else -1) * (0.05 if ((not result1['finish_year'] == None) and (not ['finish_year']==None)) else 0)
                    sim += (1 if (result1['season_of_release'] == result2['season_of_release']) else -1) * (0.05 if ((not result1['season_of_release'] == None) and (not ['season_of_release'] == None)) else 0)

                    print("--------------------------------check-----------------------------------------")
                    print(id1, title1)
                    print(id2, title2)
                    print("similarity=",sim)

                    if(sim>threshold):
                        deleteid = id1 #delete the record of id1
                        mergeid = id2 #merge row-id1 to row-id2
                        update.execute("SELECT * FROM result.anime_titles WHERE id = %s", ([deleteid]))
                        delete_row = update.fetchone()

                        update.execute("SELECT * FROM result.anime_titles WHERE id = %s", ([mergeid])) #foreign key
                        merged_row = update.fetchone()
                        merged_info = merge(delete_row,merged_row)
                        if debug:
                            print("MERGE FOLLOWING INFO--")
                            print(delete_row)
                            print(merged_row)
                            print("TO--")
                            print(merged_info)


                        #merge execute (merge)
                        update.execute("""UPDATE result.anime_titles SET 
                            synopsis=%s, duration_in_minutes=%s, number_of_episodes=%s, media_type=%s, score=%s,
                            scored_by=%s, popularity=%s, source=%s, start_year=%s, finish_year=%s, season_of_release=%s,
                            esrb_rating=%s, broadcast_time=%s
                            WHERE id=%s""",
                            (merged_info['synopsis'],
                                merged_info['duration_in_minutes'],
                                merged_info['number_of_episodes'],
                                merged_info['media_type'],
                                merged_info['score'],
                                merged_info['scored_by'],
                                merged_info['popularity'],
                                merged_info['source'],
                                merged_info['start_year'],
                                merged_info['finish_year'],
                                merged_info['season_of_release'],
                                merged_info['esrb_rating'],
                                merged_info['broadcast_time'],
                            mergeid))

                        # merge dependent table records
                        update.execute("""UPDATE result.anime_titles_content_warnings
                            SET anime_title_id=%s WHERE anime_title_id=%s""", (mergeid, deleteid))
                        update.execute("""UPDATE result.anime_titles_producers
                            SET anime_title_id=%s WHERE anime_title_id= %s""", (mergeid, deleteid))
                        update.execute("""UPDATE result.anime_titles_genres
                            SET anime_title_id=%s WHERE anime_title_id= %s""", (mergeid, deleteid))
                        update.execute("""UPDATE result.anime_titles_studios
                            SET anime_title_id=%s WHERE anime_title_id= %s""", (mergeid, deleteid))

                        # FIXME? deduplicate dependent tables (to avoid double-counting matching dependent records)

                        # delete from main table
                        update.execute("DELETE FROM result.anime_titles WHERE id= %s", (deleteid,))


if __name__ == '__main__':
    # download nltk modules
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download("wordnet")
    nltk.download("omw-1.4")
    find_dup_update()
