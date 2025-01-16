#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :pathsToStrm.py
@说明        :生成strm文件
@时间        :2025/01/06 21:52:02
'''
from tool import readJson, getAlistMountPath, getAllExtensions, removeFile, getVideoExtensions, getTxtHash
import os
from urllib.parse import quote
import json

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
    if not os.path.exists(strmSaveDir):
        os.makedirs(strmSaveDir, exist_ok=True)  # root组
    lastPathsTxtHash = config.get("lastPathsTxtHash")
    nowPathsTxtHash = getTxtHash("./data/paths.txt")
    if lastPathsTxtHash == nowPathsTxtHash:
        print("文件未发生变化，不需要重新生成strm文件")
        return
    else:
        config["lastPathsTxtHash"] = nowPathsTxtHash
        with open("./data/config.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(config, indent=4))
    removeFile(strmSaveDir)
    someExtensions = getVideoExtensions()
    with open("./data/paths.txt", "r", encoding="utf-16") as f:
        for line in f:
            line = line.strip()
            line, extention = line.split("\t")
            if extention == "dir" or extention not in someExtensions:
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
    print("strm文件生成完毕")


if __name__ == "__main__":
    pathsToStrm()
