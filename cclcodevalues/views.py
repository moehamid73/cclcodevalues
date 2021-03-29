from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import re

listCodesDictionary = dict() 

def homepage(request):
    return render(request, 'home.html')

@csrf_exempt
def parsecode(request):
    fulltext = request.POST['fulltext']

    lines = fulltext.split("\r\n")

    result = []

    for line in lines:
        if not line.startswith(";") and len(line) > 1:
            result.append("%s go" % line )
            if line.startswith('declare'):
                varname = line.split('=')[0].split(' ')[1]
                result.append("call echo(%s) go" % varname)                #call echo(dRefNum) go
            else:
                result.append(line)
        else:
            result.append(line)
 
    return render(request, 'parsecode.html', {'newCodeValuesLinesDictionary': "\n".join(result)})

@csrf_exempt
def listedcode(request):
    return render(request, 'listedcode.html')

@csrf_exempt
def query(request):
    listtext = request.POST.get('listtext')

    listlines = listtext.split("\r\n")

    global listCodesDictionary

    for i in range(len(listlines)):                    
        if listlines[i].startswith("1)call echo("):
            line2 = listlines[i][5:len(listlines[i])]
            varname2 = line2[line2.find("(")+1:line2.find(")")].strip()
            listCodesDictionary[varname2] = listlines[i+1].strip()

    return render(request, 'query.html')

@csrf_exempt
def output(request):
    global listCodesDictionary

    outputText = request.POST.get('querytext')

    outputLines = outputText.split("\r\n")
    
    for dictItem, dictValue in listCodesDictionary.items():
        for y in range(len(outputLines)):
            if outputLines[y].find(dictItem) > -1: 
                newLine = outputLines[y].replace(dictItem, dictValue)
                outputLines[y] = newLine
    print('moe')
    print(outputLines)
    outputLines.append('with time = 30, format(date, ";;q")')
    print(outputLines)
    return render(request, 'output.html', {'finalOutput' : "\n".join(outputLines)})