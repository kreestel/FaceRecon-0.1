# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 19:15:06 2023

@author: Krystal
"""

import tkinter as tk
import mysql.connector 
import face_recognition
from tkinter import filedialog
from PIL import ImageTk,Image 
from tkinter import scrolledtext
import wikipediaapi

window = tk.Tk()
window.title("Face Recognition Software")
window.configure(bg="#aab6d3")
frame = tk.Frame(window, bg="#aab6d3")
frame.pack(padx=180, pady=50)

globlaX = []
result_labelm = tk.Label(frame, text="Place Holder for result_labelm", bg="#aab6d3")


def open1():
    top = tk.Toplevel()
    top.title("Insert into Database")
    top.geometry("700x210")
    top.configure(bg="#aab6d3")
    
    def addtoDB():
        
        result_label4 = tk.Label(top, text="", bg="#aab6d3")
        result_label4.grid(row=0, column=0)
        result_label2 = tk.Label(top, text="", bg="#aab6d3")
        result_label2.grid(row=1, column=0)
        result_label3 = tk.Label(top, text="", bg="#aab6d3")
        result_label3.grid(row=2, column=0)
        result_label3 = tk.Label(top, text="", bg="#aab6d3")
        result_label3.grid(row=3, column=0)
        
        label = tk.Label(top, text="Enter name of the person:", bg="#aab6d3")
        name = tk.Entry(top, width=75)
        label2 = tk.Label(top, text="Enter file path:", bg="#aab6d3")
        path = tk.Entry(top, width=75)
        label3 = tk.Label(top, text="Enter description (optional):", bg="#aab6d3")
        desc = tk.Entry(top, width=75)
        label.grid(row=1, column=1)
        name.grid(row=1, column=2)
        label2.grid(row=2, column=1)
        path.grid(row=2, column=2) 
        label3.grid(row=3, column=1)
        desc.grid(row=3, column=2)
        
        
        def submit():
            mycon=mysql.connector.connect(host="localhost",user="root",passwd="admin123",database="facerecognition") 
            myc=mycon.cursor()
            a=name.get()
            aa=str(a)
            b=path.get()
            b1=str(b) 
            c=desc.get()
            cc=str(c) if c else None
            
            
            myc.execute('INSERT INTO faces (name, path, info) VALUES (%s,%s,%s)', (aa, b1,cc))
            mycon.commit()
            myc.close()
            mycon.close()
            name.delete(0,tk.END)
            path.delete(0,tk.END)
            desc.delete(0,tk.END)
            label3=tk.Label(top, text="successful input", bg="#aab6d3")
            label3.grid(row=6, column=2)
            top.after(3000, lambda: label3.destroy())
        submitbttn = tk.Button(top, text="Add record to databse",bg="#7186c7", command=submit)
        submitbttn.config(fg="#FFFFFF")
        submitbttn.grid(row=4, column=2)
        label6 = tk.Button(top, text= "done",bg="#7186c7", command=top.destroy)
        label6.config(fg="#FFFFFF")
        label6.grid(row=7, column=2)
        result_label2 = tk.Label(top, text="", bg="#aab6d3")
        result_label2.grid(row=8, column=2)
        exit_button2=tk.Button(top, text="Go back",bg="#7186c7", command=top.destroy)
        exit_button2.config(fg="#FFFFFF")
        exit_button2.grid(row=9, column=1) 
    addtoDB()  
    
def facerecognition():
    def fetching():
        mycon = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="admin123",
            database="facerecognition"
        )
        myc = mycon.cursor()
        q = "select * from faces"
        myc.execute(q)
        recs = myc.fetchall()
        return recs

    x = fetching()
    global globalX
    globalX = x
    
    l = []

    for i in x:
        l.append(i[1])

    selected_file = filedialog.askopenfilename(title="Select an image")
    image = Image.open(selected_file)
    photo = ImageTk.PhotoImage(image)
    label5=tk.Label(frame, image=photo)
    label5.image = photo
    label5.grid(row=9, column=0, columnspan=2)

    if not selected_file:
        return  # User canceled file selection

    image = face_recognition.load_image_file(selected_file)
    face_locations = face_recognition.face_locations(image)
    face_landmarks_list = face_recognition.face_landmarks(image)
    
    k = None
    name = ""
    for i in l:
        known_image = face_recognition.load_image_file(i)
        known_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_image = face_recognition.load_image_file(selected_file)
        unknown_image_encoding = face_recognition.face_encodings(unknown_image)[0]
        results = face_recognition.compare_faces([known_encoding], unknown_image_encoding)
        
        if results == [True]:
            
            result_label.config(text="Person identified - ")
            name = "Person Identified: "
            k = i
    if results == [False]:
         pass            

    if k:
        for p, j, m in x:
            if j == k:
                name += p
                result_label.config(text= name, fg="#000000")
                result_label.grid(row=8, column=0, columnspan=2)
                break
            else:
                pass
        def search_wikipedia(term):
            try:
                wiki_wiki = wikipediaapi.Wikipedia('english')
                page_py = wiki_wiki.page(term)

                if not page_py.exists():
                    return "No matching results found on Wikipedia."
                summary = page_py.summary[:500]  
                return summary
            except Exception as e:
                return f"An error occurred: {str(e)}"
        def checkdb():            
            global result_labelm
            found = False
            for p, j, m in globalX:
                if j==k and m != None:
                    res = m 
                    result_labelm.config(text= res, fg="#000000")
                    result_labelm.grid(row=18, column=0, columnspan=2)
                    found = True
            if found == False: 
                result_labelm.config(text= "No informtion found in Database", fg="#000000")
                result_labelm.grid(row=18, column=0, columnspan=2)

        def toggle_result_text():
            if result_text.winfo_ismapped():
                result_text.grid_forget()
            else:
                result_text.grid(row=16, column=0, columnspan=2, pady=10, padx=50)        
        def on_search_button_click():
            result = search_wikipedia(p)
            result_text.config(state=tk.NORMAL)
            result_text.delete("1.0", tk.END)  
            result_text.insert(tk.END, result)
            result_text.config(state=tk.DISABLED)
            toggle_result_text()

    
    
        search_button = tk.Button(frame, text="Search Wikipedia", bg="#7186c7", command=on_search_button_click)
        search_button.config(fg="#FFFFFF")
        search_button.grid(row=15, column=0, columnspan=2)
       
        result_text = scrolledtext.ScrolledText(frame, width=50, height=10, wrap=tk.WORD, state=tk.DISABLED)
        result_text.grid(row=16, column=0, columnspan=2)
        result_text.grid_forget()
        
        result_labe81 = tk.Label(frame, text="", bg="#aab6d3")
        result_labe81.grid(row=15, column=1)
        
        searchdb_button = tk.Button(frame, text="Search Database", bg="#7186c7", command=checkdb)
        searchdb_button.config(fg="#FFFFFF")
        searchdb_button.grid(row=17, column=0, columnspan=2)
        
    else:
        result_label.config(text="No matching face found in the database.Face not recognized", fg="#A93226")
        result_label.grid(row=8, column=0, columnspan=2)
        
label9 = tk.Label(frame, text= "Click to recognise faces", bg="#aab6d3")
label9.grid(row=0, column=0)   
    
recognize_button = tk.Button(frame, text="Recognize Face",bg="#7186c7",padx=70, pady=2, command=facerecognition)
recognize_button.config(fg="#FFFFFF")
recognize_button.grid(row=0, column=1, columnspan=1)
  

result_label = tk.Label(frame, text="",fg="#FFFFFF", bg="#aab6d3")
result_label.grid(row=1, column=0)
  
label10 = tk.Label(frame, text= "Click to Insert into Databses", bg="#aab6d3")
label10.grid(row=2, column=0)
 
input_button = tk.Button(frame, text="Insert into database",bg="#7186c7",padx=60, pady=2, command= open1)
input_button.config(fg="#FFFFFF")
input_button.grid(row=2, column=1)
  
result_labe8 = tk.Label(frame, text="", bg="#aab6d3")
result_labe8.grid(row=3, column=0)
 
exit_button=tk.Button(frame, text="EXIT",bg="#7186c7", command=window.destroy)
exit_button.config(fg="#FFFFFF")
exit_button.grid(row=4, column=0)
  
window.mainloop()        