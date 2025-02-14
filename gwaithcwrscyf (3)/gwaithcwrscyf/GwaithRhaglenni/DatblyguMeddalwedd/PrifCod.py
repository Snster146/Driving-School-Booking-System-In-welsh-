#mewnbynnu yr holl llyfgelloedd sy'n hanofodol er mwyn ir rhaglen gweithredu
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import customtkinter
import sqlite3
import random
from MakeWindowClass import MakeWindow

#gosod yr holl cronfeydd data sydd angen er mwyn storio yr holl data a
CustomerDataBase=sqlite3.connect("customers.db")
DriverDatabase=sqlite3.connect("drivers.db")
Revisiondatabase = sqlite3.connect("revision.db")
bookingsdatabase = sqlite3.connect("bookings.db")
ReceptionistDataBase = sqlite3.connect("Receptionist.db")
YmholiDataBase = sqlite3.connect("Ymholi.db")

#gosod 'Cursor' er mwyn cael mynediad ac cyflawni gweithrediadau ar yr cronfeydd 
CustomerCursor=CustomerDataBase.cursor()
DriverCursor=DriverDatabase.cursor()
RevisionCursor = Revisiondatabase.cursor()
BookingsCursor = bookingsdatabase.cursor()
ReceptionistCursor = ReceptionistDataBase.cursor()
YmholiCursor = YmholiDataBase.cursor()

#creu tabl cwsmeriaiad , sy'n cynnwys meysydd isod  er mwyn sicrhau lefelau mynediad
CustomerCursor.execute("""CREATE TABLE IF NOT EXISTS CustomersTable(
                       
                       CustomerID TEXT PRIMARY KEY,
                       Username TEXT,
                       Password TEXT,
                       Name TEXT,
                       Surname TEXT,
                       Credit INT,
                       CwestiwnGwireddu TEXT,
                       AtebGwireddu TEXT

) """)
#creu tabl gyrrwr , sy'n cynnwys meysydd isod 
DriverDatabase.execute("""CREATE TABLE IF NOT EXISTS DriversTable(
                       
                       DriversID TEXT PRIMARY KEY,
                       Username TEXT,
                       Password TEXT,
                       Name TEXT,
                       Surname TEXT,
                       Confirmed TEXT,
                       CwestiwnGwireddu TEXT,
                       AtebGwireddu TEXT

)  """)
#creu tabl adolygu , sy'n cynnwys meysydd isod 
RevisionCursor.execute("""CREATE TABLE IF NOT EXISTS RevisionTable(
                       
                       RevisionID TEXT PRIMARY KEY,
                       Question TEXT,
                       CorrectAnswer TEXT,
                       WrongAnswerOne TEXT,
                       WrongAnswerTwo TEXT,
                       WrongAnswerThree TEXT,
                       Catogry TEXT

)  """)
#creu tabl bwciadau , sy'n cynnwys meysydd isod 
BookingsCursor.execute("""CREATE TABLE IF NOT EXISTS BookingsTable(
                        BookingID TEXT PRIMARY KEY,
                        Date TEXT,
                        TypeOfBooking TEXT,
                        CustomerID INTEGER,
                        DriverID INTEGER,
                        Status TEXT,
                        WediGorffen TEXT
)""")
#creu tabl derbynydd , sy'n cynnwys meysydd isod 
ReceptionistCursor.execute("""CREATE TABLE IF NOT EXISTS ReceptionistTable(
                           
                           ReceptionistID TEXT PRIMARY KEY,
                           Username TEXT,
                           Password TEXT,
                           Name TEXT,
                           Surname TEXT,
                           CwestiwnGwireddu TEXT,
                           AtebGwireddu TEXT
)  """)
#creu tabl ymholi , sy'n cynnwys meysydd isod 
YmholiCursor.execute("""CREATE TABLE IF NOT EXISTS YmholiTable(
                     
                     YmholiadID TEXT PRIMARY KEY,
                     Neges TEXT,
                     CustomerID TEXT,
                     DriverID TEXT,
                     ReceptionistID TEXT,
                     SentFrom TEXT,
                     Status TEXT


)   """)

#gosod ffurfln customrkitner
root = customtkinter.CTk()
#gosod 'apperenece' yr ffurflen i 'dark' er mwyn sicrhau apel cyson ac greddfol rhwng ffurflenni
root._set_appearance_mode("dark")

#cymeriadau arbennig , angen ar gyfer dilysu cyfrinair
special_characters = "!,£,$,%,^,&,*,(,),-,_,+,=,/,-,+,<,>,?,|"

def AddVerification(userid):
    global VerificationQuestionPage
    UserQuestion=VerificationQuestionPage.get_combo_value("Beth yw enw eich hoff film?")
    UserAnswer=VerificationQuestionPage.get_entry_value("Eich Ateb")
    if UserAnswer=="":
        messagebox.showinfo("Gwall","Rhaid mewnbynnu ateb ir cwestiwn gwireddu")
        return
   
    CustomerCursor.execute("SELECT Name FROM CustomersTable WHERE CustomerID = ?",(userid,))
    IsCustomer=CustomerCursor.fetchone()
    CustomerDataBase.commit()
    if IsCustomer:
        CustomerCursor.execute("UPDATE CustomersTable SET CwestiwnGwireddu = ?, AtebGwireddu = ? WHERE CustomerID =? ", (UserQuestion,UserAnswer,userid,))
        messagebox.showinfo("Llwyddiant","Mae'r cyfrif wedi cael ei creu !")
        CustomerDataBase.commit()
       
        LoginPage()


    DriverCursor.execute("SELECT Name FROM DriversTable WHERE DriversID = ?",(userid,))
    IsDriver=DriverCursor.fetchone()
    DriverDatabase.commit()
    if IsDriver:
        DriverCursor.execute("UPDATE DriversTable SET CwestiwnGwireddu = ?, AtebGwireddu = ? WHERE DriversID =? ",(UserQuestion,UserAnswer,userid),)
        messagebox.showinfo("Llwyddiant","Mae'r cyfrif wedi cael ei creu !")
        DriverDatabase.commit()
        
        LoginPage()



def CreateAccountValidation():
    global CreateAccountWindow 
    global VerificationQuestionPage
    Valid =True
    digitCount=0
    SpecialCharacterCount=0
    Name = CreateAccountWindow.get_entry_value("Name")
    Surname = CreateAccountWindow.get_entry_value("Surname")
    Username = CreateAccountWindow.get_entry_value("Username")
    Password = CreateAccountWindow.get_entry_value("Password")
    EntranceLevel = CreateAccountWindow.get_combo_value("Driver")

#dilysu presenoldeb ar holl meysydd
    if Username=="" or Password=="" or DateOfBirth=="" or Name =="" or Surname =="":
        messagebox.showinfo("Gwall","rhaid llenwi holl meysydd!!!")
        Valid=False
        return
#dilysu hyd
    elif len (Username)<10:
        messagebox.showinfo("Gwall","Rhaid ir enw defnyddiwr cynnwys o leiaf 10 cymeriad!!!")
        Valid=False
        return
    elif len(Password)<12:
        messagebox.showinfo("Gwall","Rhaid ir cyfrianir cynnwys o leiaf 12 cymeriad!!!")
        Valid=False
        return
#dilysu math

    for item in Password:
        if item.isdigit()==True:
            digitCount+=1
    for item in Password:
        if item in special_characters:
            SpecialCharacterCount+=1
    if digitCount<3:
        messagebox.showinfo("Gwall","Rhaid ir cyfinair cynnwys o leiaf tair digid !!!!")
        Valid=False
        return
    elif SpecialCharacterCount<2:
        messagebox.showinfo("Gwall","Rhaid ir cyfrianir cynnwys o leiaf dau cymeriad arbennig!!!")
        Valid=False
        return
    digitCount=0
    SpecialCharacterCount=0
    
    for item in Name:
        if item.isdigit()==True:
            digitCount+=1
            
    for item in Name:
        if item in special_characters:
            SpecialCharacterCount+=1
    if digitCount>0:
        messagebox.showinfo("Gwall","Ni dylai enw cynnwys digiadau")
        Valid=False
        return
    elif SpecialCharacterCount>0:
        messagebox.showinfo("Gwall","Ni dylai enw cynnwys cymeriadau arbennig")
        Valid=False
        return
    digitCount=0
    SpecialCharacterCount=0
    
    for item in Surname:
        if item.isdigit()==True:
            digitCount+=1
    for item in Surname:
        if item in special_characters:
            SpecialCharacterCount+=1   

    if digitCount>0:
        messagebox.showinfo("Gwall","Ni dylai cyfenw cynnwys digidau")
        Valid=False
        return
    elif SpecialCharacterCount>0:
        messagebox.showinfo("Gwall","Ni dylai cyfenw cynnwys cymeriadau arbennig")
        Valid=False
        return
        

    if Valid==False:
        CreateAccount()
    else:

        if EntranceLevel =="Customer":
            CustomerCursor.execute("SELECT CustomerID FROM CustomersTable ORDER BY CustomerID DESC LIMIT 1")
            last_customer_id = CustomerCursor.fetchone()

#os oes fwy nag un rhes yn yr tabl cwsmeriaid fydd yr customerid yr cwsmer newydd syn cael ei creu yn 1 fwy na customerid yr cwsmer fwyaf diweddar
            if last_customer_id:
                last_customer_id=last_customer_id[0]
                customerid=int(last_customer_id)+1
            else:
                customerid=1

#mewnbynnu holl manylion yr defnyddiwr mewn i tabl cwsmeriaid er mwyn creu cyfrif 'cwsmer' newydd
            CustomerCursor.execute("INSERT INTO CustomersTable VALUES (? ,?, ?, ?, ?,?,?,?)",
                                  (customerid,Username, Password, Name,
                                    Surname,0,None,None))
            CustomerDataBase.commit()

            VerificationQuestionPageElements=[["Label","Ysgol Moduro Normansell","Century Gothic",45,"White"],
                                              ["Label","Dewiswch cwestiwn gwireddu","Arial",18,"White"],
                                              ["ComboBox","Beth yw enw eich hoff film?","Beth yw enw eich anifail anwes cyntaf ?","Yn pa dinas cawsoch eich geni ? "],
                                              ["Label","Mewnbynnwch ateb ir cwestiwn gwireddu","Arial",18,"White"],
                                              ["EntryBox","Eich Ateb",500,50],
                                              ["Button","Enter","Monaco",18,"Green",lambda: AddVerification(customerid)]
                                              ]
            for Widget in root.winfo_children():
                Widget.destroy()
            VerificationQuestionPage=MakeWindow(root,"Creu Cwestiwn gwireddu",VerificationQuestionPageElements)


        elif EntranceLevel =="Driver":
            DriverCursor.execute("SELECT DriversID FROM DriversTable ORDER BY DriversID DESC LIMIT 1")
            last_driver_id = DriverCursor.fetchone()

#os oes fwy nag un rhes yn yr tabl cwsmeriaid fydd yr customerid yr cwsmer newydd syn cael ei creu yn 1 fwy na customerid yr cwsmer fwyaf diweddar
            if last_driver_id:
                last_driver_id=last_driver_id[0]
                driverid=int(last_driver_id)+1
            else:
                driverid=1


#mewnbynnu holl manylion yr defnyddiwr mewn i tabl cwsmeriaid er mwyn creu cyfrif 'cwsmer' newydd
            DriverCursor.execute("INSERT INTO DriversTable VALUES (? ,?, ?, ?, ?,?,?,?)",
                                   (driverid,Username, Password, Name,
                                    Surname,0,None,None))
            DriverDatabase.commit()
            

            VerificationQuestionPageElements=[["Label","Ysgol Moduro Normansell","Century Gothic",45,"White"],
                                              ["Label","Dewiswch cwestiwn gwireddu","Arial",18,"White"],
                                              ["ComboBox","Beth yw enw eich hoff film?","Beth yw enw eich anifail anwes cyntaf ?","Yn pa dinas cawsoch eich geni ? "],
                                              ["Label","Mewnbynnwch ateb ir cwestiwn gwireddu","Arial",18,"White"],
                                              ["EntryBox","Eich Ateb",500,50],
                                              ["Button","Enter","Monaco",18,"Green",lambda: AddVerification(driverid)]
                                              ]
            for Widget in root.winfo_children():
                Widget.destroy()
            VerificationQuestionPage=MakeWindow(root,"Creu Cwestiwn gwireddu",VerificationQuestionPageElements)
        


def CreateAccount():
    global CreateAccountWindow
    for widget in root.winfo_children():
        widget.destroy()

    CreateAccountElements = [["Label", "Creu Cyfrif", "Century Gothic", 24, "white"],
                         ["Label","Mewnbynnu manylion yr cyfrif i creu","Arial",12,"White"],
                         ["EntryBox","Name",200,30],
                         ["Button","Clear","Monaco",12,"#DF5836",lambda: clear("Username")],
                         ["EntryBox","Surname",200,30],
                         ["Button","Clear","Monaco",12,"#DF5836",lambda: clear("Username")],
                         ["EntryBox","Username",200,30],
                         ["Button","Clear","Monaco",12,"#DF5836",lambda: clear("Username")],
                         ["EntryBox","Password",200,30],
                         ["Label","Choose your status using the drop down box below","Arial",16,"White"],
                         ["Button","Clear","Monaco",12,"#DF5836",lambda: clear("00/00/0000")],
                         ["ComboBox", "Driver", "Customer", "Receptionist"],
                         ["Button","Enter","Monaco",12,"green",lambda: CreateAccountValidation()],
                         ["Button","Catref","Monaco",12,"Red",lambda: LoginPage()]
                     
                     ]
    
    CreateAccountWindow = MakeWindow(root,"Create Account",CreateAccountElements)

