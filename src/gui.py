import PySimpleGUI as sg
from itertools import islice
from code.text_processor import TextProcessor

def Gui_run():
   
    tp=TextProcessor()

    #--------------------------------------
    #Functions that need to call the engine
    #--------------------------------------

    def RecomendationsGUI():
        for i in tp.recomend():
            yield Show(i)

    def SearchGUI(query):
    #this function manage the query made by the user
        tp.query_processor(query)
        for i in tp.similarity():
            yield Show(i)

    #------------------------------------------


    #-------------------------------------------
    #Auxiliar GUI Function for select categories
    #-------------------------------------------

    def Show(document):
    #these method creates the layaut of a document
        layout=[
            [
                sg.Column([[#This are the plot and the download button
                sg.Multiline(document,expand_x=True,size=(75,3),no_scrollbar=False),
                sg.Button('Is relevant?',button_color='Green',key='Relevant\0'+document)
            ]],justification='r',expand_x=True)]]
        
        return [sg.Frame('',layout=layout,element_justification='c',expand_x=True)]


    sg.theme('Material1')
    sg.set_options(font=('Arial Bold',18))


    def layout_base():#the standard heading for our app
        return [
        [sg.Text('Information Retieval System', font=('Helvetica',50))],
        [sg.Text('Introduce your query', font=('Helvetica',20),pad=3)],
        [sg.Input(key='query',size=(35,2)),sg.Button('Search',font=('Arial',14))]
    ]

    #------------------------------------------

    #-----------------------------------------------------------------------
    # ^   ^    ^    ===  ^   ¡     ===== .   . ^   ¡ ===== ===  /===\  ^   ¡
    # |\ /|   / \    |   | \ |     |     |   | | \ |   |    |   |   |  | \ |
    # | V |  /---\   |   |  \|     |==   |   | |  \|   |    |   |   |  |  \|
    # !   ! /     \ ===  !   v     |      ===  !   v   !   ===  \===/  !   v
    #-----------------------------------------------------------------------

    #displaying the initial recomendations
    layout= layout_base()+ [
        [sg.Text('Recomended for You', font=('Helvetica',30),pad=3)],
        [sg.Column(list(islice(RecomendationsGUI(),10)), scrollable=True, 
                vertical_scroll_only=True, key='scrollable_area',expand_x=True)]
    ]

    window2 = sg.Window('SRI', layout, element_justification='c',finalize=True)
    window2.Maximize()


    #EVENTS
    #--------------

    while True:
        event, values = window2.read()
        if event == sg.WIN_CLOSED:#ends the program
            window2.close()
            break

        if event == 'Search':
        #searches a document based on a query
            if values['query'] == '':
                continue
            layout = layout_base()+[[sg.Text('Results for: '+values['query'], font=('Helvetica',30),pad=3)]]
            
            #gives the results of the search
            layout=layout+[[sg.Column(list(islice(SearchGUI(values['query']),10)),
                    scrollable=True, vertical_scroll_only=True,
                    key='scrollable_area',expand_x=True)]]
            
            window2.close()
            window2=sg.Window('VPN', layout, element_justification='c',finalize=True)
            window2.Maximize()
        
        if event.__contains__('Relevant'):
        #add the document to Relevants
            document=event.split('\0')[1]
            tp.retroalimentation(document)
            window2[event].update(button_color='blue', text='Thank you!!!',disabled=True,disabled_button_color=('white','black'))

Gui_run()