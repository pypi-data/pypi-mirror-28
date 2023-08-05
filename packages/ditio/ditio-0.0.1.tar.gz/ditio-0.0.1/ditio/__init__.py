#!/usr/bin/python
#title:  Notebook Publish Example  
#github: http://github.com/thinkersilver 
#name: sveny_io_example
#package: ditio 
#date:  2017-06-23
#package: $PACKAGE_NAME
import os
import json
from shutil import copyfile
import re 


__log_debug__ = True 

def set_verbose(boolean):
    global __log_debug__ 
    __log_debug__ = boolean 
def is_verbose_log():
    global __log_debug__ 
    return __log_debug__ 
def debug(line):
    global __log_debug__ 
    if __log_debug__ == True:
        print line 

markdown_image_matcher = re.compile('.*\!\[.*\]\((.*)\)')
open_notebook = lambda f_name : json.loads(open(f_name).read())
markdown_get = lambda notebook : [ "\n".join(c['source']) for c in notebook['cells']  if c["cell_type"] == u'markdown' ]
code_get  = lambda notebook: [ "\n".join(c['source']) for c in notebook['cells']  if c["cell_type"] == u'code' ]
def meta_get(nb):
    source = None 
    for c in nb["cells"]:
        if c["cell_type"]=='code':
            source=c["source"]
            break 
    if source is None:
        return {} 
    properties = {} 
    for line in source:
        if line[0]!='#':
            break 
        (k,v)  = line.strip().split(":",1)
        k = k.replace("#","")
        v = v.strip()
        properties[k] = v 
    required_properties = ["name","date","title","package"]
    
    missing_props = [] 
    for k in required_properties:
        if k not in properties:
            missing_props.append(k)
            
    if len(missing_props)  > 0:
        debug("\n".join([  "Warning property [%s] is missing" %  k for k in missing_props]))
        #raise KeyError("Missing properities:  %s"  % str(missing_props) ) 
    return properties
#package: $PACKAGE_NAME
# def meta_get(nb):
#     source = None 
#     for c in nb["cells"]:
#         if c["cell_type"]=='code':
#             source=c["source"]
#             break 
#     if source is None:
#         return {} 
#     properties = {} 
#     for line in source:
#         if line[0]!='#':
#             break 
#         (k,v)  = line.strip().split(":",1)
#         k = k.replace("#","")
#         v = v.strip()
#         properties[k] = v 
#     return properties
def image_proximity_find(cells_all):
    outputs =  [ (c[0],pathx(c,[1,"outputs"])) for c in cells_all  if is_code(c[1]) and len(path(c,[1,"outputs"])) > 1 ]
    
    data = flatten([ map(lambda x : (o[0],x["data"]) if "data" in x else (o[0],None)  , o[1] )  for o in outputs])
    images  = [ (i[0], i[1]["image/png"] )  for i in data  if i[1] is not None and "image/png" in i[1]  ]
    reversed_cells = list(reversed([c for c in  cells_all if is_markdown(c[1]) ]))
    #print ids(reversed_cells)
    #print ids(images)
    results = []
    for (_id,img) in images:
        (cell_id,markdown) = search(reversed_cells, lambda c : path(c,[0]) < _id )
        r = {
            "_id": _id, 
            "image":img,
            "nearest_neighbour":(cell_id,markdown)
        
        }
        results.append((cell_id,r) )
    return results
def code_proximity_find(cells_all):
    source_for_inclusion = [ (c[0],c[1]["source"]) for  c in cells_all if is_code(path(c,[1])) and len(source(c[1])) > 0  and source(c[1])[0].find("#INCLUDE") == 0 ]   
    reversed_cells = list(reversed([c for c in  cells_all if is_markdown(c[1]) ]))
    #print source_for_inclusion
    results = []
    for (_id,src) in source_for_inclusion:
        (cell_id,markdown) = search(reversed_cells, lambda c : path(c,[0]) < _id )
        r = {
            "_id": _id, 
            "data":src,
            "nearest_neighbour":(cell_id,markdown)
        }
        results.append((cell_id,r) )
    return results
    
    
    
    
