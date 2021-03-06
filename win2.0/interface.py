import webbrowser
import platform
import os
import socket
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
import sqlite3
from sqlite3 import Error
import logging
import tkinter as tk
from tkinter import filedialog
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import subprocess
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s :: %(levelname)s - %(message)s',
                    datefmt='%m-%d-%Y %I:%M:%S %p')


def get_result_type0(url, id_num, pwd, path):
    options = Options()
    options.headless = True
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", path)
    profile.set_preference("browser.download.defaultFolder", path)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    profile.set_preference("pdfjs.disabled", True)
    driver = webdriver.Firefox(executable_path='../driver/geckodriver.exe', firefox_profile=profile, options=options)
    driver.get(url)
    if driver.find_elements_by_id("regnum"):
        RegNo = driver.find_element_by_id("regnum")
        RegNo.send_keys(id_num)
        if driver.find_elements_by_id("dob"):
            DoB = driver.find_element_by_id("dob")
            DoB.send_keys(pwd)
        login = driver.find_element_by_name('sub')
        login.click()
        driver.quit()
    elif driver.find_element_by_name("regno"):
        if driver.find_element_by_name("regno"):
            temp = driver.find_element_by_name("regno")
            temp.send_keys(id_num)
        else:
            temp = driver.find_element_by_id("regno")
            temp.send_keys(id_num)
        if driver.find_element_by_id("dob"):
            temp1 = driver.find_element_by_id("dob")
            temp1.send_keys(pwd)
        if driver.find_elements_by_name('but'):
            login = driver.find_element_by_name('but')
            login.click()
        else:
            login = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[5]/td/input')
            login.click()
        driver.quit()
    else:
        textBox.insert(tk.END, "Something missing Contact dev\n")
        textBox.see(tk.END)
    if platform.system() in "Windows":
        os.system("Taskkill /IM firefox.exe /F")


def log(exception, reg, value):
    error_data = 'Invalid Date of Birth'
    if error_data in str(exception):
        logging.error("Register number=" + reg + "||Dob=" + value + "||error : invalid date of birth")
        textBox.insert(tk.END, "invalid data found,check logs for more details\n")
        textBox.see(tk.END)


def get_result_type1(url, result_db, path):
    options = Options()
    options.headless = True
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", path)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    profile.set_preference("pdfjs.disabled", True)
    driver = webdriver.Firefox(firefox_profile=profile, options=options, executable_path='../driver/geckodriver.exe')
    driver.get(url)
    no = 0
    for _ in result_db:
        root.update()
        id_num = result_db[no][0]
        pwd = result_db[no][1]
        test = True
        try:
            if driver.find_elements_by_id("regnum"):
                RegNo = driver.find_element_by_id("regnum")
                RegNo.send_keys(id_num)
                if driver.find_elements_by_id("dob"):
                    DoB = driver.find_element_by_id("dob")
                    DoB.send_keys(pwd)
                login = driver.find_element_by_name('sub')
                login.click()
                RegNo.clear()
                DoB.clear()
            elif driver.find_element_by_name("regno"):
                if driver.find_element_by_name("regno"):
                    temp = driver.find_element_by_name("regno")
                    temp.send_keys(id_num)
                else:
                    temp = driver.find_element_by_id("regno")
                    temp.send_keys(id_num)
                if driver.find_element_by_id("dob"):
                    temp1 = driver.find_element_by_id("dob")
                    temp1.send_keys(pwd)
                if driver.find_elements_by_name('but'):
                    login = driver.find_element_by_name('but')
                    login.click()
                else:
                    login = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[5]/td/input')
                    login.click()
                temp1.clear()
                temp.clear()
            else:
                textBox.insert(tk.END, "Something missing Contact dev\n")
                textBox.see(tk.END)
        except TimeoutException as e:
            textBox.insert(tk.END, "timeout retrying...\n")
            textBox.see(tk.END)
            individual(url, id_num, pwd, path)
        except Exception as exception:
            test = False
            log(exception, reg=id_num, value=pwd)
            textBox.insert(tk.END, "Issue generated,check log file \n")
            textBox.see(tk.END)
        if test == True:
            val = no + 1
            textBox.insert(tk.END, '{} file downloaded \n'.format(val))
            textBox.see(tk.END)
        else:
            val = no + 1
            textBox.insert(tk.END, ' {} file not downloaded \n'.format(val))
            textBox.see(tk.END)
        no += 1
    driver.quit()
    if platform.system() in "Windows":
        os.system("Taskkill /IM firefox.exe /F")


