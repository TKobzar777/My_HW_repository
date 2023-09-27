# py hw_6_1.py C:\hw_folder
import sys
from pathlib import Path
import shutil

CATEGORIES = {"images" : ['.JPEG', '.PNG', '.JPG', '.SVG'],
              "video" : ['.AVI', '.MP4', '.MOV', '.MKV'],
              "documents" :['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'],
              "audio" : ['.MP3', '.OGG', '.WAV', '.AMR'],
              "archives": ['.ZIP', '.GZ', '.TAR']}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

global list_category
list_category = []

TRANS = {}
for c, l in zip(tuple(CYRILLIC_SYMBOLS), TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper() 

def translate(name):
    global TRANS
    return name.translate(TRANS)

def normalize(name_file:str):

    new_name = ""
    name_file = translate(name_file)
    #print(name_file)

    for lit in name_file:  
        if ord(lit) == 46 or 48 <= ord(lit) <= 57 or 65 <= ord(lit) <= 90 or 97 <= ord(lit) <= 122:
            new_name = new_name + lit
        else:
            new_name= new_name + "_"
    return new_name

def unp_archives(arch:Path, path:Path) -> None:
    name_ar = arch.stem
    ar_dir_new = path.joinpath(name_ar) 
    shutil.unpack_archive(arch,ar_dir_new)

 

def move_file(file:Path, category:str, dir:Path) -> None:
    target_dir = dir.joinpath(category)
    
    if not target_dir.exists():
        target_dir.mkdir()
        list_category.append(target_dir)
   
    file.replace(target_dir.joinpath(normalize(file.name)))


def get_categorries(file:Path)-> str:
    suf_f = file.suffix.upper()
    for cat, list_suf in CATEGORIES.items():
        #print(list_suf)
        if suf_f in list_suf:
            return cat
    return "Other"


def Sort_folder(paht:Path ) -> None:
    for item in paht.glob("**/*"):
        
        if item.is_file():
            categorie = get_categorries(item)
            move_file(item, categorie, paht)
    
    fl=True
    while fl:
        fl=False
        for item in paht.glob("**/*"):           
            if item.is_dir():
                if item in list_category:
                    continue
                else:    
                    if not list(item.iterdir()):
                        item.rmdir()
                        fl= True
                        continue
    #unpack_archive
    dir_ar = paht.joinpath("archives")
    if dir_ar.exists():
        for ar in dir_ar.iterdir(): 
            
            unp_archives(ar,dir_ar)
   

def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No past to folder"
    #path= Path("C:\\hw_folder")
    if not path.exists:
        return "Folder dos not exist"
    print(f"OK {path}")
   
    Sort_folder(path)



if __name__ == "__main__":
    print(main())

