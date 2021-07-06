import pygame                           # pip install pygame
import datetime
from pygame import mixer
from datetime import datetime
import time
from mutagen.mp3 import MP3             # pip install mutagen
from mutagen.wave import WAVE
import time                     
from tkinter import *                   # pip install tk or tkinter
from threading import Thread

########################### song play ##########################
songindex=0
counter=66600
flag=1
resume=0
breakre='unbreak'
volume=0.5
curr_time="00:00"
currenttime="00:00"
song_length=0
songlength="00:00"
songpause='unpause'
song_folder_path=None
end_recursion=False
except_flag_s=True
ss=0
flag_for=True
# creating music play function
def mus():
    global songindex
    global flag
    global volume
    global songlength
    global currenttime
    global songpause
    global song_folder_path
    global end_recursion
    global song_length
    global ss
    global flag_for
    global songs,list_song
    global Lb1
    
    try: # trying to play song
        while True:
            global counter
            # checking it is a valid path or not
            if ":\\" in song_folder_path:

                # getting songs directory and subfolder songs directory
                if flag_for==True:
                    flag_for=False
                    import os,re
                    list_path=[]
                    list_song = []
                    songs = []
                    list_l=[]
                    for i in song_folder_path:
                        if i!='*':
                            list_l.append(i)
                        else:
                            word=''.join(list_l)
                            list_l.clear()
                            list_path.append(word)
                    for path in list_path:
                        for root, dirs, files in os.walk(path, topdown=False):
                            for name in files:
                                if re.match('.*\.mp3',name.lower()) or re.match('.*\.wav',name.lower()):
                                    mp=os.path.join(root, name)
                                    list_song.append(mp)  # appending getted path
                                    n=0
                                    for i in range(-1,-len(mp),-1):
                                        if mp[i]!='\\':
                                            n+=1
                                        else:
                                            break
                                    songs.append(mp[len(mp)-n:])
                    
                # getting all files in user specified path
                String = songs[songindex]
                last3=str(String[-4:])

                # checking it is a mp3 or not
                if last3=='.mp3' or last3=='.MP3' or last3=='.wav' or last3=='.WAV':       
                    pygame.init() # installing pygame

                    # creating current time of song
                    tt = datetime.fromtimestamp(counter)
                    curtime=tt.strftime("%M%S")
                    currenttime=tt.strftime("%M:%S")        
                    z=int(curtime)

                    # getting song time length
                    try:
                        song_mut = MP3(list_song[songindex]) # for mp3 formate
                    except:
                        song_mut = WAVE(list_song[songindex]) # for wav formate
                    song_length = song_mut.info.length
                    converted_song_length = time.strftime('%M%S',time.gmtime(song_length))
                    songlength= time.strftime('%M:%S',time.gmtime(song_length))
                    x=int(converted_song_length)

                    # starting to load and play song
                    if flag<=1:
                        mixer.init() # installing mixer
                        mixer.music.load(list_song[songindex]) # loading song

                        # setting song title
                        try:
                            songname=songs[songindex]
                            canvas.itemconfig("marquee",text=songname)
                        except:
                            pass
                        mixer.music.set_volume(volume) # setting song volume
                        mixer.music.play() # playing song
                        flag+=1

                    # this condition work untill song current length equal to song length
                    if z<=x:
                        if songpause=='unpause':
                            counter+=1
                        time.sleep(1)

                    # this condition work when song current length greater_or_equal to song length
                    if z>=x:
                        songindex+=1 # increasing songs list index
                        counter=66600 # re_setting counter
                        ss=0 # re_setting ss
                        mixer.init() # installing mixer again
                        mixer.music.load(list_song[songindex]) # loading next song
                        # setting song title
                        try:
                            songname=songs[songindex]
                            canvas.itemconfig("marquee",text=songname)
                        except:
                            pass
                        mixer.music.play() # playing next song
                        # updating lb1 select position
                        try:
                            # clear all selection
                            Lb1.selection_clear(0, END)

                            # Activate new song bar
                            Lb1.activate(songindex)

                            # Set Active Bar to Next Song
                            Lb1.selection_set(songindex,None)
                        except:
                            pass
                        break

                else: # if there is any error it show error missage and play next song
                    if end_recursion!=True:
                        nextsong()
                    elif end_recursion==True:
                        if flag<=1:
                            flag+=1
                            canvas.itemconfig("marquee",text="there is no mp3 formate songs in your specified folder path") # showing error message in player
                    break
                break

            else: # if user specifed a in valid directory this get executed
                if flag<=1:
                    flag+=1
                    canvas.itemconfig("marquee",text="enter valid song folder path.") # showing error message in player
                time.sleep(2)
                break

    # if above try statement get faild and when it found 'FileNotFoundError' this except statement get executed
    except FileNotFoundError as fe:
        global except_flag_s
        if except_flag_s==True:
            canvas.itemconfig("marquee",text="enter valid song folder path.") # showing error message in player
            except_flag_s=False
        time.sleep(2)

    except Exception as e:
        nextsong()
        if except_flag_s==True:
            canvas.itemconfig("marquee",text="enter valid song folder path.") # showing error message in player
            except_flag_s=False
        time.sleep(2)

