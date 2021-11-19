from tkinter import *
import pygame
from pygame import mixer
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
root = Tk()
root.geometry("500x450")

mixer.init()

mainframe=Frame(root)
mainframe.pack(pady=20)

playlist= Listbox(mainframe,bg="black",fg="green",width=60, selectbackground="white" ,selectforeground="black")
playlist.grid(row=0, column=0)

def song_time():
    global current_time
    current_time=pygame.mixer.music.get_pos() /1000
    slider_label.config(text=f'Slider:{int(song_slider.get())} and Song Pos: {int( current_time)}')
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    current_song= playlist.curselection()
    song = playlist.get(current_song)
    song_mut=MP3(song)
    global  song_length
    song_length= song_mut.info.length
    converted_current_length = time.strftime('%M:%S', time.gmtime(song_length))
    current_time = current_time + 1
    if int(song_slider.get())==int(song_length):
        status_bar.config(text=f'Time elapsed: {converted_current_length}')
    elif int(song_slider.get())==int(current_time):
        slider_position = int(song_length)
        song_slider.config(to=slider_position, value=int(current_time))
    else:
        slider_position = int(song_length)
        song_slider.config(to=slider_position, value=int(song_slider.get()))
        converted_current_length = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))
        status_bar.config(text=f'Time elapsed:{converted_current_time} of {converted_current_length}')



    next_time=int(song_slider.get()) +1
    song_slider.config(value=next_time)

    status_bar.after(1000, song_time)

def slide(X):
   # slider_label.config(text=f'{int(song_slider.get())} of {int(song_length)}')
   song = playlist.get(ACTIVE)

   pygame.mixer.music.load(song)
   pygame.mixer.music.play(loops=0,start=int(song_slider.get()))
def volume(x):
    pass
def add_song():
        song = filedialog.askopenfilename(initialdir="allaudio/", title="choose a song",filetypes=(("mp3 files","*.mp3"),))

        playlist.insert(END,song)

def add_many_song():
    song = filedialog.askopenfilenames(initialdir="allaudio/", title="choose a song",filetypes=(("mp3 files","*.mp3"),))
    playlist.insert(END, song)


def play_song():
    song = playlist.get(ACTIVE)


    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_time()
    #slider_position= int(song_length)
   # current_time=current_time+1
  #  song_slider.config(to=slider_position, value=int(current_time))
def stop_song():
    pygame.mixer.music.stop()
    playlist.selection_clear(ACTIVE)


def prev_song():
    nxt_one = playlist.curselection()
    nxt_one = nxt_one[0]-1
    song = playlist.get(nxt_one)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    playlist.selection_clear(0, END)

    playlist.activate(nxt_one)
    playlist.selection_set(nxt_one, last=None)


def next_song():
    nxt_one = playlist.curselection()
    nxt_one=nxt_one[0]+1
    song=playlist.get(nxt_one)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    playlist.selection_clear(0,END)

    playlist.activate(nxt_one)
    playlist.selection_set(nxt_one,last=None)

global pause_glob
pause_glob=False
def pause_song(is_pause_glob):
    global pause_glob
    pause_glob=is_pause_glob
    if pause_glob:
        pygame.mixer.music.unpause()
        pause_glob=False
    else:
        pygame.mixer.music.pause()
        pause_glob = True
def del_song():
    playlist.delete(ANCHOR)
    pygame.mixer.music.stop()

def del_allsong():
    playlist.delete(0,END)
    pygame.mixer.music.stop()



backward=PhotoImage(file="back50.png")
forward=PhotoImage(file="forward50.png")

play=PhotoImage(file="play50.png")
pause=PhotoImage(file="pause50.png")

stop=PhotoImage(file="stop50.png")

framecont=Frame(mainframe)
framecont.grid(pady= 30,row=1,column=0)
backward_but=Button(framecont,image=backward, borderwidth=0,command=prev_song)
forward_but=Button(framecont, image=forward, borderwidth=0,command=next_song)
play_but=Button(framecont, image=play, borderwidth=0,command=play_song)
pause_but=Button(framecont, image=pause, borderwidth=0, command=lambda: pause_song(pause_glob))
stop_but=Button(framecont, image=stop, borderwidth=0,command=stop_song)

backward_but.grid(row=0,column=0, padx=10)
forward_but.grid(row=0,column=1, padx=10)
play_but.grid(row=0,column=2, padx=10)
pause_but.grid(row=0,column=3,padx=10)
stop_but.grid(row=0,column=4,padx=10)

selm= Menu(root)
root.config(menu=selm)

song= Menu(selm)
song.add_command(label="first song",command=add_song)
selm.add_cascade(label="Add song", menu=song)

remove= Menu(selm)
remove.add_command(label="delete song",command=del_song)
remove.add_command(label="delete all song",command=del_allsong)
selm.add_cascade(label="Remove song",menu=remove)

status_bar= Label(root, text='',bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

song_slider=ttk.Scale(root,from_=0, to=100, orient=HORIZONTAL, value=0,command=slide,length=360)
song_slider.pack(pady=10)

slider_label=Label(root, text="0")
slider_label.pack(pady=10)
root.mainloop()