# L-Edit
## Created with the much needed companionship of Souhardya Basu, Shreshtha Choudhury & Prachurjo Dutta Roy (they contributed to more or less 20 lines of code, none of which was ultimately used, the companionship helped tho)

---
---

# Pocha Text Editor
## Also my 12th grade AISSCE CS Project (a bit of an overkill for something so meagre) **

---

- Made with Python and the curses module
- Has only been tested on Linux (yet)
- Will make some updates and push them when I get the time and energy

---

You need to have Python installed and the respective curses package for your OS.
It has a built-in directory navigating system, opens the file explorer on startup, find the current working directory on top left. Find shortcuts on the bottom.
Use left and right arrow keys to jump up or down directories, up and down keys to scroll.
Press enter to start editing the selected file from the files list. Go back to files list or explorer to stop editing and exit without saving (slightly unintuitive but I was on a time crunch)
`CTRL+X` saves the file you're editing, removes it from the files list and goes back to the files list or kills the program itself if you have the files list or explorer open.
Killing the program while having files open in the files list will save them into a MySQL database and load them up the next time you open the program (yes this is convoluted, yes this will be updated)

---

`CTRL+E` - Explorer mode, navigate through directories and find your files and add them to the files list
`<` - Go up a directory, i.e. to the parent directory of the directory you are in
`>` - Go down into the highlighted directory
`CTRL+F` - Files list, view the files you have listed for editing
`Enter` - Start editing the highlighted file
`CTRL+X` - Save and close the file you're editing if it's open, kill the entire program if you're in explorer or files list

---

**Features yet to be implemented**
- Internal cut copy feature (use system's cut copy methods for now)
- Find and replace feature
- Settings file to edit color codes, toggle usage of MySQL to store unsaved files, etc.
- Create and import external plugins (a very distant dream)

[^1]: Made with ❤ in Kolkata, India
