
![LicenseBadge](https://img.shields.io/github/license/FayDoom/Strobe?style=for-the-badge)
![SizeBadge](https://img.shields.io/github/repo-size/FayDoom/Strobe?style=for-the-badge)


# Strobe
Strobe updates your wallpaper automatically.
There is two source available yet (Meteosat-11 and Himawari-8)

![Demo](https://github.com/FayDoom/Strobe/blob/master/himawari8.jpg)

## Installation
	Compat with Windows, linux, osx, freebsd

	git clone https://github.com/FayDoom/Strobe.git
	pip install --requirement requirements.txt

	There is no need to choose the background image manually, the program will do it for you.
	But you have to set the "ajusted" background mode and choose the black filling color in your Windows settings.
	(It's a pain in the a$$ to do it programmatically)

## Usage
	"python main.py -s meteosat11" or "pythonw main.py -s meteosat11" to run in background

	Man :
	-p PLATFORM, --platform PLATFORM Specify platform. Available : windows, linux or freebsd, others WiP (default : windows)
	-s SOURCE,   --source SOURCE	 Image connector name. Available : meteosat11, himawari8 (default : meteosat11)

### Run silently at startup (windows)
	$source  = 'The source you want' #e.g.: 'himawari8' or 'meteosat11'
	$path    = 'PATH TO main.py' #e.g.: 'C:\Users\<username>\Strobe\main.py'

	$arg     = '"'+$path+'" -s '+$source
	$action  = New-ScheduledTaskAction -Execute 'pythonw' -Argument $arg
	$trigger =  New-ScheduledTaskTrigger -AtLogon
	Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "Strobe-Wallpaper" -Description "Strobe, the wallpaper updater"
