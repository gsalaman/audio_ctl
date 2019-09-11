from Tkinter import *
import paho.mqtt.client as mqtt

################################################
#  Our application class definition
################################################
class Application(Frame):
    def set_client(self, client):
        self.client = client

    def send_color(self):
        color_str = str(self.time_color_slider.get())
        client.publish("display/time/color", color_str)
        print ("requesting time color "+color_str)

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.grid(row=3,column=1,columnspan=3)

        self.time_color_label = Label(self,text="Color")
        self.time_color_label.grid(row=1,column=1)
        self.time_color_slider = Scale(self,from_=0, to=360, length=200, tickinterval=120,orient=HORIZONTAL)
        self.time_color_slider.grid(row=1,column=2)
        self.time_color_button = Button(self)
        self.time_color_button["text"] = "Send"
        self.time_color_button["command"] = self.send_color
        self.time_color_button.grid(row=1,column=3)
        self.time_color_indexes = Label(self, text="Red      Green     Blue        Red")
        self.time_color_indexes.grid(row=2,column=2)


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

#####################################################
# Message callback for MQTT
#####################################################
def on_message(client, userdata, message):
  global app

  #print "CALLBACK"

  if message.topic == "ir_cam_display/value/low_temp":
    app.refresh_cold_bound(message.payload)
  elif message.topic == "ir_cam_display/value/high_temp":
    app.refresh_hot_bound(message.payload)
  else:
    print "Unhandled message topic: ",message.topic

#####################################################
# Main code 
#####################################################

root = Tk()
root.title("Audio Control")
app = Application(master=root)

broker_address = "10.0.0.17"
#broker_address = "makerlabPi1"

client = mqtt.Client("glenn_audio_ctl_app")
client.on_message = on_message
try:
  client.connect(broker_address)
except:
  print "Unable to connect to MQTT broker"
  exit(0)
client.loop_start()
client.subscribe("ir_cam_display/value/#")

app.set_client(client)

app.mainloop()
root.destroy()

