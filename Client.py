from tkinter import *
from tkinter import scrolledtext, messagebox
import sys, socket, select, _thread
 
#def connect(host, port):
running = False

def send():
   data = message.get()
   #print(data)
   try:
      s.send(data.encode())
   except:
      error = messagebox.showinfo('Disconnected', 'Server is not active')
      exit()
   response.delete(0, END)
   chat.config(state=NORMAL)
   chat.insert(END ,'<You>' + data + '\n')
   chat.see(END)
   chat.config(state=DISABLED)

def sendonreturn(event):
   data = message.get()
   #print(data)
   try:
      s.send(data.encode())
   except:
      error = messagebox.showinfo('Disconnected', 'Server is not active')
      exit()
   response.delete(0, END)
   chat.config(state=NORMAL)
   chat.insert(END ,'<You>' + data + '\n')
   chat.see(END)
   chat.config(state=DISABLED)

def receive():
   global running
   while running:
      try:
         data = s.recv(4096)
         data = data.decode()
         if '<?info?>' in data:
            #print('True')
            ind = data.index('\n')
            status.set('Users Online: '+data[8:ind])
            if len(data) > ind+1:
               chat.config(state=NORMAL)
               chat.insert(END, data[ind+1:] + '\n')
               chat.see(END)
               chat.config(state=DISABLED)
         else:
            #print(data)
            chat.config(state=NORMAL)
            chat.insert(END, data + '\n')
            chat.see(END)
            chat.config(state=DISABLED)
      except:
         running = False
      #print(history.get())

def showhistory():
   s.send('<?history?>'.encode())

def available():
   s.send('<?available?>'.encode())

def change():
   s.send('<?change?>'.encode())

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def Quit():
   try:
      s.send('<?quit?>'.encode())
   except:
      pass
   s.close()
   root.destroy()
   global running
   running = False
   quit()

def on_closing():
   if messagebox.askokcancel("Quit", "Do you want to quit?"):
      try:
         s.send('<?quit?>'.encode())
      except:
         pass
      s.close()
      root.destroy()


host = '127.0.0.1'
port = 10000
flag = 1
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#except :
#   return 'Unable to connect'''

root = Tk()
frame1 = Frame(root)
#frame2 = Frame(root)
frame1.pack(side=TOP, fill=BOTH, expand=1)
#frame2.pack(side=TOP)
root.wm_title('Chat Room')
#history = StringVar()
message = StringVar()
status = StringVar()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label = 'Connect', command=donothing)
filemenu.add_command(label = 'Disconnect', command=donothing)
filemenu.add_command(label="Exit", command=Quit)
menubar.add_cascade(label="File", menu=filemenu)
optionsmenu = Menu(menubar, tearoff=0)
optionsmenu.add_command(label = 'Show History', command=showhistory)
optionsmenu.add_command(label = 'Show Available Users in Group', command=available)
optionsmenu.add_command(label="Change Chat Room", command=change)
menubar.add_cascade(label="Options", menu=optionsmenu)
root.config(menu=menubar)

chat = scrolledtext.ScrolledText(frame1, height=10, width=80, state=DISABLED)
chat.pack(side=TOP, fill=BOTH, expand=1)
response = Entry(frame1, textvariable = message)
response.focus()
send = Button(frame1, text='Send', command=send)
response.pack(side=LEFT, fill=X, expand=1)
send.pack(side=RIGHT)
online_users = Label(root, textvariable = status, relief = SUNKEN, anchor = W)
online_users.pack(side = BOTTOM, fill = X, expand = 1)
root.bind('<Return>', sendonreturn)
root.protocol("WM_DELETE_WINDOW", on_closing)
if flag == 1:
   try :
      s.connect((host, port))
   except:
      error = messagebox.showinfo('Unable to Connect', 'Server is not active')
      root.destroy()
      _thread.interrupt_main()
      quit()
   running = True
   _thread.start_new_thread(receive, ())
   status.set('Users Online: ')
   flag+=1
root.mainloop()



