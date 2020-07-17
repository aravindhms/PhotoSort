import PySimpleGUI as sg
import os.path

# First the window layout in 2 columns

source_folder = [
    [
        sg.Text("Source Folder"),
        sg.In(size=(25, 1), enable_events=True, key="SOURCE"),
        sg.FolderBrowse(),
    ]

]

destination_folder = [
    [
        sg.Text("Destination Folder"),
        sg.In(size=(25, 1), enable_events=True, key="DESTINATION"),
        sg.FolderBrowse(),
    ]

]
Status = [
    [sg.Text(key="STATUS",size=(25, 1), enable_events=True)]
]



layout = [
    [
        sg.Column(source_folder)
    ],
    [
        sg.Column(destination_folder),

    ],
    [
        sg.Column(Status),

    ],
    [

        sg.Button("Move"),
        sg.Button("Copy")
    ]
]

window = sg.Window("PhotoSort", layout)
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == "SOURCE":
        folder = values["SOURCE"]
        window["STATUS"].update("OK")
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            # and f.lower().endswith((".png", ".gif"))
        ]
        # window["-FILE LIST-"].update(fnames)
        print(file_list)