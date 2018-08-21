import facebook
import requests
import json
import os
import datetime
import time

count=0
data = []


'''
    Facebook Modules

'''


def face_oauth (access_token):
    '''
        Facebook OAuthHandler function
    '''
    graph = facebook.GraphAPI(access_token)
    return graph



def output(data, outfile):
    '''
        Facebook Output Write Function
    '''
    with open(outfile, 'w') as file:
        json.dump(data, file)



def get_engagement(graph, post, likes_page):
    '''
        Facebook Get Post Analytics
    '''

    #Reactions
    try:
        likes = graph.get_object(id=post['id']+"/reactions?summary=total_count", fields={'type':['LIKE','LOVE', 'WOW', 'HAHA', 'SAD', 'ANGRY', 'THANKFUL']})
        likes = likes['summary']['total_count']
    except :
        likes = 0
    #Shares
    try:
        shares = graph.get_object(id=post['id'], fields='shares')
        shares = shares['shares']['count']
    except :
        shares = 0
    #Comments
    try:
        comments = graph.get_object(id=post['id']+"/comments?summary=total_count")
        comments = comments['summary']['total_count']
    except :
        comments = 0
    #Engagement
    try:
        page_likes = likes_page['fan_count']
        engagement = ((likes+shares+comments)/page_likes)*100
    except :
        engagement = 0
        page_likes = 0
    #Message
    try:
        message = post['message']
    except:
        message = ""
    #Date
    try:
        created_time = post['created_time']
    except:
        created_time = ""
    #ID
    try:
        post_id = post['id']
    except:
        post_id = ""

    data.append(
        dict(zip(['post_id', 'created', 'post_content', 'likes', 'shares', 'comments', 'engagement', 'likes_page'], \
                 [post_id, created_time, message, likes, shares, comments, engagement, page_likes])))

    return data





def facebook_intg(outfile, publisher, access_token, dateFrom, dateTo):
    '''
        Facebook Integration Process - Publisher Full Load
    '''

    print ("Tarantulla Facebook - Starting... - Publisher: " + publisher)
    print("Process Started at: "+ time.strftime("%d/%m/%Y %H:%M:%S"))

    if access_token == '':
        graph = face_oauth(access_token, version='3.0')
    else:
        graph = facebook.GraphAPI(access_token, version='3.0')

    profile = graph.get_object(publisher)
    request = 'posts?since='+dateFrom+'&until='+dateTo+'&limit=100'
    posts = graph.get_connections(profile['id'], request)
    page_likes = graph.get_object(id=profile['id'], fields='fan_count')

    toContinue = True

    while toContinue:
        try:
            for post in posts['data']:
                result = get_engagement(graph=graph, post=post, likes_page=page_likes)
                print("Collecting " + publisher + " : " + str(posts['data'].index(post)) + " statistics collected", end='\r')
            posts = requests.get(posts['paging']['next']).json()
            print("Process Finished at: "+ time.strftime("%d/%m/%Y %H:%M:%S") + " - Total of posts collected = "+str(len(posts['data'])))
        except KeyError:
            output(result, outfile)
            toContinue = False