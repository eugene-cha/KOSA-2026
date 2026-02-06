Set W=WScript.CreateObject("WScript.Shell"):W.Run "notepad":WScript.Sleep 500:W.AppActivate "Notepad":s="This is hacked!...":For i=1 To Len(s):W.SendKeys Mid(s,i,1):WScript.Sleep 200:Next  
