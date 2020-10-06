from bs4 import BeautifulSoup
import requests
import codecs
import os

'''
todo:
 - cl args?
 - Don't save duplicates / ask for overwriting ?
 - create logfile for filenames, titles, code language, etc. ?

Pastebin doesn't show publicly pastes in plain text format anymore (text)!!
'''

def getpages(url): #check for multipage
    web = requests.get(url).text
    soup = BeautifulSoup(web, 'lxml')
    if soup.find_all('div', {'class':'pagination'}):
        urls = [a['href'] for a in soup.find('div', {'class':'pagination'}).findAll('a')]
        urls = list(dict.fromkeys(urls))
        if urls:
            for i in urls:
                download('https://pastebin.com'+i)
        else:
            download(url)
    else:
        download(url)

def download(url):
    web = requests.get(url).text
    soup = BeautifulSoup(web, 'lxml')
    table = soup.find('table', {'class':'maintable'})
    for td in table.find_all('td', {'class':''}):
        for a in td.find_all('a'):
            print(a.text + ": " + a['href'])
            paste = a['href'][1:]
            data = requests.get('https://pastebin.com/raw/' + paste).text
            #print(data)
            f = codecs.open(paste+'.txt','w','utf-8')
            f.write(data)
            f.close()

def menu():
    run = True
    while run:
        print(" _____                    ____  _        \n|  __ \                  |  _ \(_)       \n| |__) |_ _ _ __ ___  ___| |_) |_ _ __   \n|  ___/ _` | '__/ __|/ _ \  _ <| | '_ \  \n| |  | (_| | |  \__ \  __/ |_) | | | | | \n|_|   \__,_|_|  |___/\___|____/|_|_| |_| \n")
        print("Select an option: \n[1] Full Archive \n[2] Syntax Archive \n[3] User page \n[4] Quit \n")
        x = input("Enter: ")
        if x.isdigit() or x=="q" or x=="Q":
            if x=="1":
                getpages("https://pastebin.com/archive")
            elif x=="2":
                print("Commons: bash, c, csharp, cpp, css, html, json, java, javascript, lua, python, php")
                syntax = input("Enter syntax: ")
                if syntax != "":
                    getpages("https://pastebin.com/archive/"+syntax)
            elif x=="3":
                user = input("Enter user: ")
                if user != "":
                    getpages("https://pastebin.com/u/"+user)
            elif x=="4" or x=="Q" or x=="q":
                run = False
        else:
            print("Invalid input!")

def main():
    menu()

if __name__ == "__main__":
    main()
