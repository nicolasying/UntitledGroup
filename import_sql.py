import mysql.connector
import re
import codecs


def import_movies():
    cnx = mysql.connector.connect(user='pywriter', database='movie_db', host='127.0.0.1', password='123456')
    cursor = cnx.cursor()
    title_re = r"(.+)\s+\([0-9]+[/]?([IVX]+)?\)\s+([0-9]+)$"
    stmt = "INSERT INTO Movies (title, year_dis, year) VALUES (%s, %s, %s);"
    # cursor.execute("DROP TABLE Movies;")
    with codecs.open('/Users/soshy/Code/sampleCode/data-movies/data/movies.list', encoding='iso-8859-1', mode='r') as file_l:
        for line in file_l:
            res = re.match(title_re, line.strip())
            if res is not None:
                try:
                    if res.groups()[1] is None:
                        sub = None
                    else:
                        sub = codecs.encode(res.groups()[1], 'utf8')
                    cursor.execute(stmt, (codecs.encode(res.groups()[0], 'utf8'), sub
                                          , codecs.encode(res.groups()[2], 'utf8')))
                except mysql.connector.errors.IntegrityError:
                    print codecs.encode(res.groups()[0], 'utf8'), codecs.encode(res.groups()[1], 'utf8'), codecs.encode(res.groups()[2], 'utf8')
        try:
            cnx.commit()
        except mysql.connector.errors.IntegrityError:
            pass
    cursor.close()
    cnx.close()
    file_l.close()


def import_length():
    cnx = mysql.connector.connect(user='pywriter', database='movie_db', host='127.0.0.1', password='123456')
    cursor = cnx.cursor()
    length_re = r"(.+)\s+\(([0-9]+)[/]?([IVX]+)?\)\s+([a-zA-Z]+)?[:]?([0-9]+).*?$"
    stmt_1 = "UPDATE Movies SET length = %s WHERE title = %s AND year_dis = %s AND year = %s;"
    stmt_2 = "UPDATE Movies SET length = %s WHERE title = %s AND year_dis is NULL AND year = %s;"
    with codecs.open('/Users/soshy/Code/sampleCode/data-movies/data/running-times.list', encoding='iso-8859-1', mode='r') as file_l:
        for line in file_l:
            res = re.match(length_re, line.strip())
            if res is not None:
                try:
                    if res.groups()[2] is None:
                        cursor.execute(stmt_2, (codecs.encode(res.groups()[4], 'utf8'), codecs.encode(res.groups()[0], 'utf8'), codecs.encode(res.groups()[1], 'utf8')))
                    else:
                        cursor.execute(stmt_1, (codecs.encode(res.groups()[4], 'utf8'), codecs.encode(res.groups()[0], 'utf8'), codecs.encode(res.groups()[2], 'utf8'), codecs.encode(res.groups()[1], 'utf8')))
                except:
                    cnx.rollback()
                    print res.groups()[0], res.groups()[1], res.groups()[2], res.groups()[3], res.groups()[4]
        try:
            cnx.commit()
        except:
            cnx.rollback()
            print("Something Wrong with commit")
    cursor.close()
    cnx.close()
    file_l.close()


