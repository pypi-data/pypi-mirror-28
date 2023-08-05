"""
A class that holds a TaskList class and related utilities.

Copyright (C) 2018 Connor Ruggles

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import json
from . import Task

class TaskList(list):
    """holds a list of Tasks"""

    def __init__(self, listFile):
        """initializes this list based on the passed in file"""
        list.__init__(self)
        self._list_file = listFile
        self._task_list = []
        with open(self._list_file, 'r') as json_file:
            data = json_file.read()
            if data:
                data = json.loads(data)
                for tmp_task in data:
                    self._task_list.append(Task.Task(tmp_task["title"], \
                        tmp_task["description"], tmp_task["done"]))

    def __getitem__(self, index):
        """implements the getitem method to iterate over task list"""
        result = self._task_list[index]
        return result

    def __len__(self):
        """len method"""
        return len(self._task_list)

    def add_task(self, task_to_add):
        """adds a task to this list"""
        self._task_list.append(task_to_add)
        self.reload_tasks()

    def delete_task(self, index):
        """deletes a task"""
        del self._task_list[index]
        self.reload_tasks()

    def finish_task(self, index):
        """finishes a task"""
        self._task_list[index].finish()

    def get_tasks(self):
        """retrieves all tasks in this task list"""
        return self._task_list

    def print_tasks(self):
        """prints the list of tasks"""
        for _task in self._task_list:
            print("Title:       {}".format(_task.get_title()))
            print("Description: {}".format(_task.get_description()))
            print("Done:        {}\n".format(str(_task.is_done())))

    def reload_tasks(self):
        """
        gets the task list from the file and reloads the
        task list
        """
        tmp_list = []
        # first iterate through the task list,
        # appending a dict form of each task to a
        # temporary list
        for task_obj in self._task_list:
            tmp_list.append(task_obj.__dict__)
        with open(self._list_file, 'w') as outfile:
            # then dump that temp list to the file
            json.dump(tmp_list, outfile)
            outfile.close()
        # reset the task list
        self._task_list = []
        # re-open the file, and add each entry as a
        # new Task
        with open(self._list_file) as json_file:
            data = json.load(json_file)
            for tmp_task in data:
                self._task_list.append(Task.Task(tmp_task["title"], \
                    tmp_task["description"], tmp_task["done"]))
