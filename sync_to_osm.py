#conding=utf8  
import os 
import requests
import _thread
import time
my_headers = {'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.31(0x18001f28) NetType/WIFI Language/en'}
session = requests.Session()
num_thread=0

def default_to_osm(x,y,z):
    global num_thread
    num_thread+=1
    try:
        with open("osm/{}/{}/{}.png".format(z,x,y),"rb") as f:
                img=f.read()
                num_thread-=1
                return(False,"检测到图片缓存，跳过, osm/{}/{}/{}".format(z,x,y))
    except Exception as ex:
        error=0
        while True:
            url="https://tile.openstreetmap.org/{}/{}/{}.png".format(z,x,y)
            print("下载：",url)
            try:
                if error>9:
                    #print("错误太多：",url)
                    num_thread-=1
                    return(False,"错误太多")
                response=session.get(url,headers=my_headers)
                if response.status_code!=200:
                    return(False,str(response.status_code))
                dirs="osm/{}/{}".format(z,x)
                #print(dirs)
                if not os.path.exists(dirs): 
                    os.makedirs(dirs)
                with open("osm/{}/{}/{}.png".format(z,x,y),"wb") as f:
                    f.write(response.content)
                    num_thread-=1
                    return(True,"已下载: osm/{}/{}/{}.png".format(z,x,y))
                return(True)
            except Exception as ex:
                print(ex)

max_thread=input("使用多少个线程下载：（整数，留空为1线程）：")
if max_thread=="":
    max_thread=1
else:
    max_thread=int(max_thread)



g = os.walk("data/")  
for path,dir_list,file_list in g:  
    for file_name in file_list:  
        if ".jpg" in str(file_name):
            tile=os.path.join(path, file_name)
            tile=tile.replace(".jpg","").replace("data/","")
            z=tile.split("/")[0]
            x=tile.split("/")[1]
            y=tile.split("/")[2]
            
            while True:
                if num_thread<max_thread:
                    if max_thread==1:
                        res=default_to_osm(z=z,x=x,y=y)
                    else:
                        res=_thread.start_new_thread(default_to_osm,(x,y,z))
                        print("现有的线程数量：",num_thread)
                    print(res)
                    break
                else:
                    time.sleep(0.1)