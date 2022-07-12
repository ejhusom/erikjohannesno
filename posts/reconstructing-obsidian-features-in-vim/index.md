---
title: "Reconstructing Obsidian features in Vim and Bash"
date: 2021-05-24T21:47:12+02:00
type: ["posts"]
draft: true
tags:
categories:
---

I have a large collection of plain text files  (mostly Markdown) that contain all my notes and writings, both for work and non-work, which I navigate and modify using Vim, fzf, shell scripts and command line utilities (on mobile I use the excellent app [Working Copy]()).
Everything is of course synced and version-controlled using Git.
I recently discovered that Obsidian has a range of interesting features, and since it is meant to manage a collection of Markdown-notes (which still can be synced through a git-repo between desktop and mobile apps), I could try it out without having to do any changes at all to my current structure or formatting of my files. 
I downloaded the apps for desktop and mobile, and everything was good to go.

The most exciting features for me in Obsidian are the following:

- Easily link between files, both between individual notes and inserting images into notes by using Markdown syntax.
- Open link to another file with a keypress.
- Button for opening a random note (yes, I actually find this useful, because it creates opportunities for sparking ideas through serendipity, and it can also work as "spaced repetition" for things you want to learn or remember).
- Links between files are updated automatically when you rename or move a file.


I think Obsidian works great in general, and even though it is closed source software, anyone can write plugins for it.
There are many useful "community plugins" that really increases the usefulness of the program.
However, I kept missing writing in my usual text editor at the command line.
Obsidian has the option of using Vim keybindings, but that does not replace the configurability of Vim, and the advantage of using command line utilities and scripting as a part of the workflow. 
Also, I kept hitting `ctrl-W [h,j,k,l]` in order to change between panes in Obsidian, but of course `ctrl-W` means "close file" when you are outside the command line.
The user experience of Obsidian on iOS is a bit "messy" in my opinion, and I found myself opening Working Copy more often than Obsidian to edit files. 
Navigating the file explorer in Obsidian on both desktop and mobile is less than optimal, among other things because of no easy way to collapse all folders, and I found myself scrolling a lot.
Some of my complaints can be fixed through plugins, either existing ones or by writing one myself, but the power of the command line  is either way out of reach.
Because if this, I wanted instead to reconstruct in Vim (or at the command line) some of the Obsidian features I liked the most.


### Easily insert links to other files

To make this work, the links to other files has to be relative paths (otherwise images and links won't work properly when rendering the Markdown in HTML).
With the plugin fzf.vim, the following line maps `ctrl-x ctrl-f` to search for any file in the parent directory from which you opened Vim (which means I always open Vim from the root directory of my note collection) and insert its relative path from the current open file:

```vim
```

### Open link to another file with a keypress

Vim already had functionality for this, I just didn't know about it.
`ctrl-w ctrl-f` opens the filepath under the cursor. 

### Opening a random note

This one was easily implemented in a bash script:


```shell

```



### Automatically update links when renaming or moving file

This one was the hardest to figure out.




    