# when this function is executed, it stop re() function
def stopsong():
    global breakre
    breakre='break'

# this function is used to repetedly call mus() function
def re():
    global breakre
    global counter
    global flag
    global volume
    global songpause
    global songlength
    global currenttime
    global end_recursion
    global except_flag_s
    global ss

    songpause='unpause'
    end_recursion=False
    except_flag_s=True

    # this loop execute mus() function repetedly
    while True:
        global breakre
        #when you call stopsong() function this condiction get true 
        #and reset the below variable value then break the loop
        if breakre=='break':
            break
        mus()

# this function call next song to load and play  
song_found=0
def nextsong():
    global counter
    global songindex
    global volume
    global song_folder_path
    global song_found
    global end_recursion
    global ss
    global songs,list_song
    
    # trying to play next song
    try:
        songindex+=1 # increasing songs list index
        counter=66600 # resetting counter
        ss=0 # resetting ss

        # getting next song
        totalitem=len(songs)-1
        # when songs list totalitem equalto index songindex this condition get true and call first song
        if songindex>=totalitem:
            songindex=0
            if song_found==0:
                end_recursion=True
        String = songs[songindex]
        last3=str(String[-4:])
        
        
                
        # try to play next song
        try:
            # checking it is a mp3 or not
            if last3=='.mp3' or last3=='.MP3' or last3=='.wav' or last3=='.WAV':
                song_found+=1 
                mixer.init() # installing mixer again
                mixer.music.load(list_song[songindex]) # loading next song 

                # re_setting song title
                try:
                    songname=songs[songindex]
                    canvas.itemconfig("marquee",text=songname)
                except:
                    pass

                mixer.music.play() # playing next song
            else:
                if end_recursion!=True:
                    nextsong()

        except: # there is any error, this function call again 
            nextsong()

    # if above try statement get faild and when it found 'FileNotFoundError' this except statement get executed
    except: 
        pass
    

# this function call previous song to load and play  
def previoussong():
    global counter
    global songindex
    global volume
    global song_folder_path
    global song_found
    global end_recursion
    global ss
    global songs,list_song

    # trying to play previous song
    try:
        songindex-=1 # decreasing songs list index
        counter=66600 # resetting counter
        ss=0 # resetting
        
        # getting previous song
        totalitem=len(songs)-1
        minus_totalitem=int('-'+str(totalitem+1))

        # when songs list songindex smaller and equalto minus_totalitem index  this condition get true and call first song
        if songindex<=minus_totalitem:
            songindex=0
            if song_found==0:
                end_recursion=True
        String = songs[songindex]
        last3=str(String[-4:])

        # trying to play previous song
        try:
            # checking it is a mp3 or not
            if last3=='.mp3' or last3=='.MP3' or last3=='.wav' or last3=='.WAV':
                song_found+=1 
                mixer.init() # installing mixer again
                mixer.music.load(list_song[songindex]) # loading previous song 

                # re_setting song title
                try:
                    songname=songs[songindex]
                    canvas.itemconfig("marquee",text=songname)
                except:
                    pass

                mixer.music.play() # playing previous song 
            else:
                if end_recursion!=True:
                    previoussong()

        except: # there is any error, this function call again 
            previoussong()

    # if above try statement get faild and when it found 'FileNotFoundError' this except statement get executed
    except:
        pass


