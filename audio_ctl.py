from Tkinter import *
import paho.mqtt.client as mqtt

def send_color():
  global time_color_slider
  global client

  color_str = str(time_color_slider.get())
  client.publish("display/time/color", color_str)
  print ("requesting time color "+color_str)

my_window=Tk()
my_window.title("Audio Display Controls")

frame_time_color=Frame(my_window)

time_color_label = Label(frame_time_color,text="Color")
time_color_label.grid(row=1,column=1)
time_color_slider = Scale(frame_time_color,from_=0, to=360, length=200, tickinterval=120,orient=HORIZONTAL)
time_color_slider.grid(row=1,column=2)
time_color_button = Button(frame_time_color)
time_color_button["text"] = "Send"
time_color_button["command"] = send_color
time_color_button.grid(row=1,column=3)
time_color_indexes = Label(frame_time_color, text="Red      Green     Blue        Red")
time_color_indexes.grid(row=2,column=2)

frame_time_color.grid(row=0,column=0)

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

my_window.mainloop()

