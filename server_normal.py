from flask import Flask, redirect, url_for, request,Response
import requests
import os
app = Flask(__name__)
my_headers = {'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.31(0x18001f28) NetType/WIFI Language/en', 'Referer' : 'http://singer.ink/index.php?m=app&a=map'}

@app.route('/')
def index_chache():
     if request.method == 'GET':
         x = request.args.get('x')
         y = request.args.get('y')
         z = request.args.get('z')
         if x==None or y==None and z==None:
            return("error: 需要参数xyz")
         if x.isdigit()!=True and y.isdigit()!=True and z.isdigit()!=True:
            return("error: 参数不是数字")

         try:
            with open("data/{}/{}/{}.jpg".format(z,x,y),"rb") as f:
                    img=f.read()
                    resp=Response(img, mimetype="image/jpeg")
                    print("检测到瓦片块，返回图片")
                    return resp
         except Exception as ex:
            with open("data/default.png","rb") as f:
                res=f.read()
            print("瓦片块不存在，返回默认图片")
            return(Response(res,mimetype="image/png"))
         
if __name__ == '__main__':
    app.run(debug = True)


     