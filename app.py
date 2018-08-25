# import necessary libraries
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///babies.sqlite"

#db = SQLAlchemy(app)


#Erased class stuff here

# create route that renders OIS_page.html template
@app.route("/")
def home():
    #return render_template("OIS_page.html")
    return render_template("index.html")

@app.route("/college")
def colly():
    return render_template("college.html")

@app.route("/about")
def me():
    return render_template("about.html")

@app.route("/maps")
def mappy():
    # Dependencies
    import requests
    import json
    import pandas as pd
    import numpy as np
    # Google developer API key
    from config import gkey
    from gmplot import gmplot

    #The last year included in the analysis or only year included
    Yr=2018
    #If you want cumulative maps, change this to False
    only_year=False
    #Victim API
    url2 = "http://clt-charlotte.opendata.arcgis.com/datasets/2564657b1e9a4883ab388badadbeef6d_5.geojson"
    response2 = requests.get(url2)
    df_victim = pd.DataFrame(response2.json()['features'])
    arr2 = []
    for b in df_victim["properties"]:
        arr2.append(b)
    df_victim = pd.DataFrame(arr2)
    #This drops an incident that is missing a latitude or a longitude
    df_victim = df_victim.dropna(axis=0, subset=['Latitude', 'Longitude'],how='any')
    df_victim=df_victim.reset_index(drop=True)
    #This drops an incident that is outside our year range
    for row in range(len(df_victim)):
        if only_year==False:
            if df_victim["YR"][row]>Yr:
                df_victim=df_victim.drop(row)
        else:
            if df_victim["YR"][row]!=Yr:
                df_victim=df_victim.drop(row)
            
    df_victim=df_victim.reset_index(drop=True)
    #Incident Data
    url4 = "http://clt-charlotte.opendata.arcgis.com/datasets/36b534fc414640fa843fc780f6d9aaf5_4.geojson"
    response4 = requests.get(url4)
    df_incident = pd.DataFrame(response4.json()['features'])
    arr4 = []
    for b in df_incident["properties"]:
        arr4.append(b)
    df_incident = pd.DataFrame(arr4)
    # Place map
    gmap = gmplot.GoogleMapPlotter(df_victim["Latitude"].mean(), df_victim["Longitude"].mean(), 11.5)

    arr = []
    for i in range(len(df_victim["Longitude"])):
        arr.append((df_victim["Latitude"][i],df_victim["Longitude"][i]))
        incident = df_victim["INCIDENT_ID"][i]
        description=df_incident.loc[df_incident["INCIDENT_ID"]==incident,["NARRATIVE"]]
        simpler_des=description.values[0]
        s_d=simpler_des[0]
        addy=df_incident.loc[df_incident["INCIDENT_ID"]==incident,["LOCATION"]]
        simpler_addy=addy.values[0]
        s_a=simpler_addy[0]
        #print(description)
        #print(simpler_des)
        #print(s_d)
        #try:
        #    gmap.marker(df_victim['Latitude'][i], df_victim['Longitude'][i],
        #                title=df_incident.loc[df_incident["INCIDENT_ID"]==incident,["NARRATIVE"]])
        #gmap.marker(df_victim['Latitude'][i], df_victim['Longitude'][i],title=description)
        each_title="Year: "+str(df_victim['YR'][i])+" Injury Type: "+df_victim['INDIVIDUAL_INJURY_TYPE'][i]+'\\n'+"Address: "+s_a+'\\n'+s_d
        gmap.marker(df_victim['Latitude'][i], df_victim['Longitude'][i],title=each_title)

    if len(df_victim)!=0:
        # Scatter points
        shots_lats, shots_lons = zip(*arr)
        gmap.scatter(shots_lats, shots_lons, 'rgb(200,0,0)', size=200, marker=False)
    else:
        gmap.marker(35.24, -80.82,title=":)")


    # Draw
    if only_year==True:
        gmap.draw("CMPD_Shootings_Map_"+str(Yr)+"exclusive.html")
    else:
        gmap.draw("CMPD_Shootings_Map_"+str(Yr)+".html")

    import webbrowser

    if only_year==True:
        webbrowser.open_new_tab("CMPD_Shootings_Map_"+str(Yr)+"exclusive.html")
    else:
        webbrowser.open_new_tab("CMPD_Shootings_Map_"+str(Yr)+".html")
    return render_template("maps.html")

