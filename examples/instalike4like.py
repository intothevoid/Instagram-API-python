import sys
import time
from InstagramAPI import InstagramAPI
import json
import random

username=""
password=""
API = InstagramAPI(username,password)

def instaLogin():
	if API.login() is not True:
		print("Error logging into user's account. Aborting...")
		return False
	else:
		print("Successfully logged in.")
		return True

def getLatestMediaID(userName=username,usernameID=None):
	# Debug
	# print("Getting latest media for user %s..." % userName)

	if usernameID:
		res = API.getUserFeed(usernameID)
	else:
		res = API.getSelfUserFeed()
	
	if res is True:
		feed = API.LastJson
		if (len(feed["items"])) > 0 and feed is not None:
			latestMediaItem = feed["items"][0] # 0 indicates first item

			try:
				if latestMediaItem is not None:
					latestMediaItemID = latestMediaItem["caption"]["media_id"]
					#print("%s's latest media ID is %s" % (userName,latestMediaItemID))
					return latestMediaItemID
			
			except Exception as e:
				print("Exception thown when getting latest media of user %s. Details: %s" % (userName, e))
				
		else:
			print("No items found in users feed")
	else:
		print("Failed to get latest media from user's feed")

def getUsersWhoLikedMedia(mediaID):
	res = API.getMediaLikers(mediaID)
	usersWhoLikedMedia = {}

	if res is True:
		for user in API.LastJson["users"]:
			usersWhoLikedMedia[user["username"]] = user["pk"]

		return usersWhoLikedMedia
	else:
		print("Failed to get users who liked media")

def likeLatestMediaAllUsers(userDict):
	if len(userDict) > 0:
		for userName,userID in userDict.items():
			likeLatestMedia(userName,userID)
			time.sleep(random.randint(1,15)) # wait a few seconds before liking next media
	else:
		print("Userlist is empty. Cannot start liking")			

def likeLatestMedia(userName,userID):
	mediaID = getLatestMediaID(userName,userID)

	if API.like(mediaID) is True:
		print("Liked media %s of user %s" % (mediaID, userName))
	else:
		print("Failed to like media %s of user %s. Details:%s" % (mediaID, userName, API.LastJson))

def printUserLikeDict(userDict):
	print("Users who liked your latest post are -")
	for key,val in userDict.items():
		print("%s:%s" % (key, val)) 

def likeTimelinePosts():
	res = API.timelineFeed()

	if res is True:
		items = API.LastJson["items"]
		for item in items:
			mediaID = item["caption"]["media_id"]
			user = item["caption"]["user"]["username"]

			if API.like(mediaID) is True:
				print("Liked media %s of user %s" % (mediaID, user))
			else:
				print("Failed to like media %s of user %s. Details:%s" % (mediaID, user, API.LastJson))

			time.sleep(random.randint(1,15)) # wait a few seconds before liking next media
	else:
		print("Failed to %s's timeline." % username)


def main():
	if instaLogin() is not True:
		sys.exit(1)

	latestMediaID = getLatestMediaID() # Get the latest media id for our accounts latest post
	
	usersWhoLikedMedia = {}
	usersWhoLikedMedia = getUsersWhoLikedMedia(latestMediaID) # Get a list of users who liked our latest post
	print("Found %d users who liked your latest post" % len(usersWhoLikedMedia))

	#printUserLikeDict(usersWhoLikedMedia) # Debug - print names of all users who liked our latest post

	likeLatestMediaAllUsers(usersWhoLikedMedia) # Like the latest post (like4like) of each user who liked our latest post

	#likeTimelinePosts() # Get posts on users timeline and like them

	# Done liking, now logout
	API.logout()

if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print("Exception occured while running script! Details: %s" % e)
		API.logout()
		raise