def import_budget():
    cnx = mysql.connector.connect(user='pywriter', database='movie_db', host='127.0.0.1', password='123456')
    cursor = cnx.cursor()
    title_re = r"MV:\s+(.+)\s+\(([0-9]+)[/]?([IVX]+)?\)\s*$"
    budget_re = r"BT:\s+USD\s+([0-9,]+)\s*$"
    stmt_1 = "UPDATE Movies SET budget = %s WHERE title = %s AND year_dis = %s AND year = %s;"
    stmt_2 = "UPDATE Movies SET budget = %s WHERE title = %s AND year_dis is NULL AND year = %s;"
    sepa = "---------"
    file_l = codecs.open('/Users/soshy/Code/sampleCode/data-movies/data/business.list', encoding='iso-8859-1', mode='r')
    for line in file_l:
        if line[:9] == "BUSINESS ":
            break
    line = next(file_l)
    line = next(file_l)
    while True:
        try:
            line = next(file_l)
            mv_res = re.match(title_re, line)
            if mv_res is not None:
                line = next(file_l)
                while line[:9] != sepa and line[:4] != "BT: ":
                    line = next(file_l)
                bt_res = re.match(budget_re, line)
                if bt_res is not None:
                    try:
                        if mv_res.groups()[2] is None:
                            cursor.execute(stmt_2, (\
                            ''.join(bt_res.groups()[0].split(',')), codecs.encode(mv_res.groups()[0], 'utf8'),\
                            codecs.encode(mv_res.groups()[1], 'utf8')))
                        else:
                            cursor.execute(stmt_1, (\
                            ''.join(bt_res.groups()[0].split(',')), codecs.encode(mv_res.groups()[0], 'utf8'),\
                            codecs.encode(mv_res.groups()[2], 'utf8'), codecs.encode(mv_res.groups()[1], 'utf8')))
                    except:
                        cnx.rollback()
                        print mv_res.groups()[0], mv_res.groups()[1], mv_res.groups()[2]
        except StopIteration:
            break
    try:
        cnx.commit()
    except:
        cnx.rollback()
        print("Something Wrong with commit")
    cursor.close()
    cnx.close()
    file_l.close()


def import_mpaa():
    cnx = mysql.connector.connect(user='pywriter', database='movie_db', host='127.0.0.1', password='123456')
    cursor = cnx.cursor()
    title_re = r"MV:\s+(.+)\s+\(([0-9]+)[/]?([IVX]+)?\)\s*$"
    rate_re = r"RE:\s+Rated\s+([-RNCPG0-9]+)\s+for.*$"
    stmt_1 = "UPDATE Movies SET mpaa_rating = %s WHERE title = %s AND year_dis = %s AND year = %s;"
    stmt_2 = "UPDATE Movies SET mpaa_rating = %s WHERE title = %s AND year_dis is NULL AND year = %s;"
    sepa = "---------"
    file_l = codecs.open('/Users/soshy/Code/sampleCode/data-movies/data/mpaa-ratings-reasons.list', encoding='iso-8859-1', mode='r')
    for line in file_l:
        if line[:9] == "MPAA RATI":
            break
    line = next(file_l)
    line = next(file_l)
    while True:
        try:
            line = next(file_l)
            mv_res = re.match(title_re, line)
            if mv_res is not None:
                line = next(file_l)
                while line[:9] != sepa and line[:4] != "RE: ":
                    line = next(file_l)
                rt_res = re.match(rate_re, line)
                if rt_res is not None:
                    try:
                        if mv_res.groups()[2] is None:
                            cursor.execute(stmt_2, (\
                            codecs.encode(rt_res.groups()[0], 'utf8'), codecs.encode(mv_res.groups()[0], 'utf8'),\
                            codecs.encode(mv_res.groups()[1], 'utf8')))
                        else:
                            cursor.execute(stmt_1, (\
                            codecs.encode(rt_res.groups()[0], 'utf8'), codecs.encode(mv_res.groups()[0], 'utf8'),\
                            codecs.encode(mv_res.groups()[2], 'utf8'), codecs.encode(mv_res.groups()[1], 'utf8')))
                    except:
                        cnx.rollback()
                        print mv_res.groups()[0], mv_res.groups()[1], mv_res.groups()[2]
        except StopIteration:
            break
    try:
        cnx.commit()
    except:
        cnx.rollback()
        print("Something Wrong with commit")
    cursor.close()
    cnx.close()
    file_l.close()


