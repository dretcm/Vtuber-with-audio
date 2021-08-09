# Vtuber-with-audio
A vtuber with audio, in this code use for the sound the packague sounddevices and the UI use PyQt5.

steps if you want add a new avatar:

1. create a folder with three images with the respectives names: normal.(png or jpg), talk.(...), and scream.(...)
2. move the folder to data/images/


Install .exe:
1. open the cmd and type
```
C:\Users\USUARIO> pip install pyinstaller
```
3. cd to the folder of file main.py:
```
C:\Users\USUARIO> cd C:\...\my apps
```
3. run this line of code:

```
C:\...\my apps> pyinstaller main.py --onefile --noconsole -i data\images\yasu.ico
```
4. move the file "...my apps\dist\main.exe" to "...\my apps\".
5. remove "dist", "main.txt", "build".
