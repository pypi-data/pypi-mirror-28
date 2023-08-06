import json
import os
from external.local.table_display import draw_table
from external.local.json_io import get_json_content
from external.local.json_handler import get_ws_exercises
from gf.start.start_service import generate_exercise_info
from external.local.file_operator import get_work_dir
from gf.settings import WORKSHOP_DATA_FILENAME


def correct_and_finished(taskname, method):
    item_dict["exercises"][taskname][method] = True


def controller():
    ws_exercises = get_ws_exercises()
    table_input = first_row_table_input(ws_exercises)
    lists_from_the_json(table_input, ws_exercises)
    draw_table(table_input)


def first_row_table_input(ws_exercises):
    method_list = ["exercises"]
    table_input = []
    for index, task in enumerate(ws_exercises):
        for method in ws_exercises[task]:
            if method != "test_path":
                if index == 0:
                    method_list.append(method)
    table_input.append(method_list)
    return table_input


def lists_from_the_json(table_input, ws_exercises):
    for task in ws_exercises:
        task_list = []
        task_list.append(task)
        method_values = []
        for method in ws_exercises[task]:
            if method != "test_path":
                method_values.append(ws_exercises[task][method])
        for status in method_values:
            task_list.append(status)
        table_input.append(task_list)
    return table_input
