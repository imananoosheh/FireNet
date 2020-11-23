from django.shortcuts import render


# Create your views here.


def addressbag(request):
    bag_list = {}
    return render(request, 'fireNet/index.html', {'bag_list': bag_list})


def addaddresstobag(request):
    if request.method == 'POST':
        bag_list = {}
        input_name = request.POST['bagname']
        ip1 = request.POST['ip1']
        ip2 = request.POST['ip2']
        ip3 = request.POST['ip3']
        ip4 = request.POST['ip4']
        ip5 = request.POST['ip5']

        # updating the address

        # updated ip list and bagname should be sent
        ip_list = []
        bagname = ""
        return render(request, 'fireNet/index.html', {'bag_list': bag_list, 'ip_list': ip_list, 'bagname': bagname})


def removeaddressfrombag(request):
    if request.method == 'POST':
        bag_list = {}
        input_name = request.POST['bagname']
        ip1 = request.POST['ip1']
        ip2 = request.POST['ip2']
        ip3 = request.POST['ip3']
        ip4 = request.POST['ip4']
        ip5 = request.POST['ip5']

        # remove and updating the address

        # updated ip list and bagname should be sent
        ip_list = []
        bagname = ""
        return render(request, 'fireNet/index.html', {'bag_list': bag_list, 'ip_list': ip_list, 'bagname': bagname})


def modifybag(request):
    if request.is_ajax():
        if request.method == 'POST':
            bag_list = {}
            input_name = request.POST['bagname']

            # remove and updating the address
            print(request.body)

            # updated ip list and bagname should be sent
            ip_list = []
            bagname = ""
            return render(request, 'fireNet/index.html', {'bag_list': bag_list, 'ip_list': ip_list, 'bagname': bagname})
