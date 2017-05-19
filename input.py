import mysql.connector
import math
import sys
from joblib import Parallel, delayed
import multiprocessing
import csv

cnx = mysql.connector.connect(user='pyacc', database='movie_db', host='59.78.21.76', port='33068', password='001100')
cursor = cnx.cursor()

cursor.execute("SELECT DISTINCT id FROM movie_db.movies WHERE imdb_rating IS NOT NULL")
m_list = cursor.fetchall()


def retrieve_one_film(m_id):
    # Get data from database
    cursor.execute("SELECT imdb_rating, mpaa_rating, length FROM movie_db.movies WHERE id = {}".format(m_id))
    imdb_r, mpaa_r, leng = cursor.fetchall()[0]
    cursor.execute("SELECT genre FROM movie_db.genre WHERE movie_id = {}".format(m_id))
    genres = [each[0] for each in cursor.fetchall()]
    cursor.execute("SELECT personnel_id FROM movie_db.actor WHERE movie_id = {}".format(m_id))
    actors = cursor.fetchall()
    vendetta = 0
    for actor in actors:
        cursor.execute("SELECT ranking FROM movie_db.personnel WHERE personnel_id = {}".format(actor[0]))
        tmp = cursor.fetchall()[0][0]
        if tmp is None:
            pass
        else:
            vendetta += math.log10(100000/tmp)
    actor_rating = math.atan(vendetta * 0.1)
    # Transform data into a vector
    genre = [False] * 28
    if b'Comedy' in genres:
        genre[0]=True
    if b'Short' in genres:
        genre[1]=True
    if b'Animation' in genres:
        genre[2]=True
    if b'Drama' in genres:
        genre[3]=True
    if b'History' in genres:
        genre[4]=True
    if b'War' in genres:
        genre[5]=True
    if b'Horror' in genres:
        genre[6]=True
    if b'Sci-Fi' in genres:
        genre[7]=True
    if b'Biography' in genres:
        genre[8]=True
    if b'Documentary' in genres:
        genre[9]=True
    if b'Family' in genres:
        genre[10]=True
    if b'News' in genres:
        genre[11]=True
    if b'Action' in genres:
        genre[12]=True
    if b'Romance' in genres:
        genre[13]=True
    if b'Musical' in genres:
        genre[14]=True
    if b'Fantasy' in genres:
        genre[15]=True
    if b'Adventure' in genres:
        genre[16]=True
    if b'Mystery' in genres:
        genre[17]=True
    if b'Thriller' in genres:
        genre[18]=True
    if b'Music' in genres:
        genre[19]=True
    if b'Crime' in genres:
        genre[20]=True
    if b'Sport' in genres:
        genre[21]=True
    if b'Western' in genres:
        genre[22]=True
    if b'Adult' in genres:
        genre[23]=True
    if b'Film-Noir' in genres:
        genre[24]=True
    if b'Talk-Show' in genres:
        genre[25]=True
    if b'Reality-TV' in genres:
        genre[26]=True
    if b'Game-Show' in genres:
        genre[27]=True
    if mpaa_r is None or mpaa_r == 'PG':
        mpaa = [True] * 4
    elif mpaa_r == b'PG-13':
        mpaa = [False] + [True] * 3
    elif mpaa_r == b'NC-17':
        mpaa = [False] * 2 + [True] * 2
    elif mpaa_r == b'R':
        mpaa = [False] * 3 + [True]
    return [actor_rating] + [leng] + genre + mpaa, imdb_r

ser = sys.argv[1]
print ser
f_out = open('/Users/soshy/Code/UntitledGroup/out'+ser+'.csv', mode='w')
csvwriter = csv.writer(f_out, dialect='excel')
split = len(m_list)//multiprocessing.cpu_count()


def print_one_line(it):
    res = retrieve_one_film(it[0])
    csvwriter.writerow(res[0] + [res[1]])

# print "Beginning paralleled threading."
ser = int(ser)
for film in m_list[split*ser:split*(ser+1)]:
    print_one_line(film)
# res = retrieve_one_film(m_list[0][0])
# csvwriter.writerow(res[0] + [res[1]])
# f_out.close()
# input("Continue ?")
# f_out = open('/Users/soshy/Code/UntitledGroup/out.csv', mode='w')
# Parallel(n_jobs=multiprocessing.cpu_count())(delayed(print_one_line)(it) for it in m_list)
# print_one_line(m_list[0])
f_out.close()

cnx = mysql.connector.connect(user='pyacc', database='movie_db', host='59.78.21.76', port='33068', password='001100')
cursor = cnx.cursor()
cursor.execute("SELECT budget, imdb_rating FROM Movies WHERE budget IS NOT NULL AND imdb_rating IS NOT NULL")
res = cursor.fetchall()
