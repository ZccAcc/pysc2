python3
pyautogui=0.9.53
pyDes=2.0.1

tkphoto-桌面截图，使用方法：tkphoto 截图名字（仅名称即可） 保存地址(带文件名的绝对路径或相对路径) ，例：tkphoto test.jpg D:\\test.jpg
nrcv-无法进行交互的命令，使用方法：nrcv 执行的命令，例：nrcv natepad.exe
fput-上传文件，使用方法：fput 本地文件地址（带文件名的绝对路径或相对路径） 上传的地址(带文件名的绝对路径或相对路径)，例：fput D:\\test.exe C:\\test.exe
fget-下载文件，使用方法:fget 远程文件地址 本地保存地址，例：fget C:\Windows\win.ini E:\win.ini
正常命令可直接进行输入，dir、whoami、ipconfig等

fput  fget 加-s即是加密的文件传输，建议可读文本使用-s，不可读文件或较大文件正常使用fput、fget
