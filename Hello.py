# coding:utf-8
from flask import Flask, g
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename
import os
from os.path import join, dirname, realpath
import math
import time

#彩色Excel文件和Excel文件

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'



UPLOAD_PATH = os.path.join(os.path.dirname(__file__),'uploads')

@app.route('/uploads/<filename>/')
def get_image(filename):
	return send_from_directory(UPLOAD_PATH,filename)


def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v
def img2ExcelColor(img,Excel):
    # 读取图片，转为excel
    import xlsxwriter  # 导入模块
    workbook = xlsxwriter.Workbook(Excel)  # 新建excel表
    worksheet = workbook.add_worksheet('sheet1')  # 新建sheet（sheet的名称为"sheet1"）
    worksheet.set_column('A:XFD', 2)  # 设置所有列宽为2
    worksheet.set_zoom(10)
    cell_format = workbook.add_format()

    from PIL import Image
    import numpy as np

    image = Image.open(img)
    # print(np.array(image))

    imageArray = []
    for i, I in enumerate(np.array(image)):
        tempRow = []
        for j, J in enumerate(I):
            tempRow.append("#{:0>2s}{:0>2s}{:0>2s}".format(hex(J[0])[2:], hex(J[1])[2:], hex(J[2])[2:]))
        imageArray.append(tempRow)

    # print(imageArray)

    for i, I in enumerate(imageArray):
        for j, J in enumerate(I):
            cell_format = workbook.add_format()
            cell_format.set_fg_color(J)
            worksheet.write(i, j, '', cell_format)

    workbook.close()
def img2ExcelBlack(img,Excel):
    import xlsxwriter  # 导入模块
    workbook = xlsxwriter.Workbook(Excel)  # 新建excel表
    worksheet = workbook.add_worksheet('sheet1')  # 新建sheet（sheet的名称为"sheet1"）
    worksheet.set_column('A:XFD', 2)  # 设置所有列宽为2

    cell_format = workbook.add_format()
    cell_format.set_bg_color('red')

    from PIL import Image
    import numpy as np

    image = Image.open(img)

    imageArray = []

    for i, I in enumerate(np.array(image)):
        tempRow = []
        for j, J in enumerate(I):
            tempRow.append(765 - sum(J))
        imageArray.append(tempRow)

    for i, I in enumerate(imageArray):
        for j, J in enumerate(I):
            worksheet.write(i, j, imageArray[i][j])
    workbook.close()

def img2ExcelColorLBP(img,Excel):
    # 读取图片，转为excel
    import xlsxwriter  # 导入模块
    workbook = xlsxwriter.Workbook(Excel)  # 新建excel表
    worksheet = workbook.add_worksheet('sheet1')  # 新建sheet（sheet的名称为"sheet1"）
    worksheet.set_column('A:XFD', 2)  # 设置所有列宽为2
    worksheet.set_zoom(10)
    cell_format = workbook.add_format()

    from PIL import Image
    import numpy as np

    image = Image.open(img)
    # print(np.array(image))

    imageArray = []
    for i, I in enumerate(np.array(image)):
        tempRow = []
        for j, J in enumerate(I):
            tempRow.append("#{:0>2s}{:0>2s}{:0>2s}".format(hex(J[0])[2:], hex(J[1])[2:], hex(J[2])[2:]))
        imageArray.append(tempRow)

    # print(imageArray)

    for i, I in enumerate(imageArray):
        for j, J in enumerate(I):
            cell_format = workbook.add_format()
            cell_format.set_fg_color(J)
            worksheet.write(i, j, '', cell_format)

    workbook.close()
