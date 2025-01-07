#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件        :pathsToStrm.py
@说明        :生成strm文件
@时间        :2025/01/06 21:52:02
'''
from tool import readJson,getAlistMountPath,getAllExtensions,removeFile
import os
from urllib.parse import quote

allExtensions = getAllExtensions()


def pathsToStrm():
    config=readJson()
    alist_base_url=getAlistMountPath(config)
    excludeOption=config.get("excludeOption")
    strmSaveDir=config.get("strmSaveDir")
    removeFile(strmSaveDir)
    if not os.path.exists(strmSaveDir):
        os.makedirs(strmSaveDir,exist_ok=True)

    with open("./data/paths.txt","r",encoding="utf-16") as f:
        for line in f:
            line=line.strip() 
            line,extention=line.split("\t")
            if extention == "dir":
                continue
            if len(line.split("/"))<excludeOption:
                continue
            addUrl='/'.join((line.split("/")[excludeOption:]))
            saveDir='/'.join((line.split("/")[excludeOption:-1]))
            saveDir=os.path.normpath(os.path.join(strmSaveDir,saveDir))
            if not os.path.exists(saveDir):
                os.makedirs(saveDir,exist_ok=True)
                print(f"创建文件夹 {saveDir}")
            fullUrl=f"{alist_base_url}/{quote(addUrl)}"
            print(f"生成URL {fullUrl}")
            writeDir=os.path.normpath(os.path.join(strmSaveDir,addUrl+".strm"))
            print(f"写入文件 {writeDir}")
            with open(writeDir,"w",encoding="utf-16") as writeFile:
                writeFile.write(fullUrl)


if __name__ == "__main__":
    pathsToStrm()