def RevisionQuestions(userid,Lefelmynediad,NiferCwestiynnau,CatogriCwestiynnau):

    

    if NiferCwestiynnau=="":
        messagebox.showinfo("Adolygu","Rhaid dewis Menwbwn ar gyfer nifer o cwestiynnau")
        CatogriAndQuestionSelecterForRevision(userid,Lefelmynediad)
        return
    elif CatogriCwestiynnau=="":
        messagebox.showinfo("Adolygu","Rhaid dewis mewnbwn ar gyfer catogri")
        CatogriAndQuestionSelecterForRevision(userid,Lefelmynediad)
        return

    if NiferCwestiynnau != "10" and NiferCwestiynnau != "20" and NiferCwestiynnau != "30" and NiferCwestiynnau != "40":
        messagebox.showinfo("Gwall","Rhaid ir nifer o cwestiynnau for yn 10,20,30 neu 40 !")
        return
    if CatogriCwestiynnau !="Alertness" and CatogriCwestiynnau !="Attitude" and CatogriCwestiynnau !="Hazard awarness" and CatogriCwestiynnau !="Motorway rules":
        messagebox.showinfo("Gwall","Rhaid ir catogri fod yn Alertness, Attitude,Hazard awarness neu motorway rules")
        return

    RevisionCursor.execute("SELECT Question FROM RevisionTable WHERE Catogry = ?",(CatogriCwestiynnau,)) # selects questions from catogry that user inputted into variable catogrytorevise
    SelectedQuestions=RevisionCursor.fetchall()
    Revisiondatabase.commit()
    global counter
    counter=1
    #score yn cynyddu gan 1 os ywr defnyddiwr yn cael ateb gywir , dim yn cynyddu os nad yw'r defnyddiwr yn cael ateb yn gywir
    global score
    score=0

    for Widget in root.winfo_children():
        Widget.destroy()
    
    def Dewis(Ateb):
        global score
        print(Ateb)
        try:
            if int(Ateb)-1 == CorrectIndex:
                score += 1
        except ValueError:
            pass
        if score != NiferCwestiynnau:
            scoreLabel.configure(text=f"Eich scor {score} / {counter-1}")  
            # Check if DewisEntry exists and is not None before attempting deletion
            if DewisEntry is not None:
                DewisEntry.delete(0, END)
        Cwestiwn(userid, Lefelmynediad)


   
    def DiweddCwestiynnau(score,NiferCwestiynnau,userid,LefeMynediad):
        for Widget in root.winfo_children():
            Widget.destroy()
        root.title("Diwedd cwestiynnau adolygu")
        
        frame=customtkinter.CTkFrame(root,fg_color="#8692F5", bg_color="#8692F5")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        customtkinter.CTkLabel(frame,text="Ysgol Moduro Normansell",font=("Century Gothic",45),text_color="White").pack()
        customtkinter.CTkLabel(frame,text="Eich sgor",font=("Roboto",36),text_color="White").pack()

        customtkinter.CTkLabel(frame,text=f"{score} / {NiferCwestiynnau}",font=("Roboto",24),text_color="Blue").pack()
        
        print(f"IRNOR {NiferCwestiynnau} NIFEERCWESESIYNNAU")
        print()
        print(f"SCORIOANI {score}")

        if int(NiferCwestiynnau)==10:
            if score>=8:
                customtkinter.CTkLabel(frame,text="Rydych wedi pasio",font=("Roboto",24),text_color="Green").pack()
            else:
                customtkinter.CTkLabel(frame,text="Nid ydych wedi pasio",font=("Roboto",24),text_color="Red").pack()
        elif NiferCwestiynnau==20:
            if score>=8:
                customtkinter.CTkLabel(frame,text="Rydych wedi pasio",font=("Roboto",24),text_color="Green").pack()
            else:
                customtkinter.CTkLabel(frame,text="Nid ydych wedi pasio",font=("Roboto",24),text_color="Red").pack()
        elif NiferCwestiynnau==30:
            if score>=8:
                customtkinter.CTkLabel(frame,text="Rydych wedi pasio",font=("Roboto",24),text_color="Green").pack()
            else:
                customtkinter.CTkLabel(frame,text="Nid ydych wedi pasio",font=("Roboto",24),text_color="Red").pack()

        if Lefelmynediad=="Cwsmer":
            BotwmCatref=customtkinter.CTkButton(frame,text="Catref",font=("Monaco",18),fg_color="Green",command=lambda: CustomerHomePage(userid))
            BotwmCatref.pack()
        elif Lefelmynediad=="Gyrrwr":
            BotwmCatref=customtkinter.CTkButton(frame,text="Catref",font=("Monaco",18),fg_color="Green",command=lambda: DriversHomePage(userid))
            BotwmCatref.pack()
        BotwmCatrefAdolygu=customtkinter.CTkButton(frame,text="Adolygu eto",font=("Monaco",18),fg_color="Red",command=lambda: CatogriAndQuestionSelecterForRevision(userid,Lefelmynediad))
        BotwmCatrefAdolygu.pack()

    def Cwestiwn(userid, LefelMynediad):
        global counter
        if int(counter) < int(NiferCwestiynnau):
            randoms = random.randint(0, len(SelectedQuestions) - 1)  # Adjusted range
            question = SelectedQuestions[randoms][0]
            print()
            CwestiwnLabel.configure(text=f"{counter}) {question}")
            print()
            counter += 1
            RevisionCursor.execute("SELECT CorrectAnswer, WrongAnswerOne, WrongAnswerTwo, WrongAnswerThree FROM RevisionTable WHERE Question = ?", (question,))
            Answers = RevisionCursor.fetchall()

            CorrectAnswer = Answers[0][0]
            WrongAnswers = [Answers[0][1], Answers[0][2], Answers[0][3]]

            AnswerList = [CorrectAnswer] + WrongAnswers
            random.shuffle(AnswerList)

            global CorrectIndex
            CorrectIndex = AnswerList.index(CorrectAnswer)

        # Print options and get user's answer
            for j in range(len(AnswerList)):
                AnswerLabels[j].configure(text=f"{j+1}. {AnswerList[j]}")
        else:
            DiweddCwestiynnau(score, NiferCwestiynnau, userid, Lefelmynediad)



    root.title("Cwestiynnau Adolygu")
    root.geometry("1000x750")

    frame=customtkinter.CTkFrame(root,fg_color="#8692F5", bg_color="#8692F5")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    customtkinter.CTkLabel(frame,text="Ysgol Moduro Normansell",font=("Century Gothic",24),text_color="White").pack()
    customtkinter.CTkLabel(frame,text="Adolygu Theori",font=("Roboto",24),text_color="White").pack()
    

    global scoreLabel
    scoreLabel=customtkinter.CTkLabel(frame,text="",font=("Arial",18),text_color="White")
    scoreLabel.pack(pady=25)

    customtkinter.CTkLabel(frame,text="Cwestiwn : ",font=("Arial",18),text_color="White").pack()

    CwestiwnLabel=customtkinter.CTkLabel(frame,text="",font=("Arial",18),text_color="White")
    CwestiwnLabel.pack(pady=25)

    customtkinter.CTkLabel(frame,text="Atebion :",font=("Arial",18),text_color="White").pack()

    AtebCywirLabel=customtkinter.CTkLabel(frame,text="",font=("Arial",18),text_color="White")
    AtebCywirLabel.pack(pady=15)
    AtebAnghywir1Label=customtkinter.CTkLabel(frame,text="",font=("Arial",18),text_color="White")
    AtebAnghywir1Label.pack(pady=15)
    AtebAnghywir2Label=customtkinter.CTkLabel(frame,text="",font=("Arial",18),text_color="White")
    AtebAnghywir2Label.pack(pady=15)
    AtebAnghywir3Label=customtkinter.CTkLabel(frame,text="",font=("Arial",18),text_color="White")
    AtebAnghywir3Label.pack(pady=15)

    customtkinter.CTkLabel(frame,text="Mewnbynnwch ateb",font=("Arial",18)).pack()

    DewisEntry = customtkinter.CTkEntry(frame, placeholder_text="",width=200,height=20)
    DewisEntry.pack(pady=15)

    CadarnhauButton = customtkinter.CTkButton(frame, text="Cadarnhau", font=("Monaco", 18), fg_color="Green",
                                                      command=lambda: Dewis(DewisEntry.get()))
    CadarnhauButton.pack()

    root.bind('<Return>', lambda event: CadarnhauButton.invoke())


    AnswerLabels=[AtebCywirLabel,AtebAnghywir1Label,AtebAnghywir2Label,AtebAnghywir3Label]

    Cwestiwn(userid,Lefelmynediad)
                            

def ffugPrawf(userid,LefelMynediad):


    for Widget in root.winfo_children():
        Widget.destroy()


    RevisionCursor.execute("SELECT Question FROM RevisionTable") # selects questions from catogry that user inputted into variable catogrytorevise
    SelectedQuestions=RevisionCursor.fetchall()
    Revisiondatabase.commit()
    global counter
    counter=1
    #score yn cynyddu gan 1 os ywr defnyddiwr yn cael ateb gywir , dim yn cynyddu os nad yw'r defnyddiwr yn cael ateb yn gywir
    global score
    score=0

    
    def DewisFfugPrawf(Ateb):
        global score
        global scoreLabel
        print(Ateb)
        if int(Ateb)-1 == CorrectIndex:
            score+=1
        scoreLabel.configure(text=f"Eich scor {score} / {counter}")   
        CwestiwnFfugPrawf(userid,LefelMynediad)

    def DiweddCwestiynnauFfugPrawf(score,NiferCwestiynnau,userid,LefelMynediad):
        for Widget in root.winfo_children():
            Widget.destroy()
        root.title("Diwedd ffug prawf ")
        
        frame=customtkinter.CTkFrame(root,fg_color="#8692F5", bg_color="#8692F5")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        customtkinter.CTkLabel(frame,text="Ysgol Moduro Normansell",font=("Century Gothic",45),text_color="White").pack()
        customtkinter.CTkLabel(frame,text="Eich sgor",font=("Roboto",36),text_color="White").pack()

        customtkinter.CTkLabel(frame,text=f"{score} / 50",font=("Roboto",24),text_color="Blue").pack()
        
      

        if score>=55:
            customtkinter.CTkLabel(frame,text="Rydych wedi pasio",font=("Roboto",24),text_color="Green").pack()
        else:
            customtkinter.CTkLabel(frame,text="Nid ydych wedi pasio",font=("Roboto",24),text_color="Red").pack()
       
        if LefelMynediad=="Cwsmer":
            BotwmCatref=customtkinter.CTkButton(frame,text="Catref",font=("Monaco",18),fg_color="Green",command=lambda: CustomerHomePage(userid))
            BotwmCatref.pack()
        elif LefelMynediad=="Gyrrwr":
            BotwmCatref=customtkinter.CTkButton(frame,text="Catref",font=("Monaco",18),fg_color="Green",command=lambda: DriversHomePage(userid))
            BotwmCatref.pack()
        BotwmCatrefAdolygu=customtkinter.CTkButton(frame,text="Adolygu eto",font=("Monaco",18),fg_color="Red",command=lambda: CatogriAndQuestionSelecterForRevision(userid,LefelMynediad))
        BotwmCatrefAdolygu.pack()

    def CwestiwnFfugPrawf(userid,LefelMynediad):
        global counter
        if int(counter) < 50:
            randoms = random.randint(1, len(SelectedQuestions) - 1)
            question = SelectedQuestions[randoms][0]
            print()
            CwestiwnLabel.configure(text=f"{counter}) {question}")
            print()
            counter += 1
            RevisionCursor.execute("SELECT CorrectAnswer, WrongAnswerOne, WrongAnswerTwo, WrongAnswerThree FROM RevisionTable WHERE Question = ?", (question,))
            Answers = RevisionCursor.fetchall()

            CorrectAnswer = Answers[0][0]
            WrongAnswers = [Answers[0][1], Answers[0][2], Answers[0][3]]

            AnswerList = [CorrectAnswer] + WrongAnswers
            random.shuffle(AnswerList)

            global CorrectIndex
            CorrectIndex = AnswerList.index(CorrectAnswer)

            # Print options and get user's answer
            for j in range(len(AnswerList)):
                AnswerLabels[j].configure(text=f"{j+1}. {AnswerList[j]}")
        else:
            DiweddCwestiynnauFfugPrawf(score,50,userid,LefelMynediad)


    root.title("Ffug Prawf")
    root.geometry("1000x750")

    frame=customtkinter.CTkFrame(root,fg_color="#8692F5", bg_color="#8692F5")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    customtkinter.CTkLabel(frame,text="Ysgol Moduro Normansell",font=("Century Gothic",24),text_color="White").pack()
    customtkinter.CTkLabel(frame,text="Ffug Prawf",font=("Roboto",24),text_color="White").pack()
    

    global scoreLabel
    scoreLabel=customtkinter.CTkLabel(frame,text="",font=("Arial",18),text_color="White")
    scoreLabel.pack(pady=25)

    customtkinter.CTkLabel(frame,text="Cwestiwn : ",font=("Arial",18),text_color="White").pack()

    CwestiwnLabel=customtkinter.CTkLabel(frame,text="",font=("Arial",18),text_color="White")
    CwestiwnLabel.pack(pady=25)

    customtkinter.CTkLabel(frame,text="Atebion :",font=("Arial",18),text_color="White").pack()

    AtebCywirLabel=customtkinter.CTkLabel(frame,text="",font=("Arial",18),text_color="White")
    AtebCywirLabel.pack(pady=15)
    AtebAnghywir1Label=customtkinter.CTkLabel(frame,text="",font=("Arial",18),text_color="White")
    AtebAnghywir1Label.pack(pady=15)
    AtebAnghywir2Label=customtkinter.CTkLabel(frame,text="",font=("Arial",18),text_color="White")
    AtebAnghywir2Label.pack(pady=15)
    AtebAnghywir3Label=customtkinter.CTkLabel(frame,text="",font=("Arial",18),text_color="White")
    AtebAnghywir3Label.pack(pady=15)

    customtkinter.CTkLabel(frame,text="Mewnbynnwch ateb",font=("Arial",18)).pack()

    DewisEntry = customtkinter.CTkEntry(frame, placeholder_text="",width=200,height=20)
    DewisEntry.pack(pady=15)

    CadarnhauButton = customtkinter.CTkButton(frame, text="Cadarnhau", font=("Monaco", 18), fg_color="Green",
                                                      command=lambda: DewisFfugPrawf(DewisEntry.get()))
    CadarnhauButton.pack()

    root.bind('<Return>', lambda event: CadarnhauButton.invoke())

    AnswerLabels=[AtebCywirLabel,AtebAnghywir1Label,AtebAnghywir2Label,AtebAnghywir3Label]

    CwestiwnFfugPrawf(userid,LefelMynediad)


      
def CatogriAndQuestionSelecterForRevision(userid,LefelMynediad):
    for Widget in root.winfo_children():
        Widget.destroy()

    root.title("Dewis opsiynnau adolygu")
    root.geometry("1000x750")
    frame=customtkinter.CTkFrame(root,fg_color="#8692F5", bg_color="#8692F5")
    frame.pack(fill="both", expand=True, padx=20, pady=20)
    customtkinter.CTkLabel(frame,text="Ysgol Moduro Normanell",font=("Century Gothic",45),text_color="White").pack()
    customtkinter.CTkLabel(frame,text="Ffurflen Opsiynnau Adolygu",font=("Roboto",36),text_color="White").pack()
    
    customtkinter.CTkLabel(frame,text="Dewiswch faint o cwestiynnau i adolygu",font=("Arial",18),text_color="White").pack()
    customtkinter.CTkButton(frame,text="10",font=("Arial",10),fg_color="Blue",command=lambda: DewisNiferCwestiynnau(10)).pack()
    customtkinter.CTkButton(frame,text="20",font=("Arial",10),fg_color="Blue",command=lambda: DewisNiferCwestiynnau(20)).pack()
    customtkinter.CTkButton(frame,text="30",font=("Arial",10),fg_color="Blue",command=lambda: DewisNiferCwestiynnau(30)).pack()
    customtkinter.CTkButton(frame,text="40",font=("Arial",10),fg_color="Blue",command=lambda: DewisNiferCwestiynnau(40)).pack()
    
    customtkinter.CTkLabel(frame,text="Dewiswch pa catogri o cwestiynnau i adolygu",font=("Arial",18),text_color="White").pack()
    customtkinter.CTkButton(frame,text="Alertness",font=("Arial",10),fg_color="Red",command=lambda: DewisCatogri("Alertness")).pack()
    customtkinter.CTkButton(frame,text="Attitude",font=("Arial",10),fg_color="Red",command=lambda: DewisCatogri("Attitude")).pack()
    customtkinter.CTkButton(frame,text="Hazard awareness",font=("Arial",10),fg_color="Red",command=lambda: DewisCatogri("Hazard awareness")).pack()
    customtkinter.CTkButton(frame,text="Motorway rules",font=("Arial",10),fg_color="Red",command=lambda: DewisCatogri("Motorway rules")).pack()

    customtkinter.CTkLabel(frame,text="Catogri o cwestiynnau i adolygu",font=("Arial",18),text_color="White").pack()
    CatogriAdolyguEntry=customtkinter.CTkEntry(frame,placeholder_text="Catogri",width=200,height=20)
    CatogriAdolyguEntry.pack(pady=20)
    customtkinter.CTkLabel(frame,text="Nifer o cwestiynnau i adolygu",font=("Arial",18),text_color="White").pack()
    NiferCwestiynnauEntry=customtkinter.CTkEntry(frame,placeholder_text="Nifer o cwestiynnau",width=200,height=20)
    NiferCwestiynnauEntry.pack(pady=20)

    ButtonDewis=customtkinter.CTkButton(frame,text="Adolygu",font=("Monaco",18),fg_color="Green",command=lambda: RevisionQuestions(userid,LefelMynediad,NiferCwestiynnauEntry.get(),CatogriAdolyguEntry.get()))
    ButtonDewis.pack(pady=20)

    ButtonYnOl=customtkinter.CTkButton(frame,text="Yn ol",font=("Monaco",18),fg_color="Red",command=lambda: RevisionHome(userid,LefelMynediad))
    ButtonYnOl.pack()

    def DewisNiferCwestiynnau(Nifer):
        NiferCwestiynnauEntry.delete(0,END)
        NiferCwestiynnauEntry.insert(0,Nifer)
        print(f"Nifer cwestiynnau {Nifer}")
        
        
    def DewisCatogri(Catogri):
        CatogriAdolyguEntry.delete(0,END)
        CatogriAdolyguEntry.insert(0,Catogri)


