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
                    print("检测到图片缓存，直接返回")
                    return resp
         except Exception as ex:
            pass
         error=0
         while True:
            url="http://data.mars3d.cn/tile/googleImg/{}/{}/{}.jpg".format(z,x,y)
            print(url)
            try:
                if error>9:
                    break
                response=requests.get(url,headers=my_headers)
                if response.status_code!=200:
                    #print(response.content)
                    print(response.status_code)
                    with open("data/default.png","rb") as f:
                        res=f.read()
                    return(Response(res,mimetype="image/png"))
                
                dirs = "data/{}/{}".format(z,x)
                if not os.path.exists(dirs): 
                    os.makedirs(dirs)
                with open("data/{}/{}/{}.jpg".format(z,x,y),"wb") as f:
                    f.write(response.content)
                    print("已缓存: {}/{}/{}.jpg".format(z,x,y))
                #print(response.status_code)
                #print(response.content)
                resp=Response(response.content, mimetype="image/jpeg")
                return resp
            
            except Exception as ex:
                print(ex)
                error+=1
                pass


if __name__ == '__main__':
    app.run(debug = True)


     