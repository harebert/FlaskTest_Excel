import os

for rootISEF, dirsISEF, filesISEF in os.walk("D:\课程备课\服务器支援网站web\FlaskTest_Excel卷积\static\ISEF\ISEFROBO",
                                             topdown=False):
    pass
#     for name in filesISEF:
#         print(os.path.join(rootISEF, name))
#     for name in dirsISEF:
#         print(os.path.join(rootISEF, name))
# print(dirsISEF)


import sqlite3
import time

conn = sqlite3.connect('D:\课程备课\服务器支援网站web\FlaskTest_Excel卷积\Data\Dataset.db')

c = conn.cursor()

for i, I in enumerate(dirsISEF):
    for root, dirs, files in os.walk("D:\课程备课\服务器支援网站web\FlaskTest_Excel卷积\static\ISEF\ISEFROBO\\" + I, topdown=False):
        itemFolder = I
        itemID = I.split(" - ")[0]
        itemName = I.split(" - ")[1]
        itemIcon = ""
        itemInfo = ""
        itemImage = ""
        itemClass = "ISEFROBO"
        itemVideo = ""
        for eachFile in files:
            fileName = eachFile.split(".")[0]
            fileExt = eachFile.split(".")[1]
            # 在文件加下，如果文件名等于项目名，则是标题图片，否则是项目图片
            if fileExt == "jpg" or fileExt == "png":
                if fileName == itemID:
                    itemIcon = eachFile
                else:
                    itemImage += "|" + eachFile
            elif fileExt == "txt":
                f = open("D:\课程备课\服务器支援网站web\FlaskTest_Excel卷积\static\ISEF\ISEFROBO\\" + I + "\\" + eachFile, "r")
                itemLineInfo = f.readlines()
            elif fileExt == "mp4":
                itemVideo = eachFile
        # print(root)
        print(itemLineInfo)

        print("itemID", itemID)
        print("itemName", itemName)
        #         itemName=itemName.replace("'","_")
        #         itemName=itemName.replace('"',"_")
        print("itemIcon", itemIcon)
        print("itemImage", itemImage)

        print("itemVideo", itemVideo)
        for i in itemLineInfo:
            itemInfo += i.replace("\n","\\n")
            #itemInfo+=i+"\\n"#.replace("\n","")+"<br>"
        print(itemInfo)
        itemInfo = itemInfo.replace("'", "_")
        itemInfo = itemInfo.replace('"', "_")
        #itemInfo = itemInfo.replace('\n', "<br>")
        print("itemInfo", itemInfo)
        print("itemFolder", itemFolder)
        print()
    sql = "INSERT INTO ISEF (itemID,  itemName,  itemIcon,  itemInfo, itemImage, itemClass, itemFolder, itemVideo) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % (
    itemID, itemName, itemIcon, itemInfo, itemImage, itemClass, itemFolder, itemVideo)
    print(sql)
    c.execute(sql)
    conn.commit()