def import_imdb():
    cnx = mysql.connector.connect(user='pywriter', database='movie_db', host='127.0.0.1', password='123456')
    cursor = cnx.cursor()
    rate_re = r"\s*[0-9.*]+\s+([0-9]+)\s+([0-9.]+)\s+(.+)\s+\(([0-9]+)[/]?([IVX]+)?\)\s*$"
    stmt_1 = "UPDATE Movies SET imdb_rating = %s, vote = %s WHERE title = %s AND year_dis = %s AND year = %s;"
    stmt_2 = "UPDATE Movies SET imdb_rating = %s, vote = %s WHERE title = %s AND year_dis is NULL AND year = %s;"
    file_l = codecs.open('/Users/soshy/Code/sampleCode/data-movies/data/ratings.list', encoding='iso-8859-1', mode='r')
    for line in file_l:
        if line[:9] == "MOVIE RAT":
            break
    line = next(file_l)
    line = next(file_l)
    while True:
        try:
            line = next(file_l)
            res = re.match(rate_re, line)
            if res is not None:
                try:
                    if res.groups()[4] is None:
                        cursor.execute(stmt_2, (\
                        codecs.encode(res.groups()[1], 'utf8'), codecs.encode(res.groups()[0], 'utf8'),\
                        codecs.encode(res.groups()[2], 'utf8'), codecs.encode(res.groups()[3], 'utf8')))
                    else:
                        cursor.execute(stmt_1, ( \
                            codecs.encode(res.groups()[1], 'utf8'), codecs.encode(res.groups()[0], 'utf8'), \
                            codecs.encode(res.groups()[2], 'utf8'), codecs.encode(res.groups()[4], 'utf8'), \
                            codecs.encode(res.groups()[3], 'utf8')))
                except:
                    cnx.rollback()
                    print res.groups()[0], res.groups()[1], res.groups()[2], res.groups()[3], res.groups()[4]
        except StopIteration:
            break
    try:
        cnx.commit()
    except:
        cnx.rollback()
        print("Something Wrong with commit")
    cursor.close()
    cnx.close()
    file_l.close()


def import_country():
    cnx = mysql.connector.connect(user='pywriter', database='movie_db', host='127.0.0.1', password='123456')
    cursor = cnx.cursor()
    country_re = r"(.+)\s+\(([0-9]+)[/]?([IVX]+)?\)\s+([-'a-zA-Z]+)$"
    stmt_1 = "INSERT INTO Countries(.Countries.movie_id, .Countries.country) VALUES ((SELECT id FROM Movies WHERE title = %s AND year_dis = %s AND year = %s), %s);"
    stmt_2 = "INSERT INTO Countries(.Countries.movie_id, .Countries.country) VALUES ((SELECT id FROM Movies WHERE title = %s AND year_dis IS NULL AND year = %s), %s);"
    file_l = codecs.open('/Users/soshy/Code/sampleCode/data-movies/data/countries.list', encoding='iso-8859-1', mode='r')
    for line in file_l:
        if line[:9] == "COUNTRIES":
            break
    line = next(file_l)
    while True:
        try:
            line = next(file_l)
            res = re.match(country_re, line)
            if res is not None:
                try:
                    if res.groups()[2] is None:
                        cursor.execute(stmt_2, (\
                        codecs.encode(res.groups()[0], 'utf8'), codecs.encode(res.groups()[1], 'utf8'),\
                        codecs.encode(res.groups()[3], 'utf8')))
                    else:
                        cursor.execute(stmt_1, ( \
                            codecs.encode(res.groups()[0], 'utf8'), codecs.encode(res.groups()[2], 'utf8'), \
                            codecs.encode(res.groups()[1], 'utf8'), codecs.encode(res.groups()[3], 'utf8')))
                except:
                    # cnx.rollback()
                    print res.groups()[0], res.groups()[1], res.groups()[2], res.groups()[3]
        except StopIteration:
            break
    try:
        cnx.commit()
    except:
        cnx.rollback()
        print("Something Wrong with commit")
    cursor.close()
    cnx.close()
    file_l.close()


