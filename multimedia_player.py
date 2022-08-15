import tkinter as tk
import vlc
import tkinter.filedialog as tkf
import tkinter.ttk as ttk
import sys 
from functools import reduce


path = None 
root = tk.Tk()
root.resizable(width=True,height=True)
root.minsize(1800,800)
root.attributes('-zoomed',True)
root.title("Media Player")
frame = tk.Frame(root)
frame.pack(fill="both",expand=True)
display = tk.Frame(frame, bd=0,background='black')
display.place(relwidth=1, relheight=1)

control = tk.Canvas(root,height=20,width=1500)
control.pack(side="bottom",padx=20,pady=20)
vol = 80
length = 0
frame = None
PLAYBACK_RATE = 1

# mixer
p = None
is_play = True
IS_FULLSCREEN = False
vol_label_in_full_screen = tk.Label()
speed_label_in_full_screen = tk.Label()

# slider
def slider(a):
    global p , my_slider
    if p != None:
        p.set_time(int(length*my_slider.get()*10))

# time 
time = tk.Label(control,text="Time : 0.00.00 / 0.00.00")
time.grid(row=0,column=0,padx=30)

# slider

my_slider = ttk.Scale(control,from_= 0, to=100 , orient= "horizontal",command=slider,length=800)
my_slider.grid(row=0,column=1,padx=30,)


# volume
volume = tk.Label(control,text="Volume : 80 / 100")
volume.grid(row=0,column=2,padx=30)

# speed
speed = tk.Label(control,text=f"Speed : {PLAYBACK_RATE} / 2")
speed.grid(row=0,column=3,padx=30)

# subtitles
speed = tk.Label(control,text=f"Speed : {PLAYBACK_RATE} / 2")
speed.grid(row=0,column=3,padx=30)

# slider



def slider_start():
    global my_slider
    my_slider.set(0)



