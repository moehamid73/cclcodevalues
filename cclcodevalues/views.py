from django.shortcuts import render

def homepage(request):
    return render(request, 'home.html')

def parsecode(request):
    fulltext = request.GET['fulltext']
    #print(fulltext)
    lines = fulltext.split("\n")
    #print(lines)
    
    print('****** starting 1st array')
    newCodeValueLines = []
    
    for line in lines:
        #print('line: ', line)
        startComment = line.find(";")
        
        if line != '\n':
            if startComment == 0: #comment line
                newCodeValueLines.append(line)
                continue
            elif startComment == -1 and line != '\n': #none-comment line
                #find the position of the parenthesis
                parenthesisPos = line.find("))") + 2
                #concat " go" after the  "))"
                modifiedLine = line[ : parenthesisPos] + " go" + line[ parenthesisPos : ]
                        #print('********************** New line with go: ', line)
                #add the new line to the new array
                newCodeValueLines.append(modifiedLine)

                #create a new line to print out the code value
                start = line.find(" ") + len(" ")
                end = line.find("=")
                if start > 0 and end > 0:
                    codeValueName = "call echo( " + line[start:end] + ") go"
                    newCodeValueLines.append(codeValueName)

    #print the new array
    print("*********** NEW ARAAY ********************")
    for line1 in newCodeValueLines:    
        print(line1)
                

    #remove meaningless lines
    print('******************** remove meaningless lines')
    for line2 in newCodeValueLines:
        print('******** strip line: |' , line2.strip(),"|")
        if(line2.strip() == "go" or line2.strip() == " go" or line2.strip() == "go " or line2.strip() == " go " 
            or line2.strip() ==  "call echo(   ) go" or line2.strip() ==  " call echo(   ) go" 
            or line2.strip() ==  "call echo(   ) go " or line2.strip() ==  " call echo(   ) go "
            or line2 == "call echo(   ) go"):
            newCodeValueLines.remove(line2)


    #print the new array
    print("*********** MODIFIED ARRAY ********************")
    for line3 in newCodeValueLines:
        line3 = line3.strip()    
        print("modified line: |", line3, "|")
                    
    return render(request, 'parsecode.html')