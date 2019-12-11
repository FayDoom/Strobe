# Strobe
Strobe updates your wallpaper automatically.
There is only one source available yet (Meteosat-11 data)

![Demo](https://github.com/FayDoom/Strobe/blob/master/demo.jpg)

## Installation
	git clone https://github.com/FayDoom/Strobe.git
	pip install --requirement requirements.txt

	There is no need to choose the background image manually, the program will do it for you.
	But you have to set the "centered" background mode and choose the black filling color in your Windows settings.
	(It's a pain in the a$$ to do it programmatically)

## Usage
	"python main.py" or "pythonw main.py" to run in background

### Run silently at startup (windows)
	$path = '"PATH TO main.py"' #e.g.: '"C:\Users\<username>\Strobe\main.py"'
	$action  = New-ScheduledTaskAction -Execute 'pythonw' -Argument $path
	$trigger =  New-ScheduledTaskTrigger -AtLogon
	Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "Strobe-Wallpaper" -Description "Strobe, the wallpaper updater"