def update_time():
    global p , length , my_slider
    if p == None or (not is_play) or IS_FULLSCREEN:
        return
    l = int((p.get_time()+.5)/1000)

    if l < 6:
        length = int((p.get_length())//1000)

    if not p.is_playing() and abs(p.get_time() - p.get_length()) < 10:
        stop_music()
        return
    
    if length > 0:
        slider_value = int(l*100/length)
        my_slider.config(value=slider_value)
    h = length//3600
    m = (length - h*3600)//60
    s = int(length - h*3600 - m*60)

    length_string = f"{h}.{m}.{s}"

    h = l//3600
    m = (l - h*3600)//60
    s = int(l - h*3600 - m*60)

    time.config(text=f"Time : {h}.{m}.{s} / {length_string}")
    time.after(800,update_time)


# menus

def play_music():
    global p , is_play
    if p == None or  is_play:
        return
    else:
        p.play()
    is_play = True
    update_time()

def pause_music():
    global p , is_play
    if p == None or (not is_play):
        return
    p.pause()
    is_play = False

def fullscreen_mode(z = None):
    global frame , p , IS_FULLSCREEN
    if path != None:
        if path.endswith('.mp4') or path.endswith('.mkv'):
            emptyMenu = tk.Menu(root)
            root.config(menu=emptyMenu)
            control.pack_forget()
            root.attributes('-fullscreen',True)
            IS_FULLSCREEN = True



def exit_fullscreen(x = None,MODE = False):
    global IS_FULLSCREEN
    if IS_FULLSCREEN:
        root.attributes('-fullscreen',MODE)
        root.config(menu=topbar)
        control.pack_forget()
        control.pack(side="bottom",padx=20,pady=20)
        IS_FULLSCREEN = False
        update_time()

def stop_music():
    global length , p , is_play , IS_FULLSCREEN
    if p == None:
        return
    p.stop()
    del p
    p = None
    length = 0
    is_play = False
    IS_FULLSCREEN = False
    time.config(text="Time : 0.00.00 / 0.00.00")
    root.title("Media Player")
    slider_start()
    audio.delete(0,'end')
    subtitle.delete(0,'end')

def slider_dimension():
    my_slider.config(length=800)

def skip_right(x = None):
    if p != None:
        p.set_time(p.get_time()+10000)
def skip_left(x = None):
    if p != None:
        p.set_time(p.get_time()-10000)

def add_menu(x = None,is_first = False):
    global subtitle
    if path != None and not is_first:
        subtitle_no.set(p.video_get_spu())
        audio_no.set(p.audio_get_track())
        value = p.video_get_spu_count()
        for i in range(0,value):
            subtitle.add_radiobutton(label=p.video_get_spu_description()[i][1],variable=subtitle_no,value=p.video_get_spu_description()[i][0],command=set_subtitle)
        value = p.audio_get_track_count()
        for i in range(0,value):
            audio.add_radiobutton(label=p.audio_get_track_description()[i][1],variable=audio_no,value=p.audio_get_track_description()[i][0],command=set_audio)


def open_file(a=True):
    global path , length , time , p , root , is_play , frame ,display ,add_menu
    temp = path
    if a:
        path = tkf.askopenfilename(
            filetypes=[["media","*.mp3"],["media","*.m4a"],["media",'*.mp4'],["media",'*.mkv'],["all files","*.*"]],
            initialdir=sys.argv[1:]
            )
        if not path:
            path = temp
            return
    stop_music()
    if path.endswith(".mp4") or path.endswith('.mkv'):
        slider_dimension()
        p = vlc.MediaPlayer(path)
        p.audio_set_volume(vol)
        p.set_rate(PLAYBACK_RATE)
        p.set_xwindow(display.winfo_id())
        p.play()
        control.after(5000,add_menu)
    else:
        p = vlc.MediaPlayer(path)
        p.set_rate(PLAYBACK_RATE)
        p.audio_set_volume(vol)
        p.play()


    
    if "/" not in path:
        title_player = path
    else:
        title_player = path[-(path[::-1].index("/")):]
    time.config(text="Time : 0.00.00 / 0.00.00")
    time.after(1000,update_time)
    root.title(title_player)
    slider_start()
    is_play = True
# full screen mode

if len(sys.argv) > 1:
    path = reduce(lambda a,b:a+" "+b ,sys.argv[1:])
    print(path)
    # path = None
    open_file(False)

def show_control(x = None):
    if IS_FULLSCREEN:
        exit_fullscreen(1,True)
        if x == None:
            control.after(4000,fullscreen_mode)


# volume

def vol_inc(x = None):
    global vol,volume
    if vol < 100:
        vol += 10
        p.audio_set_volume(vol)
        volume.config(text=f"Volume : {vol} / 100")
        show_control()

def vol_dec(x = None):
    global vol,volume
    if vol > 0:
        vol -= 10
        p.audio_set_volume(vol)
        volume.config(text=f"Volume : {vol} / 100")
        show_control()

def increase_rate(x = None):
    global PLAYBACK_RATE
    if PLAYBACK_RATE < 2:
        PLAYBACK_RATE += .1
        PLAYBACK_RATE = int(PLAYBACK_RATE*10)/10
        p.set_rate(PLAYBACK_RATE)
        speed.config(text=f"Speed : {PLAYBACK_RATE} / 2")

def decrease_rate(x = None):
    global PLAYBACK_RATE
    if PLAYBACK_RATE > 0:
        PLAYBACK_RATE -= .1
        PLAYBACK_RATE = int(PLAYBACK_RATE*10)/10
        p.set_rate(PLAYBACK_RATE)
        speed.config(text=f"Speed : {PLAYBACK_RATE} / 2")
# buttons

topbar = tk.Menu(root)
topbar.add_command(label="open",command=open_file)
topbar.add_command(label="play",command=play_music)
topbar.add_command(label="pause",command=pause_music)
topbar.add_command(label="stop",command=stop_music)
topbar.add_command(label="Vol+",command=vol_inc)
topbar.add_command(label="Vol-",command=vol_dec)
subtitle = tk.Menu(topbar)
subtitle_no = tk.IntVar()
audio = tk.Menu(topbar)
audio_no = tk.IntVar()

def set_subtitle(x=None):
    p.video_set_spu(subtitle_no.get())

def set_audio(x=None):
    p.audio_set_track(audio_no.get())

add_menu(2,True)
topbar.add_cascade(label="Subtitle",menu=subtitle)
topbar.add_cascade(label="Audio",menu=audio)
topbar.add_command(label="FullScreen",command=fullscreen_mode)

# audio_setting


root.config(menu=topbar)

def toggle_music(x):
    if is_play:
        pause_music()
    else:
        play_music()

root.bind("<space>",toggle_music)
root.bind("<Escape>",exit_fullscreen)
root.bind("<f>",fullscreen_mode)
root.bind("<Up>",vol_inc)
root.bind("<Down>",vol_dec)
root.bind("<Right>",skip_right)
root.bind("<Left>",skip_left)
root.bind("]",increase_rate)
root.bind("[",decrease_rate)
root.bind("<s>",show_control)


root.mainloop()