def img2ExcelBlackLBP(img,Excel):
    import xlsxwriter  # 导入模块
    workbook = xlsxwriter.Workbook(Excel)  # 新建excel表
    worksheet = workbook.add_worksheet('sheet1')  # 新建sheet（sheet的名称为"sheet1"）
    worksheet.set_column('A:XFD', 2)  # 设置所有列宽为2

    cell_format = workbook.add_format()
    cell_format.set_bg_color('red')

    from PIL import Image
    import numpy as np

    #image = Image.open(img)
    image=img
    imageArray = []

    for i, I in enumerate(np.array(image)):
        tempRow = []
        for j, J in enumerate(I):
            tempRow.append(765 - sum(J))
        imageArray.append(tempRow)

    for i, I in enumerate(imageArray):
        for j, J in enumerate(I):
            worksheet.write(i, j, imageArray[i][j])
    workbook.close()
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/softwareDownload')
def softwareDownload():
    return render_template('softwareDownload.html')


@app.route('/uploads', methods=['POST', 'GET'])
def uploads():
    return "uploads/"


@app.route('/convolutionScaled', methods=['POST', 'GET'])

def convolutionScaled():
    import uuid
    import xlsxwriter  # 导入模块
    newfilename = str(uuid.uuid1())
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        filename = secure_filename(f.filename)
        upload_path = os.path.join(basepath,  'uploads', secure_filename(f.filename))
        print(upload_path)
        if filename.split(".")[1].lower()=="png" or filename.split(".")[1].lower()=="jpg":

            f.save(upload_path)
            session["CONVfilename"] = newfilename
            session["CONVextName"]=filename.split(".")[1]
            import PIL.Image as Image

            infile = os.path.join(basepath,  'uploads', secure_filename(f.filename))
            outfile = os.path.join(basepath,  'static/') +newfilename+"."+ filename.split(".")[1]
            print(outfile)
            im = Image.open(infile)
            (x, y) = im.size  # read image size
            #------------------保持原始比例---------------------------------
            if x>y:
                y_s=200
                x_s=int(x/(y/200))
            else:
                x_s=200
                y_s=int(y/(x/200))

            #------------------宽高皆为200---------------------------------
            #x_s = 200  # define standard width
            #y_s = 200  # y * x_s / x  # calc height based on standard width
            #-------------------------------------------------------------
            out = im.resize((x_s, y_s), Image.ANTIALIAS)  # resize image with high-quality
            out.save(outfile)

            img2ExcelColor(outfile,os.path.join(basepath,  'static/') + newfilename + '_c.xlsx')
            img2ExcelBlack(outfile,os.path.join(basepath,  'static/') + newfilename + '_b.xlsx')

            print(newfilename)

            return redirect(url_for('convolutionScaled'))
    return render_template('uploadConvolution.html')

