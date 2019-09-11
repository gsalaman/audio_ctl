from Tkinter import *
import paho.mqtt.client as mqtt


def send_color():
  global time_color_slider
  global client

  color_str = str(time_color_slider.get())
  client.publish("display/time/color", color_str)
  print ("requesting time color "+color_str)

def send_thickness():
  global time_thickness_slider
  global client

  thickness_str = str(time_thickness_slider.get())
  client.publish("display/time/y_spread", thickness_str)
  print ("requesting time thickness "+thickness_str)

def x_zoom_in():
  global client
  client.publish("display/time/x_ctl", "+")
  print ("zoom in on time x")

def x_zoom_out():
  global client
  client.publish("display/time/x_ctl", "-")
  print ("zoom out on time x")

def y_zoom_in():
  global client
  client.publish("display/time/y_ctl", "+")
  print ("zoom in on time y")

def y_zoom_out():
  global client
  client.publish("display/time/y_ctl", "-")
  print ("zoom out on time y")

def freq_mag_zoom_in():
  global client
  client.publish("display/freq/y_ctl", "+")
  print "zoom in on freq magnitude"

def freq_mag_zoom_out():
  global client
  client.publish("display/freq/y_ctl", "-")
  print "zoom out on frequency magnitude"

def send_pixels_per_bin():
  global pixels_per_bin_slider
  global client

  my_str = str(pixels_per_bin_slider.get())
  client.publish("display/freq/pixels_per_bin", my_str)
  print ("requesting "+my_str+" pixels_per_bin")

def send_num_pts_per_bin():
  global num_pts_per_bin_slider
  global client

  my_str = str(num_pts_per_bin_slider.get())
  client.publish("display/freq/num_pts_per_bin", my_str)
  print ("requesting "+my_str+" points per bin")

def calc_hz_per_bin():
  if (pts_per_bin.get() == "?"):
    hz_per_bin.set("?")
  else:
    pts_per_bin_int = int(pts_per_bin.get())
    hz_per_bin_int = 43 * pts_per_bin_int
    hz_per_bin.set(str(hz_per_bin_int))

def calc_display_range():
  if (hz_per_bin.get() == "?"):
    display_range.set("?")
  elif (num_bins.get() == "?"):
    display_range.set("?")
  else:
    hz_per_bin_int = int(hz_per_bin.get())
    num_bins_int = int(num_bins.get())
    display_range_int = hz_per_bin_int * num_bins_int
    display_range.set(str(display_range_int))
     
def refresh_num_pts_per_bin(payload):
  pts_per_bin.set(payload)
  print "local pts_per_bin: "+payload  
  calc_hz_per_bin()
  calc_display_range()

def refresh_num_bins(payload):
  num_bins.set(payload)
  print "local num_bins: "+payload  
  calc_display_range()

###############################################
my_window=Tk()
my_window.title("Audio Display Controls")
pts_per_bin = StringVar()
pts_per_bin.set("?")
num_bins = StringVar()
num_bins.set("?")
hz_per_bin = StringVar()
hz_per_bin.set("?")
display_range = StringVar()
display_range.set("?")



frame_time=LabelFrame(my_window,text="Time Display adjustments")
time_color_label = Label(frame_time,text="Color")
time_color_label.grid(row=0,column=0)
time_color_slider = Scale(frame_time,from_=0, to=360, length=200, tickinterval=120,orient=HORIZONTAL)
time_color_slider.grid(row=0,column=1,columnspan=3)
time_color_button = Button(frame_time)
time_color_button["text"] = "Send"
time_color_button["command"] = send_color
time_color_button.grid(row=0,column=4)

time_color_indexes = Label(frame_time, text="Red      Green     Blue        Red")
time_color_indexes.grid(row=1,column=1,columnspan=3)

time_thickness_label = Label(frame_time,text="Thickness")
time_thickness_label.grid(row=2,column=0)
time_thickness_slider = Scale(frame_time,from_=0, to=10,length=200,orient=HORIZONTAL)
time_thickness_slider.grid(row=2,column=1,columnspan=3)
time_thickness_button = Button(frame_time)
time_thickness_button["text"] = "Send"
time_thickness_button["command"] = send_thickness
time_thickness_button.grid(row=2,column=4)