def get_db(db_path):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM students')
        result_db = cursor.fetchall()
        cursor.close()
        connection.close()
        return result_db
    except Error as e:
        textBox.insert(tk.END, "Error occured while accessing data from data base\nissue:{}".format(e))
        textBox.see(tk.END)


''' link Section
BCA-BSc
http://14.139.185.44/online/UG/bsc3semresult2019/bsc3semresult.php
BBA-Bcom
http://14.139.185.44/online/UG/commerce3sem2019result/index.php
BA/BBM/BSW
http://14.139.185.44/online/UG/ba3semresult/ba3semresult.php
'''

'''data section 

db_path = ''
link = ''
register_number = ''
date_of_birth = ''
download_path = ''
'''


def personal_window():
    root = tk.Tk()
    root.geometry("300x200+300+100")
    root.title("personal download")
    personal_label = tk.Label(root, text='Personal', font=('calibre', 15, 'bold', 'underline'))
    personal_label.grid(row=6, column=0)

    reg_no_label = tk.Label(root, text='Reg No. ', font=('calibre', 10, 'bold'))
    reg_no_label.grid(row=7, column=0)

    reg_no_entry = tk.Entry(root, textvariable='')
    reg_no_entry.grid(row=7, column=1)

    dob_label = tk.Label(root, text='DOB.      ', font=('calibre', 10, 'bold'))
    dob_label.grid(row=8, column=0)
    dob_entry = tk.Entry(root, textvariable='')
    dob_entry.grid(row=8, column=1)

    def personal_download():
        if CheckVar.get():
            url_link = link_entry.get()
            path = pathentry.get()
            if platform.system() in "Windows":
                path = path.replace("/", "\\")
            reg = reg_no_entry.get()
            dob = dob_entry.get()
            individual(url_link, reg, dob, path)
        else:
            textBox.insert(tk.END, 'not selected\n')
            textBox.see(tk.END)

    download_personal = tk.Button(root, text="Download", font=('Arial', 10, 'bold'), command=personal_download,
                                  width=10, height=2)
    download_personal.grid(row=9, column=1)

    root.mainloop()
def database_window():
    Droot = tk.Tk()
    Droot.title("Database download")
    Droot.geometry("500x100+300+100")
    Droot.resizable(0, 0)
    By_dataBaseL = tk.Label(Droot, text="By DB", font=('calibre', 15, 'bold', 'underline'))
    By_dataBaseL.grid(row=0)
    dataBaseL = tk.Label(Droot, text="DB   :", font=('calibre', 10, 'bold'))
    dataBaseL.grid(row=1)

    def db_select_path():
        DB_path =filedialog.askopenfilename()
        DB_pathentry.insert(tk.END,DB_path)
    DBpathvar = tk.StringVar()
    DB_pathentry = tk.Entry(Droot, textvariable=DBpathvar, font=('calibre', 10, 'normal'), width=40)
    DB_pathentry.grid(row=1, column=1)
    DB_pathbtn = tk.Button(Droot, text='select Database', command=db_select_path)
    DB_pathbtn.grid(row=1, column=2)
    DB_pathbtn.place(x=360, y=26)

    def database_download():
        if m_check_var.get():
            path = DB_pathentry.get()
            if link_entry.get() and pathentry.get():
                link = link_entry.get()
                dpath = pathentry.get()
                if platform.system() in "Windows":
                    dpath = dpath.replace("/", "\\")
                By_database(link, path, dpath)
            else:
                textBox.insert(tk.END, "check link and download path field \n")
                textBox.see(tk.END)
        else:
            textBox.insert(tk.END, "not working\n")

    DB_download = tk.Button(Droot, text="Download", command=database_download, font=('Arial', 10, 'bold'), width=10,
                            height=2)
    DB_download.grid(row=2, column=1)
    Droot.mainloop()


def individual(link, register_number, date_of_birth, download_path):
    test = True
    try:
        get_result_type0(link, register_number, date_of_birth, download_path)
    except TimeoutException as e:
        get_result_type0(link, register_number, date_of_birth, download_path)
    except Exception as e:
        test = False
        log(e, reg=register_number, value=date_of_birth)
        textBox.insert(tk.END, e)
        textBox.see(tk.END)
    finally:
        if test == True:
            textBox.insert(tk.END, "File downloaded successfully :>\n")
            textBox.see(tk.END)
        else:
            textBox.insert(tk.END, "File download failed :<\n")
            textBox.see(tk.END)


'''By database'''


def By_database(link, db_path, download_path):
    result_db = get_db(db_path)
    get_result_type1(link, result_db, download_path)


