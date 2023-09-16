import json
import pandas as pd
from shapely.geometry import Polygon, Point, MultiPolygon

############
# TO STATE #
############


def geolocationToState(latitude, longitude):
    data = json.load(open('gz_2010_us_040_00_500k.json'))
    df = pd.DataFrame(data["features"])
    df['Location'] = df['properties'].apply(lambda x: x['NAME'])
    df['Type'] = df['geometry'].apply(lambda x: x['type'])
    df['Coordinates'] = df['geometry'].apply(lambda x: x['coordinates'])
    df_new = pd.DataFrame()

    for idx, row in df.iterrows():

        if row['Type'] == 'MultiPolygon':
            list_of_polys = []
            df_row = row['Coordinates']
            for ll in df_row:
                list_of_polys.append(Polygon(ll[0]))
            poly = MultiPolygon(list_of_polys)

        elif row['Type'] == 'Polygon':
            df_row = row['Coordinates']
            poly = Polygon(df_row[0])

        else:
            poly = None

        row['Polygon'] = poly
        # print(row)
        df_new = pd.concat([df_new, pd.DataFrame([row])], ignore_index=True)

    point = Point(latitude, longitude)
    df_selection = df_new.drop(columns=['type', 'properties', 'geometry','Coordinates'] )
    state = df_selection.apply(lambda row: row['Location'] if row['Polygon'].contains(point) else None, axis=1).dropna()

    return state
    

def ipv4ToState(ipv4):
    print("TODO!")
    return

def phoneToState(phone):
    print("TODO!")
    return



for i in range (1000):
    if (i%10 ==0 ):
        print(i)
    geolocationToState(-118.250903, 33.774719)