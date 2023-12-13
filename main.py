import curses, os
from curses import wrapper
import mysql.connector as db

def sql_init():
	con = db.connect(host="localhost", user="leditor", password="Gensys666")
	cur = con.cursor()
	cur.execute("CREATE DATABASE IF NOT EXISTS Ledit")
	cur.execute("USE Ledit")
	cur.execute("CREATE TABLE IF NOT EXISTS Ledit(path varchar(200), content longtext)")
	con.commit()
	con.close()

def store_unsaved(files):
	con = db.connect(host="localhost", user="leditor", password="Gensys666")
	cur = con.cursor()
	cur.execute("USE Ledit")
	for file in files:
		cur.execute("INSERT INTO Ledit VALUES(\"" + file['path'] + "\", \"" + file['content'] + "\")")
	con.commit()
	con.close()

def load_unsaved():
	con = db.connect(host="localhost", user="leditor", password="Gensys666")
	cur = con.cursor()
	cur.execute("USE Ledit")
	cur.execute("SELECT * FROM Ledit")
	files = cur.fetchall()
	openfiles = []
	for file in files:
		openfiles.append({"path": file[0], "content": file[1], "char": 0, "line": 0, "top": 0})
	cur.execute("TRUNCATE TABLE Ledit")
	con.commit()
	con.close()
	return openfiles

