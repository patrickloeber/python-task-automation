import requests
import platform
import pwd
import os

url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
FILENAME = 'nasa_pic.png'


def get_filename():
    username = pwd.getpwuid(os.getuid()).pw_name
    if platform.system()=="Linux":
        directory = "/home/" + username + "/Downloads/"
    elif platform.system()=="Darwin":
        directory = "/Users/" + username + "/Downloads/"
        
    return os.path.join(directory, FILENAME)

  
def download_pic_of_day():
    r = requests.get(url)

    if r.status_code != 200:
        print('error')
        return
    
    picture_url = r.json()['url']
    if "jpg" not in picture_url:
        print("No image for today, must be a video")
    else:
        pic = requests.get(picture_url , allow_redirects=True)
        filename = get_filename()
        
        open(filename, 'wb').write(pic.content)
        
        print(f"saved picture of the day to {filename}!")

       
if __name__ == '__main__':
    download_pic_of_day()
    
    filename = get_filename()
    
    # set background
    if platform.system()=="Linux":
        cmd = "gsettings set org.gnome.desktop.background picture-uri file:" + filename
    elif platform.system()=="Darwin":
        cmd = "osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"" + filename +"\"'"
        # use absolute path to the image, and not a path that begins with a user path (~/Downloads/image.jpg)!

    os.system(cmd)  