def get_filtered_cells(meta,notebook,img_write=False):
    cells_all = [ c  for c in  list(enumerate(cells(notebook))) if "source" in c[1]  and len(c[1]["source"])  > 0 ] 
    cells_code_main = [ c  for c in cells_all if is_code(c[1]) and  source(c[1])[0].find("#IGNORE") < 0 and source(c[1])[0].find("#TEST") < 0  and source(c[1])[0].find("#DIST") < 0  and source(c[1])[0].find("#MAIN") < 0  and source(c[1])[0].find("#EXCLUDE") < 0] 
    cells_code_dist = [ c  for c in cells_all if is_code(c[1]) and source(c[1])[0].find("#DIST") == 0 ] 
    cells_code_exclude = [ c  for c in cells_all if is_code(c[1]) and source(c[1])[0].find("#EXCLUDE") == 0 ] 
    cells_markdown = [ c  for c in cells_all if is_markdown(c[1])  ] 
    
    
    # mark down rendering 
    image_cell_neighbours = dict(image_proximity_find(cells_all))
    code_cell_neighbours = dict(code_proximity_find(cells_all))
    
    import copy
    markdown_cells = copy.deepcopy(dict(cells_markdown))
    for cell in cells_markdown:
        _id = cell[0]
        if _id in code_cell_neighbours:
            markdown_cells[_id]["source"].append("\n")
            markdown_cells[_id]["source"].append("\n\t```\n")

            if code_cell_neighbours[_id]["data"][0].find("#INCLUDE") == 0:
                code_lines= code_cell_neighbours[_id]["data"][1:]
            else:
                code_lines= code_cell_neighbours[_id]["data"]

            #markdown_cells[_id]["source"].extend(map(lambda d:  "\t" + d ,  code_cell_neighbours[_id]["data"]))
            markdown_cells[_id]["source"].extend(map(lambda d:  "\t" + d ,  code_lines ))
            markdown_cells[_id]["source"].append("\n\t```\n")
            markdown_cells[_id]["source"].append("\n")

            code_cell_neighbours.pop(_id)
        if _id in image_cell_neighbours:
            
            fname = "%s_%s.png" % (meta["name"],image_cell_neighbours[_id]["nearest_neighbour"][0])
            if img_write:
                with open("./images/%s" % fname,'wb') as f :
                    data_img= image_cell_neighbours[_id]["image"]
                    f.write(data_img.decode("base64"))
                
            md_img_url = "\n ![](/images/%s)\n" % fname
            markdown_cells[_id]["source"].append("\n")
            markdown_cells[_id]["source"].append(md_img_url)
            markdown_cells[_id]["source"].append("\n")
            
            image_cell_neighbours.pop(_id)
    final_cells = {} 
    final_cells.update(markdown_cells)
    final_cells.update(cells_code_main)
    return final_cells.items()
        
#package: $PACKAGE_NAME.__funcs__
is_markdown = lambda c :  c["cell_type"] == u'markdown'
is_code = lambda c : c["cell_type"] == u'code'
get = lambda c,k : c[k] if k  in c else None 
has = lambda k,d :  k in d 
source = lambda c : get(c,"source")
cells = lambda c : get(c,"cells")
ids = lambda enumerated_list : [ c[0] for c in enumerated_list]
def is_any(x,patterns):
    for p in patterns: 
        if x.find(p) == 0:
            return True 
    return False 
def flatten(arr,count=1):
    result = [] 
    for el in arr:
        result.extend(el)
        
    if count > 1:
        return flatten(result,count-1)
    return result
#package: $PACKAGE_NAME.enumerated
def search(enumerated_cells, fn ):
    for cell in enumerated_cells:
        if fn(cell):
            return cell
    return None 
#package: $PACKAGE_NAME.paths
def pathx(m,keys):
    if  len(keys) == 1: 
        if type(m) == dict:
            return m[ keys[0]]
        if type(m) == list:
            return m[ keys[0]]
        return m
    
    
    if type(m[keys[0]])in [list,tuple]:
        return map(lambda x : pathx(x, keys[1:]), m[keys[0]])
                   
    return pathx(m[keys[0]], keys[1:])  