def RevisionHome(userid,LefelMynediad):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Catref Adolygu ")
    root.geometry("1000x750")
    frame=customtkinter.CTkFrame(root,fg_color="#8692F5", bg_color="#8692F5")
    frame.pack(fill="both", expand=True, padx=20, pady=20)
    customtkinter.CTkLabel(frame,text="Ysgol Moduro Normanell",font=("Century Gothic",45),text_color="White").pack()
    customtkinter.CTkLabel(frame,text="Ffurflen Catref Adolygu",font=("Roboto",36),text_color="White").pack()
    customtkinter.CTkLabel(frame,text="Dewiswch beth i wneud isod",font=("Arial",18),text_color="White").pack()
    customtkinter.CTkButton(frame,text="Ymarfer Cwestiynnau theori",font=("Monaco",24),fg_color="Green",command=lambda: CatogriAndQuestionSelecterForRevision(userid,LefelMynediad)).pack(pady=20)
    customtkinter.CTkButton(frame,text="Cymryd ffug prawf",font=("Monaco",24),fg_color="Red",command=lambda: ffugPrawf(userid,LefelMynediad)).pack(pady=20)
    
    if LefelMynediad=="Cwsmer":
        customtkinter.CTkButton(frame,text="Catref",font=("Monaco",18),fg_color="Green",command=lambda : CustomerHomePage(userid)).pack(pady=20)  
    elif LefelMynediad=="Gyrrwr":
        customtkinter.CTkButton(frame,text="Catref",font=("Monaco",18),fg_color="Green",command=lambda : DriversHomePage(userid)).pack(pady=20)  

def YchwaneguBwciadCwsmer(customerid):
    global BwcioGwersCwsmerPage
    global CustomersCredit
    SelectedBookingId=BwcioGwersCwsmerPage.get_entry_value("BookingId")

    if CustomersCredit is not None: 
        CustomersCredit = int(CustomersCredit[0])  # Convert to integer
        if CustomersCredit > 0:
            BookingsCursor.execute("SELECT BookingID FROM BookingsTable WHERE BookingID = ? AND Status =?",(SelectedBookingId,"Available"))
            isAvailable=BookingsCursor.fetchone()
            bookingsdatabase.commit()
            if isAvailable:        
                CustomersCredit=CustomersCredit-1
                CustomerCursor.execute("UPDATE CustomersTable SET Credit = ? WHERE CustomerID = ?",(CustomersCredit,customerid))
                CustomerDataBase.commit()
                BookingsCursor.execute("UPDATE BookingsTable SET CustomerID = ? ,Status = ? , WediGorffen = ? WHERE BookingID = ?",(customerid,"Not Available","Na",SelectedBookingId,))
                bookingsdatabase.commit()
                messagebox.showinfo("Llwyddiant",f"Rydych wedi bwcio gwers , rydych nawr efo {CustomersCredit} credit")
                CustomerHomePage(customerid)
            else:
                messagebox.showinfo("Anllwyddianus","Nid yw'r id bwciad rydych wedi mewnbynnu yn bodoli")
                BwcioGwersCwsmer(customerid)
        else:
            messagebox.showinfo("Bwcio Gwers",f"Yn anffodus rydych methu bwcio gan nad ydych efo digon o credit plis talu yr derbynydd . Rydych efo {CustomersCredit} credit")
            CustomerHomePage(customerid)   


def BwcioGwersCwsmer(customerid):
    for Widget in root.winfo_children():
        Widget.destroy()
    global BwcioGwersCwsmerPage
    global CustomersCredit

    CustomerCursor.execute("SELECT Credit FROM CustomersTable WHERE CustomerID = ?",(customerid,))
    CustomersCredit=CustomerCursor.fetchone()
    CustomerDataBase.commit()

    BwcioGwersCwsmerPageElements=[["Label","Ysgol Moduro Normansell","Century Gothic",45,"White"],
                                  ["Label","Bwcio Gwers","Roboto",36,"White"],
                                  ["Label",f"Rydych efo {CustomersCredit[0]} credit","Roboto",29,"White"],
                                  ["Button","Catref","Monaco",18,"Red",lambda: CustomerHomePage(customerid)],
                                  ["Label","Mewnbynnwch yr Booking ID rydych eisiau bwcio isod","Arial",18,"White"],
                                  ["EntryBox","BookingId",200,20],
                                  ["Button","Enter","Monaco",18,"Green",lambda: YchwaneguBwciadCwsmer(customerid)],
                                  ["Label"," BookingID           Enw Gyrrwr                                            Dyddiad ac Amser","Arial",16,"White"],
                                  ["Label","---------           ----------                                                ----------------","Arial",16,"Black"]
                                  ]
    
    BwcioGwersCwsmerPage=MakeWindow(root,"FFurflen Bwcio Gwers",BwcioGwersCwsmerPageElements)
    
    BookingsCursor.execute("SELECT BookingID, DATE, DriverID FROM BookingsTable WHERE Status != ? AND WediGorffen = ?", ("Not Available","Na"))
    DatesAndDriverIdToBook=BookingsCursor.fetchall()
    bookingsdatabase.commit()

    for i in range (len(DatesAndDriverIdToBook)):
#mae driverid fydd 'ail' eitem wedi cywain o cofnod yn bookings table sydd wedi storio mewn newidyn DatesAndDriverIdToBook ,cywain ai storio mewn newidyn DatesAndDriverIdToBook
                    DriverIDBooking=DatesAndDriverIdToBook[i][2]
#dewis enw ac cyfenw sydd yn cysylltiedig ar id yr gyrrwr yn index dolen i , 1 or newidyn DatesAndDriverIdToBook
                    DriverCursor.execute("SELECT Name, Surname FROM DriversTable WHERE DriversID = ?", (DriverIDBooking,))

                    EnwCyfnewGyrrwr=DriverCursor.fetchall()
                    DriverDatabase.commit()
                
                    if EnwCyfnewGyrrwr :
                        #prints name surname , driver id 
                        print(f"{EnwCyfnewGyrrwr[0][0]} {EnwCyfnewGyrrwr[0][1]} -- {DriverIDBooking}")
                        #prints date sydd yn yr eitem cyntaf yn cofnod i yr newidyn DatesAndDriversToBook 
                        print(DatesAndDriverIdToBook[i][0])
                        print()
                        BwcioGwersCwsmerPage.add_label_string(f" {DatesAndDriverIdToBook[i][0]} - {EnwCyfnewGyrrwr[0][0]} {EnwCyfnewGyrrwr[0][1]} - {DatesAndDriverIdToBook[i][1]}",24)
def DangosBwciadauYrCwsmer(customerid):
    global DyddiadurCwsmeriaidPage
    BookingsCursor.execute("SELECT Date, DriverID FROM BookingsTable WHERE CustomerID =? AND WediGorffen =?",(customerid,"Na"))
    AllCustomerBookings=BookingsCursor.fetchall()
    bookingsdatabase.commit()
    print(AllCustomerBookings)

#allow drivers to set lesson to finished, add finished field to lessons 

    for i in range (len(AllCustomerBookings)):
        DriverID=AllCustomerBookings[i][1]
        DriverCursor.execute("SELECT Name, Surname FROM DriversTable WHERE DriversID = ?", (DriverID,))
        DriversNameAndSurname=DriverCursor.fetchall()
        DriverDatabase.commit()

        
        for j in range (len(DriversNameAndSurname)):
            DyddiadurCwsmeriaidPage.add_label_string(f"{DriversNameAndSurname[j][0]} {DriversNameAndSurname[j][1]}")
            DyddiadurCwsmeriaidPage.add_label_string(AllCustomerBookings[i][0])

def DyddiadurCwsmeriaid(customerid):
    for Widget in root.winfo_children():
        Widget.destroy()

    global DyddiadurCwsmeriaidPage

    CustomerCursor.execute("SELECT Name,Credit FROM CustomersTable WHERE CustomerID = ?",(customerid))
    CustomerName=CustomerCursor.fetchone()
    CustomerDataBase.commit()

    DyddiadurCwsmeriaidPageElements=[["Label","Ysgol Moduro Normansell","Century Gothic",45,"White"],
                                     ["Label",f"Dyddiadur {CustomerName[0]}","Roboto",46,"White"],
                                     ["Label","Eich Bwciadau","Roboto",36,"White"],
                                     ["Label",f"Rydych efo {CustomerName[1]} credit","Arial",18,"White"],
                                     ["Button","Catref","Monaco",18,"Red",lambda: CustomerHomePage(customerid)]
                                     ]

    DyddiadurCwsmeriaidPage=MakeWindow(root,"Dyddiadur Cwsmeriaid",DyddiadurCwsmeriaidPageElements)

    DangosBwciadauYrCwsmer(customerid)

#page to search
#once found another page displays , user enters id 
#when enterd id new page to send message 
#when sent message calls homepage

def DanfonYmholiad(userid,LefelMynediadDanfonI,LefelMynediad,IdDefnyddiwr):
    global DanfonYmholiadPage
    global EnwDefnyddiwr
    Neges=DanfonYmholiadPage.get_entry_value("Eich ymholiad")
    print(f"SIGMA SKEIAGNRIO {IdDefnyddiwr}")

    if Neges=="":
        messagebox.showinfo("Gwall","Rhaid mewnbynnu neges")
        return
    

    YmholiCursor.execute("SELECT YmholiadID FROM YmholiTable ORDER BY YmholiadID DESC LIMIT 1")
    last_ymholi_id = YmholiCursor.fetchone()

#os oes fwy nag un rhes yn yr tabl cwsmeriaid fydd yr customerid yr cwsmer newydd syn cael ei creu yn 1 fwy na customerid yr cwsmer fwyaf diweddar
    if last_ymholi_id:
        last_ymholi_id=last_ymholi_id[0]
        ymholiID=int(last_ymholi_id)+1
    else:
        ymholiID=1
    print(ymholiID)

#make ymholiad id 
    print(LefelMynediad)
    if LefelMynediadDanfonI=="Gyrrwr": # if sending to a drirver user
        if LefelMynediad=="Cwsmer": #and if sending from a customer user
#None for Receptionist Id as receptionisit istn included in the umholiad , 
            YmholiCursor.execute("INSERT INTO YmholiTable VALUES  (?,?,?,?,?,?,?)",(ymholiID,Neges,userid,IdDefnyddiwr,None,"Cwsmer","Heb Gweld"))
            YmholiDataBase.commit()
            DriverCursor.execute("SELECT Name FROM DriversTable WHERE DriversID = ?",(IdDefnyddiwr))
            EnwDefnyddiwr=DriverCursor.fetchone()
            messagebox.showinfo("Ymholiad",f"Wedi danfon ymholiad i {EnwDefnyddiwr[0]}")
            CustomerHomePage(userid)

        elif LefelMynediad=="Derbynydd": #and if sending from a customer user
#None for Receptionist Id as receptionisit istn included in the umholiad , 
            YmholiCursor.execute("INSERT INTO YmholiTable VALUES  (?,?,?,?,?,?,?)",(ymholiID,Neges,None,IdDefnyddiwr,userid,"Derbynydd","Heb Gweld"))
            YmholiDataBase.commit()
            DriverCursor.execute("SELECT Name FROM DriversTable WHERE DriversID = ?",(IdDefnyddiwr))
            EnwDefnyddiwr=DriverCursor.fetchone()
            messagebox.showinfo("Ymholiad",f"Wedi danfon ymholiad i {EnwDefnyddiwr[0]}")
            ReceptionistHomePage(userid)

    elif LefelMynediadDanfonI=="Derbynydd":
            if LefelMynediad=="Cwsmer":
                YmholiCursor.execute("INSERT INTO YmholiTable VALUES (?,?,?,?,?,?,?)",(ymholiID,Neges,userid,None,IdDefnyddiwr,"Cwsmer","Heb Gweld"))
                YmholiDataBase.commit()
                ReceptionistCursor.execute("SELECT Name FROM ReceptionistTable WHERE ReceptionistID = ?",(IdDefnyddiwr))
                EnwDefnyddiwr=ReceptionistCursor.fetchone()
                messagebox.showinfo("Ymholiad",f"Wedi danfon ymholiad i {EnwDefnyddiwr[0]}")
                CustomerHomePage(userid)

            elif LefelMynediad=="Gyrrwr":
                YmholiCursor.execute("INSERT INTO YmholiTable VALUES (?,?,?,?,?,?,?)",(ymholiID,Neges,None,userid,IdDefnyddiwr,"Gyrrwr","Heb Gweld"))
                YmholiDataBase.commit()
                ReceptionistCursor.execute("SELECT Name FROM ReceptionistTable WHERE ReceptionistID = ?",(IdDefnyddiwr))
                EnwDefnyddiwr=ReceptionistCursor.fetchone()
                messagebox.showinfo("Ymholiad",f"Wedi danfon ymholiad i {EnwDefnyddiwr[0]}")
                DriversHomePage(userid)

    elif LefelMynediadDanfonI=="Cwsmer":
        if LefelMynediad=="Gyrrwr":
            YmholiCursor.execute("INSERT INTO YmholiTable VALUES (?,?,?,?,?,?,?)",(ymholiID,Neges,IdDefnyddiwr,userid,None,"Gyrrwr","Heb Gweld"))
            YmholiDataBase.commit()
            CustomerCursor.execute("SELECT Name FROM CustomersTable WHERE CustomerID = ?",(IdDefnyddiwr))
            EnwDefnyddiwr=CustomerCursor.fetchone()
            messagebox.showinfo("Ymholiad",f"Wedi danfon ymholiad i {EnwDefnyddiwr}")
            DriversHomePage(userid)
        
        elif LefelMynediad=="Derbynydd":
            YmholiCursor.execute("INSERT INTO YmholiTable VALUES (?,?,?,?,?,?,?)",(ymholiID,Neges,IdDefnyddiwr,None,userid,"Derbynydd","Heb Gweld"))
            YmholiDataBase.commit()
            CustomerCursor.execute("SELECT Name FROM CustomersTable WHERE CustomerID = ?",(IdDefnyddiwr))
            EnwDefnyddiwr=CustomerCursor.fetchone()
            messagebox.showinfo("Ymholiad",f"Wedi danfon ymholiad i {EnwDefnyddiwr}")
            ReceptionistHomePage(userid)


    

def MewnbynnuYmholiad(userid,LefelMynediadDanfonI,LefelMynediad):
    
    global DangosIdDefnyddiwrYmholipage
    global DanfonYmholiadPage

    IdDefnyddiwr=DangosIdDefnyddiwrYmholipage.get_entry_value("Id")

    if IdDefnyddiwr=="":
        messagebox.showinfo("Gwall","Rhaid mewnbynnu id defnyddiwr")
        return

    for Widget in root.winfo_children():
        Widget.destroy()

    if LefelMynediadDanfonI=="Cwsmer":
        CustomerCursor.execute("SELECT Name FROM CustomersTable WHERE CustomerID = ? ",(IdDefnyddiwr,))
        Exists=CustomerCursor.fetchone()
        if Exists:
            print(f"Exists:  {Exists}")
        else:
            messagebox.showinfo("Ymholi","Nid oes cwsmer efo'r ID yn bodoli")
            return
    
    if LefelMynediadDanfonI=="Gyrrwr":
        DriverCursor.execute("SELECT Name FROM DriversTable WHERE DriversID = ? ",(IdDefnyddiwr,))
        Exists=DriverCursor.fetchone()
        if Exists:
            print(f"Exists:  {Exists}")
        else:
            messagebox.showinfo("Ymholi","Nid oes Gyrrwr efo'r ID yn bodoli")
            return
        
    if LefelMynediadDanfonI=="Derbynydd":
        ReceptionistCursor.execute("SELECT Name FROM ReceptionistTable WHERE ReceptionistID = ?",(IdDefnyddiwr,))
        Exists=ReceptionistCursor.fetchone()
        if Exists:
            print(f"Exists : {Exists}")
        else:
            messagebox.showinfo("Ymholi","Nid oes Derbynydd efo'r ID yn bodoli")
            if LefelMynediad=="Cwsmer":
                CustomerHomePage(userid)

    DanfonYmholiadPageElements=[["Label","Ysgol moduro Normansell","Century Gothic",45,"White"],
                                ["Label","Danfon ymholiad i ...","Roboto",36,"White"],
                                ["EntryBox","Eich ymholiad",700,400],
                                ["Button",f"Danfon ymholiad i {Exists[0]} ","Monaco",18,"Green",lambda: DanfonYmholiad(userid,LefelMynediadDanfonI,LefelMynediad,IdDefnyddiwr)],
                                ["Button","Catref","Monaco",18,"Red",lambda: CustomerHomePage(userid)]
                                ]

    DanfonYmholiadPage=MakeWindow(root,"Danfon Ymholiad",DanfonYmholiadPageElements)

