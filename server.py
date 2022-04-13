# coding:utf-8
import web
from models.infer import PredModel
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from baiduspider import BaiduSpider


# init the torch model
model_name = 'ShuffleNetV2'
model_arg = {'class_num': 1000, 'channel_ratio': 1.0}
resize = (224, 224)
mean = [123.675, 116.28, 103.53]
std = [58.395, 57.12, 57.375]
pred_model = PredModel('ShuffleNetV2', model_arg, 'models/shufflenetv2_x1-5666bf0f80.pth', resize, mean, std)

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
            img, cls_names, cls_probs = pred_model.pred_img(image_file)

        #------------------------原版-----------------------------
        #     # matplot process image
        #     result_img = filedir + '/' + 'result.jpg'
        #     plt.clf()
        #     plt.subplot(2, 1, 1)
        #     plt.axis('off')
        #     plt.imshow(img)
        #     plt.subplot(2, 1, 2)
        #     cls_names.reverse()
        #     cls_probs.reverse()
        #     prob_max = np.array(cls_probs).max()
        #     print(prob_max)
        #     b = plt.barh(range(len(cls_names)), cls_probs, color='#6699CC')
        #     plt.yticks([])
        #     for x, y in enumerate(cls_probs):
        #         plt.text(0 + prob_max / 40, x, '%s' % cls_names[x])
        #     plt.savefig(result_img)
        #------------------------原版-----------------------------
            #取识别概率（得分）最高的一项作为检索关键字
            name = cls_names[0]
            #BaiduSpider接受的关键字不能包含空格，
                #一种方法是把空格替换成+
                #或是直接删除空格
            # index = BaiduSpider().search_pic(name.split(" ")[0]).plain        #取字符串的第一个单词
            index = BaiduSpider().search_pic(name.replace(' ', '+')).plain
            #取检索到的第一个图片链接
            img_url = index[0]['url']

        return render.detect(img_url,  'result:'+ name)
        # return render.detect(result_img, 'result:')       #原版


if __name__ == "__main__":

    # start the web server
    app = web.application(urls, globals())
    app.run()