path = lambda m,keys  : m[ keys[0]]  if  len(keys) == 1 else path(m[keys[0]], keys[1:])  
# pathx({'a': [1, 2, 3]},['a', 0])
# pathx([1,2,{"a":[{"a":3},{"a":4},{"a":6}]},4], [2,"a"])
#pathx([1,[2],{"a":[{"a":[3,1]} ]}],[2,"a","a",0])  # [2,"a:*,0,"a"]
#package: $PACKAGE_ NAME.os 
import shutil
get_path = lambda f_name : os.path.dirname(f_name)  if os.path.dirname(f_name) != '' else os.getcwd()
def create_dir(path):
    if os.path.exists(path) == False:
        os.makedirs( path)    
        
def export_path_get(meta):
    export_path  = '%s/export/%s' 
    full_path = export_path % (meta["path"],meta["name"])
    return full_path
def mkdirs(meta,notebook):
    full_path = export_path_get(meta)
    
    create_dir(full_path)
    
    for folder in ["content","assets","images"]:
        
        create_dir(full_path + "/" +  folder)
        
def base(meta,f):
    if "name" not in meta:
        meta.update( {"name":f.rsplit(".",1)[0].replace(" ","_")} )
    if "title" not in meta:
        meta.update( {"title":f.rsplit(".",1)[0]} ) 
    
    if "package" not in meta: 
        meta.update( {"package": "pkg_%s" % meta["name"] } ) 
    if "date" not in meta: 
        from datetime import datetime
        meta.update( {"date":  str(datetime.now())  } )  
    return meta
        
    
def copytree(src,dst):
    shutil.copytree(src,dst)
    
#package: $PACKAGE_ NAME.export  
def export_code(meta,notebook):
    join_str = lambda lines : "\n".join([l for l in lines])
    cells = [cell for cell in  notebook["cells"] if cell["cell_type"] =='code' and len(cell["source"]) > 1  and  cell["source"][0].find('#IGNORE ') < 0  ]
    
    filtered_cells = [ c[1] for c in get_filtered_cells(meta,notebook) if is_code(c[1])]
    
    code = join_str( [ join_str(c["source"]) for c in filtered_cells ])
    if "package" in meta:
        source_fname = "%s/assets/%s"  % (export_path_get(meta), meta["package"] )
    else:
        source_fname = "%s/assets/%s"  % (export_path_get(meta), meta["name"] + ".py")
    
    code = "\n".join([l for l in code.split("\n") if len(l) > 1 and l[0]!='%'])
    code = "\n".join(['#!/usr/bin/python',code])
    
    package_dir = "%s/assets/%s"   % (export_path_get(meta), meta["package"] )
    if os.path.exists(package_dir) is False:
        create_dir(package_dir)
                                       
    package_init_file = "%s/%s" %  (package_dir,"__init__.py")                        
    with open(package_init_file,'w') as f:
        f.write(code)
        
    
    # export dist 
    
    dist_cells =  [ cell for cell in notebook["cells"] if is_code(c) and len(cell["source"]) > 1  and  cell["source"][0].find('#DIST') == 0   ]
    #package_dist_file = "%s/%s" %  (package_dir,"__init__.py")                        
    code = join_str( [ join_str(c["source"]) for c in dist_cells ])
    package_dist_file = "%s/assets/%s"   % (export_path_get(meta),"setup.py" )
    with open(package_dist_file,'w') as f:
        f.write(code)
        
    #export scripts file 
    main_cells =  [ cell for cell in notebook["cells"] if is_code(c) and len(cell["source"]) > 1  and  cell["source"][0].find('#MAIN') == 0   ]
    code = join_str( [ join_str(c["source"]) for c in main_cells ])
    package_bin_dir = "%s/assets/bin"  % (export_path_get(meta))  
    create_dir(package_bin_dir) 
    package_script_file = "%s/%s"   %  (package_bin_dir, meta["package"] ) 
        
        
    
    code = "\n".join([ '#!/usr/bin/python\n' ,"from %s import *" % meta["package"],code])
    with open(package_script_file,'w') as f:
        f.write(code)    


    package_manifest = "%s/assets/%s"   % (export_path_get(meta),"MANIFEST.in" )
    with open(package_manifest,'w') as f:
        f.write("include *.json")

