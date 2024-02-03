
from tkinter import *
import os


class App():
    def __init__(self):
        self.root = Tk()
        self.root.title("Replacer")
        self.root.geometry("500x350")
        

        self.w=500
        self.h=20
                
        self.hint_files = r'file.txt, file.html'
        self.hint_folder = ""
        self.hint_pattern = "dip"
        self.hint_func = '100-x-1*2'


    def build_ui(self):
        self.info = Text(self.root)
        self.log = Text(self.root)

        self.split = Label(self.root, background="black")

        self.label_file = Label(self.root, text="названия файлов (file1.txt, file2.html, file3.data)")
        self.field_file = Entry(self.root)
        self.field_file.insert(END, self.hint_files)

        self.label_folder = Label(self.root, text="каталог для поиска (полный путь)")
        self.field_folder = Entry(self.root)
        self.field_folder.insert(END, self.hint_folder)


        self.label_pattern = Label(self.root, text="паттерн для поиска")
        self.field_pattern = Entry(self.root)
        self.field_pattern.insert(END, self.hint_pattern)

        self.label_func = Label(self.root, text="функция замены (x*2 or x-1/2 or 100-x)")
        self.field_func = Entry(self.root)
        self.field_func.insert(END, self.hint_func)

        self.btn_start = Button(self.root, background="gray", text="Применить и запустить" ,command=self.com_run)


        # =================

        self.info.place(x=0,y=0,width=self.w,height=self.h*4)
        self.log.place(x=0,y=self.h*4,width=self.w,height=self.h*1)

        self.split.place(x=0, y=self.h*5, width=self.w, height=2)

        self.label_file.place(x=0,y=self.h*6,width=self.w,height=self.h)
        self.field_file.place(x=0,y=self.h*7,width=self.w,height=self.h)

        self.label_folder.place(x=0,y=self.h*8,width=self.w,height=self.h)
        self.field_folder.place(x=0,y=self.h*9,width=self.w,height=self.h)

        self.label_pattern.place(x=0,y=self.h*10,width=self.w,height=self.h)
        self.field_pattern.place(x=0,y=self.h*11,width=self.w,height=self.h)

        self.label_func.place(x=0,y=self.h*12,width=self.w,height=self.h)
        self.field_func.place(x=0,y=self.h*13,width=self.w,height=self.h)

        self.btn_start.place(x=0,y=self.h*14,width=self.w,height=self.h*3)



    def set_log(self, text,color=""):
        if color != "":
            self.log['background'] = color
        self.log.delete(0.0,END)
        self.log.insert(END,text)
        self.root.update()
        

    def set_info(self, text):
        self.info.delete(1.0,END)
        self.info.insert(1.0,text)
        self.root.update()


    def launch_func(self, folder, files, pattern, function ):
        data_result = ""
        count_replaces = 0
        
        try:
            os.listdir(folder)
        except Exception as e:
            self.set_info('err:'+str(e))
            self.set_log("ошибка","red")
            return 0
            
        temp_f = []
        for f in files:
            temp_f.append(f.strip())
        
        files = temp_f

        list_files = os.listdir(folder)
        os.chdir(folder)   

        finish_files = []
        for name in list_files:
            for temp in files:
                if name == temp:
                    finish_files.append(name)
                    
        arrfiles = ""
                    
        for file in finish_files:
            arrfiles+="\n["+file+"]"
            reader = open(folder + r"\\" + file, "r+")
            data_file = reader.read().strip()
            reader.close()

            data_lines = data_file.split(pattern)[0:-1]
            count_replaces += len(data_lines)
            new_data = data_file
            list_new_values = []


            for line in data_lines:
                value = line.split(">")[-1]
                list_new_values.append(self.func_value(value, function))

            c = 0
            for line in data_lines:
                old_line = str(line.split(">")[-1])+pattern
                new_line = str(list_new_values[c])+"pattern_temp"
                new_data = new_data.replace(old_line,new_line)
                c+=1

            new_data = new_data.replace("pattern_temp", pattern)
            data_file = open(folder + r"\\" + file, "w")
            data_file.write(new_data)
            data_file.close()
            
        data_result = " Каталог:" + folder + "\n" + "Файлы:" + arrfiles + "\n\t\t"+"заменено:"+ str(count_replaces) + "\n\n"
        self.set_info(data_result)


    def func_value(self, value, str_func):
        line = str_func.replace("x", "float("+value+")")
        return eval(line)


    def com_run(self):
        str_folder, str_filenames, str_pattern, str_func = self.get_fields()

        self.set_log("Обработка",'blue')
        for nf in str_filenames:
            self.set_info(nf)


        if str_folder == "":
            self.set_log('ошибка директории',"red")
            return
        elif len(str_filenames) == 0:
            self.set_log('ошибка паттерна',"red")
            return
        elif str_pattern =="":
           self.set_log('ошибка шаблона',"red")
           return
        elif str_func =="":
            self.set_log('ошибка функции',"red")
            return
        else:
            self.set_log("Выполняется..","yellow")
            res = self.launch_func(str_folder, str_filenames, str_pattern, str_func)
            if res != 0:
                self.set_log("Выполнено","green")
        # return new_data




    def get_fields(self):
        return self.field_folder.get(), self.field_file.get().split(","), self.field_pattern.get(), self.field_func.get()


    def mainloop(self):
        self.root.mainloop()



app = App()
app.build_ui()
app.mainloop()