def DangosIdDefnyddiwrYmholi(customerid,EnwDefnyddiwrIdYmholi,LefelMynediadDanfonI,LefelMynediad):
    for Widget in root.winfo_children():
        Widget.destroy()

    global DangosIdDefnyddiwrYmholipage
    
    DangosIdDefnyddiwrYmholipageElements=[["Label","Ysgol Moduro Normansell","Century Gothic",45,"White"],
                                          ["Label","Dewis defnyddiwr i ymholi","Roboto",36,"White"],
                                          ["Label","Mewnbynnwch Id defnyddiwr i ymholi isod","Arial",18,"White"],
                                          ["EntryBox","Id",200,20],
                                          ["Button","Ymholi","Monaco",18,"Green",lambda: MewnbynnuYmholiad(customerid,LefelMynediadDanfonI,LefelMynediad)],
                                          ["Button","Yn ol","Monaco",18,"Red",lambda: CatrefYmholi(customerid,LefelMynediad)],
                                          ["Button","Catref","Monaco",18,"Red",lambda: CustomerHomePage(customerid)]
                                          ]

    DangosIdDefnyddiwrYmholipage=MakeWindow(root,"Dewis defnyddiwr i ymholi",DangosIdDefnyddiwrYmholipageElements)

    for i in range (len(EnwDefnyddiwrIdYmholi)):
        DangosIdDefnyddiwrYmholipage.add_label_string(f""" Enw {LefelMynediad} : {EnwDefnyddiwrIdYmholi[i][0]}
Id {LefelMynediadDanfonI} : {EnwDefnyddiwrIdYmholi[i][1]}
                                                  """)


def ChwilioAmDefnyddiwrYmholi(userid,LefelMynediad):
    

    global CatrefYmholiPage

    

    EnwDefnyddiwrYmholi=CatrefYmholiPage.get_entry_value("Mewnbynnwch enw defnyddiwr") #entrybox ar gyfer enw defnyddiwr 
    CyfenwDefnyddiwrYmholi=CatrefYmholiPage.get_entry_value("Mewnbynnwch cyfenw defnyddiwr") #entrybox ar gyfer cyfenw defnyddiwr
    LefelMynediadYmholi=CatrefYmholiPage.get_combo_value("Gyrrwr") # Combo ar gyfer lefel myneidad

#dilysu enw defnyddiwr
    if EnwDefnyddiwrYmholi == "":
        messagebox.showinfo("Ymholi","Rhaid mewnbynnu enw defnyddiwr yn yr blwch mynediad priodol !")
        CatrefYmholi(userid,LefelMynediad)
    EnwDefnyddiwrMathDilys=True
    for char in EnwDefnyddiwrYmholi:
        if char.isdigit()==True:
            EnwDefnyddiwrMathDilys=False
    if EnwDefnyddiwrMathDilys==False:
        messagebox.showinfo("Ymholi","Ni dylai enw defnyddiwr cynnwys rhifau !")
        CatrefYmholi(userid,LefelMynediad)
#dilsyu cyfenw
    if CyfenwDefnyddiwrYmholi == "":
        messagebox.showinfo("Ymholi","Rhaid mewnbynnu cyfewn defnyddiwr yn yr blwch mynediad priodol !")
        CatrefYmholi(userid,LefelMynediad)
    CyfenwDefnyddiwrMathDilys=True
    for char in CyfenwDefnyddiwrYmholi:
        if char.isdigit()==True:
            CyfenwDefnyddiwrMathDilys=False
    if CyfenwDefnyddiwrMathDilys==False:
        messagebox.showinfo("Ymholi","Ni dylai cyfenw defnyddiwr cynnwys rhifau !")
        CatrefYmholi(userid,LefelMynediad)



    if LefelMynediadYmholi=="Gyrrwr":
        print("Fries")
        DriverCursor.execute("SELECT Username , DriversID FROM DriversTable WHERE Name = ? AND surname = ?",(EnwDefnyddiwrYmholi,CyfenwDefnyddiwrYmholi))
        EnwDefnyddiwrIdYmholi=DriverCursor.fetchall()
        DriverDatabase.commit()
        print(EnwDefnyddiwrIdYmholi)

        if EnwDefnyddiwrIdYmholi:
            DangosIdDefnyddiwrYmholi(userid,EnwDefnyddiwrIdYmholi,"Gyrrwr",LefelMynediad)
        else:
            messagebox.showinfo("Ymholi","Nid yw defnyddiwr efo manylion sydd wedi mewnbynnu yn bodoli")
            CatrefYmholi(userid,LefelMynediad)
    
    elif LefelMynediadYmholi=="Cwsmer":
        print("chips")
        CustomerCursor.execute("SELECT Username , CustomerID FROM CustomersTable WHERE Name = ? AND surname = ?",(EnwDefnyddiwrYmholi,CyfenwDefnyddiwrYmholi))
        EnwDefnyddiwrIdYmholi=CustomerCursor.fetchall()
        CustomerDataBase.commit()
        print(EnwDefnyddiwrIdYmholi)

        if EnwDefnyddiwrIdYmholi:
            DangosIdDefnyddiwrYmholi(userid,EnwDefnyddiwrIdYmholi,"Cwsmer",LefelMynediad)
        else:
            messagebox.showinfo("Ymholi","Nid yw defnyddiwr efo manylion sydd wedi mewnbynnu yn bodoli")
            CatrefYmholi(userid,LefelMynediad)

    elif LefelMynediadYmholi=="Derbynydd":
        print("Blob Fish")
        ReceptionistCursor.execute("SELECT Username , ReceptionistID FROM ReceptionistTable WHERE Name = ? AND Surname = ?",(EnwDefnyddiwrYmholi,CyfenwDefnyddiwrYmholi))
        EnwDefnyddiwrIdYmholi=ReceptionistCursor.fetchall()
        print(EnwDefnyddiwrIdYmholi)

        if EnwDefnyddiwrIdYmholi:
            DangosIdDefnyddiwrYmholi(userid,EnwDefnyddiwrIdYmholi,"Derbynydd",LefelMynediad)
        else:
            messagebox.showinfo("Ymholi","Nid oes defnyddiwr efo manylion hyn yn bodoli")
            CatrefYmholi(userid,LefelMynediad   )

  # dont make new window in this function , see use for dilysu 

def CatrefYmholi(userid,LefelMynediad):
    for Widget in root.winfo_children():
        Widget.destroy()
    
    global CatrefYmholiPage

    CatrefYmholiPageElements=[["Label","Ysgol Moduro Normansell","Century Gothic",45,"White"],
                              ["Label","Catref Ymholiadau","Roboto",36,"White"],
                              ["Label","Chwilio am defnyddiwr","Arial",19,"White"],
                              ["EntryBox","Mewnbynnwch enw defnyddiwr",400,40],
                              ["EntryBox","Mewnbynnwch cyfenw defnyddiwr",400,40],
                              ["ComboBox","Gyrrwr","Derbynydd","Cwsmer"],
                              ["Button","Chwilio","Monaco",18,"Red",lambda: ChwilioAmDefnyddiwrYmholi(userid,LefelMynediad)],
                              ["Button","Catref","Monaco",18,"Green",lambda: DriversHomePage(userid) if LefelMynediad == "Gyrrwr" else CustomerHomePage(userid) ]
                              ]

    CatrefYmholiPage=MakeWindow(root,"Ffurflen Catref Ymholiad",CatrefYmholiPageElements)
    



def CustomerHomePage(customerid):
    for Widget in root.winfo_children():
        Widget.destroy()

    CustomerCursor.execute("SELECT Name FROM CustomersTable WHERE CustomerID = ? ",(customerid,))
    UserNameAndSurname=CustomerCursor.fetchone()
    CustomerDataBase.commit()


    CustomerHomePageElements=[
       
        ["Label","Ysgol Moduro Normansell","Roboto",45,"White"],
        ["Label",f"Croeso {UserNameAndSurname[0]}","Roboto",36,"White" ],
        ["Label","Beth hoffwch wneud ? ","Arial",18,"White"],
        ["Button","Adolygu","Monaco",36,"Green",lambda: RevisionHome(customerid,"Cwsmer")],
        ["Button","Dyddiadur","Monaco",36,"Blue",lambda: DyddiadurCwsmeriaid(customerid)],
        ["Button","Bwcio Gwers","Monaco",36,"Green",lambda: BwcioGwersCwsmer(customerid)],
        ["Button","Ymholi","Monaco",36,"Blue",lambda: CatrefYmholi(customerid,"Cwsmer")],
        ["Button","Gweld ymholiadau","Monaco",36,"Green",lambda: DewisYmholiad(customerid,"Cwsmer")],
        ["Button","Logio Allan","Monaco",36,"Red",lambda: LoginPage()]

                              ]
    
    CustomerHomePagewindow = MakeWindow(root, "CustomerHomePage",  CustomerHomePageElements)

def DyddiadurGyrrwr(driverid):
    for Widget in root.winfo_children():
        Widget.destroy()

    DriverCursor.execute("SELECT Name FROM DriversTable WHERE DriversID=?",(driverid))
    EnwGyrrwr=DriverCursor.fetchone()
    EnwGyrrwr=EnwGyrrwr[0]
    DriverDatabase.commit()

    BookingsCursor.execute("SELECT Date, TypeOfBooking, CustomerID,Status FROM BookingsTable WHERE DriverID = ? AND WediGorffen = ?",(driverid,"Na"))
    Bookings=BookingsCursor.fetchall()
    bookingsdatabase.commit()

    root.title("Dyddiadur Gyrrwr")

    frame = customtkinter.CTkFrame(root, fg_color="#8692F5", bg_color="#8692F5")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    customtkinter.CTkLabel(frame,text=(f"Bwciadau {EnwGyrrwr}"),font=("Century Gothic",36)).pack()
    
    DyddiadurGyrrwrTextBox=customtkinter.CTkTextbox(frame,width=500,height=500)
    DyddiadurGyrrwrTextBox.pack()
    
    if Bookings:
        for i in range (len(Bookings)):
            CustomerCursor.execute("SELECT Name ,Surname , Username FROM CustomersTable WHERE CustomerID = ?",(Bookings[i][2],))
            CustomerName = CustomerCursor.fetchone()
            if CustomerName:


                DyddiadurGyrrwrTextBox.insert(tk.END,f"""
Bwciad {i+1}   
Dyddiad : {Bookings[i][0]} ,
Math : {Bookings[i][1]} , 
Enw Cwsmer : {CustomerName[0]} {CustomerName[1]} ,
Enw Defnyddiwr : {CustomerName[2]} 
Statws : {Bookings[i][3]}
""")
            else:
                DyddiadurGyrrwrTextBox.insert(tk.END,f"""
Bwciad {i+1}   
Dyddiad : {Bookings[i][0]} ,
Math : {Bookings[i][1]} , 
Statws : {Bookings[i][3]}
""")
    
    ButtonCatref = customtkinter.CTkButton(frame,text=("Catref"),font=("Monaco",18),fg_color="Red",command=lambda: DriversHomePage(driverid))
    ButtonCatref.pack()

    

def ychwaneguBwciadGyrrwr(driverid):
    global BwciadauGyrrwrPage

    #angen DILYSU DILYSU 
    DyddiadBwciad=BwciadauGyrrwrPage.get_entry_value("Dyddiad Bwciad")
    AmserBwciad=BwciadauGyrrwrPage.get_entry_value("Amser Bwciad")
    MathBwciad=BwciadauGyrrwrPage.get_combo_value("Heb Pasio")

    MaesyddYchwaneguBwciad =[DyddiadBwciad,AmserBwciad]

    for Maes in MaesyddYchwaneguBwciad:
        if Maes=="":
            messagebox.showinfo("Ychwanegu Bwciad","Rhaid llenwi holl meysydd")
            BwciadauGyrrwr(driverid)
            return
    
    print(DyddiadBwciad)
    #dilysu dyddiad
    if DyddiadBwciad[0:2].isdigit()==False or DyddiadBwciad[3:4].isdigit()==False or DyddiadBwciad[6:].isdigit()==False:
        messagebox.showinfo("Ychwanegu bwciad","Rhaid ir dyddiad dilyn format (00/00/0000) ")
        BwciadauGyrrwr(driverid)
        return
    elif len (DyddiadBwciad)!=10:
        messagebox.showinfo("Ychwanegu bwciad","Rhaid ir dyddiad cynnwys 9 cymerid yn dilyn format (00/00/0000) ")
        BwciadauGyrrwr(driverid)
        return
    elif DyddiadBwciad[2] !="/" or DyddiadBwciad[5]!="/":
        messagebox.showinfo("Ychwanegu bwciad","Rhaid defnyddio '/' i gwahanu dyddiad , mis ac blwyddyn (00/00/0000)")
        BwciadauGyrrwr(driverid)
        return
    #dilysu amser
    print(AmserBwciad)
    if AmserBwciad[0:2].isdigit()==False or AmserBwciad[3:5].isdigit()==False or AmserBwciad[6:8].isdigit()==False or AmserBwciad[9:].isdigit()==False:
        messagebox.showinfo("Ychwanegu Bwciad","Rhaid i cymeriadau priodol yr amser cynnwys digidau , format yw (00:00-00:00)")
        BwciadauGyrrwr(driverid)
        return


    #angen wneud dilysu ar gyfer dyddiad ac amser bwciad

    BookingsCursor.execute("SELECT BookingID FROM BookingsTable ORDER BY BookingID DESC LIMIT 1")
    Last_booking_id = BookingsCursor.fetchone()

#os oes fwy nag un rhes yn yr tabl cwsmeriaid fydd yr customerid yr cwsmer newydd syn cael ei creu yn 1 fwy na customerid yr cwsmer fwyaf diweddar
    if Last_booking_id:
        Last_booking_id=Last_booking_id[0]
        bookingId=int(Last_booking_id)+1
    else:
        bookingId=1

        print(bookingId)

    date=(f"{DyddiadBwciad}-{AmserBwciad}")
    print(date)
    print(MathBwciad)



    BookingsCursor.execute("INSERT INTO BookingsTable VALUES (?,?,?,?,?,?,?)",
                           (bookingId,date,MathBwciad,None,driverid,"Available","Na"))
    
  
    bookingsdatabase.commit()

    messagebox.showinfo("LLwyddiant","Mae'r bwciad wedi cael ei ychwanegu")

    for Widget in root.winfo_children():
        Widget.destroy()
    DriversHomePage(driverid)


def BwciadauGyrrwr(driverid):
    for Widget in root.winfo_children():
        Widget.destroy()#add math o bwcaid to bookingstable
    global BwciadauGyrrwrPage
    
    BwciadauGyrrwrPageElements=[["Label","Ysgol Moduro Normansell","Century Gothic",56,"White"],
                                ["Label","Mewnbynnwch manylion yr bwciad i ychwanegu","Arial",18,"White"],
                                ["EntryBox","Dyddiad Bwciad",200,30],
                                ["EntryBox","Amser Bwciad",200,30],
                                ["Label","Dewiswch math o bwciad ","Arial",18,"White"],
                                ["ComboBox","Heb Pasio","Wedi Pasio",""],
                                ["Button","Enter","Monaco",18,"Green",lambda: ychwaneguBwciadGyrrwr(driverid)],
                                ["Button","Catref","Monaco",18,"Green",lambda: DriversHomePage(driverid)]
                                ]

    BwciadauGyrrwrPage=MakeWindow(root,"Ffurflen Ychawngu Bwciadau",BwciadauGyrrwrPageElements)

