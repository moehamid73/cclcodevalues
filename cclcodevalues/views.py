from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

listCodesDictionary = dict()


def homepage(request):
    return render(request, 'home.html')


@csrf_exempt
def parsecode(request):
    lines = []
    result = []

    fulltext = request.POST['fulltext']
    temp_lines = fulltext.split("declare")

    # for i in range(len(temp_lines)):
    #     print(f"{i} == {temp_lines[i]}")

    for temp_line in temp_lines:
        if len(temp_line) > 1:  # If not empty line
            temp_line = "declare" + temp_line
            lines.append(temp_line)
        # print(f"{temp_line}")

    for line in lines:
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
    output_lines.append('with time = 30, format(date, ";;q")')
    print(output_lines)
    return render(request, 'output.html', {'finalOutput': "\n".join(output_lines)})