# Query the database and send the jsonified results
@app.route("/OIS_page/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        #num = request.form["findNum"]
        #st = request.form["findSt"]
        #city = request.form["findCity"]
        #stt = request.form["findStt"]
        address=request.form["findAddy"]
        narrative=""
        yr=""
        loc_of_shooting=""
        #print("Yo")

        # Dependencies
        import requests
        import json
        import pandas as pd
        import numpy as np
        # Google developer API key
        from config import gkey
        from gmplot import gmplot
        import textwrap
        #http://clt-charlotte.opendata.arcgis.com/datasets/36b534fc414640fa843fc780f6d9aaf5_4.geojson
        #Incident Data
        url4 = "http://clt-charlotte.opendata.arcgis.com/datasets/36b534fc414640fa843fc780f6d9aaf5_4.geojson"
        response4 = requests.get(url4)
        df_incident = pd.DataFrame(response4.json()['features'])
        arr4 = []
        for b in df_incident["properties"]:
            arr4.append(b)
        df_incident = pd.DataFrame(arr4)
        #check that we read in
        #print(df_incident.head())
        #This drops an incident that is missing a latitude or a longitude
        df_incident = df_incident.dropna(axis=0, subset=['Latitude', 'Longitude'],how='any')
        df_incident=df_incident.reset_index(drop=True)
        #another check
        #print(df_incident.head())
        #geocoding does not want spaces, so we replace them with plus signs in the city
        #city=city.replace(" ","+")
        #address=num+" "+st+" "+city+", "+stt
        address=address.replace(",","+")
        address=address.replace(".","+")
        address=address.replace(" ","+")

        #Now we use google to find the person's search address
        base_url="https://maps.googleapis.com/maps/api/geocode/json?address="
        key_base="&key="+gkey

        response=requests.get(base_url+address+key_base,"Problem").json()
        print(response)
        if response =="Problem":
                
            nearest_lat=float('nan')
            nearest_lng=float('nan')

        else:
            try:
                nearest_lat=response["results"][0]["geometry"]["location"]["lat"]
                nearest_lng=response["results"][0]["geometry"]["location"]["lng"]
            except:
                nearest_lat=float('nan')
                nearest_lng=float('nan')
        #Now compare the user's address to the shootings and see which is closest
        from math import sin, cos, sqrt, atan2, radians

        #Greatest distance between any two points in U.S. territory: 9,514 miles. 
        #So, distances should be smaller than this and we are looking for the closest points
        winning_distance=9514

        # approximate radius of earth in km
        R = 6373.0
        lat1 = radians(abs(nearest_lat))
        lng1 = radians(abs(nearest_lng))

        for row in range(len(df_incident)):
            lat2 = radians(abs(df_incident.iloc[row]["Latitude"]))
            lng2 = radians(abs(df_incident.iloc[row]["Longitude"]))
            
            dlng = lng2 - lng1
            dlat = lat2 - lat1

            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlng / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c
            
            if distance<winning_distance:
                winning_distance=distance
                location_index=row

        #The fatality/nonfatality/miss data is stored in a different API, so we will grab that info and cross reference by incident ID
        #This will tell us if the shooting resulted in a fatality, nonfatality, or miss
        #Victim API
        url2 = "http://clt-charlotte.opendata.arcgis.com/datasets/2564657b1e9a4883ab388badadbeef6d_5.geojson"
        response2 = requests.get(url2)
        df_victim = pd.DataFrame(response2.json()['features'])
        arr2 = []
        for b in df_victim["properties"]:
            arr2.append(b)
        df_victim = pd.DataFrame(arr2)
        try:
            incident_num=df_incident.iloc[location_index]["INCIDENT_ID"]
            result=df_victim.loc[df_victim["INCIDENT_ID"]==incident_num,"INDIVIDUAL_INJURY_TYPE"].values
        except:
            result="No shooting information found."   

        #Print the results, including the official recorded narrative
        if result!="No shooting information found.":
            #print("\n**********************************************************************\n")
            #print("I have found the closest officer involved shooting to your search location.")
            #print("\n**********************************************************************\n")
            #print("Let me tell you about it:")
            yr=str(df_incident.iloc[location_index]["YR"])
            loc_of_shooting=df_incident.iloc[location_index]["LOCATION"].title()
            #print("In "+str(df_incident.iloc[location_index]["YR"])+ " there was a shooting at "+df_incident.iloc[location_index]["LOCATION"].title()+".")
            #print("According to records, this is what happened:")
            #This prevents words from being chopped up
            
  
            narrative=textwrap.fill(df_incident.iloc[location_index]["NARRATIVE"])

   
            #print(narrative+"\n")
            #print("The shooting resulted in a "+str(result))

            intro="In "+yr+" there was a shooting at "+ loc_of_shooting+", the closest officer-involved shooting to your requested address: "+address
            description="The following describes the incident: "+ narrative
        return render_template('OIS_page.html', intro=intro, description=description)
        #return render_template('OIS_page.html', result=result, narrative=narrative, address = address, yr=yr, loc_of_shooting=loc_of_shooting)

        #return render_template('OIS_page.html', name=name, answer=answer, gender = gender, tweeting_name=a['full_text'],additional=link)

#This part said render form.html in the pet pals thing
    return render_template("OIS_page.html")
    #return render_template('index.html', {'boys': years["boys"],'girls': years["girls"]})



if __name__ == "__main__":
    app.run()