def YchwaneguCwestiwnTheoriAtTabl(driverid):
    global YchwaneguCwestiynnauTheoriPage

    Cwestiwn=YchwaneguCwestiynnauTheoriPage.get_entry_value("Cwestiwn i ychwanegu")
    AtebCywir=YchwaneguCwestiynnauTheoriPage.get_entry_value("Ateb cywir ir cwestiwn")
    AtebAnghywirCyntaf=YchwaneguCwestiynnauTheoriPage.get_entry_value("Ateb anghywir ir cwestiwn")
    AtebAnghywirAil=YchwaneguCwestiynnauTheoriPage.get_entry_value("Ail ateb anghywir ir cwestiwn")
    AtebAnghywirTrydydd=YchwaneguCwestiynnauTheoriPage.get_entry_value("Trydydd ateb anghywir ir cwestiwn")

    Catogri=YchwaneguCwestiynnauTheoriPage.get_combo_value("Alertness")

    MewnbynnauAiDilysu=[
        [Cwestiwn,"Rhaid mewnbynnu Cwestiwn theori"],
        [AtebCywir,"Rhaid mewnbynnu ateb ir cwestiwn"],
        [AtebAnghywirCyntaf,"Rhaid mewnbynnu ateb anghywir cyntaf"],
        [AtebAnghywirAil,"Rhaid mewnbynnu ail ateb anghywir"],
        [AtebAnghywirTrydydd,"Rhaid mewnbynnu trydydd ateb anghywir"],
                                 ]


    Dilys = True
    for i in range (len(MewnbynnauAiDilysu)):
        if MewnbynnauAiDilysu[i][0]=="":
            messagebox.showinfo("Gwall",MewnbynnauAiDilysu[i][1])
            return

    if Dilys==False:
        YchwaneguCwestiynnauTheori(driverid)

    RevisionCursor.execute("SELECT RevisionID FROM RevisionTable ORDER BY RevisionID DESC LIMIT 1")
    last_revision_id = RevisionCursor.fetchone()

#os oes fwy nag un rhes yn yr tabl cwsmeriaid fydd yr customerid yr cwsmer newydd syn cael ei creu yn 1 fwy na customerid yr cwsmer fwyaf diweddar
    if last_revision_id:
        last_revision_id=last_revision_id[0]
        revisionID=int(last_revision_id)+1
    else:
        revisionID=1

    print(revisionID)
    
    
    if Dilys==True:
        RevisionCursor.execute("INSERT INTO RevisionTable VALUES (?,?,?,?,?,?,?)", (revisionID,Cwestiwn, AtebCywir, AtebAnghywirCyntaf, AtebAnghywirAil, AtebAnghywirTrydydd, Catogri))
        Revisiondatabase.commit()
        messagebox.showinfo("LLwyddiant","Mae'r cwestiwn wedi cael ei ychwanegu at tabl cwestiynnau")

        DriversHomePage(driverid)


def YchwaneguCwestiynnauTheori(driverid):
    for Widget in root.winfo_children():
        Widget.destroy()
    global YchwaneguCwestiynnauTheoriPage

    YchwaneguCwestiynnauTheoriElements=[["Label","Ysgol Moduro Normansell","Century Gothic",56,"White"],
                                        ["Label","Ychwanegu Cwestiynnau theori","Roboto",36,"White"],
                                        ["Label","Mewnbynnwch eich cwestiynnau ar atebion isod","Arial",18,"White"],
                                        ["EntryBox","Cwestiwn i ychwanegu",500,100],
                                        ["EntryBox","Ateb cywir ir cwestiwn",500,50],
                                        ["EntryBox","Ateb anghywir ir cwestiwn",500,50],
                                        ["EntryBox","Ail ateb anghywir ir cwestiwn",500,50],
                                        ["EntryBox","Trydydd ateb anghywir ir cwestiwn",500,50],
                                        ["Label","Dewiswch catogri cysylltiedig","Arial",19,"White"],
                                        ["ComboBox","Alertness","Hazard Awarness","Attitude"],
                                        ["Button","Enter","Monaco",24,"Green",lambda: YchwaneguCwestiwnTheoriAtTabl(driverid)],
                                        ["Button","Catref","Monaco",18,"Red",lambda: DriversHomePage(driverid)]
                                        ]

    YchwaneguCwestiynnauTheoriPage=MakeWindow(root,"Ffurflen Ychwanegu Cwestiynnau Theori",YchwaneguCwestiynnauTheoriElements)

def ArddangosCwestiwnCatogri(driverid):
    global GweldCwestiynnauTheoriPage


    Catogri=GweldCwestiynnauTheoriPage.get_entry_value("Catogri")

    for Widget in root.winfo_children():
        Widget.destroy()

    #dilysu presenoldeb
    if Catogri=="":
        messagebox.showinfo("Gweld cwestiynnau theori","Rhaid mewnbynnu catogri")
        GweldCwestiynnauTheori(driverid)
        return
    elif Catogri != "Alertness" and Catogri != "Awarness" and Catogri != "Hazard Awarness" and Catogri != "Motorway rules":
        messagebox.showinfo("Gweld cwestiynnau theori","Rhaid ir catogri fod yn Alertness, Awarness, Hazard Awarness neu Motorway rules")
        GweldCwestiynnauTheori(driverid)
        return

    RevisionCursor.execute("SELECT Question FROM RevisionTable WHERE Catogry=?", (Catogri,))

    Questions=RevisionCursor.fetchall()
    Revisiondatabase.commit()
    print(Questions)

    root.title("Arddangos Cwestiynnau theori")

    frame = customtkinter.CTkFrame(root, fg_color="#8692F5", bg_color="#8692F5")  
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    customtkinter.CTkLabel(frame,text="Ysgol Moduro Normansell",font=("Century Gothic",36),text_color="White").pack()
    customtkinter.CTkLabel(frame,text=f"Cwestiynnau {Catogri}",font=("Roboto",24),text_color="White").pack()

    BoxCwestiynnau=customtkinter.CTkTextbox(frame,width=750,height=500)
    BoxCwestiynnau.pack()


    counter=0
    for Question in Questions:
        counter+=1
        BoxCwestiynnau.insert(tk.END, f"{counter}) {Question[0]}\n")

    customtkinter.CTkButton(frame,text="Catref",font=("Monaco",18),fg_color="Green",command=lambda: DriversHomePage(driverid)).pack()


def GweldCwestiynnauTheori(driverid):
    for Widget in root.winfo_children():
        Widget.destroy()

    global GweldCwestiynnauTheoriPage

    GweldCwestiynnauTheoriPageElements=[["Label","Ysgol Moduro Normansell","Century Gothic",45,"White"],
                                        ["Label","Dewiswch Catogri","Arial",18,"White"],
                                        ["Label","Mewnbynnwch catogri i gweld ('Alertness','Awarness','Hazard Awarness' neu 'Motorway rules)","Arial",18,"White"],
                                        ["EntryBox","Catogri",200,20],
                                        ["Button","Enter","Monaco",18,"Green",lambda: ArddangosCwestiwnCatogri(driverid)],
                                        ["Button","Catref","Monaco",18,"Red",lambda: DriversHomePage(driverid)]
                                        ]
                                       

    GweldCwestiynnauTheoriPage=MakeWindow(root,"Ffurflen Gweld Cwestiynnau Theori",GweldCwestiynnauTheoriPageElements)

def WediGweldYmholiad(userid,Neges,IdDefnyddiwr,LefelMynediadDefnyddiwr,LefelMynediad):
    print(f"OHIO {LefelMynediadDefnyddiwr}")
    print(f"SIGMA {LefelMynediad}")
    if LefelMynediadDefnyddiwr=="Cwsmer":
        print(f" neges {Neges[0]}")
        print(f" IdDefnyddiwr {IdDefnyddiwr}")
        print(f" userid {userid}")
        YmholiCursor.execute("UPDATE YmholiTable SET Status=? WHERE Neges=? AND CustomerID=? AND DriverID=?", ("Wedi Gweld", (Neges[0]), IdDefnyddiwr, userid))
        YmholiDataBase.commit()
        if LefelMynediad=="Cwsmer":
            CustomerHomePage(userid)
        elif LefelMynediad=="Gyrrwr":
            DriversHomePage(userid)
        #DriversHomePage(userid)
    if LefelMynediadDefnyddiwr=="Gyrrwr":
    
        YmholiCursor.execute("UPDATE YmholiTable SET Status=? WHERE Neges=? AND CustomerID=? AND DriverID=?", ("Wedi Gweld", (Neges[0]), userid, IdDefnyddiwr))
        YmholiDataBase.commit()
        if LefelMynediad=="Cwsmer":
            CustomerHomePage(userid)
        elif LefelMynediad=="Gyrrwr":
            DriversHomePage(userid)
      

def MarcioFelWediGweld(userid,LefelMynediad,YmholiadId):
    YmholiCursor.execute("UPDATE YmholiTable SET Status = ? WHERE YmholiadId = ?",("Wedi Gweld",YmholiadId))
    YmholiDataBase.commit()
    if LefelMynediad=="Cwsmer":
        CustomerHomePage(userid)
    elif LefelMynediad=="Gyrrwr":
        DriversHomePage(userid)

def GweldYmholiad(userid, LefelMynediad,EnwCyfenwSentFrom):
    global IdYmholiadEntry

    YmholiadId = IdYmholiadEntry.get()
    
    if YmholiadId =="":
        messagebox.showinfo("Gwall","Rhaid mewnbynnu id ymholiad yn yr blwch mynediad")
        return
    
    #select negrs from ymholitable where ymholiadid  = ? 
    YmholiCursor.execute("SELECT Neges FROM YmholiTable WHERE YmholiadID = ?",(YmholiadId,))
    Neges=YmholiCursor.fetchone()
    
    if Neges:
        pass
    else:
        messagebox.showinfo("Gwall","Nid ydych wedi mewnbynnu id ymholiad dilys , mae'nt i weld uchod")
        return
    
    YmholiDataBase.commit()

    for Widget in root.winfo_children():
        Widget.destroy()

    root.title("Gweld Ymholiad")
    frame = customtkinter.CTkFrame(root, fg_color="#8692F5", bg_color="#8692F5")
    frame.pack(fill="both", expand=True, padx=20, pady=20)
    customtkinter.CTkLabel(frame, text="Ysgol Moduro Normansell", font=("Century Gothic", 45), text_color="White").pack()
    customtkinter.CTkLabel(frame, text=f"Neges oddi {EnwCyfenwSentFrom[0][0]} {EnwCyfenwSentFrom[0][1]} ", font=("Roboto", 36), text_color="White").pack()
    TextboxYmholiad=customtkinter.CTkTextbox(frame,width=500,height=500)
    TextboxYmholiad.pack()
    TextboxYmholiad.insert(tk.END, f"{Neges[0]}\n")

    print(LefelMynediad)
    if LefelMynediad=="Gyrrwr":
        customtkinter.CTkButton(frame, text="Catref", font=("Monaco", 18), fg_color="Red", command=lambda: DriversHomePage(userid)).pack()
    elif LefelMynediad=="Cwsmer":
        customtkinter.CTkButton(frame, text="Catref", font=("Monaco", 18), fg_color="Red", command=lambda: CustomerHomePage(userid)).pack()
    elif LefelMynediad=="Derbynydd":
        customtkinter.CTkButton(frame,text="Catref",font=("Monaco",18),fg_color="Red",command=lambda: ReceptionistHomePage(userid)).pack()

    customtkinter.CTkButton(frame,text="Marcio fel Wedi gweld",font=("Monaco",18),fg_color="Green",command=lambda: MarcioFelWediGweld(userid,LefelMynediad,YmholiadId)).pack()


def DewisYmholiad(userid, LefelMynediad):
    for Widget in root.winfo_children():
        Widget.destroy()

    global IdYmholiadEntry
    root.title("Dewis ymholiad Page")
    frame = customtkinter.CTkFrame(root, fg_color="#8692F5", bg_color="#8692F5")
    frame.pack(fill="both", expand=True, padx=20, pady=20)
    customtkinter.CTkLabel(frame, text="Ysgol Moduro Normansell", font=("Century Gothic", 45), text_color="White").pack()
    customtkinter.CTkLabel(frame, text="Eich ymholiadau", font=("Roboto", 36), text_color="White").pack()

    # If the user who is viewing their bookings is a driver
    if LefelMynediad == "Gyrrwr":
        print(f"USERID {userid}")
        # Select fields form the ymholiTable where the driverId = userid, because lefel mynediad = driver
        YmholiCursor.execute("SELECT YmholiadID, Neges, CustomerID, ReceptionistID, SentFrom FROM YmholiTable WHERE DriverID = ? AND Status = ? ", (userid, "Heb Gweld"))
        Ymholiadau = YmholiCursor.fetchall()
        YmholiDataBase.commit()
        # Repeat through all records fetched
        if Ymholiadau:
            for i in range(len(Ymholiadau)):
                # Only go through records that aren't sent from driver
                if Ymholiadau[i][4] != "Gyrrwr":
                    # If it was sent from a customer, select the customerid from the table to know the name and surname of whoever sent
                    if Ymholiadau[i][4] == "Cwsmer":  # If SentFrom field = Cwsmer, then show customerid
                        CustomerCursor.execute("SELECT Name, Surname, Username FROM CustomersTable WHERE CustomerID = ?", (Ymholiadau[i][2],))
                        EnwCyfenwSentFrom = CustomerCursor.fetchall()
                        print(f"Sent from {EnwCyfenwSentFrom}")
                        customtkinter.CTkLabel(frame, text=(f"""Enw : {EnwCyfenwSentFrom[0][0]} , Cyfenw : {EnwCyfenwSentFrom[0][1]}
    Enw Defnyddiwr : {EnwCyfenwSentFrom[0][2]}
    Id Ymholiad : {Ymholiadau[i][0]}
    """), font=("Arial", 18), text_color="White").pack(pady=10)
                        
                    elif Ymholiadau[i][4] == "Derbynydd":  # If SentFrom field = Cwsmer, then show customerid
                        ReceptionistCursor.execute("SELECT Name, Surname, Username FROM ReceptionistTable WHERE ReceptionistID = ?", (Ymholiadau[i][3],))
                        EnwCyfenwSentFrom = ReceptionistCursor.fetchall()
                        print(f"Sent from {EnwCyfenwSentFrom}")
                        customtkinter.CTkLabel(frame, text=(f"""Enw : {EnwCyfenwSentFrom[0][0]} , Cyfenw : {EnwCyfenwSentFrom[0][1]}
    Enw Defnyddiwr : {EnwCyfenwSentFrom[0][2]}
    Id Ymholiad : {Ymholiadau[i][0]}
    """), font=("Arial", 18), text_color="White").pack(pady=10)                   
                                      
            IdYmholiadEntry = customtkinter.CTkEntry(frame, placeholder_text="Id Ymholiad", font=("Arial", 16), width=200, height=20)
            IdYmholiadEntry.pack(pady=20)
        else:
            customtkinter.CTkLabel(frame,text="Nad ydych efo unrhyw ymholiadau yn anffodus",font=("Roboto",36),text_color="Red").pack()
            
                    

    elif LefelMynediad == "Cwsmer": # if lefel mynediad = cwsmer should have two if statments for driver and recptionist users
        print(f"USERID {userid}")
        # Select fields form the ymholiTable where the driverId = userid, because lefel mynediad = driver
        YmholiCursor.execute("SELECT YmholiadID, Neges, DriverID, ReceptionistID, SentFrom FROM YmholiTable WHERE CustomerID = ? AND Status = ? AND SentFROM != ? ", (userid, "Heb Gweld","Cwsmer"))
        Ymholiadau = YmholiCursor.fetchall()
        YmholiDataBase.commit()
        print("HELOEFIEONR",Ymholiadau)
        # Repeat through all records fetched
        if Ymholiadau:
            for i in range(len(Ymholiadau)):
                # Only go through records that aren't sent from driver
                if Ymholiadau[i][4] != "Cwsmer":
                    print("IloveELVISPRESLEY")
                    # If it was sent from a customer, select the customerid from the table to know the name and surname of whoever sent
                    if Ymholiadau[i][4] == "Gyrrwr":  # If SentFrom field = Cwsmer, then show customerid
                        DriverCursor.execute("SELECT Name, Surname, Username FROM DriversTable WHERE DriversID = ?", (Ymholiadau[i][2],))
                        EnwCyfenwSentFrom = DriverCursor.fetchall()
                        print(f"Sent from {EnwCyfenwSentFrom}")
                        customtkinter.CTkLabel(frame, text=(f"""Enw : {EnwCyfenwSentFrom[0][0]} , Cyfenw : {EnwCyfenwSentFrom[0][1]}
    Enw Defnyddiwr : {EnwCyfenwSentFrom[0][2]}
    Id Ymholiad : {Ymholiadau[i][0]}
    """), font=("Arial", 18), text_color="White").pack(pady=10)
                        
                    elif Ymholiadau[i][4] == "Derbynydd":  # If SentFrom field = Cwsmer, then show customerid
                        ReceptionistCursor.execute("SELECT Name, Surname, Username FROM ReceptionistTable WHERE ReceptionistID = ?", (Ymholiadau[i][3],))
                        EnwCyfenwSentFrom = ReceptionistCursor.fetchall()
                        print(f"Sent from {EnwCyfenwSentFrom}")
                        customtkinter.CTkLabel(frame, text=(f"""Enw : {EnwCyfenwSentFrom[0][0]} , Cyfenw : {EnwCyfenwSentFrom[0][1]}
    Enw Defnyddiwr : {EnwCyfenwSentFrom[0][2]}
    Id Ymholiad : {Ymholiadau[i][0]}
    """), font=("Arial", 18), text_color="White").pack(pady=10)                   
                    IdYmholiadEntry = customtkinter.CTkEntry(frame, placeholder_text="Id Ymholiad", font=("Arial", 16), width=200, height=20)
                    IdYmholiadEntry.pack(pady=20)

        else:
            customtkinter.CTkLabel(frame,text="Nad ydych efo unrhyw ymholiadau yn anffodus",font=("Roboto",36),text_color="Red").pack()

    elif LefelMynediad=="Derbynydd":
        YmholiCursor.execute("SELECT YmholiadID, Neges, DriverID, CustomerID, SentFrom FROM YmholiTable WHERE ReceptionistID = ? AND Status = ? AND SentFROM != ? ", (userid, "Heb Gweld","Derbynydd"))
        Ymholiadau = YmholiCursor.fetchall()
        YmholiDataBase.commit()
        print("HELOEFIEONR",Ymholiadau)

        # Repeat through all records fetched
        if Ymholiadau:
            for i in range(len(Ymholiadau)):
                # Only go through records that aren't sent from derbynydd
                if Ymholiadau[i][4] != "Derbynydd":
                    print("IloveALEXTURNER")
                    # If it was sent from a customer, select the customerid from the table to know the name and surname of whoever sent
                    if Ymholiadau[i][4] == "Gyrrwr":  # If SentFrom field = Cwsmer, then show customerid
                        DriverCursor.execute("SELECT Name, Surname, Username FROM DriversTable WHERE DriversID = ?", (Ymholiadau[i][2],))
                        EnwCyfenwSentFrom = DriverCursor.fetchall()
                        print(f"Sent from {EnwCyfenwSentFrom}")
                        customtkinter.CTkLabel(frame, text=(f"""Enw : {EnwCyfenwSentFrom[0][0]} , Cyfenw : {EnwCyfenwSentFrom[0][1]}
    Enw Defnyddiwr : {EnwCyfenwSentFrom[0][2]}
    Id Ymholiad : {Ymholiadau[i][0]}
    """), font=("Arial", 18), text_color="White").pack(pady=10)
                        
                    elif Ymholiadau[i][4] == "Cwsmer":  # If SentFrom field = Cwsmer, then show customerid
                        CustomerCursor.execute("SELECT Name, Surname, Username FROM CustomersTable WHERE CustomerID = ?", (Ymholiadau[i][3],))
                        EnwCyfenwSentFrom = CustomerCursor.fetchall()
                        print(f"Sent from {EnwCyfenwSentFrom}")
                        customtkinter.CTkLabel(frame, text=(f"""Enw : {EnwCyfenwSentFrom[0][0]} , Cyfenw : {EnwCyfenwSentFrom[0][1]}
    Enw Defnyddiwr : {EnwCyfenwSentFrom[0][2]}
    Id Ymholiad : {Ymholiadau[0][0]}
    """), font=("Arial", 18), text_color="White").pack(pady=10)
                   

                    IdYmholiadEntry = customtkinter.CTkEntry(frame, placeholder_text="Id Ymholiad", font=("Arial", 16), width=200, height=20)
                    IdYmholiadEntry.pack(pady=20)

        else:
            customtkinter.CTkLabel(frame,text="Nad ydych efo unrhyw ymholiadau yn anffodus",font=("Roboto",36),text_color="Red").pack()


    if LefelMynediad=="Cwsmer":
        customtkinter.CTkButton(frame,text="Catref",font=("Monaco",18),fg_color="Green",command=lambda: CustomerHomePage(userid)).pack()
    elif LefelMynediad=="Gyrrwr":
        customtkinter.CTkButton(frame,text="Catref",font=("Monaco",18),fg_color="Green",command=lambda: DriversHomePage(userid)).pack()
    elif LefelMynediad=="Derbynydd":
        customtkinter.CTkButton(frame,text="Catref",font=("Monaco",18),fg_color="Green",command=lambda: ReceptionistHomePage(userid)).pack()

    def on_enter():
        GweldYmholiad(userid, LefelMynediad,EnwCyfenwSentFrom)

    EntryButton = customtkinter.CTkButton(frame, text="Enter", font=("Monaco", 18), fg_color="Red", command=on_enter)
    EntryButton.pack(pady=10)