time_x_label = Label(frame_time, text="X-axis")
time_x_label.grid(row=3,column=0)
time_x_zoom_in_button = Button(frame_time, text="Zoom In", command=x_zoom_in)
time_x_zoom_in_button.grid(row=3,column=1)
time_x_zoom_out_button = Button(frame_time, text="Zoom Out", command=x_zoom_out)
time_x_zoom_out_button.grid(row=3,column=2)
time_y_label = Label(frame_time, text="Y-axis")
time_y_label.grid(row=4,column=0)
time_y_zoom_in_button = Button(frame_time, text="Zoom In", command=y_zoom_in)
time_y_zoom_in_button.grid(row=4,column=1)
time_y_zoom_out_button = Button(frame_time, text="Zoom Out", command=y_zoom_out)
time_y_zoom_out_button.grid(row=4,column=2)

frame_time.grid(row=0,column=0)

frame_freq=LabelFrame(my_window,text="Frequency Display adjustments")

freq_y_label = Label(frame_freq, text="magnitude")
freq_y_label.grid(row=0,column=0)
freq_y_zoom_in_button = Button(frame_freq, text="Zoom In", command=freq_mag_zoom_in)
freq_y_zoom_in_button.grid(row=0,column=1)
freq_y_zoom_out_button = Button(frame_freq, text="Zoom Out", command=freq_mag_zoom_out)
freq_y_zoom_out_button.grid(row=0,column=2)

pixels_per_bin_label = Label(frame_freq,text="Pixels per bin")
pixels_per_bin_label.grid(row=1,column=0)
pixels_per_bin_slider = Scale(frame_freq,from_=1,to=10,length=200,orient=HORIZONTAL)
pixels_per_bin_slider.grid(row=1,column=1,columnspan=3)
pixels_per_bin_button = Button(frame_freq)
pixels_per_bin_button["text"] = "Send"
pixels_per_bin_button["command"] = send_pixels_per_bin
pixels_per_bin_button.grid(row=1,column=4)

num_pts_per_bin_label = Label(frame_freq,text="Num pts per bin")
num_pts_per_bin_label.grid(row=2,column=0)
num_pts_per_bin_slider = Scale(frame_freq,from_=1,to=20,length=200,orient=HORIZONTAL)
num_pts_per_bin_slider.grid(row=2,column=1,columnspan=3)
num_pts_per_bin_button = Button(frame_freq)
num_pts_per_bin_button["text"] = "Send"
num_pts_per_bin_button["command"] = send_num_pts_per_bin
num_pts_per_bin_button.grid(row=2,column=4)

pts_per_bin_text = Label(frame_freq, text="Pts per bin: ")
pts_per_bin_text.grid(row=3,column=0)
pts_per_bin_label = Label(frame_freq, textvariable=pts_per_bin)
pts_per_bin_label.grid(row=3,column=1)

num_bins_text = Label(frame_freq, text="num bins: ")
num_bins_text.grid(row=3,column=2)
num_bins_label = Label(frame_freq, textvariable=num_bins)
num_bins_label.grid(row=3,column=3)

hz_per_bin_text = Label(frame_freq, text="Hz per bin: ")
hz_per_bin_text.grid(row=4,column=0)
hz_per_bin_label = Label(frame_freq, textvariable=hz_per_bin)
hz_per_bin_label.grid(row=4,column=1)

freq_range_text = Label(frame_freq, text="Total Frequency Range: ")
freq_range_text.grid(row=4, column=2)
freq_range_label = Label(frame_freq, textvariable=display_range)
freq_range_label.grid(row=4,column=3)

frame_freq.grid(row=1,column=0)

#####################################################
# Message callback for MQTT
#####################################################
def on_message(client, userdata, message):
  #print "CALLBACK"

  if message.topic == "display/freq/num_pts_per_bin":
    refresh_num_pts_per_bin(message.payload)
  elif message.topic == "display/freq/num_bins":
    refresh_num_bins(message.payload)
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
client.subscribe("display/freq/num_bins")
client.subscribe("display/freq/num_pts_per_bin")

my_window.mainloop()

