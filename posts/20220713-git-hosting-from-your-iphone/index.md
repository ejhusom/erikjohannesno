---
title: "On self-hosting, local storage and portable git hosting on iPhone"
date: 2022-07-13T07:47:12+02:00
type: ["posts"]
draft: false
tags:
categories:
---

I prefer having control of my own data, and therefore try to avoid using cloud services if I absolutely don't have to (e. g., at work I'm pretty much forced to use the cloud services of my employer, which is Microsoft of course).
Earlier I have been self-hosting some services, including file storage (Nextcloud), music server (Subsonic), git (gitea) and social media (Hubzilla).
Then I moved to a place where I couldn't easily set up my own server with port forwarding for external access, and my self-hosting was put on pause.
As an experiment, partly motivated by the increased focus on the environmental impact of the expanding use of servers and cloud services, I attempted to reduce my use of cloud services to a minimum. 
Some of the things I did:

- Deleted my Spotify account and started using only my own local music collection (extra privacy benefit of eliminating the data collection of Spotify)
- Stopped using cloud file storage (up until then I had used Nextcloud and MEGA), and moved to using local storage with backups on external hard drives
- Archived all emails to local storage, keeping my email inbox clean.
- Deleted old and unecessary GitHub and Codeberg repositories.

I moved to a more offline workflow, and realized that I don't need to have all my digital stuff instantly available on any device with an Internet connection.
This also have the added benefit of enabling me to go offline, which often improves my focus, without losing access to my files.
Since I now live a place without Wi-Fi, it is a great advantage that I'm not that dependent on bandwith.

The single most important cloud service for me, both professionally and privately, is git hosting.
It is where I sync most of my work, code, notes and writings.
Some things are private/personal (or at least should be hidden from the eyes of others), which of course are kept in private repos, but I would much prefer to host those repos myself.
One option I have been considering is to pay for hosting of my own gitea instance, but I both want to save money and avoid having another cloud service (even though it would be managed by myself).
I could also choose to have local repos without storage in the cloud, but I need to easily keep the repos synced between my personal latop, work laptop and phone.
I started playing with the idea of having a portable git server on a Raspberry Pi Zero, powered by a power bank, which could set up its own Wi-Fi and start a git server automatically when booted and let me push and pull from repos hosted on it.
This would however require me to carry an extra device.

I then realized that maybe my phone, an iPhone, could serve as the git server instead.
The App Store lists some apps that claim to be able to setup a git server, but after reading a couple of the prvacy policies, I decided I would sleep better at night if I didn't have to trust some ambiguous wording on what and how data is collected.
I use the Working Copy git client app a lot, which can serve the git repos in the app on a WebDAV server.
I was able to access the server through Finder on macOS, but I gave up after failing to connect to it at the command line from Ubuntu.
Instead I tried setting up a git server at the command line in the iSH app.
It proved to be the simplest and most usable approach for me.
When using the iSH app, the setup is identical to how you would do it when setting up a git server on a normal Linux machine.
In the app I installed git and git-daemon (they have to be installed individually):

```shell
apk add git
apk add git-daemon
```

Then I initialized a bare git repo:

```shell
mkdir myrepo.git
cd myrepo.git
git init --bare
```

To serve the repo (and any other git repos in the same folder:

```shell
cd ..
git daemon --reuseaddr --base-path=. --export-all --verbose --informative-errors --enable=receive-pack
```

If you want to disable the ability to push to the repos (i. e., clone-only access), skip the last flag.
To clone repos into Working Copy on the same phone, use `git://127.0.0.1:9418/myrepo.git` or `git://localhost:9418/myrepo.git` as the URL (9418 is the default port of `git daemon`).
I don't think iSH handles running inthe background well, so you might have to press "Clone" in Working Copy (after filling out the URL), switch to iSH to enable the server to complete the request, and then back to Working Copy.
To clone to other devices, run

```shell
git clone git://[ipaddress]:9418/myrepo.git
```

where `[ipaddress]` is the IP-address of your iPhone on the local network (the other devices obviously have to be connected to the same network).

The drawback is of course having to start the server before every push/pull, but for my uses this is acceptable.
Also, there is no authentication required to pull from the server, so one needs to be sure that there are no bad actors on the local network.

Next up is trying the same thing on an Android phone (which I expect to be just as easy to do inside Termux), and then maybe setting up a mobile git server with authentication.