import json
def export_meta(meta):
    package_meta_file = "%s/assets/%s"   % (export_path_get(meta),"config.json" )
    with open(package_meta_file,'w') as f:
        f.write(json.dumps(meta))
    
def export_markdown(meta,notebook):
    global markdown_image_matcher
    property_excludes = ["path"]
    join_str = lambda lines : "".join([l for l in lines])
    
    
#     cells = [cell for cell in  notebook["cells"] if cell["cell_type"] =='markdown']
    
    
    filtered_cells = [ c[1] for c in get_filtered_cells(meta,notebook)]
    
    src = join_str( [ join_str(c["source"]) for c in filtered_cells if is_markdown(c) ])
    source_fname = "%s/content/%s"  % (export_path_get(meta), meta["name"] + ".md")
    for img in markdown_image_matcher.findall(src):
        if img.find("http") > -1 :
            continue 
            
        new_img = "/images/" + img.split("/")[-1]
        src = src.replace(img,new_img)
    value_formatter = lambda v : ",".join(list(v)) if type(v) in [list,tuple,set] else str(v)
    with open(source_fname,'w') as f:
        f.write("\n".join(["%s: %s" % (k,value_formatter(v)) for (k,v) in meta.items() if k not in property_excludes]))
        f.write("\n")
        f.write("---\n")
        f.write(src)
def export_images(meta,notebook):
    debug("Exporting Images ... ")
    global markdown_image_matcher
    property_excludes = ["path"]
    join_str = lambda lines : "\n".join([l.strip() for l in lines])
    
    
    filtered_cells = [ c[1] for c in get_filtered_cells(meta,notebook,img_write=True)]
    
    #cells = [cell for cell in  notebook["cells"] if cell["cell_type"] =='markdown']
    cells = [cell for cell in  filtered_cells if cell["cell_type"] =='markdown']
    
    
    code = join_str( [ join_str(c["source"]) for c in cells ])
    for img in markdown_image_matcher.findall(code):
        dest_fname = "%s/images/%s"  % (export_path_get(meta), img.split("/")[-1])
        src_fname = "%s/%s" % (meta["path"],img) 
        if img.find("http") > -1 :
            continue 
        copyfile(src_fname,dest_fname)
        
        
    
def push_assets(meta,path):
    debug("Pushing Assets ... %s" % path )
    content_dir = "%s/assets"  % (export_path_get(meta))
    
    #package_dir = "%s/%s" %
    
    export_asset_dir = path + "/assets/%s" % meta["name"]
    import os;  os.system("cp -dpR  %s %s" % (content_dir,export_asset_dir))
#   copytree(content_dir,export_asset_dir)
#     for f in os.listdir(content_dir):
#         src = content_dir + "/" + f
#         dst = path + "/assets/%s" %f 
#         print "* %s -> %s " % (src,dst)          
#         copyfile(content_dir + "/" + f, path + "/assets/%s" %f  )
    
    pass

def push_markdown_only(meta,path):
    content_dir = "%s/content"  % (export_path_get(meta))
    for md in os.listdir(content_dir):
        debug("- %s/%s" % (path,md))
        copyfile(content_dir + "/" + md, path + "/%s" %md  )
        
    pass

def push_markdown(meta,path):
    debug("Pushing Markdown ... [%s]" % path)
    content_dir = "%s/content"  % (export_path_get(meta))
    for md in os.listdir(content_dir):
        debug("- %s" % md)
        copyfile(content_dir + "/" + md, path + "/content/%s" %md  )
    pass