@app.route('/uploadLBP', methods=['POST', 'GET'])
def uploadLBP():
    def saveTextFile(fileName, image):
        import numpy as np
        tempTxt = ""
        imageArray = []
        imageArray = np.array(image)
        for i, I in enumerate(imageArray):
            for j, J in enumerate(I):
                tempTxt = tempTxt + str(int(sum(imageArray[i][j])/7.65)) + "\n"
        txtFileName = os.path.join(basepath, 'static/') + fileName + ".txt"
        f = open(txtFileName, 'w')
        f.write(tempTxt)
        f.close()

    print("this is lbp")
    import uuid
    import xlsxwriter  # 导入模块
    newfilename = str(uuid.uuid1())
    if request.method == 'POST':
        print("this is upload")
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        filename = secure_filename(f.filename)
        upload_path = os.path.join(basepath,  'uploads', secure_filename(f.filename))
        print(upload_path)
        if filename.split(".")[1].lower()=="png" or filename.split(".")[1].lower()=="jpg":

            f.save(upload_path)
            session["LBPfilename"] = newfilename
            session["LBPextName"]=filename.split(".")[1]
            import PIL.Image as Image
            import PIL.ImageEnhance as ImageEnhance
            infile = os.path.join(basepath,  'uploads', secure_filename(f.filename))
            outfile = os.path.join(basepath,  'static/') +newfilename+"."+ filename.split(".")[1]
            outfileB = os.path.join(basepath, 'static/') + newfilename + "B." + filename.split(".")[1]
            outfileD = os.path.join(basepath, 'static/') + newfilename + "D." + filename.split(".")[1]
            outfileT4 = os.path.join(basepath, 'static/') + newfilename + "T4." + filename.split(".")[1]
            #print(outfile)
            im = Image.open(infile)


            (x, y) = im.size  # read image size
            x_s = 200  # define standard width
            y_s = 200  # y * x_s / x  # calc height based on standard width
            out = im.resize((x_s, y_s), Image.ANTIALIAS)  # resize image with high-quality

            en = ImageEnhance.Brightness(out)
            imDefault=out
            imBright = en.enhance(1.8)
            imDark = en.enhance(0.6)
            imDeep=en.enhance(0.2)

            out.save(outfile)
            imBright.save(outfileB)
            imDark.save(outfileD)


            #拼多宫格图片
            IMAGES_FORMAT = ['.png', '.PNG', '.jpg', ".JPG"]  # 图片格式
            # 获取图片集地址下的所有图片名称
            #image_names = [name for name in os.listdir(imgDir) for item in IMAGES_FORMAT if os.path.splitext(name)[1] == item]
            # 定义图像拼接函数
            to_image = Image.new('RGB', (200, 200))  # 创建一个新图
            # 循环遍历，把每张图片按顺序粘贴到对应位置上
            from_image = None
            from_image = imDeep.resize((100, 100), Image.ANTIALIAS)
            to_image.paste(from_image, (0, 0))
            from_image = imDark.resize((100, 100), Image.ANTIALIAS)
            to_image.paste(from_image, (100, 0))
            from_image = imDefault.resize((100, 100), Image.ANTIALIAS)
            to_image.paste(from_image, (0, 100))
            from_image = imBright.resize((100, 100), Image.ANTIALIAS)
            to_image.paste(from_image, (100, 100))
            to_image.save(outfileT4)
            saveTextFile(newfilename + "T4",to_image)
            img2ExcelBlackLBP(to_image,os.path.join(basepath,  'static/') +newfilename+"T4.xlsx")
            saveTextFile(newfilename + "B", imBright)
            img2ExcelBlackLBP(imBright, os.path.join(basepath,  'static/') +newfilename + "B.xlsx")
            saveTextFile(newfilename + "D", imDark)
            img2ExcelBlackLBP(imDark, os.path.join(basepath,  'static/') +newfilename + "D.xlsx")
            saveTextFile(newfilename + "f", out)
            img2ExcelBlackLBP(out, os.path.join(basepath,  'static/') +newfilename + "f.xlsx")






            return redirect(url_for('uploadLBP'))
    return render_template('uploadLBP.html')


