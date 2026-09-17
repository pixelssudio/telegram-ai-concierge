Set fso = CreateObject("Scripting.FileSystemObject")
botFolder = fso.GetParentFolderName(WScript.ScriptFullName)

Set shell = CreateObject("WScript.Shell")
shell.CurrentDirectory = botFolder

' Install deps if needed
Set proc = shell.Exec("cmd /c pip install python-telegram-bot[job-queue]==20.7 python-dotenv==1.0.0 --quiet")
Do While proc.Status = 0: WScript.Sleep 500: Loop

' Run bot
cmd = "python bot.py"
Set run = shell.Exec(cmd)

' Log PID
Set f = fso.OpenTextFile(botFolder & "\bot_started.txt", 2, True)
f.WriteLine run.ProcessID
f.Close

WScript.Quit
