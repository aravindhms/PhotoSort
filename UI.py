import os.path
import PySimpleGUI as sg
import photosort

# First the window layout in 2 columns

source_folder_input = [
    [
        sg.Text("Source Folder"),
        sg.In(size=(25, 1), enable_events=True, key="SOURCE"),
        sg.FolderBrowse(),
    ]

]

destination_folder_input = [
    [
        sg.Text("Destination Folder"),
        sg.In(size=(25, 1), enable_events=True, key="DESTINATION"),
        sg.FolderBrowse(),
    ]

]
Status = [
    [sg.Text(key="STATUS", size=(50, 1), enable_events=True)]
]

Progress = [
    []
]

layout = [
    [
        sg.Column(source_folder_input)
    ],
    [
        sg.Column(destination_folder_input),

    ],
    [
        sg.Column(Status),

    ],
    [

        sg.Button("Move", enable_events=True, key="MOVE", button_color=(sg.YELLOWS[0], sg.BLUES[0])),
        sg.Button("Copy", enable_events=True, key="COPY", button_color=(sg.YELLOWS[0], sg.BLUES[0]))
    ]
]

window = sg.Window("PhotoSort", layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == "SOURCE":
        source_folder = values["SOURCE"]

        try:
            # Get list of files in folder
            file_list = os.listdir(source_folder)
            filecount = photosort.image_count(source_folder)
        except Exception:
            file_list = []
            filecount = 0
        window["STATUS"].update(str(filecount) + " photo(s) found.")

    if event == "DESTINATION":
        destination_folder = values["DESTINATION"]
        if source_folder == destination_folder:
            window["STATUS"].update("Warning : Source and destination are same!!!")

    if event == "MOVE":
        window["STATUS"].update("Processing....")
        process_type = 'move'
        window["STATUS"].update(str(filecount) + " photo(s) moved.")

    if event == "COPY":
        window["STATUS"].update("Processing....")
        process_type = 'copy'
        print(source_folder+"/", destination_folder, process_type)
        sort_count, error_count = photosort.sort_photos(source_folder+"/", destination_folder, process_type)
        window["STATUS"].update(str(sort_count) + " photo(s) copied. "+str(error_count) + " Error(s) ")
