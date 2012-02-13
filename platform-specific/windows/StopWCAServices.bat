REM StopWCAServices.bat
REM -------------------
REM Basic tool which stops and removes from the service manager any services
REM which are associated with the previous Windows Client Agent.

for /F "tokens=3 delims=: " %%H in ('sc query "EILTAFService" ^| findstr "        STATE"') do (
  if /I "%%H" EQU "RUNNING" (
   REM Put your code you want to execute here
   REM For example, the following line
   net stop "EILTAFService"
  )
)