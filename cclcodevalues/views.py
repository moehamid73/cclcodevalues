from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

listCodesDictionary = dict()


def homepage(request):
    print("************************************************* HOME", request);    #mh
    if request.method == 'POST':
        print("************************************************* HOME POST", request);  #mh
        return redirect('parse')
    print("************************************************* HOME POST POST", request);    #mh  
    return render(request, 'home.html')


@csrf_exempt
def parsecode(request):
    lines = []
    result = []
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ PARSE", request);    #mh
    fulltext = request.POST.get('fulltext', "")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ PARSE", fulltext);    #mh
    temp_lines = fulltext.split("declare")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ PARSE", len(temp_lines));    #mh
    # for i in range(len(temp_lines)):
    #     print(f"{i} == {temp_lines[i]}")

    if len(temp_lines) >= 1: 
        for temp_line in temp_lines:
            # If not empty line
            if len(temp_line) >= 10:
                temp_line = "declare" + temp_line
                lines.append(temp_line.strip())
        print(f"lines: {lines}")            #mh

        #Check to see if there is a ";" +/- comment at the end of the line
        #and replace it with "go"
        for line in lines:
            print(f"&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&line.strip(): {line.strip()}")            #mh
            if line != "\n" or not line.strip():
                if not line.startswith(";") and len(line) > 1:
                    semicolon_pos = line.find(";")
                    if semicolon_pos > 0:
                        if line[semicolon_pos - 1] != " ":
                            temp_line = line[:semicolon_pos:]
                            result.append("%s go" % temp_line)
                        else:
                            temp_line = line[0:semicolon_pos - 1:1]
                            result.append("%s go" % temp_line)
                            # print(f"result: {result}")            #mh

                        if line.startswith('declare'):
                            varname = temp_line.split('=')[0].split(' ')[1]
                            result.append("call echo(%s) go" % varname)  # call echo(dRefNum) go
                        else:
                            result.append(line)
                    else:
                        result.append("%s go" % line)
                        if line.startswith('declare'):
                            varname = line.split('=')[0].split(' ')[1]
                            result.append("call echo(%s) go" % varname)  # call echo(dRefNum) go
                        else:
                            result.append(line)
                else:
                    result.append(line)

        return render(request, 'parsecode.html', {'newCodeValuesLinesDictionary': "\n".join(result)})
    else:
        return redirect('home')

@csrf_exempt
def listedcode(request):
    return render(request, 'listedcode.html')


@csrf_exempt
def query(request):
    list_text = request.POST.get('list_text')

    list_lines = list_text.split("\r\n")

    global listCodesDictionary

    for i in range(len(list_lines)):
        if list_lines[i].startswith("1)call echo("):
            line2 = list_lines[i][5:len(list_lines[i])]
            print(f"LINE 2: {line2}")
            varname2 = line2[line2.find("(") + 1:line2.find(")")].strip()
            listCodesDictionary[varname2] = list_lines[i + 1].strip()

    return render(request, 'query.html')


@csrf_exempt
def output(request):
    global listCodesDictionary

    output_text = request.POST.get('querytext')

    output_lines = output_text.split("\r\n")

    for dictItem, dictValue in listCodesDictionary.items():
        for y in range(len(output_lines)):
            if output_lines[y].find(dictItem) > -1:
                if not dictValue.isnumeric():
                    new_line = output_lines[y].replace(dictItem, dictValue)
                    output_lines[y] = new_line
    print(output_lines)
    if not output_lines[-1].startswith("with"):
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%", output_lines[-1])
        output_lines.append('with time = 30, format(date, ";;q")')
    
    print(output_lines)
    return render(request, 'output.html', {'finalOutput': "\n".join(output_lines)})
