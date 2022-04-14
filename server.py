# coding:utf-8
import web
import os
from baiduspider import BaiduSpider
from models.xception65 import run_moudle

# init the web server
render = web.template.render('templates/')
urls = ('/.*', 'process')

class process:
    def GET(self):
        return render.index()
        
    def POST(self):
        x = web.input(image_file={})
        if 'image_file' in x:
            # save image
            filedir = './static'
            filepath=x.image_file.filename.replace('\\','/')
            filename=filepath.split('/')[-1]
            fout = open(filedir +'/'+ filename,'wb')
            fout.write(x.image_file.file.read())
            fout.close()

            # pred image
            image_file = filedir + '/' + filename
            #通过图像识别模块返回识别到的内容字段：cls_names
            cls_names, cls_probs = run_moudle(image_file)

            #取识别概率（得分）最高的一项作为检索关键字
            name = cls_names[0]
            #BaiduSpider接受的关键字不能包含空格，
                #一种方法是把空格替换成+
                #或是直接删除空格
            index = BaiduSpider().search_pic(name.replace(' ', '+')).plain
            #取检索到的第一个图片链接
            img_url = index[0]['url']
        return render.detect(img_url,  'result:'+ name)


if __name__ == "__main__":
    # start the web server
    app = web.application(urls, globals())
    app.run()


