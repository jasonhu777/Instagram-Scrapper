from logging import currentframe
from tkinter import font
from selenium import webdriver
import os
import time
import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import tkinter as tk

from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()
sched.start()


class ScheduleObject:
    def __init__(self, username, password, amount, hashtag, date, label):
        self.username = username.get()
        self.password = password.get()
        self.amount = amount.get()
        self.hashtag = hashtag.get()
        self.date = date.get()
        self.label = label
        self.timestamp = time.mktime(
            datetime.datetime.strptime(self.date, '%Y-%m-%d %H:%M').timetuple())


class InstagramBot:
    def __init__(self, username, password, amount, hashtag):
        self.username = username
        self.password = password
        self.amount = amount
        self.hashtag = hashtag

        self.driver = webdriver.Chrome('./chromedriver.exe')

        self.by = By
        self.ec = EC
        self.webDriverWait = WebDriverWait

        time.sleep(1)
        self.login()
        time.sleep(5)
        self.explore_hashtages(self.hashtag)
        time.sleep(2)
        self.like_posts()
        time.sleep(3)
        self.driver.quit()

    def login(self):
        self.driver.get('https://www.instagram.com/accounts/login/')

        self.webDriverWait(self.driver, 20).until(
            self.ec.presence_of_element_located((self.by.NAME, 'username')))

        self.webDriverWait(self.driver, 20).until(
            self.ec.presence_of_element_located((self.by.NAME, 'password')))

        self.webDriverWait(self.driver, 20).until(
            self.ec.element_to_be_clickable((self.by.XPATH, '//*[contains(text(),"Log In")]')))

        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_element_by_xpath(
            '//*[contains(text(),"Log In")]').click()

    def explore_hashtages(self, hashtag):
        self.driver.get(
            'https://www.instagram.com/explore/tags/' + self.hashtag)

    def like_posts(self):
        self.driver.find_element_by_class_name('v1Nh3').click()

        i = 1
        while i <= int(self.amount):
            time.sleep(2)
            self.driver.find_element_by_class_name('fr66n').click()
            self.driver.find_element_by_class_name(
                'coreSpriteRightPaginationArrow').click()
            i += 1
        self.driver.get('https://www.instagram.com/')


class MainApp(tk.Frame):
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.gui = self.configure_gui()
        self.widgets = self.create_widgets()
        self.scheduleObjects = []

    def configure_gui(self):
        self.master.geometry('700x800')

    def create_widgets(self):
        scheduleRun = tk.Button(self.master, text="Schedule", font=(
            "Helvatica", 18), padx=10, pady=5, fg="#fff", bg="#3582e8", command=self.runBot)
        scheduleRun.grid(column=0, row=5, padx=10, pady=30)

        usernameLabel = tk.Label(
            self.master, text="Username", font=("Helvatica", 18))
        usernameLabel.grid(column=0, row=0, padx=10, pady=30)

        usernameEntry = tk.Entry(self.master, width=15, font=("Helvatica", 18))
        usernameEntry.grid(column=1, row=0, padx=10, pady=10)

        passwordLabel = tk.Label(
            self.master, text="Password", font=("Helvatica", 18))
        passwordLabel.grid(column=0, row=1, padx=10, pady=30)

        passwordEntry = tk.Entry(
            self.master, width=15, show="*",   font=("Helvatica", 18))
        passwordEntry.grid(column=1, row=1, padx=10, pady=10)

        amountLabel = tk.Label(
            self.master, text="Amount", font=("Helvatica", 18))
        amountLabel.grid(column=0, row=2, padx=10, pady=30)

        amountEntry = tk.Entry(
            self.master, width=15,   font=("Helvatica", 18))
        amountEntry.grid(column=1, row=2, padx=10, pady=10)

        hashtagLabel = tk.Label(
            self.master, text="Hashtag", font=("Helvatica", 18))
        hashtagLabel.grid(column=0, row=3, padx=10, pady=30)

        hashtagEntry = tk.Entry(
            self.master, width=15,   font=("Helvatica", 18))
        hashtagEntry.grid(column=1, row=3, padx=10, pady=10)

        dateLabel = tk.Label(
            self.master, text="Date (Format: 2021-01-01 00:00)", font=("Helvatica", 18))
        dateLabel.grid(column=0, row=4, padx=10, pady=30)

        dateEntry = tk.Entry(
            self.master, width=15,   font=("Helvatica", 18))
        dateEntry.grid(column=1, row=4, padx=10, pady=10)

        return usernameEntry, passwordEntry, amountEntry, hashtagEntry, dateEntry

    def runBot(self):
        username, password, amount, hashtag, date = self.widgets
        resultsLabel = tk.Label(self.master, anchor="e", justify=tk.LEFT,
                                text=" * Hastag: " + hashtag.get()+" | Amount: "+amount.get()+" | Date: " + date.get(), font=("Helvatica", 13))
        resultsLabel.grid(column=0, row=len(
            self.scheduleObjects)+6, padx=10, pady=2)

        scheduleObject = ScheduleObject(
            username, password, amount, hashtag, date, resultsLabel)
        self.scheduleObjects.append(scheduleObject)

        sched.add_job(lambda: self.startBot(
            username, password, amount, hashtag), "date", next_run_time=date.get()+":00")
        print("Schedule Bot")

    def startBot(self, username, password, amount, hashtag):
        ts = int(time.time())
        currentObj = None
        for o in self.scheduleObjects:
            if o.timestamp == ts:
                currentObj = o
                o.label.destroy()
                self.scheduleObjects.remove(o)

        print("Bot Started")
        ig = InstagramBot(currentObj.username,
                          currentObj.password,
                          currentObj.amount,
                          currentObj.hashtag)


        # ig = InstagramBot('tester90011', 'JAYhz123098', 2, 'chicken', '2021-01-0')
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Instagram Data Extraction Bot")
    main_app = MainApp(root)
    root.mainloop()