@app.route('/uploadHSV',methods=['POST','GET'])
def uploadHSV():
    import uuid
    import xlsxwriter  # 导入模块
    newfilename = str(uuid.uuid1())
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        filename = secure_filename(f.filename)
        upload_path = os.path.join(basepath,  'uploads', secure_filename(f.filename))
        print(upload_path)
        if filename.split(".")[1].lower()=="png" or filename.split(".")[1].lower()=="jpg":

            f.save(upload_path)
            session["HSVfilename"] = newfilename
            session["HSVextName"]=filename.split(".")[1]
            import PIL.Image as Image

            infile = os.path.join(basepath,  'uploads', secure_filename(f.filename))
            outfile = os.path.join(basepath,  'static/') +newfilename+"."+ filename.split(".")[1]
            print(outfile)
            im = Image.open(infile)
            (x, y) = im.size  # read image size
            x_s = 200  # define standard width
            y_s = 200  # y * x_s / x  # calc height based on standard width
            out = im.resize((x_s, y_s), Image.ANTIALIAS)  # resize image with high-quality
            out.save(outfile)


            print(newfilename)
            workbook = xlsxwriter.Workbook(os.path.join(basepath,  'static/') + newfilename + '.xlsx')  # 新建excel表
            worksheet = workbook.add_worksheet('sheet1')  # 新建sheet（sheet的名称为"sheet1"）
            worksheet.set_column('A:XFD', 2)  # 设置所有列宽为2

            cell_format = workbook.add_format()
            cell_format.set_bg_color('red')

            from PIL import Image
            import numpy as np

            image = Image.open(outfile)
            # print(np.array(image))
            tempTxt=""
            imageArray = []
            HArray=[]
            SArray=[]
            VArray=[]
            for i, I in enumerate(np.array(image)):
                tempRow = []
                for j, J in enumerate(I):
                    tempRow.append(765 - sum(J))
                    H,S,V=rgb2hsv(J[0],J[1],J[2])
                    HArray.append(int(H/3.6))
                    SArray.append(int(S*100))
                    VArray.append(int(V*100))
                imageArray.append(tempRow)

            #print(imageArray)

            for i, I in enumerate(imageArray):
                for j, J in enumerate(I):
                    worksheet.write(i, j, imageArray[i][j])
                    tempTxt = tempTxt + str(imageArray[i][j]) +"\n"
            workbook.close()
            txtFileName=os.path.join(basepath,  'static/') + newfilename+".txt"
            f = open(txtFileName,'w')
            f.write(tempTxt)
            f.close()
            print(HArray)


            tempTxt = ""
            for i, I in enumerate(HArray):
                tempTxt = tempTxt + str(I) +"\n"
            txtFileName=os.path.join(basepath,  'static/') + newfilename+"_H.txt"
            f = open(txtFileName,'w')
            f.write(tempTxt)
            f.close()


            tempTxt = ""
            for i, I in enumerate(SArray):
                tempTxt = tempTxt + str(I) +"\n"
            txtFileName=os.path.join(basepath,  'static/') + newfilename+"_S.txt"
            f = open(txtFileName,'w')
            f.write(tempTxt)
            f.close()

            tempTxt = ""
            for i, I in enumerate(VArray):
                    tempTxt = tempTxt + str(I) +"\n"
            txtFileName=os.path.join(basepath,  'static/') + newfilename+"_V.txt"
            f = open(txtFileName,'w')
            f.write(tempTxt)
            f.close()
            return redirect(url_for('uploadHSV'))
    return render_template('uploadHSV.html')


@app.route('/recordRelative',methods=['POST','GET'])    #正负相关性网页学生作品记录
def recordRelative():
    tempDic = {}
    if request.method == 'POST':
        tempDic={}
        for i,I in request.values.items():
            tempDic[i]=I
        print(tempDic)
        import sqlite3
        import time
        basepath = os.path.dirname(__file__)
        datafilePath=os.path.join(basepath, 'Data/Dataset.db')
        conn = sqlite3.connect(datafilePath)
        class_=tempDic["Grade"]
        stu_s=tempDic["stus"]
        Urls=tempDic["url"].replace("'","_")
        date_=time.strftime("%Y-%m-%d", time.localtime())
        time_=time.strftime("%H:%M:%S", time.localtime())
        c = conn.cursor()
        timeNow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #print(timeNow)
        sql = "INSERT INTO relativeData (class_,stus_,Urls_,date_,time_) VALUES ('%s','%s','%s','%s','%s')" % (class_,stu_s,Urls,date_, time_)
        print(sql)
        c.execute(sql)

        conn.commit()
        # conn.close()
        tempDic["status"]="Success"
        print("增加数据成功")
        return render_template('uploadSuccess.html' ,contents=tempDic)
    else:
        tempDic["status"] = "Failed"
        tempDic["url"]="ai.sfls.cn"
        return render_template('uploadSuccess.html' ,contents=tempDic)

