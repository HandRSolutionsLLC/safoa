from tkinter import *
from tkinter import ttk,filedialog,messagebox
from os import path 
import os, random, time
from Crypto.Cipher import AES
from Crypto.Hash import SHA256



class App():

	def __init__(safoa):

		def getKey(password):
			hasher = SHA256.new(password.encode())
			return hasher.digest()

		safoa.key = getKey('h')
		safoa.userIsValid = False

		def chooseLocation(): 
			if dirOpt.get() == 2: messagebox.showinfo('SAFOA',"Please 'CHOOSE LOCATION'!")
			else: 
				safoa.dir_Opt = filedialog.askopenfilename() if dirOpt.get() else filedialog.askdirectory() 
				dir_Entry.delete(0.0,END),dir_Entry.insert(END,safoa.dir_Opt)		


		def activate(lock):
			targetPath = dir_Entry.get(0.0,END).strip() 
			if dirOpt.get() == 2: messagebox.showinfo('SAFOA',"Please 'CHOOSE LOCATION'!")
			elif targetPath == '' or not path.exists(targetPath): messagebox.showinfo('SAFOA',"File/Folder NOT FOUND!.")
			else:
				if lock:
					if not path.isdir(targetPath): 
						encrypt_file(targetPath)
						messagebox.showinfo('SAFOA',f"Encryption was successful!")
					else: encrypt_folder(targetPath)

				else: 
					if not path.isdir(targetPath): 
						decrypt_file(targetPath)
						messagebox.showinfo('SAFOA',f"Decryption was successful!")
					else: decrypt_folder(targetPath)

		def encrypt_file(filename):
			if b'safoa' in open(filename, 'rb').read(): print('Already encrypted!')
			else:
				chunksize = 64*1024 # 64 KB
				outputFile = filename.replace(os.path.basename(filename),f"{os.path.basename(filename)}#_")
				filesize = str(os.path.getsize(filename)).zfill(16)
				IV = b'safoa'
				while (len(IV)!=16): 	IV=b'safoa' if len(IV) > 16 else IV+chr(random.randint(0, 0xFF)).encode()	
				encryptor = AES.new(safoa.key, AES.MODE_CBC, IV)
				with open(filename, 'rb') as infile:
					with open(outputFile, 'wb') as outfile:
						outfile.write(filesize.encode())
						outfile.write(IV)
						while True:
							chunk = infile.read(chunksize)
							if len(chunk) == 0:	break
							elif len(chunk) % 16 != 0: chunk += b' ' * (16 - (len(chunk) % 16))
							outfile.write(encryptor.encrypt(chunk))
				os.remove(filename)
				os.rename(outputFile,filename)


		def decrypt_file(filename):
			if not b'safoa' in open(filename, 'rb').read(): print('Not encrypted!')
			else:
				chunksize = 64*1024
				outputFile = filename.replace(os.path.basename(filename),f"{os.path.basename(filename)}#_")
				with open(filename, 'rb') as infile:
					filesize = int(infile.read(16))
					IV = infile.read(16)
					decryptor = AES.new(safoa.key, AES.MODE_CBC, IV)
					with open(outputFile, 'wb') as outfile:
						while True:
							chunk = infile.read(chunksize)
							if len(chunk) == 0:	break
							outfile.write(decryptor.decrypt(chunk))
						outfile.truncate(filesize)
				os.remove(filename)
				os.rename(outputFile,filename)

		class progress_bar:
			def __init__(self,mode,length,dirpath,files):
				self.window = Toplevel(root)
				self.window.title('SAFOA')
				self.window.configure(background=keyType)
				s=ttk.Style()
				s.configure("TProgressbar", foreground='red', background='springgreen')
				self.info = Label(self.window,
					text=f'{mode} Data... 0.0 %',bg=keyType,font=('Gothic Bold',20,'bold italic'))
				self.info.pack()
				self.bar = ttk.Progressbar(self.window,orient=HORIZONTAL,length=400,
					mode='determinate',maximum=length)
				self.bar.pack(ipady=20)
				self.window.after(100,lambda:self.encryptFolder(mode,dirpath,files))
				self.window.mainloop()
			def encryptFolder(self,mode,dirpath,files):
				for index,file in enumerate(files,start=1): 
					time.sleep(0.5)
					encrypt_file(path.join(dirpath,file)) if mode == 'Encrypting' else decrypt_file(path.join(dirpath,file)) 
					self.info['text']=f'{mode} Data... {round(index/len(files)*100,1)} %'
					self.bar['value']=index
					self.window.update_idletasks()
				messagebox.showinfo('SAFOA',f"{mode.replace('ng','on')} was successful!")
				self.window.destroy()
		def encrypt_folder(foldername):
			for dirpath,folders,files in os.walk(foldername):
				if files != []: progressBar =  progress_bar('Encrypting',len(files),dirpath,files) 
		def decrypt_folder(foldername):
			for dirpath,folders,files in os.walk(foldername): 
				if files != []:	progressBar =  progress_bar('Decrypting',len(files),dirpath,files) 


		keyType = 'gold'

		def Login():

			def focusIn(event):
				if passwordEntry.get() == 'ENTER PASSWORD HERE...': 
					passwordEntry.delete(0,END)
					passwordEntry['fg']='red'
					passwordEntry['show']='*'
			def focusOut(event):
				if passwordEntry.get() == '': 
					passwordEntry['fg']='red'
					passwordEntry['show']=''
					passwordEntry.insert(0,'ENTER PASSWORD HERE...')

			def confirm(event):
				if passwordEntry.get() == '1234': 
					safoa.userIsValid = True
					root.destroy() 
				else: messagebox.showinfo('SAFOA','Wrong Key! Try Again.'),passwordEntry.delete(0,'end')

			root = Tk()
			style = ttk.Style()
			style.theme_use('clam')
			style.configure('TFrame',background=keyType)
			style.configure('TLabel',background='white',font=('Sylfaen',10,'bold'))
			icon_img = PhotoImage(file='images/icon.gif')
			logo_img = PhotoImage(file='images/logo.png')
			root.tk.call('wm','iconphoto',root._w,icon_img)
			root.title('SAFOA')
			root.wm_resizable(width=False,height=False)
			root.configure(background='white')
			Frame = ttk.Frame(relief='ridge',border=5)
			Frame.grid(row=0,column=0)
			ttk.Label(root,text='© 2020 BITBANK SOFTWARE').grid(row=1,column=0)
			ttk.Label(Frame,image=logo_img).pack()
			passwordEntry = Entry(root,fg='red',font=('Couurier',18,'bold'),width=23)
			passwordEntry.insert(0,'ENTER PASSWORD HERE...')
			passwordEntry.bind('<FocusIn>',focusIn)
			passwordEntry.bind('<FocusOut>',focusOut)
			passwordEntry.bind('<Return>',confirm)
			passwordEntry.place(x=60,y=170)
			root.mainloop()


		# Login()

		# if not safoa.userIsValid: exit()


		root = Tk()
		style = ttk.Style()
		style.theme_use('clam')
		style.configure('TFrame',background=keyType)
		style.configure('TLabel',background='white',font=('Sylfaen',12,'bold'))
		style.configure('TButton',background=keyType,
			font=('Arial',13,'bold'),relief='raised')
		style.configure('OpenLocation.TButton',background='green',foreground='white',
			font=('Arial',13,'bold'))
		style.configure('lock.TButton',background='red',foreground='black',
			font=('Arial',13,'bold'))
		style.configure('unlock.TButton',background='green',foreground='black',
			font=('Arial',13,'bold'))
		style.configure('file.TRadiobutton',font=('Arial',13,'bold'),background='yellow')
		style.configure('folder.TRadiobutton',font=('Arial',13,'bold'),background='orange')
		style.map('TButton',background=[('pressed',keyType)],foreground=[('pressed','black')])
		style.map('OpenLocation.TButton',background=[('pressed','yellow')],foreground=[('pressed','black')])
		style.map('TRadiobutton',background=[('pressed','blue')],foreground=[('pressed','white')])
		dirOpt,safoa.dir_Opt = IntVar(),False
		dirOpt.set(2)
		icon_img = PhotoImage(file='images/icon.gif')
		logo_img = PhotoImage(file='images/logo.png')
		lock_img = PhotoImage(file='images/encrypt.png')
		unlock_img = PhotoImage(file='images/decrypt.png')
		root.tk.call('wm','iconphoto',root._w,icon_img)
		root.title('SAFOA')
		root.wm_resizable(width=False,height=False)
		root.configure(background='white')
		topFrame = ttk.Frame(relief='ridge',border=5)
		midFrame = ttk.Frame(style='mid.TFrame',relief='raised',border=5)
		bottomFrame = ttk.Frame(relief='ridge')
		topFrame.grid(row=0,column=0)
		midFrame.grid(row=1,column=0)
		bottomFrame.grid(row=2,column=0)
		ttk.Label(root,text='© 2020 BITBANK SOFTWARE').grid(row=3,column=0)
		############# TOP FRAME ###############
		ttk.Label(topFrame,image=logo_img).pack()
		############# MID FRAME ###############
		fileOpt_btn = ttk.Radiobutton(midFrame,text='File',style='file.TRadiobutton',variable=dirOpt,value=1,width=10)
		folderOpt_btn = ttk.Radiobutton(midFrame,text='Folder',style='folder.TRadiobutton',variable=dirOpt,value=0,width=10)
		dir_Entry = Text(midFrame,width=50,font=('Times New Roman',15,'bold'),height=4)
		openDir_btn = ttk.Button(midFrame,style='OpenLocation.TButton',text='Choose Location',command=chooseLocation)
		ttk.Label(midFrame,text='Enter Key: ',background=keyType).grid(row=2,column=0,columnspan=2,sticky='W')
		key_Entry = Entry(midFrame,show='*',width=12,bg='black',fg='white',font=('Times New Roman',15,'bold'))
		ttk.Label(midFrame,text='Confirm Key: ',background=keyType).grid(row=2,column=2,sticky='W')
		keyConfirm_Entry = Entry(midFrame,show='*',width=12,bg='black',fg='white',font=('Times New Roman',15,'bold'))
		fileOpt_btn.grid(row=0,column=0)
		folderOpt_btn.grid(row=0,column=1)
		dir_Entry.grid(row=1,column=0,columnspan=4)
		openDir_btn.grid(row=0,column=2,columnspan=2,sticky='E')
		key_Entry.grid(row=2,column=1)
		keyConfirm_Entry.grid(row=2,column=3)
		############# BOTTOM FRAME ############
		lock_btn = ttk.Button(bottomFrame,style='lock.TButton',text='LOCK',width=24,image=lock_img,compound='top',command=lambda:activate(True)).grid(row=0,column=0)
		unlock_btn = ttk.Button(bottomFrame,style='unlock.TButton',text='UNLOCK',width=24,image=unlock_img,compound='top',command=lambda:activate(False)).grid(row=0,column=1)
		# print(help(root.wm_resizable))
		root.mainloop()

App()