set dirname="C:\Program Files\V-REP3\V-REP_PRO_EDU\"
if exist %dirname%vrep.exe (goto LAUNCH) else goto CHECK_X86

:CHECK_X86
set dirname="C:\Program Files\V-REP3 (x86)\V-REP_PRO_EDU\"
if exist %dirname%vrep.exe (goto LAUNCH) else goto NOT_FOUND

:LAUNCH
set "CURRENT_DIR=%cd%"
cd %dirname%
vrep -gREMOTEAPISERVERSERVICE_19998_FALSE_TRUE %CURRENT_DIR%\simple.ttt
goto END

:NOT_FOUND
echo "ERROR: vrep.exe is not found."
:END
