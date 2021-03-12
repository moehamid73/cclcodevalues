from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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

def listedcode(request):
    return render(request, 'listedcode.html')