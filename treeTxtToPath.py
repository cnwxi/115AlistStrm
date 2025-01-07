#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :treeTxtToPath.py
@说明        :将115生成的树形目录转换为文件路径
@时间        :2025/01/06 20:58:24
"""

import os
import requests
from tool import readJson, getAllExtensions, removeFile, getTreeTxt


def convertTreeToPaths(filePath):
    paths = []
    stack = []

    with open(filePath, "r", encoding="utf-16") as f:
        for line in f:
            depth = line.count("|") - 1
            name = line.split("|")[-1].strip().strip("-").strip("—")
            while len(stack) > depth:
                stack.pop()
            stack.append(name)
            singlePath = "/".join(stack)

            _, extention = os.path.splitext(singlePath)
            extention = extention.lower().strip(".")
            allExtensions = getAllExtensions()
            if extention not in allExtensions:
                extention = "dir"
            paths.append(f"{singlePath}\t{extention}")
    return paths


def main():
    config = readJson()
    txtFile = getTreeTxt(config.get("directoryTreeFile"))
    paths = convertTreeToPaths(txtFile)
    with open("./data/paths.txt", "w", encoding="utf-16") as f:
        for path in paths:
            f.write(path + "\n")
            print(path)


if __name__ == "__main__":
    main()
