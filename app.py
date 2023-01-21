from distutils.log import debug
from flask import Flask, render_template, request
import pyodbc
import math
from math import sin, cos, sqrt, atan2

server = 'danna.database.windows.net' 
database = 'datadxs' 
username = 'dxsdb' 
password = 'Happyme@1'

dbConnection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = dbConnection.cursor()


app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/viewEarthquakes')
def viewEarthquakes():
    cursor.execute("Select * from ds")
    result = cursor.fetchall()
    return render_template('viewEntity.html', countRows = len(result), values = result)

@app.route('/largestSmallestQuakes')
def largestSmallestQuakes():
    return render_template('largestSmallestQuakes.html')

@app.route('/lsQuakes', methods=['POST','GET'])
def lsQuakes():
    if request.form['ls'] == "largest" :
        cursor.execute("select top "+request.form['count']+" ds.id, place, mag from ds INNER JOIN dsi on ds.id = dsi.id where mag between "+request.form['magstart']+" and "+request.form['magend']+" order BY mag DESC")
        result = cursor.fetchall()
        return render_template('largestSmallestQuakes.html', countRows = len(result), values = result)
    else:
        cursor.execute("select top "+request.form['count']+" ds.id, place, mag from ds INNER JOIN dsi on ds.id = dsi.id where mag between "+request.form['magstart']+" and "+request.form['magend']+" order BY mag ASC")
        result = cursor.fetchall()
        return render_template('largestSmallestQuakes.html', countRows = len(result), values = result)
   

@app.route('/twolatlong')
def twolatlong():
    return render_template('twolatlong.html')

@app.route('/findtwolatlon', methods=['POST','GET'])
def findtwolatlon():
    cursor.execute("select time, latitude, longitude, ds.id, place from ds INNER JOIN dsi on ds.id = dsi.id where (latitude >= '"+request.form['minlatitude']+"' and latitude <= '"+request.form['maxlatitude']+"') and (longitude >= '"+request.form['maxlongitude']+"' and longitude <= '"+request.form['minlongitude']+"') ")
    result=cursor.fetchall()
    return render_template('twolatlong.html', countRows = len(result), values = result)


@app.route('/dateTimeNet')
def dateTimeNet():
    return render_template('dateTimeNet.html')


@app.route('/finddateTimeNet', methods=['POST','GET'])
def finddateTimeNet():
    cursor.execute("select net, count(net) as countOfNet from ds INNER JOIN dsi on ds.id = dsi.id where SUBSTRING(time,0,11) = '"+request.form['date']+"' and (SUBSTRING(time,12,12)>='"+request.form['timestart']+"' or SUBSTRING(time,12,12)<='"+request.form['timeend']+"') group by net order by countOfNet DESC")
    result=cursor.fetchall()
    return render_template('dateTimeNet.html', countRows = len(result), values = result)


@app.route('/updateMagnitude')
def updateMagnitude():
    return render_template('updateMagnitude.html')

@app.route('/updMag', methods=['POST','GET'])
def updMag():
    cursor.execute("update ds set mag = "+request.form['magnew']+" from ds INNER JOIN dsi on ds.id = dsi.id  where  net = '"+request.form['net']+"' and (mag between "+request.form['magstart']+" and "+request.form['magend']+")")
    count=cursor.rowcount()
    return render_template('viewEntity.html', countRows = count)









# @app.route('/searchMagnitude')
# def searchMagnitude():
#     return render_template('searchMagnitude.html')

# @app.route('/sMag', methods=['POST','GET'])
# def sMag():
#     print("Select * from earth where mag between "+request.form['magstart']+" and "+request.form['magend']+" ")
#     cursor.execute("Select * from earth where mag between "+request.form['magstart']+" and "+request.form['magend']+" ")
#     result = cursor.fetchall()
#     return render_template('viewEntity.html', countRows = len(result), values = result)



# @app.route('/lsQuakes', methods=['POST','GET'])
# def lsQuakes():
#     if request.form['ls'] == "largest" :
#         cursor.execute("select top "+request.form['count']+" * from earth order BY mag DESC")
#         result = cursor.fetchall()
#         return render_template('viewEntity.html', countRows = len(result), values = result)
#     else:
#         cursor.execute("select top "+request.form['count']+" * from earth order BY mag ASC")
#         result = cursor.fetchall()
#         return render_template('viewEntity.html', countRows = len(result), values = result)
    

# @app.route('/dateMagnitudeRange')
# def dateMagnitudeRange():
#     return render_template('dateMagnitudeRange.html')

# @app.route('/dateMagRange', methods=['POST','GET'])
# def dateMagRange():
#     cursor.execute("Select * from earth where (mag between "+request.form['magstart']+" and "+request.form['magend']+") and (period between '"+request.form['dateStart']+"' and '"+request.form['dateEnd']+"') ")
#     result = cursor.fetchall()
#     return render_template('viewEntity.html', countRows = len(result), values = result)

# @app.route('/latlonkm')
# def latlonkm():
#     return render_template('latlonkm.html')

# def getDitanceWithlatlongkm(userlat,userlong, alllat, alllong):
#     radius = 6373.0
#     lat = math.radians(alllat) - math.radians(userlat)
#     long = math.radians(alllong) - math.radians(userlong)
#     trigVal = sin(lat / 2)**2 + cos(math.radians(userlat)) * cos(math.radians(alllat)) * sin(long / 2)**2
#     area = 2 * atan2(sqrt(trigVal), sqrt(1 - trigVal))
#     finalDis = radius * area
#     return finalDis

