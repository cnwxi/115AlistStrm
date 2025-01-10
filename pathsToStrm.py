#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :pathsToStrm.py
@说明        :生成strm文件
@时间        :2025/01/06 21:52:02
'''
from tool import readJson, getAlistMountPath, getAllExtensions, removeFile
import os
from urllib.parse import quote

allExtensions = getAllExtensions()


def recursive_chown(strmSaveDir, uid, gid):
    for root, dirs, files in os.walk(strmSaveDir):
        os.chown(root, uid, gid)
        for file in files:
            file_path = os.path.join(root, file)
            os.chown(file_path, uid, gid)


def pathsToStrm():
    config = readJson()
    alist_base_url = getAlistMountPath(config)
    excludeOption = config.get("excludeOption")
    strmSaveDir = config.get("strmSaveDir")
    removeFile(strmSaveDir)
    if not os.path.exists(strmSaveDir):
        os.makedirs(strmSaveDir, exist_ok=True)  # root组

    with open("./data/paths.txt", "r", encoding="utf-16") as f:
        for line in f:
            line = line.strip()
            line, extention = line.split("\t")
            if extention == "dir":
                continue
            if len(line.split("/")) < excludeOption:
                continue
            addUrl = '/'.join((line.split("/")[excludeOption:]))
            saveDir = '/'.join((line.split("/")[excludeOption:-1]))
            saveDir = os.path.normpath(os.path.join(strmSaveDir, saveDir))
            if not os.path.exists(saveDir):
                os.makedirs(saveDir, exist_ok=True)
            fullUrl = f"{alist_base_url}/{quote(addUrl)}"
            writeDir = os.path.normpath(
                os.path.join(strmSaveDir, addUrl + ".strm"))
            with open(writeDir, "w", encoding="utf-8") as writeFile:
                writeFile.write(fullUrl)
    # 处理权限
    recursive_chown(strmSaveDir, 998, 998)


if __name__ == "__main__":
    pathsToStrm()
