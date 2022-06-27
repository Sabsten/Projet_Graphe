import folium
import webbrowser
import os

def genererCarte(ordrepasage, PointLivraison, algo):
    "Génère une carte"
    #Permet de génerer une carte
    Carte = folium.Map(location=[PointLivraison[0].Latitude, PointLivraison[0].Longitude], zoom_start=10)
    i=1
    for each_item in PointLivraison:
        folium.Marker(location=[each_item.Latitude, each_item.Longitude], popup=f"{each_item.Ville}", icon=folium.Icon(color='green')).add_to(Carte)
        each_item.ordre = i-1
        i=i+1

    for each_item in ordrepasage:
        for indice in range(len(ordrepasage[each_item])):
            if type(ordrepasage[each_item][indice]) == str:
                ordrepasage[each_item][indice] = 0

    ListColor = ['red', 'blue', 'green', 'grey', 'orange', 'purple', 'pink', 'brown', 'black']
    for indice in ordrepasage:
        folium.PolyLine([(float(PointLivraison[each_item].Latitude), float(PointLivraison[each_item].Longitude)) for each_item in ordrepasage[indice]], color=ListColor[indice], weight=2).add_to(Carte)


    filename = 'Map' + algo +'.html'
    filepath = os.path.abspath(os.path.dirname(__file__))+ "\\Maps\\" + filename
    Carte.save(filepath)
    webbrowser.open('file://' + filepath)