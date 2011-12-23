cd C:\home\rfchauvx\IronPythonApplication2r\IronPythonApplication2r
python EILUNifiedClientAgent.py --username localsystem --startup auto install >> c:\eil\eilframework\eilsetup.txt

sc failure UnifiedClientAgt reset= 30 actions= restart/5000 >> c:\eil\eilframework\eilsetup.txt

sc start UnifiedClientAgt >> c:\eil\eilframework\eilsetup.txt

sc queryex UnifiedClientAgt >> c:\eil\eilframework\eilsetup.txt