class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics"""
        )

    def add(self, args):
        priority = int(args[0])
        task = args[1]

        list_keys = sorted(list(self.current_items))
        found = 0

        if priority in list_keys:
            found = 1

        if found:
            last = -1
            i = priority + 1
            while i in list_keys:
                last = i
                i += 1
            if last == -1:
                self.current_items[priority + 1] = self.current_items[priority]
            else:
                new_current_items = dict(
                    [
                        (key, self.current_items[key])
                        for key in list_keys
                        if key < priority or key > last
                    ]
                )
                for i in range(priority, last + 1):
                    new_current_items[i + 1] = self.current_items[i]

                self.current_items = new_current_items

        self.current_items[priority] = task
        self.write_current()
        print(f'Added task: "{task}" with priority {priority}')

    def done(self, args):
        priority = int(args[0])

        for p in self.current_items:
            if p == priority:
                self.completed_items.append(self.current_items[p])
                self.write_completed()
                del self.current_items[p]
                self.write_current()
                print("Marked item as done.")
                return

        print(f"Error: no incomplete item with priority {priority} exists.")

    def delete(self, args):
        priority = int(args[0])

        found = 0
        for p in self.current_items:
            if p == priority:
                found = 1
                break
        if found:
            del self.current_items[p]
            self.write_current()
            print(f"Deleted item with priority {priority}")
            return
        print(f"Error: item with priority {priority} does not exist. Nothing deleted.")

    def ls(self):
        index = 1
        for p in sorted(self.current_items.keys()):
            print(f"{index}. {self.current_items[p]} [{p}]")
            index += 1

    def report(self):

        self.read_current()
        self.read_completed()

        print(f"Pending : {len(self.current_items)}")
        index = 1
        for p in sorted(self.current_items.keys()):
            print(f"{index}. {self.current_items[p]} [{p}]")
            index += 1
        print(f"\nCompleted : {len(self.completed_items)}")
        index = 1
        for item in self.completed_items:
            print(f"{index}. {item}")
            index += 1
