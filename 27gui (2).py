from Tkinter import *
from Queue import Queue
import threading
import Image
import os
import glob
import tkMessageBox
import time




class gui():
    def __init__(self):
        self.root=Tk()
        self.Allfile_frame=LabelFrame(self.root,text='All image file:')
        self.Allfile_frame.pack()
        
        all_file_label=(self.Allfile_frame)
        #all_file_label.pack()
        
        self.allfile_scrollbar=Scrollbar(self.Allfile_frame)
        self.allfile_scrollbar.pack(side=RIGHT,fill=Y)

        self.my_text=Text(self.Allfile_frame,width=40,height=10,yscrollcommand=self.allfile_scrollbar.set)
        self.my_text.pack()

        self.failfile_frame=LabelFrame(self.root,text='Failed image file:')
        self.failfile_frame.pack()

        fail_file_label=Label(self.failfile_frame,text='Fail file compred rate:')
        #fail_file_label.pack()

        self.failfile_scrollbar=Scrollbar(self.failfile_frame)
        self.failfile_scrollbar.pack(side=RIGHT,fill=Y)

        self.failed_text=Text(self.failfile_frame,width=40,height=10,yscrollcommand=self.failfile_scrollbar.set)
        self.failed_text.pack()
        
        self.button_frame=Frame(self.root)
        self.button_frame.pack()

        self.rate_label=Label(self.button_frame,text='Set the compare rate:',width=30)
        self.rate_label.pack()

        self.rate_entry=Entry(self.button_frame,width=25)
        self.rate_entry.pack()

        self.label1=Label(self.button_frame,text='original dir:',width=30)
        self.label1.pack()

        self.entry1=Entry(self.button_frame,width=25)
        self.entry1.pack()
        self.label2=Label(self.button_frame,text='compare dir:')
        self.label2.pack()
        self.entry2=Entry(self.button_frame,width=25)
        self.entry2.pack()
        
        self.button_submit=Button(self.button_frame,text='submit',command=self.list_dir)
        
        self.button_submit.pack()
        self.root.mainloop()

    def list_dir(self):
        #print('sublmit ok')
        original_dir=Entry.get(self.entry1)
        compare_dir=Entry.get(self.entry2)
        
        #print(compare_rate)
        if original_dir=='' or compare_dir=='' or Entry.get(self.rate_entry)=='':
            print('please input dir and compare rate')
            tkMessageBox.showinfo("Note", "Input the file dir and compare rate")
        else:
            #print(os.path.isdir(original_dir))
            compare_rate=int(Entry.get(self.rate_entry))
            if os.path.isdir(original_dir) and os.path.isdir(compare_dir):
                #print('path exist')
                #self.my_text.insert(END,original_dir)
                length=len(original_dir)
                #self.entry1.delete(0,length)
                compare_dir_len=len(compare_dir)
                #self.entry2.delete(0,compare_dir_len)
                cthread=calc_thread('Calc',queue,original_dir,compare_dir)
                cthread.start()
                dthread=display_thread('display',queue,self.my_text,self.failed_text,compare_rate,compare_dir_len)
                dthread.start()
            else :
                tkMessageBox.showinfo("Note", "Invalide dir,please check the dir")
                
class calc_thread(threading.Thread):
    def __init__(self,thread_name,queue,path1,path2):
        threading.Thread.__init__(self,name=thread_name)
        self.data=queue
        self.original=path1
        self.compare=path2
    def run(self):
        original_file=glob.glob(self.original+'\\*.png')
        #print(original_file)
        compare_file=glob.glob(self.compare+'\\*.png')
        #print(compare_file)
        sum_pic=len(compare_file)
        #print(sum_pic)
        for i in range(0,sum_pic):
            (filepath,filename)=os.path.split(compare_file[i])
            (file_name,filetype)=os.path.splitext(filename)
            pic_compare_rate=self.calc_similar_by_path(original_file[i],compare_file[i])*100
            compare_item=[file_name,pic_compare_rate]
            self.data.put(compare_item)
            
    def make_regalur_image(self,img,size =(256,256)):
        return img.resize(size).convert('RGB')

    def hist_similar(self,lh,rh):
        assert len(lh) == len(rh)
        return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)

    def calc_similar(self,li,ri):
        return self.hist_similar(li.histogram(), ri.histogram())

    def calc_similar_by_path(self,lf,rf):
        li,ri =self.make_regalur_image(Image.open(lf)),self.make_regalur_image(Image.open(rf))
        return self.calc_similar(li, ri)

class display_thread(threading.Thread):
    def __init__(self,thread_name,queue,oktext,failtext,compare_rate,total_pic):
        threading.Thread.__init__(self,name=thread_name)
        self.data=queue
        self.my_text=oktext
        self.failtext=failtext
        self.compare_rate=compare_rate
        self.total_pic=total_pic
        
    def run(self):
        for i in range(0,self.total_pic,1):
            compare_item=self.data.get()
            pic_compare_rate=compare_item[1]
            self.my_text.insert(END,compare_item[0]+': '+str(pic_compare_rate)+'\n')
            if pic_compare_rate<self.compare_rate:
                time.sleep(1)
                self.failed_text.insert(END,compare_item[0]+': '+str(pic_compare_rate)+'\n')
                    
        
if __name__ == '__main__':
    queue=Queue()
    my_gui=gui()
    #print('%.3f%%'%calc_similar_by_path('f:/a/a.jpg','f:/a/b.jpg'))