@app.route('/seeRelativeScore',methods=['POST','GET'])    #正负相关性网页学生作品记录查看
def seeRelativeScore():
    import sqlite3
    #如果有加分减分的动作，则先登分
    basepath = os.path.dirname(__file__)
    datafilePath = os.path.join(basepath, 'Data/Dataset.db')
    conn = sqlite3.connect(datafilePath)
    c = conn.cursor()
    if request.method == 'POST':
        tempDic = {}
        #print(request.values)
        for i, I in request.values.items():
            tempDic[i] = I
            print(I)
        pass

        if tempDic["action"]=="add":
            sql = "UPDATE relativeData SET score = score +1  where id=%d" % int(tempDic["id_"])
        elif tempDic["action"]=="min":
            sql = "UPDATE relativeData SET score = score -1  where id=%d" % int(tempDic["id_"])
        elif tempDic["action"][0] == "p":  # tempDic是P1 P2 P3 P4 P5等字符进行拆分
            sql = "UPDATE relativeData SET score = %d  where id=%d" % (int(tempDic["action"][1]), int(tempDic["id_"]))
            print(sql)
            # elif tempDic["action"] == "p8":
            #     sql = "UPDATE relativeData SET score = 8  where id=%d" % int(tempDic["id_"])
            #     print(sql)
            # elif tempDic["action"] == "p10":
            #     sql = "UPDATE relativeData SET score = 10  where id=%d" % int(tempDic["id_"])
        elif tempDic["action"] == "vote":  # tempDic是P1 P2 P3 P4 P5等字符进行拆分
            #sql = "UPDATE relativeData SET score = %d  where id=%d" % (int(tempDic["action"][1]), int(tempDic["id_"]))
            sql = "UPDATE relativeData SET A = %d,B = %d,C = %d,D = %d,E = %d  where id=%d" % (int(tempDic["A"]),int(tempDic["B"]),int(tempDic["C"]),int(tempDic["D"]),int(tempDic["E"]), int(tempDic["id_"]))
            #print(sql)
            #print(sql)
        print(sql)
        c.execute(sql)

        conn.commit()
        # conn.close()

    #如果是查看GET，则返回所有记录

    classDic = {}
    # print(request.values)
    for i, I in request.values.items():
        classDic[i] = I
        print(I)
    print(classDic)
    # 通过get方式，选择班级，
    try:
        if classDic["class"] == "G6C2":
            sql = "select * from relativeData where class_='%s' order by score desc" % "中预(2)班"
        elif classDic["class"] == "G6C3":
            sql = "select * from relativeData where class_='%s' order by score desc" % "中预(3)班"
        elif classDic["class"] == "G6C7":
            sql = "select * from relativeData where class_='%s' order by score desc" % "中预(MYP)班"
        else:
            sql = "select * from relativeData order by score desc"
    except:
        classDic["class"] = ""
        sql = "select * from relativeData order by score desc"

    content = c.execute(sql)
    record=[]
    for row in content:
        tempDic = {}
        tempDic["id_"]=row[0]
        tempDic["class_"] = row[1]
        tempDic["stus_"] = row[2]
        tempDic["Urls_"] = row[3]
        tempDic["date_"] = row[4]
        tempDic["time_"] = row[5]
        tempDic["score_"] = row[6]
        tempDic["A"] = row[7]
        tempDic["B"] = row[8]
        tempDic["C"] = row[9]
        tempDic["D"] = row[10]
        tempDic["E"] = row[11]
        if (int(row[7])+int(row[8])+int(row[9])+int(row[10])+int(row[11]))!=0:
            tempDic["voteScore"]=100/((int(row[7])+int(row[8])+int(row[9])+int(row[10])+int(row[11]))*4)*((int(row[7])*4+int(row[8])*3+int(row[9])*2+int(row[10])))
        else:
            tempDic["voteScore"] = 0
        #tempDic["id"] = row[0]
        record.append(tempDic)
        #print(row)
    #print(record)
    return render_template('seeRelativeScore.html' ,contents=record)

        # tempDic["status"] = "Failed"
        # tempDic["url"]="ai.sfls.cn"
       # return render_template('uploadSuccess.html' ,contents=tempDic)