# this function pause the playing song   
def pause():
    global counter
    global resume
    global songpause
    songpause='pause'
    resume = counter
    try:
        mixer.music.pause() 
    except:
        pass

# this function unpause the paused song 
def unpause():
    global counter
    global resume
    global songpause
    songpause='unpause'
    if songpause=='pause':
        counter = resume
    try:
        mixer.music.unpause() 
    except:
        pass

# this function increase song volume
def volumeup():
    global volume
    global vol2
    if volume<1.0:
        volume=round(volume,1)
        volume+=0.1
        volume=round(volume,1)
        try:
            text1=int(volume*10)
            vol2.config(text=(text1))
        except:
            pass
        mixer.init()
        mixer.music.set_volume(volume)
    if volume>=1.0:
        pass
        
# this function decrease song volume
def volumedown():
    global volume
    global vol2
    if volume>0.0:
        volume=round(volume,1)
        volume-=0.1
        volume=round(volume,1)
        try:
            text1=int(volume*10)
            vol2.config(text=(text1))
        except:
            pass
        mixer.init()
        mixer.music.set_volume(volume)
       
    if volume<=0.0:
        volume=0.0

# this function set max volume
def max_volume():
    global volume
    global vol2
    volume=1.0

    # re_setting volume displayed in player
    try:
        text1=int(volume*10)
        vol2.config(text=(text1))
    except:
        pass

    mixer.init()
    mixer.music.set_volume(volume)

# this function set middle volume
def mid_volume():
    global volume
    global vol2
    volume=0.5

    # re_setting volume displayed in player
    try:
        text1=int(volume*10)
        vol2.config(text=(text1))
    except:
        pass

    mixer.init()
    mixer.music.set_volume(volume)

# this function set zero volume
def mute():
    global volume
    global vol2
    volume=0.0

    # re_setting volume displayed in player
    try:
        text1=int(volume)
        vol2.config(text=(text1))
    except:
        pass

    mixer.init()
    mixer.music.set_volume(volume)

######################## song play end #########################

######################### music player #########################

