---
title: "A feed for sports and outdoors activities"
date: 2022-08-02T21:47:12+02:00
type: ["posts"]
draft: false
tags:
categories:
---

![Screenshot of the activity feed](posts/20220802-a-feed-for-sports-and-outdoors-activities/activities.png)

[Strava](https://www.strava.com/) is a popular tool for sharing sports and outdoors activities, and has become the *de facto* social medium for athletes, runners, cyclists etc. 
I'm not the kind of person who likes to share every detail about how I train or my daily activities, but sometimes I enjoy sharing a workout, race or a route I've done in the mountains. 
I also enjoy keeping control of my own data and how it is accessed and displayed, and I have only reluctantly used Strava and Garmin Connect to share activities.

While I'm waiting for someone to make an [ActivityPub](https://en.wikipedia.org/wiki/ActivityPub)-enabled Strava-clone, I made my own [Activities-feed](https://erikjohannes.no/activities.html) on this website.
To add an activity, I upload a gpx-file containing the GPS-track (including elevation data and timestamps), and optionally add a textfile with a description and images from the activity.
The feed uses [Leaflet](https://leafletjs.com/) and [leaflet-evelation.js](https://github.com/Raruto/leaflet-elevation) to display gpx-files on map tiles, and plot the elevation profile and speed graph.
I have chosen to use map tiles from [OpenTopoMap](https://opentopomap.org/), since it's important for me to have detailed terrain information when visualizing the activities.
My very messy [build-script](https://codeberg.org/erikjohannes/erikjohannesno/src/branch/pages/buildsite.py) for this website takes care of putting the text description and images in the correct places. 

This way I can easily share workouts and activities with friends and family.
The activities also show up in my [RSS-feed](https://erikjohannes.no/index.xml).
The feed is not very visually pleasing yet, but I will probably fine-tune to CSS to make it look a bit more clean.

Check out the new feed at [this link](https://erikjohannes.no/activities.html)!