@app.route('/seeRelativeStu',methods=['POST','GET'])    #正负相关性网页学生作品记录查看
def seeRelativeSut():
    import sqlite3
    #如果有加分减分的动作，则先登分
    basepath = os.path.dirname(__file__)
    datafilePath = os.path.join(basepath, 'Data/Dataset.db')
    conn = sqlite3.connect(datafilePath)
    c = conn.cursor()
    if request.method == 'POST':
        tempDic = {}
        print(request.values)
        for i, I in request.values.items():
            tempDic[i] = I
            print(I)
        print(tempDic)

        if tempDic["action"]=="add":
            sql = "UPDATE relativeData SET score = score +1  where id=%d" % int(tempDic["id_"])
            print(sql)
        elif tempDic["action"]=="min":
            sql = "UPDATE relativeData SET score = score -1  where id=%d" % int(tempDic["id_"])
            print(sql)
        elif tempDic["action"][0]=="p": #tempDic是P1 P2 P3 P4 P5等字符进行拆分
            sql = "UPDATE relativeData SET score = %d  where id=%d" % (tempDic["action"][1],int(tempDic["id_"]))
            print(sql)
        # elif tempDic["action"] == "p8":
        #     sql = "UPDATE relativeData SET score = 8  where id=%d" % int(tempDic["id_"])
        #     print(sql)
        # elif tempDic["action"] == "p10":
        #     sql = "UPDATE relativeData SET score = 10  where id=%d" % int(tempDic["id_"])
            print(sql)

        c.execute(sql)

        conn.commit()
        # conn.close()

    #如果是查看GET，则返回所有记录


    classDic={}
    #print(request.values)
    for i, I in request.values.items():
        classDic[i] = I
        print(I)
    print(classDic)
    #通过get方式，选择班级，
    try:
        if classDic["class"]=="G6C2":
            sql="select * from relativeData where class_='%s' order by score desc"%"中预(2)班"
        elif classDic["class"]=="G6C3":
            sql = "select * from relativeData where class_='%s' order by score desc"%"中预(3)班"
        elif classDic["class"]=="G6C7":
            sql = "select * from relativeData where class_='%s' order by score desc"%"中预(MYP)班"
        else:
            sql = "select * from relativeData order by score desc"
    except:
        classDic["class"] = ""
        sql="select * from relativeData order by score desc"

    content = c.execute(sql)
    record= {}
    success=[]
    failed=[]
    unknown=[]
    for row in content:
        tempDic = {}
        tempDic["id_"]=row[0]
        tempDic["class_"] = row[1]
        tempDic["stus_"] = row[2]
        tempDic["Urls_"] = row[3]
        tempDic["date_"] = row[4]
        tempDic["time_"] = row[5]
        tempDic["score_"] = row[6]
        tempDic["A"] = row[7]
        tempDic["B"] = row[8]
        tempDic["C"] = row[9]
        tempDic["D"] = row[10]
        tempDic["E"] = row[11]
        if (int(row[7])+int(row[8])+int(row[9])+int(row[10])+int(row[11]))!=0:
            tempDic["voteScore"]=int(100/((int(row[7])+int(row[8])+int(row[9])+int(row[10])+int(row[11]))*4)*((int(row[7])*4+int(row[8])*3+int(row[9])*2+int(row[10]))))
        else:
            tempDic["voteScore"] = 0
        #tempDic["id"] = row[0]
        if tempDic["score_"]>5:
            success.append(tempDic)
        elif tempDic["score_"]>0:
            failed.append(tempDic)
        else:
            unknown.append(tempDic)
        #print(row)
    record["success"]=success
    record["failed"]=failed
    record["unknown"]=unknown
    record["class_"]=classDic["class"]
    #print(record)
    #return render_template('seeRelativeStu.html' ,contents=record)
    return render_template('fixing.html')
        # tempDic["status"] = "Failed"
        # tempDic["url"]="ai.sfls.cn"
       # return render_template('uploadSuccess.html' ,contents=tempDic)
if __name__=="__main__":
    app.run(host="0.0.0.0", port=5050,debug=True)