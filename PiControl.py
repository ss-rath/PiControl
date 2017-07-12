''' Developed by Soumya Sambit Rath, NIT Rourkela on 12.07.2017
rath.soumyasambit@gmail.com'''
from Tkinter import *
import ttk
import tkMessageBox
import RPi.GPIO as GPIO


class Main():
	def __init__(self):
		self.SelectedPins=[]
	
	def Update(self):
		
		for i in range(len(self.OutputPinsSelected)):
			GPIO.output(self.OutputPinsSelected[i],self.OutputPinValues[i].get())
		
		for i in range(len(self.InputPinsSelected)):
			Text="GPIO "+str(self.InputPinsSelected[i])+ " is "
			Label(self.Window3,text=Text).grid(column=0,row=len(self.OutputPinsSelected)+4+i)
			Value=GPIO.input(self.InputPinsSelected[i])
			if Value:
				Label(self.Window3, text="HIGH").grid(column=1, row=len(self.OutputPinsSelected)+4+i)
			else:
				Label(self.Window3, text="LOW").grid(column=1, row=len(self.OutputPinsSelected)+4+i)
		
		print "Updated"
			
	
	def ControlWindow(self):
		self.Window3=Tk()
		img = Image("photo", file="rpi.gif") 
		self.Window3.call('wm','iconphoto',self.Window3._w,img)
		self.Window3.wm_title("RPi")
		self.OutputPinValues=[]
		self.InputPinsSelected=[]
		self.OutputPinsSelected=[]
		Label(self.Window3, text="Control Panel", font=("bold")).grid(column=0, row=0)
		
		for i in range(len(self.SelectedPins)):
			if self.PinType[self.SelectedPins[i]]==1:
				k=IntVar()
				k.set(0)
				self.OutputPinsSelected.append(self.SelectedPins[i])
				self.OutputPinValues.append(k)
			else:
				self.InputPinsSelected.append(self.SelectedPins[i])
		
		for i in range(len(self.OutputPinsSelected)):
			Label(self.Window3, text="GPIO "+str(self.OutputPinsSelected[i])+" : ").grid(column=0, row=i+1)
			Radiobutton(self.Window3, text="HIGH", variable=self.OutputPinValues[i], value=1).grid(column=1, row=i+1)
			Radiobutton(self.Window3, text="LOW", variable=self.OutputPinValues[i], value=0).grid(column=2, row=i+1)
		
		if len(self.InputPinsSelected)!=0:
			Label(self.Window3, text="Pin Status", font=("bold")).grid(column=0, row=len(self.OutputPinsSelected)+2)
		for i in range(len(self.InputPinsSelected)):
			Text="GPIO "+str(self.InputPinsSelected[i])+ " is "
			Label(self.Window3, text=Text).grid(column=0, row=len(self.OutputPinsSelected)+4+i)
			Value=GPIO.input(self.InputPinsSelected[i])
			if Value:
				Label(self.Window3, text="HIGH").grid(column=1, row=len(self.OutputPinsSelected)+4+i)
			else:
				Label(self.Window3, text="LOW").grid(column=1, row=len(self.OutputPinsSelected)+4+i)
			
		SetButton=Button(self.Window3, text="Update", command=self.Update)
		SetButton.grid(column=1)
		self.Window3.mainloop()
		

	def Action(self):
		
		self.PinType={}
		
		for i in range(len(self.SelectedPins)):
			self.PinType[self.SelectedPins[i]]=self.RadioButtonVariables[i].get()
		
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		for i in range(len(self.SelectedPins)):
			if self.PinType[self.SelectedPins[i]]==1:
				GPIO.setup(self.SelectedPins[i],GPIO.OUT)
			else:
				GPIO.setup(self.SelectedPins[i],GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		
		
		tkMessageBox.showinfo("Finished", "All Selected Pins have now been configured" )
		self.Window2.quit()
		self.Window2.destroy()
		self.ControlWindow()

	def PinMode(self):
		self.Window2=Tk()
		img = Image("photo", file="rpi.gif") 
		self.Window2.call('wm','iconphoto',self.Window2._w,img)
		self.Window2.wm_title("Set")
		self.RadioButtonVariables=[]
		Label(self.Window2, text="Please choose pin mode").grid(column=0, row=0,columnspan=2)
		for i in range(len(self.SelectedPins)):
			i=IntVar()
			i.set(1)
			self.RadioButtonVariables.append(i)
		
		for i in range(len(self.SelectedPins)):
			Label(self.Window2, text="GPIO"+str(self.SelectedPins[i])+" : ").grid(column=0, row=i+1)
			Radiobutton(self.Window2, text="Output", variable=self.RadioButtonVariables[i], value=1).grid(column=1, row=i+1)
			Radiobutton(self.Window2, text="Input", variable=self.RadioButtonVariables[i], value=0).grid(column=2, row=i+1)
		SetButton=Button(self.Window2, text="Set", command=self.Action)
		SetButton.grid(column=1, row=len(self.SelectedPins)+1)
		self.Window2.mainloop()
			

	def ShowPinout(self):
		self.Window1 = Tk()
		self.Window1.wm_title('Pinout')
		photo = PhotoImage(file = "pinout.gif")
		label = Label(self.Window1,image = photo)
		label.pack()
		self.Window1.mainloop()
		  
	def SelectPins(self):
		for i in range(28):
			if self.PinVars[i].get()==1:
				self.SelectedPins.append(i)
		if len(self.SelectedPins)==0:
			tkMessageBox.showinfo("Error", "No Pins Selected" )
		else:
			print "The Selected pins are:"
			print self.SelectedPins
			#self.Window1.quit()
			self.root.quit()
			#self.Window1.destroy()
			self.root.destroy()
			self.PinMode()

	def Cancel(self):
		self.root.quit()
		self.root.destroy()
			

	def CreateRootWindow(self):
		self.root=Tk()
		img = Image("photo", file="rpi.gif") 
		self.root.call('wm','iconphoto',self.root._w,img)
		self.root.wm_title("Select pins to be used")
		
		self.PinVars=[]
		for i in range(28):
			i=BooleanVar()
			i.set(False)
			self.PinVars.append(i)
		self.PinButtons=[]
		for i in range(28):
			Temp=Checkbutton(self.root, text="GPIO"+str(i), variable=self.PinVars[i])
			self.PinButtons.append(Temp)

		Pinout=Button(self.root, text="Pinout Chart", command=self.ShowPinout)
		Select = Button(self.root, text="Select", command=self.SelectPins)
		Cancel = Button(self.root, text="Cancel", command=self.Cancel)

		for i in range(28):
			self.PinButtons[i].grid(column=i/4,row=i%4)

		Pinout.grid(column=2, row=10)
		Select.grid(column=3, row=10)
		Cancel.grid(column=4, row=10)
		self.root.mainloop()


Window1=Main()
Window1.CreateRootWindow()
        