# creating music player window
flag_pause=0
def music_player():
    global canvas
    global root
    global songindex
    global volume
    global curr_time
    global songlength
    global vol2
    global time2
    global flag_button
    global curtime
    global song_length
    global counter
    
    # this finction run the song title from right to left again and again
    def shift():
        x1,y1,x2,y2 = canvas.bbox("marquee")
        if(x2<0 or y1<0): #reset the coordinates
            x1 = canvas.winfo_width()
            y1 = canvas.winfo_height()//2
            canvas.coords("marquee",x1,y1)
        else:
            canvas.move("marquee", -2, 0)
        canvas.after(1000//fps,shift)
    ############# Main program ###############
    root=Tk() 
    width1= root.winfo_screenwidth() # getting your computer screen with           
    height1= root.winfo_screenheight() # getting over computer screen height 
    x=width1-487
    y=height1-215
    root.geometry(f'+{int(x)}+{int(y)}') # setting position for music player   
    root.maxsize(height=133,width=466) # setting max size for player
    root.minsize(height=133,width=466) # setting min size for player
    root.title('mp3 and wav player') # creating player title
    root.iconbitmap("i.ico") # setting icon
    canvas=Canvas(root,bg='cyan3')

    # this function is used to get song folder path from user 
    def s_path():
        msg.itemconfig("welcome",text="❀ WELCOME ❀")
        # which function is used to change test 
        def textch():
            global song_folder_path
            paths2.destroy()
            song_folder_path=entry1.get(1.0,"end-1c")
            entry1.destroy()
            msg.itemconfig("welcome",text=" NOW PLAYING:")
            msg.config(bg="blue4",height=25,width=188) #420
            # calling re() function using thread 
            if __name__ == '__main__':
                Thread(target = re).start()

            # creating slider value change function
            def slide_ch():
                global counter
                global ss
                global songs,list_song
                
                try:
                    # configuring sl slider
                    rr=round(song_length)
                    sl.config(to=int(rr))

                    if ss!=0:
                        ss=sl.get()

                    
                    if counter==int(ss+66601):
                        sl.set(counter-66600)
                        ss=sl.get()

                    if counter!=int(ss+66600):
                        counter=int(ss+66600)
                        
                        String = songs[songindex]
                        last3=str(String[-4:])
                        if last3=='.mp3' or last3=='.MP3':
                            try:
                                mixer.init()
                                mixer.music.load(list_song[songindex])
                                mixer.music.play(start=counter-66600)
                            except:
                                pass
                    sl.after(200,slide_ch)
                except:
                    pass

            # creating song len slider
            sl = Scale(frame1, from_=0, to=200, orient=HORIZONTAL,showvalue=0,length=225,background="violet",borderwidth=2,
            highlightbackground="white",highlightthickness=2,troughcolor="yellow",sliderlength=15)     
            sl.set(0)
            sl.pack(side=LEFT)
            slide_ch()

        # creating test frame to get input from user 
        entry1=Text(frame1,bg='yellow',height=1,width=25)
        msg.config(bg="blue4",height=25,width=188)

        newpaths.destroy()

        # creating 'ok' button 
        paths2=Button(frame1,text="OK",font=("arial",10,"bold"),bg="brown",borderwidth=1,command=lambda:textch())
        paths2.pack(side=RIGHT)
        entry1.pack(side=LEFT)
    
    frame1=Frame(root)
    frame1.pack(side=TOP)
    msg = Canvas(frame1, bg="blue4",height=25,width=295)
    msg.create_text(0,0,text="❀❀❀ WELCOME ❀❀❀",font=('Algerian',19,'italic'),fill='red',tags="welcome",anchor='nw')
    msg.pack(side=LEFT)

    # when help button is clicked this function get executed 
    def help():
        frame1.pack_forget()
        frame2.pack_forget()
        canvas.pack_forget()
        frame3=Frame(root)
        frame3.pack(side=TOP)
        frame7=Frame(frame3)
        frame7.pack(side=BOTTOM,fill=BOTH)

        # creating help text label 
        help_text1=Label(frame3,font=("arial",11,"bold"), text="Ex path: D:\*C:\songs*(here '*' is a split operator to split path). To ", fg="black",bg='green')
        help_text1.pack(fill=BOTH)
        help_text1=Label(frame3,font=("arial",11,"bold"), text="enter path 'Click to enter path' button; NOTE: 1)this player include", fg="black",bg='green')
        help_text1.pack(fill=BOTH)
        help_text1=Label(frame3,font=("arial",11,"bold"), text="all the subfolder. 2)must enter '*' at end of the path.     ", fg="black",bg='green')
        help_text1.pack(fill=BOTH)
        help_text1=Label(frame3,font=("arial",11,"bold"), text="button-'>' pre song, '<' next song, 'play' play song, '+' rise vol,", fg="black",bg='green')
        help_text1.pack()
        help_text2=Label(frame3,font=("arial",11,"bold"), text="'-' low vol, '~' mute vol', 'pause' pause song        ", fg="black",bg='green')
        help_text2.pack(side=LEFT)
        help_text2=Label(frame7,font=("arial",1,"bold"), text="fhfhfhf", fg="black",bg='purple')
        help_text2.pack(fill=BOTH)
        
        # when info button is clicked this function get executed
        def infof():
            global songs,songindex,info1,Lb1,credit
            frame3.pack_forget()
            frame4=Frame(root)
            frame4.pack(fill=BOTH,side=TOP)
            try:
                totalitem=len(songs)-1
                songindex1=songindex
            except:
                totalitem="enter path"
                songindex1="enter path" #55
            info1=Label(frame4,width=49,font=("arial",10,"bold"), text=f" total song={totalitem}    ;    current song index={songindex1}", fg="black",bg='green',anchor=W)
            info1.pack(fill=BOTH,side=LEFT)
            def creditf():
                frame5.pack_forget()
                frame6.pack_forget()
                frame4.pack_forget()
                frame8=Frame(root)
                frame8.pack(fill=BOTH,side=TOP)
                info1=Label(frame8,width=49,font=("arial",12,"bold"), text="PRASANNA . K", fg="blue4",bg='cyan3',anchor=W)
                info1.pack(fill=BOTH)
                info2=Label(frame8,width=49,font=("arial",12,"bold"), text="STUDENT AT SAIRAM ENGINEERING COLLEGE CHENNAI", fg="blue4",bg='cyan3',anchor=W)
                info2.pack(fill=BOTH)
                info3=Label(frame8,width=49,font=("arial",12,"bold"), text="GITHUB > https://github.com/prasanna892?tab=stars", fg="blue4",bg='cyan3',anchor=W)
                info3.pack(fill=BOTH)
                info4=Label(frame8,width=49,font=("arial",12,"bold"), text="MAIL ID : k.prasannagh@gmail.com", fg="blue4",bg='cyan3',anchor=W)
                info4.pack(fill=BOTH)
                info5=Label(frame8,width=44,font=("arial",12,"bold"), text="LANGUAGE USED : PYTHON", fg="blue4",bg='cyan3',anchor=W)
                info5.pack(fill=BOTH,side=LEFT)

                def recall():
                    frame8.destroy()
                    frame9.destroy()
                    frame4.pack()
                    frame5.pack()
                    frame6.pack()

                cancelx2=Button(frame8,text=" X ",font=("arial",10,"bold"),bg="red",borderwidth=0,command=lambda:recall())
                cancelx2.pack(fill=BOTH,side=LEFT)
                frame9=Frame(root)
                frame9.pack(fill=BOTH,side=TOP)
                info6=Label(frame9,width=49,font=("arial",12,"bold"), fg="blue4",bg='purple',anchor=W)
                info6.pack(fill=BOTH)

            credit=Button(frame4,text="credit",font=("arial",10,"bold"),bg="gold",borderwidth=0,command=lambda:creditf())
            credit.pack(side=LEFT)
            frame5=Frame(root)
            frame5.pack(fill=BOTH,side=TOP)

            # creating song box
            Lb1 = Listbox(frame5,bg='black',fg='cyan3',selectbackground="blue",selectforeground="yellow",font=("arial",10,"bold"),width=63,height=5)
            Lb1.pack(side=LEFT)
            try:
                for i in range(len(songs)):
                    Lb1.insert(i,f"{i}) {songs[i]}")
                
                def go(event):
                    global songindex,counter,ss
                    cs = Lb1.curselection()
                    
                    # playing selected music
                    for index in cs:
                        songindex=index
                        counter=int(66600)
                        ss=0
                        # re_setting song title
                        try:
                            songname=songs[songindex]
                            canvas.itemconfig("marquee",text=songname)
                        except:
                            pass
                        mixer.init()
                        mixer.music.load(list_song[int(index)])
                        mixer.music.play()
                    
                # Activate new song bar
                Lb1.activate(songindex)

                # Set Active Bar to Next Song
                Lb1.selection_set(songindex,None)

                Lb1.bind('<Double-1>', go)
                Lb1.bind('<Return>', go)
            except:
                Lb1.insert(1,"enter path")
    
            # setting vertical scrollbar to song box
            scrollbar = Scrollbar(frame5)
            scrollbar.pack(side = RIGHT, fill = BOTH)
            Lb1.config(yscrollcommand = scrollbar.set)
            scrollbar.config(command = Lb1.yview)

            # setting horizontal scrollbar to song box
            frame6=Frame(root)
            frame6.pack(fill=BOTH,side=BOTTOM)
            scrollbar = Scrollbar(frame6,orient=HORIZONTAL,bg="purple")
            scrollbar.pack(fill=BOTH,side=BOTTOM)
            Lb1.config(xscrollcommand = scrollbar.set)
            scrollbar.config(command = Lb1.xview)
            
            def recall():
                frame4.destroy()
                frame5.destroy()
                frame6.destroy()
                frame3.pack()

            cancelx1=Button(frame4,text=" X ",font=("arial",10,"bold"),bg="red",borderwidth=0,command=lambda:recall())
            cancelx1.pack(fill=BOTH,side=RIGHT)

        info=Button(frame3,text="MORE INFO",font=("arial",10,"bold"),bg="yellow",borderwidth=0,command=lambda:infof())
        info.pack(side=LEFT)


        # when cancel button is clicked this function get executed  
        def recall():
            canvas.pack_forget()
            frame1.pack()
            canvas.pack(fill=BOTH, expand=1)
            frame2.pack()
            frame3.destroy()

        # creating cancel 'X' button 
        cancelx=Button(frame3,text=" X ",font=("arial",10,"bold"),bg="red",borderwidth=0,command=lambda:recall())
        cancelx.pack(side=LEFT)

    # creating 'help' button 
    helps=Button(frame1,text="help",font=("arial",10,"bold"),bg="brown",borderwidth=1,command=lambda:help())
    helps.pack(side=RIGHT)

    # creating 'new path' button 
    newpaths=Button(frame1,text="Click to enter path",font=("arial",10,"bold"),bg="red",borderwidth=1,command=lambda:s_path())
    newpaths.pack(side=RIGHT)

    # creating some information label to display
    canvas.pack(fill=BOTH, expand=1)
    canvas.create_text(0,-2000,text="Enter song folder path",font=('Bauhaus 93',50,'bold'),fill='saddle brown',tags=("marquee",),anchor='w')
    frame2=Frame(root)
    frame2.pack(side=BOTTOM)
    vol1= Label(frame2, font=("arial",13,"bold"), text=(" volume:"), fg="black",bg='green') 
    text1=int(volume*10)
    vol2= Label(frame2, font=("arial",13,"bold"), text=(text1), fg="black",bg='green')
    flag_gap=Label(frame2,font=("arial",13,"bold"), text=("     "), fg="black",bg='green')
    time1= Label(frame2, font=("arial",13,"bold"), text=("    time elapsed:"), fg="black",bg='green')
    text2=f"{curr_time}/{songlength}"
    time2= Label(frame2, font=("arial",13,"bold"), text=(text2), fg="black",bg='green')

    # creating previous song button 
    previouss=Button(frame2,text="<",font=("arial",10,"bold"),bg="gold",borderwidth=0, command=lambda:previoussong())
    previouss.pack(side=LEFT)

    # creating volume up button 
    volups=Button(frame2,text="+",font=("arial",10,"bold"),bg="gold",borderwidth=0, command=lambda:volumeup())
    volups.pack(side=LEFT)

    # when pause button is clicked this function get executed 
    def play_s():
        pause()
        pauses.pack_forget()

        # when play button is clicked this function get executed 
        def playes():
            unpause()
            plays.destroy()
            pauses.pack()
        plays=Button(frame2,text=" play",font=("arial",10,"bold"),bg="gold",borderwidth=0, command=lambda:playes())
        plays.pack(side=RIGHT)

    # creating volume mute button
    volmutes=Button(frame2,text="~",font=("arial",10,"bold"),bg="gold",borderwidth=0, command=lambda:mute())
    volmutes.pack(side=LEFT)

    # creating pause button 
    pauses=Button(frame2,text="pause",font=("arial",10,"bold"),bg="gold",borderwidth=0, command=lambda:play_s())

    # creating volume decrease button  
    voldowns=Button(frame2,text="-",font=("arial",10,"bold"),bg="gold",borderwidth=0, command=lambda:volumedown())
    voldowns.pack(side=LEFT)

    # creating next song button 
    nexts=Button(frame2,text=">",font=("arial",10,"bold"),bg="gold",borderwidth=0, command=lambda:nextsong())
    nexts.pack(side=LEFT)

    pauses.pack(side=LEFT)

    frame4=Frame(frame2)
    frame4.pack(side=RIGHT)

    # packing some buttons and labels 
    time2.pack(side=RIGHT)
    time1.pack(side=RIGHT)
    flag_gap.pack(side=RIGHT)
    vol2.pack(side=RIGHT)
    vol1.pack(side=RIGHT)

    # setting convex width and height 
    x1,y1,x2,y2 = canvas.bbox("marquee")
    #width = x2-x1
    height = y2-y1
    canvas['width']=300
    canvas['height']=height   
    fps=45    #Change the fps to make the animation faster/slower
    shift() # calling shift() function 

    # reacting song time function 
    # this function repeatedly update the song current time and song length 
    def songtime():
        global info1,Lb1

        # updating time and song index
        try:
            totalitem=len(songs)-1
            songindex1=songindex
            try:
                credit.destroy()
            except:
                pass
            info1.config(width=55,text=f"total song={totalitem} ; current song index={songindex1} ; time elapsed-> {currenttime}/{songlength}")
        except:
            pass
        
        text2=f"{currenttime}/{songlength}"
        time2.config(text=(text2))  
        time2.after(100,songtime)
    songtime() # calling songtime() function

    # closeing main loop
    def re2():
        def on_closing():
            stopsong()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.after(100,re2)
    re2()
    root.mainloop()
    
# clling main function
music_player()