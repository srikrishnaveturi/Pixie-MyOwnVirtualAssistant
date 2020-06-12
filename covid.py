import requests

url = 'https://api.covid19india.org/v3/data.json'
#state = input("enter state")
#district = input("enter district")


jsonData = requests.get(url).json()
stateKeys = list(jsonData.keys())
stateNames = ["Andaman and Nicobar Islands","Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chandigarh","Chhattisgarh","National Capital Territory of Delhi","Dadra and Nagar Haveli","Goa","Gujarat","Himachal Pradesh","Haryana","Jharkhand","Jammu and Kashmir","Karnataka","Kerala","Leh Ladakh","Lakshadweep","Maharashtra","Meghalaya","Manipur","Madhya Pradesh","Mizoram","Nagaland","Odisha","Punjab","Puducherry","Rajasthan","Sikkim","Telangana","Tamil Nadu","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"]

stateDict = {}
 #tt and un mean total and idk in the json
#for a in range(len(stateKeys)):
	#stateDict[stateNames[a]] = stateKeys[a]
print(len(stateNames))
print(len(stateKeys))
print(stateNames)
print(stateKeys)
 