def main(stdscr):
	data = {"mode": "explorer", "dir": os.getcwd(), "files": os.listdir(), "top":0, "selected": 0, "msg": "", "openfiles": load_unsaved(), "opentop": 0, "openselected": 0}
	msg2 = {"^E": "Explorer", ">": "Enter dir", "<": "Exit dir", "Enter": "Open", "^F": "View Files", "^K": "Cut", "^L": "Copy", "^U": "Paste", "^W": "Find", "^X": "Save & Exit"}

	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)

	WHITE_AND_BLACK = curses.color_pair(1)
	BLACK_AND_WHITE = curses.color_pair(2)
	YELLOW_AND_BLACK = curses.color_pair(3)
	BLACK_AND_YELLOW = curses.color_pair(4)

	def render():
		stdscr.clear()
		stdscr.refresh()

		mode = data["mode"]
		dir = data["dir"]
		files = data["files"]
		top = data["top"]
		selected = data["selected"]
		msg = data["msg"]
		openfiles = data["openfiles"]
		opentop = data["opentop"]
		openselected = data["openselected"]
		y, x = stdscr.getmaxyx()

		stdscr.addstr(y - 2, 0, msg, WHITE_AND_BLACK)
		c = (x - len(" ".join(list(msg2.keys())) + "  ".join(list(msg2.values()))))//2
		for item in msg2:
			stdscr.addstr(y - 1, c, item, BLACK_AND_WHITE)
			c += len(item)
			stdscr.addstr(y - 1, c, " " + msg2[item] + "  ", WHITE_AND_BLACK)
			c += len(msg2[item]) + 3

		if mode == "explorer":
			path = ""
			if len(dir) >= x:
				path = dir[:x]
			else:
				path = dir + " "*(x - len(dir))
			stdscr.addstr(0, 0, path, BLACK_AND_WHITE)

			l = top + y - 3 if top + y - 3 <= len(files) else len(files)

			for i in range(top, l):

				if os.path.isfile(dir + "/" + files[i]):
					if selected == i:
						stdscr.addstr(i - top + 1, 0, f"{i + 1}. " + files[i], BLACK_AND_WHITE)
					else:
						stdscr.addstr(i - top + 1, 0, f"{i + 1}. " + files[i], WHITE_AND_BLACK)
				elif os.path.isdir(dir + "/" + files[i]):
					if selected == i:
						stdscr.addstr(i - top + 1, 0, f"{i + 1}. " + files[i], BLACK_AND_YELLOW)
					else:
						stdscr.addstr(i - top + 1, 0, f"{i + 1}. " + files[i], YELLOW_AND_BLACK)
		elif mode == "files":
			stdscr.addstr(0, 0, " "*((x - 18)//2) + "List of open files" + " "*((x - 18)//2), BLACK_AND_WHITE)
			l = opentop + y - 3 if opentop + y - 3 <= len(openfiles) else len(openfiles)

			for i in range(opentop, l):
				if openselected == i:
					stdscr.addstr(i - opentop + 1, 0, f"{i + 1}. " + openfiles[i]["path"], BLACK_AND_WHITE)
				else:
					stdscr.addstr(i - opentop + 1, 0, f"{i + 1}. " + openfiles[i]["path"], WHITE_AND_BLACK)
		elif mode == "editor":
			file = openfiles[openselected]
			lines = file["content"].split("\n")
			ltop = file["top"]
			line, char = file["line"], file["char"]
			path = file["path"]
			if len(dir) >= x:
				path = path[:x]
			else:
				path = path + " "*(x - len(path))
			stdscr.addstr(0, 0, path, BLACK_AND_WHITE)

			l = ltop + y - 3 if ltop + y - 3 <= len(lines) else len(lines)

			for i in range(ltop, l):
				substr = [lines[i][j:j + x] for j in range(0, len(lines[i]), x)] + ['']
				if i == line:
					stdscr.addstr(i - ltop + 1, 0, substr[char//x], WHITE_AND_BLACK)
				else:
					stdscr.addstr(i - ltop + 1, 0, substr[0], WHITE_AND_BLACK)

			stdscr.move(line - ltop + 1, char % x)



	def handle_input(ch, data):
		mode = data["mode"]
		dir = data["dir"]
		files = data["files"]
		top = data["top"]
		selected = data["selected"]
		msg = data["msg"]
		openfiles = data["openfiles"]
		opentop = data["opentop"]
		openselected = data["openselected"]
		y, x = stdscr.getmaxyx()


		if ch == 5:
			data["mode"] = "explorer"
			return data
		elif ch == 6:
			data["mode"] = "files"
			return data

		if mode == "explorer":
			if ch == curses.KEY_DOWN:
				if selected == len(files) - 1:
					top = 0
					selected = 0
				elif selected == top + y - 4:
					top += y - 3
					selected = top
				else:
					selected += 1
			elif ch == curses.KEY_UP:
				if selected == 0:
					while len(files) - 1 - top > y - 3:
						top += y - 3
					selected = len(files) - 1
				elif selected == top:
					top -= y - 3
					selected -= 1
				else:
					selected -= 1
			elif ch == curses.KEY_LEFT:
				try:
					os.chdir("..")
					dir = os.getcwd()
					files = os.listdir()
					top = 0
					selected = 0
				except:
					msg = "The directory you're trying to access requires higher privileges"
			elif ch == curses.KEY_RIGHT:
				if os.path.isfile(dir + "/" + files[selected]):
					msg = "You cannot change directories into a file!"
				else:
					try:
						os.chdir(files[selected])
						dir = os.getcwd()
						files = os.listdir()
						top = 0
						selected = 0
					except:
						msg = "The directory you're trying to access requires higher privileges"
			elif ch == curses.KEY_ENTER or ch == 10 or ch == 13:
				if os.path.isdir(dir + "/" + files[selected]):
					msg = "You cannot edit a directory!"
				elif dir + "/" + files[selected] in [i["path"] for i in openfiles]:
					msg = "That file is already being edited"
				else:
					try:
						with open(dir + "/" + files[selected], "r+") as f:
							openfiles.append({'path': dir + "/" + files[selected], 'content': f.read(), 'line': 0, 'char': 0, 'top': 0})
						msg = "The file has been opened in the editor"
					except Exception as e:
						print(e)
						msg = "The file you're trying to edit requires higher privileges"
			elif ch == 24:
				store_unsaved(openfiles)
				exit()

		elif mode == "files":
			if ch == curses.KEY_DOWN:
				if openselected == len(openfiles) - 1:
					opentop = 0
					openselected = 0
				elif openselected == opentop + y - 4:
					opentop += y - 3
					openselected = opentop
				else:
					openselected += 1
			elif ch == curses.KEY_UP:
				if openselected == 0:
					while len(openfiles) - 1 - opentop > y - 3:
						opentop += y - 3
					openselected = len(openfiles) - 1
				elif openselected == opentop:
					opentop -= y - 3
					openselected -= 1
				else:
					openselected -= 1
			elif ch == curses.KEY_ENTER or ch == 10 or ch == 13:
				mode = "editor"
			elif ch == 24:
				store_unsaved(openfiles)
				exit()

		elif mode == "editor":
			if ch == curses.KEY_DOWN:
				if openfiles[openselected]["line"] < len(openfiles[openselected]["content"].split("\n")) - 2:
					openfiles[openselected]["line"] += 1
					if openfiles[openselected]["char"] > len(openfiles[openselected]["content"].split("\n")[openfiles[openselected]["line"]]):
						openfiles[openselected]["char"] = len(openfiles[openselected]["content"].split("\n")[openfiles[openselected]["line"]])
					if openfiles[openselected]["line"] > openfiles[openselected]["top"] + y - 4:
						openfiles[openselected]["top"] += 1
			elif ch == curses.KEY_UP:
				if openfiles[openselected]["line"] > 0:
					openfiles[openselected]["line"] -= 1
					if openfiles[openselected]["char"] > len(openfiles[openselected]["content"].split("\n")[openfiles[openselected]["line"]]):
						openfiles[openselected]["char"] = len(openfiles[openselected]["content"].split("\n")[openfiles[openselected]["line"]])
					if openfiles[openselected]["line"] < openfiles[openselected]["top"]:
						openfiles[openselected]["top"] -= 1
			elif ch == curses.KEY_LEFT:
				if openfiles[openselected]["char"] == 0:
					if openfiles[openselected]["line"] != 0:
						openfiles[openselected]["line"] -= 1
						openfiles[openselected]["char"] = len(openfiles[openselected]["content"].split("\n")[openfiles[openselected]["line"]])
						if openfiles[openselected]["line"] < openfiles[openselected]["top"]:
                                                	openfiles[openselected]["top"] -= 1
				else:
					openfiles[openselected]["char"] -= 1
			elif ch == curses.KEY_RIGHT:
				if openfiles[openselected]["char"] == len(openfiles[openselected]["content"].split("\n")[openfiles[openselected]["line"]]):
					if openfiles[openselected]["line"] < len(openfiles[openselected]["content"].split("\n")) - 2:
						openfiles[openselected]["char"] = 0
						openfiles[openselected]["line"] += 1
						if openfiles[openselected]["line"] > openfiles[openselected]["top"] + y - 4:
                                                	openfiles[openselected]["top"] += 1
				else:
					openfiles[openselected]["char"] += 1
			elif ch == curses.KEY_BACKSPACE:
				if openfiles[openselected]["char"] == 0 and openfiles[openselected]["line"] != 0:
					line, char = openfiles[openselected]["line"], openfiles[openselected]["char"]
					lines = openfiles[openselected]["content"].split("\n")
					p = len(lines[line - 1])
					lines[line - 1] += lines[line]
					lines = lines[:line] + lines[line + 1:]
					openfiles[openselected]["content"] = "\n".join(lines)
					openfiles[openselected]["line"] -= 1
					openfiles[openselected]["char"] = p
				elif openfiles[openselected]["char"] != 0:
					line, char = openfiles[openselected]["line"], openfiles[openselected]["char"]
					lines = openfiles[openselected]["content"].split("\n")
					lines[line] = lines[line][:char - 1] + lines[line][char:]
					openfiles[openselected]["content"] = "\n".join(lines)
					openfiles[openselected]["char"] -= 1
			elif ch == curses.KEY_ENTER or ch == 10 or ch == 13:
				line, char = openfiles[openselected]["line"], openfiles[openselected]["char"]
				lines = openfiles[openselected]["content"].split("\n")
				lines = lines[:line] + [lines[line][:char]] + [lines[line][char:]] + lines[line+1:]
				openfiles[openselected]["content"] = "\n".join(lines)
				openfiles[openselected]["line"] += 1
				openfiles[openselected]["char"] = 0
				if openfiles[openselected]["line"] > openfiles[openselected]["top"] + y - 4:
						openfiles[openselected]["top"] += 1
			elif ch == 24:
				with open("/media/hilogen/Extra Disk1/Projects/L-Edit/log.txt", "w") as f:
					f.write(f"Saved at {openfiles[openselected]['path']}")
				with open(openfiles[openselected]["path"], "w") as f:
					f.write(openfiles[openselected]["content"])
				msg = "File saved successfully"
				openfiles.pop(openselected)
				mode = "files"
			else:
				try:
					line, char = openfiles[openselected]["line"], openfiles[openselected]["char"]
					lines = openfiles[openselected]["content"].split("\n")
					lines[line] = lines[line][:char] + chr(ch) + lines[line][char:]
					openfiles[openselected]["content"] = "\n".join(lines)
					openfiles[openselected]["char"] += 1
				except:
					pass

		data["mode"] = mode
		data["dir"] = dir
		data["files"] = files
		data["top"] = top
		data["selected"] = selected
		data["msg"] = msg
		data["openfiles"] = openfiles
		data["opentop"] = opentop
		data["openselected"] = openselected

		return data

	while True:
		stdscr.clear()
		stdscr.refresh()
		render()
		data["msg"] = ""
		ch = stdscr.getch()
		new_data = handle_input(ch, data)
		data = new_data

sql_init()
wrapper(main)
