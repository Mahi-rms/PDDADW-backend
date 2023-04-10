import requests
with open("D:/Users/Mahesh Vanam/Downloads/4994014ef5c834e4803541aa1dc874_jumbo.jpeg","rb") as myfile:
    file=myfile.read()
res=requests.post("https://demo.storj-ipfs.com/api/v0/add",files={'upload_file':file}).text
print(res)