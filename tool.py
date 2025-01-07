#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :tool.py
@说明        :工具函数
@时间        :2025/01/06 21:49:37
"""
import json
import shutil
import os
from urllib.parse import quote


builtinAudioExtensions = [
    "mp3",
    "flac",
    "wav",
    "aac",
    "ogg",
    "wma",
    "alac",
    "m4a",
    "aiff",
    "ape",
    "dsf",
    "dff",
    "wv",
    "pcm",
    "tta",
]
builtinVideoExtensions = [
    "mp4",
    "mkv",
    "avi",
    "mov",
    "wmv",
    "flv",
    "webm",
    "vob",
    "mpg",
    "mpeg",
]
builtinImageExtensions = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "svg", "heic"]
builtinProgramExtensions = ["apk", "exe", "msi", "dmg", "deb", "rpm", "appimage"]
builtinZipExtensions = ["zip", "7z", "rar"]
builtinOtherExtensions = [
    "iso",
    "img",
    "bin",
    "nrg",
    "cue",
    "dvd",
    "lrc",
    "srt",
    "sub",
    "ssa",
    "ass",
    "vtt",
    "txt",
    "pdf",
    "doc",
    "docx",
    "csv",
    "xml",
    "new",
]


def getAllExtensions():
    allExtensions = (
        builtinAudioExtensions
        + builtinVideoExtensions
        + builtinImageExtensions
        + builtinProgramExtensions
        + builtinZipExtensions
        + builtinOtherExtensions
    )
    return allExtensions


def readJson():
    filePath = "./data/config.json"
    with open(filePath, "r", encoding="utf-8") as file:
        return json.load(file)


def getAlistMountPath(config):
    alist_url = config.get("alistUrl")
    mount_path = config.get("mountPath")
    if alist_url[-1] == "/":
        alist_url = alist_url[:-1]
    if mount_path[0] == "/":
        mount_path = mount_path[1:]
    return f"{alist_url}/{quote(mount_path)}"


def removeFile(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"已删除文件夹: {folder_path}")
    else:
        print(f"文件夹不存在: {folder_path}")