def push_images(meta,path):
    debug("Pushing Images.")
    content_dir = "%s/images"  % (export_path_get(meta))
    for img in os.listdir(content_dir):
        from_to_message = "%s->%s" % (content_dir + "/" + img, path + "/images/%s" % img  )
        debug("* %s " % from_to_message )
        copyfile(content_dir + "/" + img, path + "/images/%s" % img  )
    pass
def export(meta,notebook):
    export_code(meta,notebook)
    meta.update({"assets": os.listdir(export_path_get(meta) + "/assets"  )})
    export_markdown(meta,notebook)
    export_images(meta,notebook)
    export_meta(meta)
def push(meta,path):
    push_assets(meta,path)
    push_markdown(meta,path)
    print 
    push_images(meta,path)
    
    
def publish(meta,notebook,export_path):
    export(meta,notebook)
    push(meta,export_path)

def publish_markdown(meta,notebook,export_path):
    export(meta,notebook)
    push_markdown_only(meta,export_path)

    # clean markdown 
    for md in os.listdir(export_path):
        path_to_md = export_path + "/" + md 
        if os.path.isdir(path_to_md):
            continue 

        lines =  enumerate(open(path_to_md ).readlines())
        for l in lines:
            if l[1].find("---") == 0:
                break 
        with open(path_to_md,'w') as f:
            for pos,l in lines:
                f.write(l) 
    if os.path.exists(export_path +  "/images") is False:
        os.mkdir(export_path + "/images" ) 
    push_images(meta,export_path)



#package: $APP 
join = lambda sep,arr:  sep.join(arr)
def cmd_info(params):
    nb_fname = params[0]
    notebook = open_notebook(nb_fname)
    meta = meta_get(notebook)
    meta = base(meta,nb_fname)
    print "[%s]" % nb_fname
    print join("\n", ["%s: %s" %(k,v) for k,v in meta.items() ])
    
    
def cmd_export(params):
    nb_fname = params[0]
    
    #print "Exporting ...",
    notebook = open_notebook(nb_fname)
    meta = meta_get(notebook)
    meta = base(meta,nb_fname)
    
    meta.update({"path": get_path(nb_fname)})
    mkdirs(meta,notebook)
    export(meta,notebook)
    
    #print "[DONE]"
def cmd_push(params):
    nb_fname = params[0]
    export_path = params[1]
    
    #print "Pushing ...",
    notebook = open_notebook(nb_fname)
    meta = meta_get(notebook)
    meta = base(meta,nb_fname)
    
    
    #meta.update({"path":"./"})
    meta.update({"path": get_path(nb_fname)})
    mkdirs(meta,notebook)
    push(meta,export_path)


def cmd_publish_all(params):
    cmd_publish(params) 
def cmd_publish_markdown(params):
    debug("Publishing markdown  ...")
    nb_fname = params[0]
    export_path = params[1]
    
    notebook = open_notebook(nb_fname)
    meta = meta_get(notebook)
    meta = base(meta,nb_fname)
    
    
    #meta.update({"path":"./"})
    meta.update({"path": get_path(nb_fname)})
    mkdirs(meta,notebook)    

    publish_markdown(meta,notebook,export_path)
   

def cmd_publish(params):
    nb_fname = params[0]
    export_path = params[1]
    
    notebook = open_notebook(nb_fname)
    meta = meta_get(notebook)
    meta = base(meta,nb_fname)
    
    
    #meta.update({"path":"./"})
    meta.update({"path": get_path(nb_fname)})
    mkdirs(meta,notebook)    
    publish(meta,notebook,export_path)
    

def cmd_dist_install(params):
    #print "Package install ... "
    nb_fname = params[0]
    export_path = params[1]
    
    notebook = open_notebook(nb_fname)
    meta = meta_get(notebook)
    meta = base(meta,nb_fname)
    meta.update({"path": get_path(nb_fname)})
    asset_path = "%s/%s" % (export_path_get(meta),"assets")
    import os; os.system("cd %s; python setup.py install;cd - "  % asset_path)
    debug(asset_path)
    
