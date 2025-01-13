#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :pathsToDb.py
@说明        :修改alist数据库
@时间        :2025/01/06 22:33:47
'''
import sqlite3
import os
from tool import readJson, getAlistMountPath, removeFile, stopAlist, startAlist, getTxtHash
import shutil
import tempfile
import json


def backupDb():
    config = readJson()
    dbPath = config.get("dataDbPath")
    backupPath = dbPath + ".bak"
    if os.path.exists(backupPath):
        os.remove(backupPath)
    shutil.copy(dbPath, backupPath)
    print(f"备份数据库 {backupPath}")


def list_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM x_search_nodes")
    tables = cursor.fetchall()
    cursor.close()
    conn.close()
    return tables


def preTempDB():
    config = readJson()
    pathsPath = "./data/paths.txt"
    excludeOption = config.get("excludeOption")
    mountPath = config.get("mountPath")
    # conn = sqlite3.connect(dbPath)
    if not os.path.exists("./data/tmp"):
        os.makedirs("./data/tmp", exist_ok=True)
    temp_db_file = tempfile.NamedTemporaryFile(suffix=".db",
                                               delete=False,
                                               dir="./data/tmp")
    temp_db_path = temp_db_file.name
    temp_db_file.close()
    print(f"临时数据库路径: {temp_db_path}")
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    # 创建表结构
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS x_search_nodes (
        parent TEXT,
        name TEXT,
        is_dir INTEGER,
        size INTEGER
    )
    ''')
    with open(pathsPath, 'r', encoding='utf-16') as file:
        for line in file:
            line = line.strip()
            line, extention = line.split('\t')
            path_parts = line.split('/')[excludeOption:]
            if len(path_parts) < 1:
                continue
            # 新增目录层级加到剔除目录层级后的信息前面
            parent = mountPath + '/' + '/'.join(path_parts[:-1])
            name = path_parts[-1]
            isDir = 1 if extention == "dir" else 0
            # 插入数据到表中
            cursor.execute(
                'INSERT INTO x_search_nodes (parent, name, is_dir, size) VALUES (?, ?, ?, 0)',
                (parent, name, isDir))
    cursor.execute('SELECT * FROM x_search_nodes WHERE is_dir = 1')
    with open('./data/dir.txt', 'w', encoding='utf-16') as file:
        for row in cursor.fetchall():
            file.write(str(row) + '\n')
    conn.commit()
    conn.close()
    return temp_db_path


def addDb(tempDbPath):
    config = readJson()
    targetDbPath = config.get("dataDbPath")
    conn = sqlite3.connect(targetDbPath)
    cursor = conn.cursor()
    cursor.execute(f"ATTACH DATABASE '{tempDbPath}' AS tempDb")
    cursor.execute('''
    INSERT INTO main.x_search_nodes (parent, name, is_dir, size)
    SELECT parent, name, is_dir, size FROM tempDb.x_search_nodes
    ''')
    cursor.execute('''
    DELETE FROM x_search_nodes 
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM x_search_nodes
        GROUP BY parent, name
    )
    ''')
    conn.commit()
    cursor.execute("DETACH DATABASE tempDb")
    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_x_search_nodes_parent ON x_search_nodes (parent);
    ''')
    conn.commit()
    conn.close()


def replaceDb(tempDbPath):
    config = readJson()
    targetDbPath = config.get("dataDbPath")
    conn = sqlite3.connect(targetDbPath)
    cursor = conn.cursor()
    cursor.execute(f"ATTACH DATABASE '{tempDbPath}' AS tempDb")
    cursor.execute("DELETE FROM x_search_nodes")
    cursor.execute(
        "INSERT INTO main.x_search_nodes (parent, name, is_dir, size) SELECT parent, name, is_dir, size FROM tempDb.x_search_nodes"
    )
    conn.commit()
    cursor.execute("DETACH DATABASE tempDb")
    cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_x_search_nodes_parent ON x_search_nodes (parent);
    ''')
    conn.commit()
    conn.commit()
    conn.close()


def main():
    config = readJson()
    lastPathsTxtHash = config.get("lastPathsTxtHash")
    nowPathsTxtHash = getTxtHash("./data/paths.txt")
    if lastPathsTxtHash == nowPathsTxtHash:
        print("文件未发生变化，不需要重新处理数据库索引")
        return
    else:
        config["lastPathsTxtHash"] = nowPathsTxtHash
        with open("./data/config.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(config, indent=4))
    print("关闭Alist")
    stopAlist()
    backupDb()
    # print(list_tables(config.get("dataDbPath")))
    tmpdb = preTempDB()
    if config.get("dbOperation") == "add":
        addDb(tmpdb)
    else:
        replaceDb(tmpdb)
    removeFile("./data/tmp")
    print("启动Alist")
    startAlist()


if __name__ == "__main__":
    main()