# @app.route('/findlatlonkm', methods=['POST','GET'])
# def findlatlonkm():
#     if request.form['lsa'] == "largest" :
#         cursor.execute("Select * from earth where type = 'earthquake' order by mag DESC")
#         result = cursor.fetchall()
#     elif request.form['lsa'] == "smallest" :
#         cursor.execute("Select * from earth where type = 'earthquake' order by mag ASC")
#         result = cursor.fetchall()
#     else:
#         cursor.execute("Select * from earth where type = 'earthquake'")
#         result = cursor.fetchall()
#     finalOp = list()
#     for res in result:
#         if float(getDitanceWithlatlongkm(float(request.form['latitude']), float(request.form['longitude']), res[1], res[2])) <= int(request.form['km']):
#             finalOp.append(res)
#     if request.form['lsa'] == "all" :
#         return render_template('viewEntity.html', countRows = len(finalOp), values = finalOp)
#     else:
#         return render_template('viewEntity.html', countRows = 1, values = [finalOp[0]])

# @app.route('/moreOftenNightDay')
# def latlmoreOftenNightDayonkm():
#     return render_template('moreOftenNightDay.html')

    
# @app.route('/nightDay', methods=['POST','GET'])
# def nightDay():
#     cursor.execute("select * from earth where (mag between "+request.form['magstart']+" and "+request.form['magend']+") and type= 'earthquake' and period not in (select period from earth where (SUBSTRING(period,12,12) > '20:00:00.000' or SUBSTRING(period,12,12)  <'06:00:00.000'))" )
#     result1=cursor.fetchall()
#     cursor.execute("select *  from earth where (SUBSTRING(period,12,12)>'20:00:00.000' or SUBSTRING(period,12,12)<'06:00:00.000') and (mag between "+request.form['magstart']+" and "+request.form['magend']+") and type= 'earthquake' ")
#     result2=cursor.fetchall()
#     return render_template('moreOftenNightDay.html', countRowsDay = len(result1), valuesDay = result1, countRowsNight = len(result2), valuesNight = result2)

# @app.route('/clusters')
# def clusters():
#     return render_template('clusters.html')

    
# @app.route('/findClusters', methods=['POST','GET'])
# def findClusters():
#     cursor.execute("Select * from earth where mag= '"+request.form['mag']+"' and type='earthquake'")
#     result=cursor.fetchall()
#     return render_template('clusters.html', countRows = len(result), values = result)

# @app.route('/magNet')
# def magNet():
#     return render_template('magNet.html')

# @app.route('/findmagNet', methods=['POST','GET'])
# def findmagNet():
#     cursor.execute("Select top 5 period, latitude, longitude, id, place from earth where (mag between '"+request.form['magstart']+"' and '"+request.form['magend']+"') and (net = '"+request.form['net']+"') order by mag desc")
#     result=cursor.fetchall()
#     return render_template('viewEntity.html', countRows = len(result), values = result)




# @app.route('/compareLatLong')
# def compareLatLong():
#     return render_template('comparelatlonkm.html')


# @app.route('/findComparelatlonkm', methods=['POST','GET'])
# def findComparelatlonkm():
#     if request.form['longitude1'].endswith('W'):
#         deli = "-"
#         long1Len = len(request.form['longitude1'])-1
#         long1sub = request.form['longitude1'][0:long1Len]
#         long1 = deli+long1sub
#         print(long1)
#     if request.form['longitude2'].endswith('W'):
#         deli = "-"
#         long2Len = len(request.form['longitude2'])-1
#         long2sub = request.form['longitude2'][0:long2Len]
#         long2 = deli+long2sub
#         print(long2)
#     if request.form['latitude1'].endswith('N'):
#         lat1Len = len(request.form['latitude1'])-1
#         lat1sub = request.form['latitude1'][0:lat1Len]
#         lat1 = lat1sub
#         print(lat1)
#     if request.form['latitude2'].endswith('N'):
#         lat2Len = len(request.form['latitude2'])-1
#         lat2sub = request.form['latitude2'][0:lat2Len]
#         lat2 = lat2sub
#         print(lat2)
#     cursor.execute("Select * from earth where type = 'earthquake'")
#     result = cursor.fetchall()
#     finalOp1 = list()
#     finalOp2 = list()
#     for res in result:
#         if float(getDitanceWithlatlongkm(float(lat1), float(long1), res[1], res[2])) <= int(request.form['km1']):
#             finalOp1.append(res)
#         if float(getDitanceWithlatlongkm(float(lat2), float(long2), res[1], res[2])) <= int(request.form['km2']):
#             finalOp2.append(res)
    
#     return render_template('comparelatlonkm.html',p1 = request.form['place1'], countRows1 = len(finalOp1), values1 = finalOp1, p2 = request.form['place2'], countRows2 = len(finalOp2), values2 = finalOp2)








# @app.route('/updRec', methods=['POST','GET'])
# def recordUpdate():
#     cursor.execute("update danna set class = '"+request.form['class']+"', comments = '"+request.form['comments']+"' where name = '"+request.form['name']+"' ")
#     cursor.execute("Select * from danna where name = '"+request.form['name']+"'")
#     result = cursor.fetchall()
#     return render_template("viewEntity.html",values = result)

# @app.route('/addEntry', methods=['POST','GET'])
# def addEntry():
#     cursor.execute("INSERT INTO danna VALUES ('"+request.form['name']+"','"+request.form['age']+"','"+request.form['class']+"','"+request.form['picture']+"','"+request.form['comments']+"')")
#     cursor.execute("Select * from danna where name = '"+request.form['name']+"'")
#     result = cursor.fetchall()
#     return render_template("viewEntity.html",values = result)


if __name__ == '__main__':
    app.run(debug = True)
    