def GosodWediCyflawni(driverid, idBwciad):
    print(f"ID gyrrwr {driverid}")
    print(f"Id bwciad {idBwciad}")

    BookingsCursor.execute("SELECT BookingID , Date, CustomerID FROM BookingsTable WHERE Status = ? AND WediGorffen = ? AND BookingID = ?", ("Not Available","Na",idBwciad))
    BwciadauDiweddaru=BookingsCursor.fetchall()

    if idBwciad=="":
        messagebox.showinfo("Gwall","Rhaid mewnbynnu id Bwciad")
        DiweddaruBwciad(driverid)
        return

    if BwciadauDiweddaru:
        if BwciadauDiweddaru[0][0]==idBwciad:
            BookingsCursor.execute("UPDATE BookingsTable SET WediGorffen = ? WHERE BookingID = ?",("Ydy",idBwciad))
            bookingsdatabase.commit()
            messagebox.showinfo("Diweddaru Bwciad","Wedi diweddaru")
            DriversHomePage(driverid)
    else:
        messagebox.showinfo("Diweddaru Bwaciad","Nid oes bwciad heb ei gorffen efo'r id bwciad yn bodoli")
        return

def  DiweddaruBwciad(driverid):
    for Widget in root.winfo_children():
        Widget.destroy()

    root.title("Diweddaru bwciadau")
    frame=customtkinter.CTkFrame(root, fg_color="#8692F5", bg_color="#8692F5")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    customtkinter.CTkLabel(frame,text="Ysgol Moduro Normansell",font=("Century Gothic",45),text_color="White").pack()
    customtkinter.CTkLabel(frame,text="Diweddaru bwciadau",font=("Roboto",36),text_color="White").pack()
    customtkinter.CTkLabel(frame,text="Mewnbynnwch id yr bwciad i gosod fel 'wedi cyflawni' ",font=("Arial",18),text_color="White").pack()

    BookingsCursor.execute("SELECT BookingID , Date, CustomerID FROM BookingsTable WHERE Status = ? AND WediGorffen = ? AND DriverID = ?", ("Not Available","Na",driverid))
    BwciadauDiweddaru=BookingsCursor.fetchall()

    if BwciadauDiweddaru:
        customtkinter.CTkLabel(frame,text="Eich bwciadau",font=("Roboto",24),text_color="White").pack()
    else:
        customtkinter.CTkLabel(frame,text="Nad ydych efo unrhyw bwciadau sydd wedi marcio fel 'heb gorffen'",font=("Roboto",24),text_color="Red").pack(8)
    
    for i in range(len(BwciadauDiweddaru)):
        CustomerCursor.execute("SELECT Name , Surname , Username FROM CustomersTable WHERE CustomerID = ?",(BwciadauDiweddaru[i][2],))
        EnwCyfenwCwsmer=CustomerCursor.fetchall()
        CustomerDataBase.commit
        customtkinter.CTkLabel(frame,text=(f""" Id bwciad : {BwciadauDiweddaru[i][0]}
Dyddiad Bwciad : {BwciadauDiweddaru[i][1]}
Manylion Cwsmer : {EnwCyfenwCwsmer[0][0]} , {EnwCyfenwCwsmer[0][1]} , {EnwCyfenwCwsmer[0][2]}
"""),font=("Arial",14)).pack()

    IdBwciadEntry=customtkinter.CTkEntry(frame,placeholder_text="Id bwciad",font=("Arial",14))
    IdBwciadEntry.pack()

    BotwmDiweddaru=customtkinter.CTkButton(frame,text="Diweddaru",font=("Monaco",14),fg_color="Red",command= lambda: GosodWediCyflawni(driverid,IdBwciadEntry.get()))
    BotwmDiweddaru.pack()

    BotwmCatref=customtkinter.CTkButton(frame,text="Catref",font=("Monaco",14),fg_color="Green",command=lambda: DriversHomePage(driverid))
    BotwmCatref.pack()
    
def DileuCwestiwnTheori(driverid,IdCwestiwn):
    if IdCwestiwn=="":
        messagebox.showinfo("Gwall","Rhaid mewnbynnu id cwestiwn i dileu")
        DewisCwestiwnDileu(driverid)
        return
    RevisionCursor.execute("SELECT RevisionID from RevisionTable WHERE RevisionID = ?",(IdCwestiwn,))
    IdCwestiwnDilys=RevisionCursor.fetchone()
    if IdCwestiwnDilys:
        pass
    else:
        messagebox.showinfo("Gwall","Nid oes cwestiwn theori i dileu sy'n cyfateb ir id wedi mewnbynnu !")
        DewisCwestiwnDileu(driverid)
        return

    RevisionCursor.execute("DELETE FROM RevisionTable WHERE RevisionID = ?",(IdCwestiwn,))
    Revisiondatabase.commit()
    messagebox.showinfo("Dileu Cwestiwn","Mae'r cwestiwn wedi cael ei dileu")
    DriversHomePage(driverid)
    

def DewisCwestiwnDileu(driverid,Catogri):
 
    RevisionCursor.execute("SELECT RevisionID , Question FROM RevisionTable WHERE Catogry = ?",(Catogri,))
    CwestiynnauIdCatogri=RevisionCursor.fetchall()
    print(CwestiynnauIdCatogri)

    for Widget in root.winfo_children():
        Widget.destroy()

    root.title("Dewis cwestiwn i dileu")

    frame=customtkinter.CTkFrame(root, fg_color="#8692F5", bg_color="#8692F5")
    frame.pack(fill="both", expand=True, padx=20, pady=20)   

    customtkinter.CTkLabel(frame,text="Ysgol Moduro Normansell",font=("Century Gothic",36),text_color="White").pack()

    customtkinter.CTkLabel(frame,text="Dewis cwestiwn i dileu",font=("Roboto",18),text_color="White").pack()

    BoxCwestiynnau=customtkinter.CTkTextbox(frame,width=750,height=400)
    BoxCwestiynnau.pack() 

    for i in range (len(CwestiynnauIdCatogri)):
        BoxCwestiynnau.insert(tk.END, f""" ID : {CwestiynnauIdCatogri[i][0]} 
Cwestiwn : {CwestiynnauIdCatogri[i][1]}\n""")
        
    IdCwestiwnEntry=customtkinter.CTkEntry(frame,placeholder_text="Mewnbynnwch id yr cwestiwn i dileu",font=("Arial",16))
    IdCwestiwnEntry.pack()

    BotwmDewis=customtkinter.CTkButton(frame,text="Dileu",font=("Monaco",18),fg_color="Green",command=lambda: DileuCwestiwnTheori(driverid,IdCwestiwnEntry.get()))
    BotwmDewis.pack()

    customtkinter.CTkButton(frame,text="Catref",font=("Monaco",18),fg_color="Red",command=lambda: DriversHomePage(driverid)).pack() 

def DewisCatogriDileu (Driverid):
    for Widget in root.winfo_children():
        Widget.destroy()

    root.title("Dewis catogri cwestiwn i dileu")

    frame=customtkinter.CTkFrame(root, fg_color="#8692F5", bg_color="#8692F5")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    customtkinter.CTkLabel(frame,text="Ysgol Moduro Normansell",font=("Century Gothic",36),text_color="White").pack()

    customtkinter.CTkLabel(frame,text="""Mewnbynnwch catogri i dewis 
(Alertness, Awarness, Hazard Awarness neu Motorway rules)""",font=("Roboto",20),text_color="White").pack()

    CatogriComboBox=customtkinter.CTkComboBox(frame,values=["Alertness","Awarness","Hazard Awarness","Motorway rules"])
    CatogriComboBox.pack(pady=25)

    ButtonDewisCatogri=customtkinter.CTkButton(frame,text="Dewis",font=("Monaco",18),fg_color="Green",command=lambda: DewisCwestiwnDileu(Driverid,CatogriComboBox.get()))
    ButtonDewisCatogri.pack(pady=25)

    customtkinter.CTkButton(frame,text="Catref",font=("Monaco",18),fg_color="Red",command=lambda: DriversHomePage(Driverid)).pack(pady=25) 


def DriversHomePage(driverid):
    DriverCursor.execute("SELECT Name FROM DriversTable WHERE DriversID = ? ",(driverid))
    UserNameAndSurname=DriverCursor.fetchone()
    DriverDatabase.commit()

    for Widget in root.winfo_children():
        Widget.destroy()
    

    DriversHomePageElements=[["Label","Ysgol Moduro Normansell","Roboto",45,"White"],
                              ["Label",f"Welcome {UserNameAndSurname[0]}","Roboto",36,"White" ],
                              ["Label","Beth hoffwch wneud","Arial",18,"White"],
                              ["Button","Dyddiadur","Monaco",24,"Green",lambda: DyddiadurGyrrwr(driverid)],
                              ["Button","Bwciadau","Monaco",24,"Blue",lambda: BwciadauGyrrwr(driverid)],
                              ["Button","Diweddaru Bwciadau","Monaco",24,"Green",lambda: DiweddaruBwciad(driverid)],
                              ["Button","Ymholi","Monaco",24,"Blue",lambda: CatrefYmholi(driverid,"Gyrrwr")],
                              ["Button","Gweld Ymholiadau","Monaco",24,"Green",lambda: DewisYmholiad(driverid,"Gyrrwr")],
                              ["Button","Ffurflen Adolygu","Monaco",24,"Blue",lambda: RevisionHome(driverid,"Gyrrwr")],
                              ["Button","Ychwanegu Cwestiynnau theori","Monaco",24,"Green",lambda: YchwaneguCwestiynnauTheori(driverid)],
                              ["Button","Gweld Cwestiynnau theori","Monaco",24,"Blue",lambda: GweldCwestiynnauTheori(driverid)],
                              ["Button","Dileu Cwestiynnau theori","Monaco",24,"Green",lambda: DewisCatogriDileu(driverid)],
                              ["Button","Logio Allan","Monaco",24,"Red",lambda: LoginPage()]
                              ]
    DriversHomePageWindow = MakeWindow(root, "DriversHomePage",  DriversHomePageElements)


def ArddangosCyfrifGyrrwyrCadarnhau():
    global CadarnhauCyfrifGyrrwyrPage
    DriverCursor.execute("SELECT Name ,Username, DriversID FROM DriversTable WHERE Confirmed = ?",(0,))
    NamesAndIdToVerify=DriverCursor.fetchall()
    DriverDatabase.commit()
    print(NamesAndIdToVerify)  
    CadarnhauCyfrifGyrrwyrPage.add_label_string("""Enw Gyrrwr      Enw-defnyddiwr Gyrrwr      ID gyrrwr
--------------       --------------------      --------------""")  
    for i in range (len(NamesAndIdToVerify)):
        DriverName=NamesAndIdToVerify[i][0]
        DriverUsername=NamesAndIdToVerify[i][1]
        DriverID=NamesAndIdToVerify[i][2]
        print(DriverName)
        print(DriverUsername)
        print(DriverID)
        CadarnhauCyfrifGyrrwyrPage.add_label_string(f"{DriverName}      {DriverUsername}       {DriverID}")

def CadarnhauGyrrwrID(ReceptionistID):
    global CadarnhauCyfrifGyrrwyrPage
    IdGyrrwrCadarnhau=CadarnhauCyfrifGyrrwyrPage.get_entry_value("ID Gyrrwr")
    if IdGyrrwrCadarnhau=="":
        messagebox.showinfo("Gwall","Rhaid mewnbynnu id gyrrwr i dileu")
        DefnyddiwrIdDileu(ReceptionistID)
        return    
    DriverCursor.execute("SELECT DriversID FROM DriversTable WHERE DriversID = ?", (IdGyrrwrCadarnhau,))
    IdGyrrwrDilys=DriverCursor.fetchone()
    if IdGyrrwrDilys:
        pass
    else:
        messagebox.showinfo("Gwall","Nid yw gyrrwr yn bodoli efo'r id wedi mewnbynnu")
        DefnyddiwrIdDileu(ReceptionistID)
        return

    DriverCursor.execute("UPDATE DriversTable SET Confirmed = ? WHERE DriversID=?",(1,IdGyrrwrCadarnhau))
    DriverDatabase.commit()

    messagebox.showinfo("Llwyddiant","Mae'r gyrrwr wedi cael ei cadarnhau")
    ReceptionistHomePage(ReceptionistID)
        
        
