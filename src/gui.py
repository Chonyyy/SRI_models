import PySimpleGUI as sg
from itertools import islice

def Gui_run():
    #Current categories in database. If the categories changes, you must edit this list
    #----------------------------------------------------------------------------------
    
    
    
    #--------------------------------------
    #Functions that need to call the engine
    #--------------------------------------

    def RecomendationsGUI():
        return []
        for i in Recomendations(categories_selected):
            yield Show(i)

    def SearchGUI(query):
    #this function manage the query made by the user
        return []
        for i in Search(query,selected_categories):
            yield Show(i)

    #------------------------------------------


    #-------------------------------------------
    #Auxiliar GUI Function for select categories
    #-------------------------------------------

    def Show(game):
    #these method creates the layaut of a videogame
        layout=[
            [
                sg.Text('year: '), sg.Text(game['year']),
                sg.Text('rating: '), sg.Text(game['rating']),
            ] + [
                #These are the categories of the game
                sg.Button(cat,font=('Arial',10),disabled=True,disabled_button_color=('black','white')) 
                    for cat in game['categories']], 
            [
                sg.Column([[#This are the plot and the download button
                sg.Multiline(game['plot'],expand_x=True,size=(75,3),no_scrollbar=False),
                sg.Button('Download🔽',button_color='Green',key='Download\0'+str(game))
            ]],justification='r',expand_x=True)]]
        
        return [sg.Frame(game['name'],layout=layout,element_justification='c',expand_x=True)]


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
        #searches a game based on a query
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
        
        if event.__contains__('Download'):
        #add the game to recomendations
            name=event.split('\0')[1]
            #Download(name)
            window2[event].update(button_color='blue', text='Downloaded',disabled=True,disabled_button_color=('white','black'))

Gui_run()