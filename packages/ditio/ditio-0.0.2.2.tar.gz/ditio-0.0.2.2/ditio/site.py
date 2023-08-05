
from __init__  import create_dir 
import os,json 

def shift(arr):
    return arr[1:]


class SitePaths:
    CONTENT_DIR='%s/content'
    ASSETS_DIR='%s/assets'

def verify(site_dir):    
    if os.path.exists(SitePaths.CONTENT_DIR % site_dir) is False:
        raise Exception("No valid content_dir: %s" % SitePaths.CONTENT_DIR % site_dir)


def index(site_dir):
    print "Indexing ... "
    
    
    verify(site_dir)
    content_dir = SitePaths.CONTENT_DIR % site_dir
    index = []
    for md in os.listdir(content_dir):
        if md.find(".md")  < 0:
            continue 
        print " * ", md 
        full_path= "%s/%s"  % (content_dir,md)
        with open( full_path,'r') as f:
            meta = {} 
            for line in f:
                if line.find("---") == 0:
                    break                 
                if line.strip() == "":
                    continue 
                
                (k,v) = line.strip().split(":",1)
                meta[k] = v.strip()
           
            if len(meta) > 0:

                line_count=3
                preview = "" 
                for line in f:
                    if line.find('#') > -1:
                        continue
                    if line_count < 0  :
                        break 
                    preview=  preview + " " + line 
                    line_count = line_count - 1 

                meta["preview"] = preview  
                meta["file"]=md.split(".md")[0]
                index.append(meta)
    index_file = "%s/index.json" % (content_dir)
    with open(index_file,'w') as f:
        f.write(json.dumps(index))
    print "article-count:%s" % len(index)
    print "" 
def cmd(params):
    cmd = params[0]
    params = shift(params)


    if cmd == "init":
        site_name = "."
        create_dir(site_name)
        create_dir("%s/content" % site_name)
        create_dir("%s/images"  % site_name)
        create_dir("%s/assets"  % site_name)


        import ditio
        package_site_dir = "%s/site" % os.path.dirname(os.path.abspath(ditio.__file__))
        print site_name,"->",  package_site_dir 
        
        os.system("cp -dpR %s/*  %s" % (package_site_dir, site_name))


    if cmd == "new":
        site_name = params[0]
        create_dir(site_name)
        create_dir("%s/content" % site_name)
        create_dir("%s/images"  % site_name)
        create_dir("%s/assets"  % site_name)


        import ditio
        package_site_dir = "%s/site" % os.path.dirname(os.path.abspath(ditio.__file__))
        
        os.system("cp -dpR %s/*  %s" % (package_site_dir, site_name))

    if cmd == "index": 
        if len(params)  == 0:
            site_dir = "."
        else: 
            site_dir = params[0]
        index(site_dir)

    if cmd == "server":
        site_port = 9999
        if len(params)  == 0:
            site_dir = "."
        elif len(params) == 1 : 
            site_dir = params[0]
        elif len(params) == 2: 
            site_dir = params[0]
            site_port = params[1]
        
        print "Starting Server on .... http://127.0.0.1:%s/" % str(site_port)
        os.system("cd %s;  python -m SimpleHTTPServer %s" % (site_dir,site_port)    )
        print cmd
    pass 