def DefnyddiwrIdDileu(ReceptionistID):
    global DiweddaruCyfrifionCwsmeriaidAcGyrrwyrPage
    IdDefnyddiwrDileu = DiweddaruCyfrifionCwsmeriaidAcGyrrwyrPage.get_entry_value("Id")   
    IdDefnyddiwrDileu=str(IdDefnyddiwrDileu)
    LefelMynediad = DiweddaruCyfrifionCwsmeriaidAcGyrrwyrPage.get_combo_value("Cwsmeriaid")

    if LefelMynediad == "Gyrrwyr":
        print("helo")
        DriverCursor.execute("DELETE FROM DriversTable WHERE DriversID = ?", (IdDefnyddiwrDileu,))
        DriverDatabase.commit()
        messagebox.showinfo("Dileu Defnyddiwr","Mae'r gyrrwr wedi cael ei dileu")
        ReceptionistHomePage(ReceptionistID)
    
    elif LefelMynediad == "Cwsmeriaid":
        print("goodbye")
        CustomerCursor.execute("DELETE FROM CustomersTable WHERE CustomerID = ? ",(IdDefnyddiwrDileu,))
        CustomerDataBase.commit()
        messagebox.showinfo("Dileu defyddiwr","Mae'r cwsmer wedi cael ei dileu")
        ReceptionistHomePage(ReceptionistID)

def CadarnhauCyfrifGyrrwyr(ReceptionistID):
    for Widget in root.winfo_children():
        Widget.destroy()
   
    CadarnhauCyfrifGyrrwyrPageElements=[["Label","Ysgol Moduro Normansell","Century Gothic",56,"White"],
                                        ["Label","Cadarnhau Cyfrif Gyrrwyr","Roboto",36,"White"],
                                        ["Label","Mewnbynnwch ID gyrrwr i cadarnhau isod","Arial",18,"White"],
                                        ["EntryBox","ID Gyrrwr",200,20],
                                        ["Button","Cadarnhau","Monaco",24,"Green",lambda: CadarnhauGyrrwrID(ReceptionistID)],
                                        ["Button","Catref","Monaco",24,"Red",lambda: ReceptionistHomePage(ReceptionistID)],
                                        

                                        ]
    
    global CadarnhauCyfrifGyrrwyrPage
    CadarnhauCyfrifGyrrwyrPage=MakeWindow(root,"Cadarnhau Cyfrif Gyrrwyr",CadarnhauCyfrifGyrrwyrPageElements)
    ArddangosCyfrifGyrrwyrCadarnhau()

def DewisLefelMynediadDiweddaru(ReceptionistID):
    global DiweddaruCyfrifionCwsmeriaidAcGyrrwyrPage
    LefelMynediad=DiweddaruCyfrifionCwsmeriaidAcGyrrwyrPage.get_combo_value("Gyrrwyr")
    Enw=DiweddaruCyfrifionCwsmeriaidAcGyrrwyrPage.get_entry_value("Mewnbynnwch Enw yr defnyddiwr i dileu")
    Cyfenw=DiweddaruCyfrifionCwsmeriaidAcGyrrwyrPage.get_entry_value("Mewnbynnwch Cyfenw yr defnyddiwr i dileu")

    if Enw =="" and Cyfenw=="":
        messagebox.showinfo("Gwall","Rhaid mewnbynnu enw ac cyfenw defnyddiwr i dileu")
        DiweddaruCyfrifionCwsmeriaidAcGyrrwyr(ReceptionistID)
        return
    elif Enw=="":
        messagebox.showinfo("Gwall","Rhaid mewnbynnu enw defnyddiwr i dileu")
        DiweddaruCyfrifionCwsmeriaidAcGyrrwyr(ReceptionistID)
        return
    elif Cyfenw=="":
        messagebox.showinfo("Gwall","Rhaid mewnbynnu cyfenw defnyddiwr i dileu")
        DiweddaruCyfrifionCwsmeriaidAcGyrrwyr(ReceptionistID)
        return


    if LefelMynediad=="Gyrrwyr":
        DriverCursor.execute("SELECT Name, Username, DriversID FROM DriversTable WHERE Name = ? AND Surname = ?", (Enw, Cyfenw))
        AllDriversDetails=DriverCursor.fetchall()
        DriverDatabase.commit()
        if AllDriversDetails:
            for i in range (len(AllDriversDetails)):
                print(AllDriversDetails[i])
                DiweddaruCyfrifionCwsmeriaidAcGyrrwyrPage.add_label_string(f"""Enw: {AllDriversDetails[i][0]} 
Enw-defnyddiwr: {AllDriversDetails[i][1]} 
DriverID: {AllDriversDetails[i][2]}
""")    
        else:
            messagebox.showinfo("Gwall","Nid oes gyrrwr yn bodoli efo'r enw ac cyfenw sydd wedi mewnbynnu")
            DiweddaruCyfrifionCwsmeriaidAcGyrrwyr(ReceptionistID)
            return
        
    elif LefelMynediad=="Cwsmeriaid":
        CustomerCursor.execute("SELECT Name , Username , CustomerID FROM CustomersTable WHERE Name = ? AND Surname = ?",(Enw,Cyfenw))
        AllCustomerDetails=CustomerCursor.fetchall()
        CustomerDataBase.commit()
        if AllCustomerDetails:
            for i in range (len(AllCustomerDetails)):
                print(AllCustomerDetails[i])
                DiweddaruCyfrifionCwsmeriaidAcGyrrwyrPage.add_label_string(f"""Enw: {AllCustomerDetails[i][0]} 
Enw-defnyddiwr: {AllCustomerDetails[i][1]} 
CustomerID: {AllCustomerDetails[i][2]}
""")
        else:
            messagebox.showinfo("Gwall","Nid oes cwsmer yn bodoli efo'r enw ac cyfenw sydd wedi mewnbynnu")
            DiweddaruCyfrifionCwsmeriaidAcGyrrwyr(ReceptionistID)
            return

#prints all names username and id of userse with selected lefel mynediad 
#user inputs id of driver to delete from other functions with enter button and entrybox


def DiweddaruCyfrifionCwsmeriaidAcGyrrwyr(ReceptionistID):
    for Widget in root.winfo_children():
        Widget.destroy()
    global DiweddaruCyfrifionCwsmeriaidAcGyrrwyrPage
    
    DiweddaruCyfrifionCwsmeriaidAcGyrrwyrPageElements=[["Label","Ysgol Moduro Normansell","Century Gothic",56,"White"],
                                                     #  ["Button","Catref","Monaco",18,"Red",lambda: ReceptionistHomePage(ReceptionistID)],
                                                       ["Label", "Diwedaru Cyfrifion","Roboto",36,"White"],
                                                       ["Label","Dewiwch Lefel mynediad yr defnyddiwr i dileu","Arial",18,"White"],
                                                       ["ComboBox","Gyrrwyr","Cwsmeriaid",""],
                                                       ["EntryBox","Mewnbynnwch Enw yr defnyddiwr i dileu",300,20],
                                                       ["EntryBox","Mewnbynnwch Cyfenw yr defnyddiwr i dileu",300,20],
                                                       ["Button","Gweld","Monaco",18,"Green",lambda: DewisLefelMynediadDiweddaru(ReceptionistID)],
                                                       ["Label","Mewnbynnwch Id yr defnyddiwr i dileu","Arial",18,"White"],
                                                       ["EntryBox","Id",200,20],
                                                       ["Label","Dewiswch lefel mynediad yr defnyddiwr i dileu","Arial",18,"White"],
                                                       ["ComboBox","Cwsmeriaid","Gyrrwyr",""],
                                                       ["Button","Enter","Monaco",18,"Green",lambda: DefnyddiwrIdDileu(ReceptionistID)],
                                                       ["Button","Catref","Monaco",18,"Red",lambda: ReceptionistHomePage(ReceptionistID)]
                                                       ]

    DiweddaruCyfrifionCwsmeriaidAcGyrrwyrPage=MakeWindow(root,"Diweddaru Cyfrifion",DiweddaruCyfrifionCwsmeriaidAcGyrrwyrPageElements)

def DiweddaruCredit(ReceptionistId):
    global DiweddaruCreditCwsmeriaidPage

    CustomerIdDiweddaru = DiweddaruCreditCwsmeriaidPage.get_entry_value("CustomerId")
    CreditDiweddaruCwsmer = DiweddaruCreditCwsmeriaidPage.get_entry_value("Mewnbynnwch faint o credit i ychwanegu")

    CustomerCursor.execute("SELECT Credit FROM CustomersTable WHERE CustomerID = ?", (CustomerIdDiweddaru,))
    CurrentCustomerCredit = CustomerCursor.fetchone()
    CustomerDataBase.commit()

    if CurrentCustomerCredit is not None:
        # If CurrentCustomerCredit is not None, convert it to an integer and add it to CreditDiweddaruCwsmer
        CurrentCustomerCredit = int(CurrentCustomerCredit[0])
        CreditDiweddaruCwsmer = int(CreditDiweddaruCwsmer) + CurrentCustomerCredit
        print(CreditDiweddaruCwsmer)
    else:
        print("Customer not found or has no credit.")
    
    CustomerCursor.execute("UPDATE CustomersTable SET Credit = ? WHERE CustomerID = ?",(CreditDiweddaruCwsmer,CustomerIdDiweddaru))
    CustomerDataBase.commit()
    messagebox.showinfo("Diweddaru Credit","Mae'r credit wedi cael ei diweddaru")
    ReceptionistHomePage(ReceptionistId)


def ManylionCwsmerDiweddaruCredit(ReceptionistID):
    global DiweddaruCreditCwsmeriaidPage

    EnwCwsmer=DiweddaruCreditCwsmeriaidPage.get_entry_value("Enw Cwsmer")
    CyfenwCwsmer=DiweddaruCreditCwsmeriaidPage.get_entry_value("Cyfenw Cwsmer")

    CustomerCursor.execute("SELECT CustomerID , Username , Credit  FROM CustomersTable WHERE Name = ? AND Surname = ?",(EnwCwsmer,CyfenwCwsmer))
    ManylionCwsmer=CustomerCursor.fetchall()
    CustomerDataBase.commit()
    
    for i in range (len(ManylionCwsmer)):
        DiweddaruCreditCwsmeriaidPage.add_label_string(f"""Enw Cwsmer: {EnwCwsmer}  
Cyfenw Cwsmer : {CyfenwCwsmer}  
Id Cwsmer : {ManylionCwsmer[i][0]}  
EnwDefnyddiwr : {ManylionCwsmer[i][1]} 
Credit : {ManylionCwsmer[i][2]}
""")


def DiweddaruCreditCwsmeriaid(ReceptionistID):
    for Widget in root.winfo_children():
        Widget.destroy()
    global DiweddaruCreditCwsmeriaidPage

    DiweddaruCreditCwsmeriaidElements=[["Label","Ysgol Moduro Normansell","Century Gothic",54,"White"],
                                       ["Label","Diweddaru Credit Cwmseriaid ","Monaco",36,"white"],
                                       ["Label","Mewnbynnwch enw ac cyfenw yr cwsmer i diweddaru credit","Arial",18,"White"],
                                       ["EntryBox","Enw Cwsmer",200,20],
                                       ["EntryBox","Cyfenw Cwsmer",200,20],
                                       ["Button","Gweld","Monaco",18,"Red",lambda: ManylionCwsmerDiweddaruCredit(ReceptionistID)],
                                       ["Label","Mewnbynnwch CustomerId yr defnyddiwr i diweddaru credit","Arial",18,"White"],
                                       ["EntryBox","CustomerId",200,20],
                                       ["EntryBox","Mewnbynnwch faint o credit i ychwanegu",300,20],
                                       ["Button","Diweddaru","Monaco",18,"Green",lambda: DiweddaruCredit(ReceptionistID)],
                                       ["Button","Catref","Monaco",18,"Red",lambda: ReceptionistHomePage(ReceptionistID)]
                                       ]

    DiweddaruCreditCwsmeriaidPage=MakeWindow(root,"Diweddaru Credit Cwsmeriaid",DiweddaruCreditCwsmeriaidElements)

def ReceptionistHomePage(ReceptionistID):
    for Widget in root.winfo_children():
        Widget.destroy()

    ReceptionistCursor.execute("SELECT Name FROM ReceptionistTable WHERE ReceptionistID = ?",(ReceptionistID,))
    ReceptionistName=ReceptionistCursor.fetchone()
    ReceptionistDataBase.commit()

    ReceptionistHomePage_Elements=[["Label","Ysgol Moduro Normansell","Century Gothic",56,"White"],
                                   ["Label",f"Croeso {ReceptionistName[0]}","Roboto",36,"White"],
                                   ["Label","Beth hoffwch wneud ?","Arial",18,"White"],
                                   ["Button","Cadarnhau cyfrif gyrrwyr","Monaco",36,"Blue",lambda: CadarnhauCyfrifGyrrwyr(ReceptionistID)],
                                   ["Button","Diweddaru Credit cwsmeriaid","Monaco",36,"Green",lambda: DiweddaruCreditCwsmeriaid(ReceptionistID)],
                                   ["Button","Diweddaru cyfrifion cwsmeriaid ac gyrrwyr","Monaco",36,"Blue",lambda: DiweddaruCyfrifionCwsmeriaidAcGyrrwyr(ReceptionistID)],
                                   ["Button","Gweld Ymholidau","Monaco",36,"Green",lambda: DewisYmholiad(ReceptionistID,"Derbynydd")],
                                   ["Button","Ymholi","Monaco",36,"Green",lambda: CatrefYmholi(ReceptionistID,"Derbynydd")],
                                   ["Button","Logio Allan","Monaco",36,"Red",lambda: LoginPage()]
                                   
                                   ]

    ReceptionistHomePage_=MakeWindow(root,"Catref derbynydd",ReceptionistHomePage_Elements)

def AccountLoginCheck():
    global LoginPageWindow
   
    
#uses function get_entry_values with instance of class LoginPageWindow in , uses 'username' as is placeholder text to the entry box in order to 
#get the input  ('Username' : userinput)
    username = LoginPageWindow.get_entry_value("Username")
    password = LoginPageWindow.get_entry_value("Password")
    EntryLevel = LoginPageWindow.get_combo_value("Driver")
    for widget in root.winfo_children():
        widget.destroy()
    
    #LoginPage(root)
    if EntryLevel=="Customer":
#dewis customerId ac enw ar sail confod lle mae maes Userrname yn cyfateb ir enw-defnyddiwr wedi mewnbynnu 
#dewis oddia ar  tabl cwsmeriaid oherwydd dewir defnyddiwr lefel mynediad cwsmeriaid 
        CustomerCursor.execute("SELECT CustomerID, Name FROM CustomersTable WHERE Username = ? ", (username,))
        UsernameCustomerLogIn=CustomerCursor.fetchone()
#dewis customerid ac enw yn y confod lle mae maes password yn cyfateb ir password wedi mewnbynnu gan yr  defnyddiwr
        CustomerCursor.execute("SELECT CustomerID , Name FROM CustomersTable WHERE Password = ?",(password,))
        passwordCustomerLogIn=CustomerCursor.fetchone()
        CustomerDataBase.commit()
#dewis ar sail username ac password er mwyn gweld os mae username mae'r defnyddiwr wedi mewnbynnu yn bodoli ar tabl cwsmeraidi ac felly yn cyfateb i cyfrif cwsmer
#Gellir hefyd weld os mae'r cyfrianir yn cyfateb ac felly gellir rhoi neges gwall fwy penodol ir defnyddiwr wrth dilysu er enghraifft os oes cofnod yn bodoli lle mae'r enwdefnyddiwr yn cyfateb ond nad oes cofndo yn bodoli lel mae cyfrinair yn cyfateb mae'r cyfrianri yn anghywir felly gellir rhoi neeges gwall penodol yn adrodd fod cyfrianir yn anghywir
        
