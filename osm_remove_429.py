#conding=utf8  
import os 

g = os.walk("osm/")  
for path,dir_list,file_list in g:  
    for file_name in file_list:  
        if ".png" in str(file_name):
            tile=os.path.join(path, file_name)
            size=os.path.getsize(tile)
            if size==316:
                os.remove(tile)