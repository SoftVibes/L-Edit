import curses, os
from curses import wrapper

def sql_init():
	pass

def store_unsaved(filepath, content):
	pass

def main(stdscr):
	data = {"mode": "explorer", "dir": os.getcwd(), "files": os.listdir(), "top":0, "selected": 0, "msg": ""}

	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)

	WHITE_AND_BLACK = curses.color_pair(1)
	BLACK_AND_WHITE = curses.color_pair(2)
	YELLOW_AND_BLACK = curses.color_pair(3)
	BLACK_AND_YELLOW = curses.color_pair(4)

	def render():
		mode = data["mode"]
		dir = data["dir"]
		files = data["files"]
		top = data["top"]
		selected = data["selected"]
		msg = data["msg"]

		if mode == "explorer":
			y, x = stdscr.getmaxyx()

			#Formatting and printing path
			path = ""
			if len(dir) >= x:
				path = dir[:x]
			else:
				path = dir + " "*(x - len(dir))
			stdscr.addstr(0, 0, path, BLACK_AND_WHITE)

			#Printing files and directories
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

	def handle_input(ch, data):
		mode = data["mode"]
		dir = data["dir"]
		files = data["files"]
		top = data["top"]
		selected = data["selected"]
		msg = data["msg"]
		y, x = stdscr.getmaxyx()

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
					msg = "An error occured while trying to change directories"
			elif ch == curses.KEY_RIGHT:
				try:
					os.chdir(files[selected])
					dir = os.getcwd()
					files = os.listdir()
					top = 0
					selected = 0
				except:
					msg = "An error occured while trying to change directories"
		data["mode"] = mode
		data["dir"] = dir
		data["files"] = files
		data["top"] = top
		data["selected"] = selected
		data["msg"] = msg

		return data

	while True:
		stdscr.clear()
		stdscr.refresh()
		render()
		ch = stdscr.getch()
		new_data = handle_input(ch, data)
		data = new_data
	print(data["top"], data["selected"])

wrapper(main)
