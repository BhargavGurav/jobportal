import requests

url = "https://indeed12.p.rapidapi.com/job/b762b8d1132bd276"

headers = {
	"X-RapidAPI-Key": "ccf377d689msh3907d6153450c13p1c409bjsne180aa5acedb",
	"X-RapidAPI-Host": "indeed12.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

print(response.text)