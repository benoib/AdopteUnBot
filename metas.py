#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, json

def mystats(text):
    stats = {}
    text = re.sub(r'[\n\r]', '', text)
    for var in ["myAchievementsData", "chatListing", "earnedAchievement", "new_chat", "myPicture", "myPseudo", "myId", "new_mail"]:
        defv = "var %s = " % var
        pos = text.find(defv)
        if pos != -1:
            stats[var] = text[pos+len(defv):text.find(";",pos+len(defv))].strip("'")
            try:
                stats[var] = json.loads(stats[var])
            except:
                pass
    if stats["myAchievementsData"]:
        stats["nb_achievements"] = len(stats["myAchievementsData"])
    if stats["chatListing"]:
        stats["nb_chats"] = len(stats["chatListing"]["contacts"])
    for var in ["mails", "visites", "basket", "chats"]:
        key = "new_%s" % var.rstrip("s")
        if '<li id="%s"' % var in text:
            stats[key] = int(re.search(r'<li id="%s".*?<span[^>]*>(\d+)</span>' % var, text).group(1))
    if "<span class='nb-products'>" in text:
        stats["panier"] = int(re.search(r"<span class='nb-products'>(\d+)</span>", text).group(1))
    if "Il me reste " in text:
        stats["charmes"] = int(re.search(r"Il me reste (\d+) charme", text).group(1))
    if '<p id="ma-popu">' in text:
        stats["score"] = int(re.sub(r'\D', '', re.search(r'<p id="ma-popu">.*?<span>(.*?)</span>', text).group(1)))
    return stats

def diffstats(s1, s2, key=""):
    if s1 == s2:
        pass
    elif type(s1) == dict:
        for k in s1.keys():
            diffstats(s1[k], s2[k], k)
    elif type(s1) == list:
        for i in range(max(len(s1), len(s2))):
            if i > len(s1)-1:
                print "[INFO] - %s: _ -> %s" % (key, s2[i])
            elif i > len(s2)-1:
                print "[INFO] - %s: %s -> _" % (key, s1[i])
            else:
                diffstats(s1[i], s2[i], key)
    else:
        print "[INFO] - %s: %s -> %s" % (key, s1, s2)
