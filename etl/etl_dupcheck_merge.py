import psycopg
from psycopg.rows import dict_row

import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import copy
from nltk.util import ngrams
from queue import Queue


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
        # print(row)
        return row
    str1Token = splitch(str1Token)
    str2Token = splitch(str2Token)

    str1ngrams = [u''.join(w) for w in ngrams(str1Token, 3)]
    str2ngrams = [u''.join(w) for w in ngrams(str2Token, 3)]
    def similarity(listA, listB, threshold=0.55):
        joint = set(listA).intersection(set(listB))  # get the joint
        union = set(listA).union(set(listB))
        if (len(union)==0):
            sim = 0
        else:
            sim = len(joint) / len(union)

        return sim
    return similarity(str1ngrams,str2ngrams)

def merge(row1,row2):
    if(row1['synopsis']!=None):
        if(row2['synopsis']!=None):
            row2['synopsis'] += row1['synopsis']
        else:
            row2['synopsis'] = row1['synopsis']


    if(row2['duration_in_minutes']==None):
        row2['duration_in_minutes'] = row1['duration_in_minutes']
    if(row2['number_of_episodes'] ==None):
        row2['number_of_episodes'] = row1['number_of_episodes']
    if (row2['media_type'] == None):
        row2['media_type'] = row1['media_type']

    if (row2['score'] == None):
        row2['score'] = row1['score']
    if((not row2['score'] == None) and (not row2['score'] != None)):
        row2['score'] = (row1['score']+row2['score'])/2

    if (row2['scored_by'] == None):
        row2['scored_by'] = row1['scored_by']

    if (row2['popularity'] == None):
        row2['popularity'] = row1['popularity']
    if (row2['source'] == None):
        row2['source'] = row1['source']
    if (row2['start_year'] == None):
        row2['start_year'] = row1['start_year']
    if (row2['finish_year'] == None):
        row2['finish_year'] = row1['finish_year']
    if (row2['season_of_release'] == None):
        row2['season_of_release'] = row1['season_of_release']
    if (row2['esrb_rating'] == None):
        row2['esrb_rating'] = row1['esrb_rating']
    if (row2['broadcast_time'] == None):
        row2['broadcast_time'] = row1['broadcast_time']

    return row2

def find_dup_update():

    with psycopg.connect("host=127.0.0.1 dbname=integrated_system user=postgres password=password", row_factory=dict_row) as conn:
        with conn.cursor() as cursor, conn.cursor() as update:
            cursor.execute(
                """SELECT * FROM result.anime_titles ORDER BY title DESC""")

         


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

                    #print("similarity=",sim)
                    update.execute("SELECT * FROM result.anime_titles WHERE id = %s",([id1]))

                    result1 = update.fetchone()
                    update.execute("SELECT * FROM result.anime_titles WHERE id = %s", ([id2]))
                    # many records' year = None, thus only consider num_episodes
                    result2 = update.fetchone()

                    #weighted similarity
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
                        print("MERGE FOLLOWING INFO--")
                        print(delete_row)
                        print(merged_row)
                        print("TO--")
                        print(merged_info)


                        #merge execute (merge)
                        update.execute(
                            "UPDATE result.anime_titles SET synopsis=%s,duration_in_minutes=%s,number_of_episodes=%s,media_type=%s,score=%s,scored_by=%s,popularity=%s,source=%s,start_year=%s,finish_year=%s,season_of_release=%s,esrb_rating=%s,broadcast_time=%s",
                            ( merged_info['synopsis'],merged_info['duration_in_minutes'],merged_info['number_of_episodes'],merged_info['media_type'],merged_info['score'],merged_info['scored_by'],merged_info['popularity'],merged_info['source'],merged_info['start_year'],merged_info['finish_year'],merged_info['season_of_release'],merged_info['esrb_rating'],merged_info['broadcast_time'],))

                        #delete execute
                         #delete from children tables
                        update.execute("DELETE FROM result.anime_titles_content_warnings AS t2  WHERE t2.anime_title_id= %s", (deleteid,))
                        update.execute(
                            "DELETE FROM result.anime_titles_producers AS t2  WHERE t2.anime_title_id= %s",
                            (deleteid,))
                        update.execute(
                            "DELETE FROM result.anime_titles_genres AS t2  WHERE t2.anime_title_id= %s",
                            (deleteid,))
                        update.execute(
                            "DELETE FROM result.anime_titles_studios AS t2  WHERE t2.anime_title_id= %s",
                            (deleteid,))
                         #delete from parent table
                        update.execute("DELETE FROM result.anime_titles AS t2  WHERE t2.id= %s",
                            (deleteid,))  # foreign key





if __name__ == '__main__':
    find_dup_update()
