"""
# json viewer
## python edition


Copyright © 2021 tom0427. All rights reserved.
"""


import tkinter
from tkinter import ttk, Scrollbar,filedialog
import json
import platform
import os



#developer tool
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#logging.disable(logging.DEBUG)

class json_view(ttk.Treeview):
    def __init__(self,master):
        super().__init__(master,height=15,show="tree")
    @classmethod
    def App(cls,master):
        return json_view(master)
    def clear_tree(self)->None:
        for i in tree.get_children():
            tree.delete(i)
    def maketree(self,parent, data, depth=[]) -> None:
        if type(data) is dict:
            for i in data:
                depthlist: list = depth
                child = self.insert(parent, tkinter.END, text=str(
                    i), values=(json.dumps({"depth": depthlist+[str(i)],"type":"Object"}),),tags=["object"])
                self.maketree(child, data[i], depth=depthlist+[str(i)])
        elif type(data) is list:
            if len(data)==0:
                depthlist: list = depth
                child = self.insert(parent, tkinter.END, text=str(), values=(json.dumps({"depth": depthlist+[], "type": "Array"}),), tags=["array"])
            else:
                for i, j in enumerate(data):
                    depthlist: list = depth
                    child = self.insert(parent, tkinter.END, text=str(
                        i), values=(json.dumps({"depth": depthlist+[i], "type": "Array"}),), tags=["array"])
                    self.maketree(child, j, depth=depthlist+[i])
        else:
            depthlist: list = depth
            tags_str=["value","str"]
            tags_num=["value","num"]
            tags_null=["value","null"]
            tags_bool = ["value", "bool"]
            if data is None:
                child = self.insert(parent, tkinter.END, text="null", values=(
                    json.dumps({"depth": depthlist+["null"],"type":"null"}),),tags=tags_null)
            elif type(data) is int:
                child = self.insert(parent, tkinter.END, text=str(data), values=(
                    json.dumps({"depth": depthlist+[str(data)], "type": "Number"}),), tags=tags_num)
            elif type(data) is bool:
                child = self.insert(parent, tkinter.END, text=str(data).lower(), values=(
                    json.dumps({"depth": depthlist+[str(data)], "type": "Boolean"}),), tags=tags_bool)
            else:
                child = self.insert(parent, tkinter.END, text=str(data), values=(
                    json.dumps({"depth": depthlist+[str(data)], "type": "String"}),), tags=tags_str)
    def tag_color(self):
        #value
        self.tag_configure("null", foreground="#ff0000")
        self.tag_configure("str", foreground="#ff7700")
        self.tag_configure("bool", foreground="blue")
        self.tag_configure("num", foreground="#008c1c")
        self.tag_configure("value", background="#e8e8e8")
        #object
        self.tag_configure("object", background="#d4fbff")
        #array
        self.tag_configure("array", background="#fbd4ff")
    def selectedevent(self,e):
        focusid=self.focus()
        logging.debug(self.item(focusid))
        #textbox1_1.delete("0",tkinter.END)
        #アクセスコード
        insert_text=""
        for i in json.loads(self.item(focusid, "values")[0])["depth"][:-1]:
            text = f'"{i}"' if type(i) is str else i
            insert_text+=f'[{text}]'
        textbox1_1.configure(state='normal')
        textbox1_1.delete(0,tkinter.END)
        textbox1_1.insert("0",insert_text)
        textbox1_1.configure(state='readonly')
        insert_text = json.loads(self.item(focusid, "values")[0])["type"]
        textbox1_2.configure(state='normal')
        textbox1_2.delete(0, tkinter.END)
        textbox1_2.insert("0", insert_text)
        textbox1_2.configure(state='readonly')
        insert_text=self.item(focusid,"text")
        textbox1_3.configure(state='normal')
        textbox1_3.delete(0, tkinter.END)
        textbox1_3.insert("0", insert_text)
        textbox1_3.configure(state='readonly')




class winApp(tkinter.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("json viewer")
        self.iconphoto(False, tkinter.PhotoImage(file=os.path.join("image","icon.png")))
        self.geometry("600x600")
        menu = tkinter.Menu(self)
        menu0 = tkinter.Menu(menu, tearoff=0)
        menu0.add_command(label="開く", command=self.openfile)
        menu0.add_separator()
        menu0.add_command(label="終了", command=self.destroy)
        menu.add_cascade(label='ファイル', menu=menu0)
        menu1 = tkinter.Menu(menu, tearoff=0)
        menu1.add_command(label="文字コード", command=lambda:True)
        menu1.add_separator()
        menu1.add_command(label="何かの設定", command=lambda: True)#--------工事中
        menu.add_cascade(label='設定', menu=menu1)
        self.config(menu=menu)
        self.openfilename = ""
        self.encodeing = "utf-8"
    def openfile(self):
        if platform.system() == "Darwin":
            ftyp = [("json files", "*.json")]
        else:
            ftyp = [("datafile", "*.json")]
        self.openfilename=filedialog.askopenfile(filetypes=ftyp)
        if self.openfilename is None:
            logging.debug("ファイルは選ばれませんでした")
        else:
            logging.debug(self.openfilename.name)
            with open(self.openfilename.name, mode="r", encoding="utf-8")as f:
                a = f.read()
            data = json.loads(a)
            tree.clear_tree()
            tree.maketree("", data)
            tree.tag_color()
    def clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(textbox1_1.get())


root = winApp()


frame = tkinter.Frame()
tree = json_view(frame)

frame.pack(expand=True, fill=tkinter.BOTH)


vscrollbar = Scrollbar(frame, orient=tkinter.VERTICAL, command=tree.yview)
tree.configure( yscrollcommand=vscrollbar.set)
tree.grid(row=0, column=0,sticky=tkinter.W+tkinter.E)
tree.bind("<<TreeviewSelect>>",tree.selectedevent)
vscrollbar.grid(row=0,column=1,sticky=tkinter.N+tkinter.S)
frame.grid_columnconfigure(0,weight=1)


frame1 = ttk.LabelFrame(frame,text="情報")
frame1.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)


label1_1 = tkinter.Label(frame1, text="アクセスコード:", anchor=tkinter.W)
label1_1.grid(row=0,column=0,sticky=tkinter.E+tkinter.W)
textbox1_1 = tkinter.Entry(frame1, width=50)
textbox1_1.grid(row=0,column=1)
textbox1_1.configure(state='readonly')
copybutton1_1 = ttk.Button(frame1,text="copy", command=root.clipboard)
copybutton1_1.grid(row=0, column=2,sticky=tkinter.E+tkinter.W)

label1_2 = tkinter.Label(frame1, text="オブジェクトタイプ:", anchor=tkinter.W)
label1_2.grid(row=1,column=0,sticky=tkinter.E+tkinter.W)
textbox1_2 = tkinter.Entry(frame1)
textbox1_2.configure(state='readonly')
textbox1_2.grid(row=1,column=1,sticky=tkinter.E+tkinter.W)

label1_3 = tkinter.Label(frame1, text="データ:", anchor=tkinter.W)
label1_3.grid(row=2,column=0,sticky=tkinter.E+tkinter.W)
textbox1_3 = tkinter.Entry(frame1, width=50)
textbox1_3.configure(state='readonly')
textbox1_3.grid(row=2, column=1, sticky=tkinter.E+tkinter.W)



root.mainloop()