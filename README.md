# Strobe
Strobe updates your wallpaper automatically.
There is two source available yet (Meteosat-11 and Himawari-8)

![Demo](https://github.com/FayDoom/Strobe/blob/master/himawari8.jpg)

## Installation
	Compat with Windows only

	git clone https://github.com/FayDoom/Strobe.git
	pip install --requirement requirements.txt

	There is no need to choose the background image manually, the program will do it for you.
	But you have to set the "centered" background mode and choose the black filling color in your Windows settings.
	(It's a pain in the a$$ to do it programmatically)

## Usage
	"python main.py" or "pythonw main.py" to run in background

### Run silently at startup (windows)
	$source  = 'The source you want' #e.g.: 'himawari8' or 'meteosat11'
	$path    = 'PATH TO main.py' #e.g.: 'C:\Users\<username>\Strobe\main.py'

	$arg     = '"'+$path+'" -s '+$source
	$action  = New-ScheduledTaskAction -Execute 'pythonw' -Argument $arg
	$trigger =  New-ScheduledTaskTrigger -AtLogon
	Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "Strobe-Wallpaper" -Description "Strobe, the wallpaper updater"
