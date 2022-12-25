import requests
import os
import _thread
import time
my_headers = {'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.31(0x18001f28) NetType/WIFI Language/en'}
session = requests.Session()
num_thread=0

def download_image(z,x,y):
    global num_thread
    num_thread+=1
    z=str(z)
    x=str(x)
    y=str(y)
    try:
        with open("osm/{}/{}/{}.png".format(z,x,y),"rb") as f:
                img=f.read()
                num_thread-=1
                return "文件已经下载" #文件已经下载
    except Exception as ex:
        pass
        #开始下载
        error=0
        while True:
            url="https://tile.openstreetmap.org/{}/{}/{}.png".format(z,x,y)
            #print(url)
            try:
                if error>9:
                    return("TooManyErrors")
                response=session.get(url,headers=my_headers)
                if response.status_code!=200:
                    #print(response.content)
                    #print(response.status_code)
                    num_thread-=1
                    return(str(response.status_code))
                
                dirs = "osm/{}/{}".format(z,x)
                if not os.path.exists(dirs): 
                    os.makedirs(dirs)
                with open("osm/{}/{}/{}.png".format(z,x,y),"wb") as f:
                    f.write(response.content)
                #print(response.status_code)
                #print(response.content)
                #resp=Response(response.content, mimetype="image/jpeg")
                num_thread-=1
                return "下载成功"
            
            except Exception as ex:
                print(ex)
                error+=1
                pass

z=int(input("下载的层（整数）："))
max_thread=input("使用多少个线程下载：（整数，留空为1线程）：")
xi=input("X的值从几开始（针对10级以上的数据，如果中间停止了，可指定X的值来跳过很大一部分内容。留空默认值为0即从头开始抓取）：")


if max_thread=="":
    max_thread=1
else:
    max_thread=int(max_thread)

if xi=="":
    xi=0
else:
    xi=int(xi)


for x in range(xi,2**z):
    for y in range(0,2**z):
        while True:
            if num_thread<max_thread:
                if max_thread==1:
                    res=download_image(z,x,y)
                else:
                    res=_thread.start_new_thread(download_image,(z,x,y))
                    print("现有的线程数量：",num_thread)
                print(res,z,x,y,((x)*pow(2,z)+y)*100/(pow(2,z*2)),"%")
                break
            else:
                time.sleep(0.1)
        #if res=="404":
        #    break

'''
y_edge=False
while z<12:
    while x<999:
        while y<999:
            if y_edge==True:
                res=download_image(z,x,y)
                if res=="404":
                    z+=1
                    x=0
                    y=0
                    y_edge=False
                elif res=="Exist":
                    print("文件存在")
            res=download_image(z,x,y)
            y+=1
            if res=="404":
                y_edge=True
                break
            
        x+=1
    z+=1            
'''