def import_language():
    cnx = mysql.connector.connect(user='pywriter', database='movie_db', host='127.0.0.1', password='123456')
    cursor = cnx.cursor()
    language_re = r"(.+)\s+\(([0-9]+)[/]?([IVX]+)?\)\s+([-'a-zA-Z]+)\s+(\(.*\))?\s*$"
    stmt_1 = "INSERT INTO Language(.Language.movie_id, .Language.language) VALUES ((SELECT id FROM Movies WHERE title = %s AND year_dis = %s AND year = %s), %s);"
    stmt_2 = "INSERT INTO Language(.Language.movie_id, .Language.language) VALUES ((SELECT id FROM Movies WHERE title = %s AND year_dis IS NULL AND year = %s), %s);"
    file_l = codecs.open('/Users/soshy/Code/sampleCode/data-movies/data/language.list', encoding='iso-8859-1', mode='r')
    for line in file_l:
        if line[:9] == "LANGUAGE ":
            break
    line = next(file_l)
    while True:
        try:
            line = next(file_l)
            res = re.match(language_re, line)
            if res is not None:
                try:
                    if res.groups()[2] is None:
                        cursor.execute(stmt_2, (\
                        codecs.encode(res.groups()[0], 'utf8'), codecs.encode(res.groups()[1], 'utf8'),\
                        codecs.encode(res.groups()[3], 'utf8')))
                    else:
                        cursor.execute(stmt_1, ( \
                            codecs.encode(res.groups()[0], 'utf8'), codecs.encode(res.groups()[2], 'utf8'), \
                            codecs.encode(res.groups()[1], 'utf8'), codecs.encode(res.groups()[3], 'utf8')))
                except:
                    # cnx.rollback()
                    print res.groups()[0], res.groups()[1], res.groups()[2], res.groups()[3], res.groups()[4]
        except StopIteration:
            cnx.commit()
            break
    try:
        cnx.commit()
    except:
        cnx.rollback()
        print("Something Wrong with commit")
    cursor.close()
    cnx.close()
    file_l.close()


def import_genre():
    cnx = mysql.connector.connect(user='pywriter', database='movie_db', host='127.0.0.1', password='123456')
    cursor = cnx.cursor()
    genre_re = r"(.+)\s+\(([0-9]+)[/]?([IVX]+)?\)\s+([-'a-zA-Z]+)\s*$"
    stmt_1 = "INSERT INTO Genre(.Genre.movie_id, .Genre.genre) VALUES ((SELECT id FROM Movies WHERE title = %s AND year_dis = %s AND year = %s), %s);"
    stmt_2 = "INSERT INTO Genre(.Genre.movie_id, .Genre.genre) VALUES ((SELECT id FROM Movies WHERE title = %s AND year_dis IS NULL AND year = %s), %s);"
    file_l = codecs.open('/Users/soshy/Code/sampleCode/data-movies/data/genres.list', encoding='iso-8859-1', mode='r')
    for line in file_l:
        if line[:9] == "8: THE GE":
            break
    line = next(file_l)
    while True:
        try:
            line = next(file_l)
            res = re.match(genre_re, line)
            if res is not None:
                try:
                    if res.groups()[2] is None:
                        cursor.execute(stmt_2, (\
                        codecs.encode(res.groups()[0], 'utf8'), codecs.encode(res.groups()[1], 'utf8'),\
                        codecs.encode(res.groups()[3], 'utf8')))
                    else:
                        cursor.execute(stmt_1, ( \
                            codecs.encode(res.groups()[0], 'utf8'), codecs.encode(res.groups()[2], 'utf8'), \
                            codecs.encode(res.groups()[1], 'utf8'), codecs.encode(res.groups()[3], 'utf8')))
                except:
                    # cnx.rollback()
                    print res.groups()[0], res.groups()[1], res.groups()[2], res.groups()[3]
        except StopIteration:
            break
    try:
        cnx.commit()
    except:
        cnx.rollback()
        print("Something Wrong with commit")
    cursor.close()
    cnx.close()
    file_l.close()
# import_movies()  # 967181 entries
# import_length()  # 333257 entries deleted, 633924 left
# import_budget()  # 42986 left
# import_mpaa()
# import_imdb()
# import_country()
import_language()

import_genre()

