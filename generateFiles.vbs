Dim objFSO, objFile
Dim strScriptPath, strReqFilePath
Dim strRunRobotContent, strInstallerContent
Dim arrLibraries, strLibrary, strVersion
Dim allLibrariesFound

' Create a FileSystemObject
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the path of the script
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Define the paths of requirements.txt, RunRobot.bat, and Installer.bat files
strReqFilePath = strScriptPath & "\requirements.txt"
strRunRobotFilePath = strScriptPath & "\Launcher.bat"
strInstallerFilePath = strScriptPath & "\Installer.bat"

' Check if requirements.txt exists
If Not objFSO.FileExists(strReqFilePath) Then
    WScript.Echo "requirements.txt file not found!"
    WScript.Quit
End If

' Read requirements.txt file
on error resume next
Set objFile = objFSO.OpenTextFile(strReqFilePath)
strContents = objFile.ReadAll
objFile.Close
on error goto 0

' If requirements.txt is empty, ask the user whether to continue
If Len(strContents) = 0 Then
    If MsgBox("requirements.txt file is empty. Do you want to continue?", vbYesNo, "Empty File") = vbNo Then
        WScript.Quit
    End If
Else
    ' Split the contents by line
    arrLibraries = Split(strContents, vbCrLf)

    ' Flag to track if all required libraries are found
    allLibrariesFound = True

    ' Loop through each line in requirements.txt
    For Each line In arrLibraries
        ' Check if the line contains '=='
        If InStr(1, line, "==") > 0 Then
            ' Split the line by '=='
            arrLine = Split(line, "==")
            strLibrary = arrLine(0)
            strVersion = arrLine(1)

            ' Check if the library with correct version exists
            If Trim(strLibrary) = "" OR Trim(strVersion) = "" Then
                WScript.Echo "Warning: Required library " & strLibrary & " with version " & strVersion & " not found in requirements.txt!"
                allLibrariesFound = False
            End If
        Else
	WScript.Echo "Warning: All libraries in requirements.txt must have versions!"
	WScript.Quit
               allLibrariesFound = False
        End If
    Next

    ' If any required library is missing, stop further processing
    If Not allLibrariesFound Then
        WScript.Quit
    End If
End If

' Generate content for RunRobot.bat file
strRunRobotContent = "@echo off" & vbCrLf & _
                     "echo Running Application..." & vbCrLf & _
                     "python main.py" ' Adjust as needed

' Generate content for Installer.bat file
strInstallerContent = "@echo off" & vbCrLf & _
                      "echo Installing dependencies..." & vbCrLf & _
                      "pip install -r requirements.txt"  & vbCrLf & _
		      "DEL *.vbs"

' Create RunRobot.bat file
Set objFile = objFSO.CreateTextFile(strRunRobotFilePath)
objFile.Write strRunRobotContent
objFile.Close

' Create Installer.bat file
Set objFile = objFSO.CreateTextFile(strInstallerFilePath)
objFile.Write strInstallerContent
objFile.Close

WScript.Echo "RunRobot.bat and Installer.bat files generated successfully."
