from mapbox import Datasets

datasets = Datasets(access_token="sk.eyJ1IjoiYW5hbnRqIiwiYSI6ImNqcm5pa3NjbDA2cW8zeW8zb25nOTczY2sifQ.QkSZBaZnn6KxwO-YpRtA8A")

def getJSON(name):
    collections = datasets.list_features('cjrna6cc80dbo2wphvazyuf89').json()
    collections = collections['features']
    out = -1
    for col in collections:
        if (col['properties']['title'] == name):
            out = col
            break
    return out

def update(name, value):
    data = getJSON(name)
    if (not(data == -1)):
        data['properties']['description'] = value
        update = datasets.update_feature('cjrna6cc80dbo2wphvazyuf89', data['id'], data).json()
        return update
    else:
        return None
    