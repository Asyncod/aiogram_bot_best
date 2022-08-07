# -*- coding: utf-8 -*-
import sqlite3 as sql

con = sql.connect("data.db")
cur = con.cursor()


## CREATE DATEBASE ##
def create_db():
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    id_user INTEGER,
                    username TEXT,
                    name TEXT,
                    refer_count INTEGER,
                    invited INTEGER,
                    balance INTEGER,    
                    withdraw INTEGER)""")
    con.commit()


## ALL NEW DATA : CHANGE BASE ##
def new_user(id_user, username, name):
    print(f"в базе появился {username}")
    if username != None:
        cur.execute("""INSERT INTO users(id_user, username, name, refer_count, invited, balance, withdraw) VALUES(?, ?, ?, ?, ?, ?, ?)""",
                    (id_user, username, name, 0, 0, 0, 0))
        con.commit()
    else:
        cur.execute("""INSERT INTO users(id_user, username, name, refer_count, invited, balance, withdraw) VALUES(?, ?, ?, ?, ?, ?, ?)""",
                    (id_user, None, name, 0, 0, 0, 0))
        con.commit()

def new_referal(id_user):
    cur.execute("UPDATE users SET refer_count=refer_count+1 WHERE id_user = ?", (id_user,))
    con.commit()

def add_balance(id_user):
    # Open file, check ID and get her BABLO
    all_unik_id = open("unik_id.txt", "r").read().split("\n")
    all_balance = open("unik_balance.txt", "r").read().split("\n")
    dict_unik = dict(zip(all_unik_id, all_balance))

    ref_count = get_referal(id_user)
    if str(id_user) in all_unik_id:
        count = dict_unik[str(id_user)]
    elif (0 <= ref_count < 10):
        count = 0.015
    elif (10 <= ref_count < 20):
        count = 0.03
    elif (20 <= ref_count < 30):
        count = 0.048
    elif (30 <= ref_count < 40):
        count = 0.063
    elif (40 <= ref_count < 50):
        count = 0.079
    elif (50 <= ref_count < 60):
        count = 0.094
    elif (60 <= ref_count < 70):
        count = 0.11
    elif (70 <= ref_count < 80):
        count = 0.13
    elif (80 <= ref_count < 90):
        count = 0.14
    elif (90 <= ref_count < 100):
        count = 0.16
    elif (ref_count >= 100):
        count = 0.16

    cur.execute(f"UPDATE users SET balance=balance+{count} WHERE id_user = ?", (id_user,))
    cur.execute(f"UPDATE users SET withdraw=withdraw+{count} WHERE id_user = ?", (id_user,))
    con.commit()

def add_invited(id_user, inviter):
    cur.execute(f"UPDATE users SET invited = ? WHERE id_user = ?", (inviter, id_user,))
    con.commit()

def cleaning_withdraw(id_user):
    cur.execute("UPDATE users SET withdraw = ? WHERE id_user = ?", (0, id_user,))
    con.commit()


## ALL GET DATA : VIEW BASE ##
def get_user(id_user):
    cur.execute("SELECT id_user FROM users WHERE id_user = ?", (id_user,))
    id_us = cur.fetchone()
    return id_us

def get_referal(id_user):
    cur.execute("SELECT refer_count FROM users WHERE id_user = ?", (id_user,))
    refer = cur.fetchone()
    if (refer == None):
        return 0
    else:
        return refer[0]

def get_balance(id_user):
    cur.execute("SELECT balance FROM users WHERE id_user = ?", (id_user,))
    balance = cur.fetchone()
    if (balance == None):
        return 0
    else:
        return balance[0]

def get_withdraw(id_user):
    cur.execute("SELECT withdraw FROM users WHERE id_user = ?", (id_user,))
    withdraw = cur.fetchone()
    if (withdraw == None):
        return 0
    else:
        return withdraw[0]

def get_name(id_user):
    cur.execute("SELECT name FROM users WHERE id_user = ?", (id_user,))
    name = cur.fetchone()
    return name[0]

def get_username(id_user):
    cur.execute("SELECT username FROM users WHERE id_user = ?", (id_user,))
    username = cur.fetchone()
    return username[0]

def get_count_man():
    cur.execute("SELECT id FROM users")
    all_man = cur.fetchall()
    return (len(all_man))

def get_lider():
    cur.execute("SELECT id_user, username, name, refer_count FROM users ORDER BY refer_count DESC")
    table = cur.fetchall()
    return table
