import json
import os
from tool import getTreeTxt
from treeTxtToPath import convertTreeToPaths


def main():
    jsonDict = {
        "directoryTreeFile": " ",
        "strmSaveDir": " ",
        "alistUrl": " ",
        "mountPath": " ",
        "excludeOption": 0,
        "dataDbPath": " ",
        "dbOperation": " "
    }
    if not os.path.exists("./data"):
        os.makedirs("./data", exist_ok=True)
    with open("./data/config.json", "w", encoding="utf-8") as f:
        print("这里是配置文件生成器，使用前请先准备好目录树文件")
        txtPath = None
        while txtPath == None:
            inputPath = input("请输入目录树文件路径/URL：\n=>")
            txtPath = getTreeTxt(inputPath)
        jsonDict["directoryTreeFile"] = inputPath
        print("请准备一个空文件夹用于保存strm文件")
        strmSaveDir = input("请输入strm文件保存文件夹路径：\n=>")
        jsonDict["strmSaveDir"] = strmSaveDir
        print("strm文件保存文件夹路径已保存,请继续")
        alistUrl = input("请输入115网盘Alist URL：(例子：https://127.0.0.1:5244)\n=>")
        if alistUrl[-1] == "/":
            alistUrl = alistUrl[:-1]
        jsonDict["alistUrl"] = alistUrl
        mountPath = input("请输入Alist挂载路径：(例子：/我的文件)\n=>")
        if mountPath[0] == "/":
            mountPath = mountPath[1:]
        jsonDict["mountPath"] = mountPath
        print("Alist挂载路径已保存,请继续")
        paths = convertTreeToPaths(txtPath)[:10]
        convertTreeToPaths
        while True:
            print(f"当前指定alist地址为{alistUrl}/{mountPath}")
            print("以下是转换后的文件路径(前10条)：")
            for i in range(len(paths)):
                paths[i] = paths[i].split("\t")[0]
                print(paths[i])
            excludeOption = input(
                "请输入排除文件夹层级，0表示不排除，1表示排除根目录，以此类推：(例子：0-10)\n=>")
            print(f"处理后的文件路径将会排除前{excludeOption}层，如下:")
            for i in range(len(paths)):
                paths[i] = "/".join(paths[i].split("/")[int(excludeOption):])
            urls = []
            for path in paths:
                url = alistUrl + "/" + mountPath + "/" + path
                urls.append(url)
            for url in urls:
                print(f"处理后的文件路径：{url}")
            if input("是否确认？(Y/N)\n=>") == "Y" or "y":
                break
        jsonDict["excludeOption"] = int(excludeOption)
        dbPath = input("请输入数据库文件路径：\n=>")
        jsonDict["dataDbPath"] = dbPath
        print("请指定数据库操作类型")
        print("1.插入数据库")
        print("2.替换数据库")
        dbOperation = input("请选择数据库操作类型：\n=>")
        if dbOperation == "1":
            dbOperation = "add"
        elif dbOperation == "2":
            dbOperation = "replace"
        jsonDict["dbOperation"] = dbOperation
        print("config.json已生成")
        json.dump(jsonDict, f, indent=4)


if __name__ == "__main__":
    main()