root = tk.Tk()
root.title("Result Downloader")
root.geometry("700x500+300+120")
p1 = tk.PhotoImage(file='cloud-computing.png')
root.iconphoto(False, p1)
root.resizable(0, 0)
heading = tk.Label(root, text='Result Downloader', font=('Times Roman New', 40, 'bold'))
heading.grid(row=0, column=1)
link_url = tk.Label(root, text='URL', font=('Calibre', 10, 'bold'))
link_url.grid(row=3, column=0)
link_url.place(x=0, y=70)
link_entry = tk.Entry(root, font=('calibre', 10, 'normal'), width=45)
link_entry.grid(row=3, column=1)
link_entry.place(x=145, y=70)
valid = tk.Label(root)


def submit():
    text = ""
    url = link_entry.get()
    if not urlparse(url).scheme:
        url = 'http://' + url
    req = Request(url)
    text = ''
    try:
        response = urlopen(req)

    except HTTPError as e:
        text = '❌ not Valid'
    except URLError as e:
        text = '❌ not Valid'
    else:
        text = '✅ Valid'
    valid.config(text=text)
    valid.grid(row=3, column=2)
    valid.place(x=600, y=71)


check_valid = tk.Button(root, text='validate', command=submit)
check_valid.grid(row=3, column=2)
check_valid.place(x=515, y=65)


def select_path():
    path = filedialog.askdirectory()
    pathvar.set(path)


pathvar = tk.StringVar()
pathvar.set('')
path_label = tk.Label(root, text='Download location', font=('calibre', 10, 'bold'))
path_label.grid(row=4, column=0)
path_label.place(x=0, y=100)
pathentry = tk.Entry(root, textvariable=pathvar, font=('calibre', 10, 'normal'), width=45)
pathentry.grid(row=4, column=1)
pathentry.place(x=145, y=100)
pathbtn = tk.Button(root, text='select folder', command=select_path)
pathbtn.grid(row=4, column=2)
pathbtn.place(x=515, y=100)

Opt = tk.Label(root, text='Choose Method:', font=('calibre', 10, 'bold'))
Opt.grid(row=5, column=0)
Opt.place(x=0, y=129)
CheckVar = tk.BooleanVar()
CheckVar.set(False)
m_check_var = tk.BooleanVar()
m_check_var.set(False)
personal = tk.Checkbutton(root, text='Personal', variable=CheckVar)
multiple = tk.Checkbutton(root, text='By DataBase', variable=m_check_var)
personal.grid(row=5, column=1)
multiple.grid(row=5, column=2)
personal.place(x=135, y=128)
multiple.place(x=220, y=128)


def download_file():
    if CheckVar.get() and m_check_var.get():
        personal_window()
        database_window()
    elif CheckVar.get():
        personal_window()
    elif m_check_var.get():
        database_window()
    else:
        textBox.insert(tk.END, "no option selected\n")
        textBox.see(tk.END)


download_btn = tk.Button(root, text='Download', font=('Arial', 20, 'bold'), command=download_file, width=39)
download_btn.place(x=10, y=150)
textBox = tk.Text(root, height=15, width=84, bg='white', fg='black')
textBox.place(x=10, y=220)


def isConnected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        sock = socket.create_connection(("www.google.com", 80))
        if sock is not None:
            sock.close
        return True
    except OSError:
        pass
    return False


if isConnected():
    textBox.insert(tk.END, "Online\n")
else:
    textBox.insert(tk.END, "offline,Check your network!!\n")
menubar = tk.Menu()


def exit():
    if platform.system() in "Windows":
        os.system("Taskkill /IM firefox.exe /F")

    quit()


def view_log():
    if platform.system() in "Windows":
        subprocess.call(['notepad.exe', 'app.log'])
    else:
        os.system('./app.log')


menu_list = tk.Menu(menubar, tearoff=0)
menu_list.add_command(label="view-log", command=view_log)
menu_list.add_command(label="Exit", command=exit)
menubar.add_cascade(label="Options", menu=menu_list, font=("arial", 10))
root.config(menu=menubar)
def about():
    print("hello")
def how_to_use():
    webbrowser.open("https://github.com/CodeX3/Result_Downloader/blob/master/win2.0/Result%20downloader.pdf")
menu_list = tk.Menu(menubar, tearoff=0)
menu_list.add_command(label="About", command=about)
menu_list.add_command(label="How-To-Use", command=how_to_use)
menubar.add_cascade(label="Info", menu=menu_list, font=("arial", 10))
root.config(menu=menubar)
root.mainloop()