#os oes customerid ac enw wedi darganfod ar sail mewnbwn defnyddiwr ar gyfer enw-defnyddiwr
        if UsernameCustomerLogIn:
#os oes customer id ac enw hefyd wedi darganfod ar sail mewnbwn defnyddiwr ar gyfer cyfrianir rydym yn gwybod fod cyfirf yn bodoli efo enw defnyddiwr ac cyfrianir wed imewnbynnu ac felly gellir galw ffrwythiant er mwyn dangos ffurflen catref ir cwsmer
            if passwordCustomerLogIn:
                messagebox.showinfo("Llwyddiant",f"Croeso {UsernameCustomerLogIn[1]}")
                customerid=UsernameCustomerLogIn[0]
                CustomerHomePage(customerid)
                
            else:
#os oes customer id ac enw wedi darganfod ar sail maes username ond nid ar sail yr cyfrianir rydym yn gwybod fod denfyddiwr yn bodoli efo yr enwdefnyddiwr ond nad yw'r cyfrianir wedi mewnbynnu yn cyfateb ir cyfrif yr lefel mynediad
                messagebox.showinfo("Gwall","Mae cwsmer yn bodoli efo enw defnyddiwr , nid yw'r cyfrianir yn cyfateb")
                LoginPage()
#os yw customer id ac enw wedi darganfod ar sail cyfrianir ac felly mae'r cyfrianir yn cyfayeb i cyfrianir cyfrif cwsmer
        elif passwordCustomerLogIn:
            if UsernameCustomerLogIn:
                pass
#os nad yw'r enw denfydidwr yn cyfateb i cyfrif cwsmer ond mae'r cyfrianir yn rydym yn gwybod fod enw denfyddiwr yn anghywir ac gellir rhoi negs gwall penodol
            else:
                messagebox.showinfo("Gwall","Mae cwsmer efo yr cyfrinair yn bodoli , nid yw'r enw defnyddiwr yn cyfateb ")
                LoginPage()
        else:
            messagebox.showinfo("Gwall","Nid yw denfyddiwr yn bodoli efo manylion sydd wedi mewnbynnu")
            LoginPage()

    elif EntryLevel=="Driver":
        DriverCursor.execute("SELECT DriversID, Name , Confirmed FROM DriversTable WHERE Username = ? ", (username,))
        UsernameDriverLogIn=DriverCursor.fetchone()
#dewis customerid ac enw yn y confod lle mae maes password yn cyfateb ir password wedi mewnbynnu gan yr  defnyddiwr
        DriverCursor.execute("SELECT DriversID , Name , Confirmed FROM DriversTable WHERE Password = ?",(password,))
        passwordDriverLogIn=DriverCursor.fetchone()
        CustomerDataBase.commit()
#dewis ar sail username ac password er mwyn gweld os mae username mae'r defnyddiwr wedi mewnbynnu yn bodoli ar tabl cwsmeraidi ac felly yn cyfateb i cyfrif cwsmer
#Gellir hefyd weld os mae'r cyfrianir yn cyfateb ac felly gellir rhoi neges gwall fwy penodol ir defnyddiwr wrth dilysu er enghraifft os oes cofnod yn bodoli lle mae'r enwdefnyddiwr yn cyfateb ond nad oes cofndo yn bodoli lel mae cyfrinair yn cyfateb mae'r cyfrianri yn anghywir felly gellir rhoi neeges gwall penodol yn adrodd fod cyfrianir yn anghywir
        
#os oes customerid ac enw wedi darganfod ar sail mewnbwn defnyddiwr ar gyfer enw-defnyddiwr
        if UsernameDriverLogIn:
#os oes customer id ac enw hefyd wedi darganfod ar sail mewnbwn defnyddiwr ar gyfer cyfrianir rydym yn gwybod fod cyfirf yn bodoli efo enw defnyddiwr ac cyfrianir wed imewnbynnu ac felly gellir galw ffrwythiant er mwyn dangos ffurflen catref ir cwsmer
            if passwordDriverLogIn:
              
                #os nad ywr cyfrif gyrrwr wedi cadarnhau 
                print(UsernameDriverLogIn[2])
                if int(UsernameDriverLogIn[2]) ==1:
                    pass
                else:
                    messagebox.showinfo("Gwall","Rhaid aros ir cyfrif cael ei cadarnhau gan yr derbynydd")
                    LoginPage()
                    return
              #  if UsernameDriverLogIn[2]
                messagebox.showinfo("Llwyddiant",f"Croeso {UsernameDriverLogIn[1]}")
                DriverID=UsernameDriverLogIn[0]
                DriversHomePage(DriverID)
                
            else:
#os oes customer id ac enw wedi darganfod ar sail maes username ond nid ar sail yr cyfrianir rydym yn gwybod fod denfyddiwr yn bodoli efo yr enwdefnyddiwr ond nad yw'r cyfrianir wedi mewnbynnu yn cyfateb ir cyfrif yr lefel mynediad
                messagebox.showinfo("Gwall","Mae gyrrwr yn bodoli efo enw defnyddiwr , nid yw'r cyfrianir yn cyfateb")
                LoginPage()
#os yw customer id ac enw wedi darganfod ar sail cyfrianir ac felly mae'r cyfrianir yn cyfayeb i cyfrianir cyfrif cwsmer
        elif passwordDriverLogIn:
            if UsernameDriverLogIn:
                pass
#os nad yw'r enw denfydidwr yn cyfateb i cyfrif cwsmer ond mae'r cyfrianir yn rydym yn gwybod fod enw denfyddiwr yn anghywir ac gellir rhoi negs gwall penodol
            else:
                messagebox.showinfo("Gwall","Mae gyrrwr efo yr cyfrinair yn bodoli , nid yw'r enw defnyddiwr yn cyfateb ")
                LoginPage()
        else:
            messagebox.showinfo("Gwall","Nid yw gyrrwr yn bodoli efo manylion sydd wedi mewnbynnu")
            LoginPage()

    elif EntryLevel=="Receptionist":
        ReceptionistCursor.execute("SELECT ReceptionistID, Name FROM ReceptionistTable WHERE Username = ? AND Password = ?", (username, password,))
        ReceptionistLogin=ReceptionistCursor.fetchone()
        ReceptionistDataBase.commit()
        if ReceptionistLogin:
            messagebox.showinfo("welcome",f"Welcome {ReceptionistLogin[1]}")
            print(ReceptionistLogin[1])
            # Call CustomerHomePage function
            ReceptionistHomePage(ReceptionistLogin[0][0])
        else:
            messagebox.showinfo("Error","Customer with those details doesnt exist , please try again or create a account !")
            LoginPage()


    



def clear(DictRefrence):
    global CreateAccountWindow
    EntryBoxChange=CreateAccountWindow.get_entry_box(DictRefrence)

def ForgotPasswordCheck():
    global ForgotPasswordPage
    Username=ForgotPasswordPage.get_entry_value("Username")
    Entrylevel=ForgotPasswordPage.get_combo_value("Driver")
    SelectedQuestion=ForgotPasswordPage.get_combo_value("Beth yw enw eich hoff film?")
    UsersAnswer=ForgotPasswordPage.get_entry_value("Eich Ateb")

    NewPassword = ForgotPasswordPage.get_entry_value("Password")
    
    if Username=="" or UsersAnswer=="" or NewPassword=="":
        messagebox.showinfo("Gwall","Rhaid mewnbynnu data ir holl meysydd")
        return

    if len(NewPassword)<12:
        messagebox.showinfo("Gwall","Rhaid ir cyfrinair cynnwys o leiaf 12 cymeriad")
        return
    digitCount = 0
    SpecialCharacterCount = 0

    for item in NewPassword:
        if item.isdigit()==True:
            digitCount+=1
    for item in NewPassword:
        if item in special_characters:
            SpecialCharacterCount+=1

    if digitCount<3:
        messagebox.showinfo("Gwall","Rhaid cynnwys o leiaf tair digid yn yr cyfrinair newydd")
        return
    if SpecialCharacterCount<2:
        messagebox.showinfo("Gwall","Rhaid cynnwys oleaif dau cymeriad arbennig yn yr cyfrinar newydd")
        return


    if Entrylevel == "Customer":
        CustomerCursor.execute("SELECT CustomerID FROM CustomersTable WHERE Username = ? ", (Username, ))
        CustomerIdForgotPassword = CustomerCursor.fetchone()
        CustomerDataBase.commit()
        if CustomerIdForgotPassword:
            CustomerIdForgotPassword = CustomerIdForgotPassword[0]  
        else:
            messagebox.showinfo("Gwall","Nid oes cwsmer yn bodoli efo'r enw defnyddiwr wedi mewnbynu  ")
            return

        CustomerCursor.execute("SELECT CwestiwnGwireddu, AtebGwireddu FROM CustomersTable WHERE CustomerID = ?", (CustomerIdForgotPassword,))
        CwestiwnAcAtebGwireddu = CustomerCursor.fetchall()
        CustomerDataBase.commit()
        CwestiwnGwireddu=CwestiwnAcAtebGwireddu[0][0]
        AtebGwireddu=CwestiwnAcAtebGwireddu[0][1]
        
        if SelectedQuestion!=CwestiwnGwireddu:
            messagebox.showinfo("Gwall","Mae'r cwestiwn sydd wedi cael ei dewis ddim yn cyfateb ir cwestiwn rydych wedi dewis wrth creu cyfrif")
        elif SelectedQuestion==CwestiwnGwireddu and UsersAnswer!=AtebGwireddu:
            messagebox.showinfo("Gwall","Nid ydych wedi mewnbynnu yr ateb cywir ir cwestiwn gwireddu")  
        else:
            CustomerCursor.execute("UPDATE CustomersTable SET Password = ? WHERE CustomerID = ? ",(NewPassword,CustomerIdForgotPassword))
            CustomerDataBase.commit()
            messagebox.showinfo("Llwyddiant","mae eich cyfrianir newydd wedi osod ")
            LoginPage()
      


    elif Entrylevel == "Driver":
        DriverCursor.execute("SELECT DriversID FROM DriversTable WHERE Username = ?", (Username,))
        DriverIdForgotPassword = DriverCursor.fetchone()
        DriverDatabase.commit()  # Assuming it should be DriverDataBase instead of DriverDatabase
        if DriverIdForgotPassword:
            DriverIdForgotPassword=DriverIdForgotPassword[0]
        else:
            messagebox.showinfo("Gwall","Nad oes gyrrwr yn bodoli efo enw defnyddiwr wedi mewnbynnu ")

        DriverCursor.execute("SELECT CwestiwnGwireddu, AtebGwireddu FROM DriversTable WHERE DriversID = ?", (DriverIdForgotPassword,))
        CwestiwnAcAtebGwireddu = DriverCursor.fetchall()
        CustomerDataBase.commit()
        CwestiwnGwireddu=CwestiwnAcAtebGwireddu[0][0]
        AtebGwireddu=CwestiwnAcAtebGwireddu[0][1]
        
        if SelectedQuestion!=CwestiwnGwireddu:
            messagebox.showinfo("Gwall","Mae'r cwestiwn sydd wedi cael ei dewis ddim yn cyfateb ir cwestiwn rydych wedi dewis wrth creu cyfrif")
        elif SelectedQuestion==CwestiwnGwireddu and UsersAnswer!=AtebGwireddu:
            messagebox.showinfo("Gwall","Nid ydych wedi mewnbynnu yr ateb cywir ir cwestiwn gwireddu")  
        else:
            DriverCursor.execute("UPDATE DriversTable SET Password = ? WHERE DriversID = ? ",(NewPassword,DriverIdForgotPassword))
            DriverDatabase.commit()
            messagebox.showinfo("Llwyddiant","mae eich cyfrianir newydd wedi osod ")
            LoginPage()

    elif Entrylevel=="Receptionist":
        ReceptionistCursor.execute("SELECT ReceptionistID FROM ReceptionistTable WHERE Username = ?", (Username,))
        ReceptionistIdForgotPassword = ReceptionistCursor.fetchone()
        ReceptionistDataBase.commit()  # Assuming it should be DriverDataBase instead of DriverDatabase
        ReceptionistIdForgotPassword=ReceptionistIdForgotPassword[0]

        ReceptionistCursor.execute("SELECT CwestiwnGwireddu, AtebGwireddu FROM ReceptionistTable WHERE ReceptionistID = ?", (ReceptionistIdForgotPassword,))
        CwestiwnAcAtebGwireddu = ReceptionistCursor.fetchall()
        ReceptionistDataBase.commit()
        CwestiwnGwireddu=CwestiwnAcAtebGwireddu[0][0]
        AtebGwireddu=CwestiwnAcAtebGwireddu[0][1]
        if SelectedQuestion!=CwestiwnGwireddu:
            messagebox.showinfo("Error","Mae'r cwestiwn sydd wedi cael ei dewis ddim yn cyfateb ir cwestiwn rydych wedi dewis wrth creu cyfrif")
        elif SelectedQuestion==CwestiwnGwireddu and UsersAnswer!=AtebGwireddu:
            messagebox.showinfo("Error","Nid ydych wedi mewnbynnu yr ateb cywir ir cwestiwn gwireddu")  
        else:
            ReceptionistCursor.execute("UPDATE ReceptionistTable SET Password = ? WHERE ReceptionistID = ? ",(NewPassword,ReceptionistIdForgotPassword))
            ReceptionistDataBase.commit()
            messagebox.showinfo("Success","Your new password has been set")
            LoginPage()

      

    

def ForgotPassword():
    global LoginPageWindow
    global ForgotPasswordPage
    for Widget in root.winfo_children():
        Widget.destroy()

    ForgotPasswordElements=[["Label","Ysgol Moduro Normansell","Century Gothic",56,"White"],
                            ["Label","Mewnbynnwch eich manylion presennol","Arial",18,"White"],
                            ["EntryBox","Username",200,30],
                            ["ComboBox","Driver","Customer","Receptionist"],
                            ["Label","Mewnbynnwch cyfrinair newydd","Arial",18,"White"],
                            ["EntryBox","Password",200,30],
                            ["Label","Dewiwch yr cwestiwn gwireddu rydych wedi osod ai ateb","Arial",18,"White"],
                            ["ComboBox","Beth yw enw eich hoff film?","Beth yw enw eich anifail anwes cyntaf ?","Yn pa dinas cawsoch eich geni ? "],
                            ["EntryBox","Eich Ateb",500,50],
                            ["Button","Enter","Monaco",18,"#DF5836",lambda: ForgotPasswordCheck()],
                            ["Button","Catref","Monaco",18,"Red",lambda: LoginPage()]
                            ]

    ForgotPasswordPage=MakeWindow(root,"Tudalen Ailosod Cyfrinair",ForgotPasswordElements)


LoginPageElements = [["Label", "LoginPage", "Century Gothic", 56, "white"],
                     ["Label", "Please fill your account details in below", "Arial", 18, "White"],
                     ["EntryBox", "Username", 200, 30],
                     ["EntryBox", "Password", 200, 30],
                     ["ComboBox", "Driver", "Customer", "Receptionist"],
                     ["Button", "Enter", "Monaco", 16, "green", AccountLoginCheck],
                     ["Button", "Forgot Password", "Monaco", 18, "#DF5836", ForgotPassword],
                     ["Button", "Create Account", "Monaco", 18, "#DF5836", CreateAccount],
                     ]



def LoginPage():
    global LoginPageWindow
    #cael gwared or holl ffurflenni sydd yn cael ei arddangos yn presennol er mwyn sicrhau fod ond yr ffurflen hyn yn cael ei arddangos
    for Widget in root.winfo_children():
        Widget.destroy()
#Creu ystod or dosbarth makewindow pasio paramedrau er mwyn creu tudalen newydd , fydd yr paramederau yn cael ei defnyddio er mwyn ychwanegu eiconau at ffurflen newydd
    LoginPageWindow = MakeWindow(root, "Ffurflen Logio i mewn ",  LoginPageElements)
    
#galw ffrwythiant login page er mwyn cychwyn yr rhaglen , fydd ffurflen logio yn yr ffurflen cyntaf i cael ei arddangos ac yn cysylltu a ffurflenni eraill er mwyn llywio trwy yr rhaglen
LoginPage()

root.mainloop()