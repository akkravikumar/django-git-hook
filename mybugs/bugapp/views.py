from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Bugs, User
import sys
import os
import subprocess
import re
import urllib, json
import string
# Create your views here.

def index(request):
	return HttpResponse("Index method called")

def indexhome(request):
	context = {'username':''}
	return render(request, 'bugs/login_auth.html', context)
	# try:
	# 	bugs = Bugs.objects.all()
	# except Bugs.DoesNotExist:
	# 	raise Http404("Bugs does not exist")
	# return render(request, 'bugs/index.html', {'bugs':bugs})

def authenticate(request):
	if request.method == 'POST':
		user = request.POST.get('email', None)
		pwd = request.POST.get('pwd', None)
		checkUser = User.objects.filter(username=user)
		if checkUser:
			isSuccess = User.objects.filter(password=pwd)
			if isSuccess:
				try:
					bugs = Bugs.objects.all()
				except Bugs.DoesNotExist:
					raise Http404("Bugs does not exist")
				return render(request, 'bugs/index.html', {'bugs':bugs})
			else:
				return HttpResponse("Invalid password, try again")
		else:
			return HttpResponse("User not found")
	# 	bData = Bugs(bugId=bugNumber, desc=bugDescription)
	# 	bData.save()
	# 	return HttpResponse("Success! Please refresh the page.")
	else:
		return HttpResponse("Request method is not a POST")

def addUiBug(request):
	if request.method == 'POST':
		bugNumber = request.POST.get('bugid', None)
		bugDescription = request.POST.get('desc', None)
		bData = Bugs(bugId=bugNumber, desc=bugDescription)
		bData.save()
		return HttpResponse("Success! Please refresh the page.")
	else:
		return HttpResponse("Request method is not a POST")

def get_bugIds():
	try:
		bugs = Bugs.objects.all()
	except Bugs.DoesNotExist:
		raise Http404("Bugs not found")
	listOfBugs = []
	for bug in bugs:
		listOfBugs.append(bug.bugId)
	return listOfBugs

def readBugs(request):
	try:
		separator = "----****----"
		message = request.GET.get('message')
		commit_list = message.strip().split(separator)[:-1]
		bugIds = get_bugIds()
		listings = []
		stringval = ''
		for commit in commit_list:
			line_list = commit.strip().split("\n")
			hash1 = line_list[0]
			date = line_list[1]
			committed_msg = " ".join(line_list[2:])
			print(committed_msg)
			if not re.findall("refs *#[0-9]+", committed_msg):
				if committed_msg.startswith('Bug Id:'):
					text = committed_msg.replace("Bug Id:", "")
					if len(text.strip()) == 0:
						response_data = {}
						response_data['Action'] = 'Abort'
						response_data['message'] = 'Comments should be the following format: Bug Id:<bug_id>-your_comment_here'
						return HttpResponse(json.dumps(response_data), content_type="application/json")
					else:
						bugsTextList = text.split('-')
						strBugs = str(bugsTextList[0].strip())
						listings.append(bugIds)
						if any(strBugs in s for s in bugIds):
							result = {'Action':'Push','message':'Success'}
							return JsonResponse(result,safe=False)
						else:
							result = {'Action':'Abort','message':strBugs +' Bug not found in the list'}
							return JsonResponse(result,safe=False)
				else:
					response_data = {}
					response_data['Action'] = 'Abort'
					response_data['message'] = 'Comments should be the following format: Bug Id:<bug_id>-your_comment_here'
					return HttpResponse(json.dumps(response_data), content_type="application/json")
	except:
		return HttpResponse("Exception")
	return HttpResponse('')

def deleteBug(request):
	if request.method == 'POST':
		bugNumber = request.POST.get('bugid', None)
		Bugs.objects.get(bugId=bugNumber).delete()
		return HttpResponse("Successfully deleted! Please refresh the page.")
	else:
		return HttpResponse("Request method is not a POST")
