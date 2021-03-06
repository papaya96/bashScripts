import paho.mqtt.client as mqtt
import time
import csv
import mysql.connector


def on_connect(client, userdata, flags, rc):
  print("Connected with result code" + str(rc))
  client.subscribe("osh/all/test/com", 0)
  client.subscribe("osh/kit/coffee/prep", 0)
  client.subscribe("osh/kit/coffee/stat", 0)
#  client.subscribe("012/io/1675495/butt1", 0)
#  client.subscribe("018/io/1675495/butt1", 0)
  client.subscribe("016/+/io/+", 0)
  client.subscribe("013/+/io/+", 0)

def on_message(client, userdata, msg):
  print(msg.topic + " " + str(msg.payload))
  serial = msg.topic[4:11]
  type = msg.topic[0:3]
  rules(serial, type, msg.topic)

def verify(serial):
    sql = "SELECT target, source, detail, active, type, user_name FROM rules WHERE source='%s'" % serial
    query.execute(sql)
    db.commit()
    count1 = query.rowcount
    if not count1 > 0:
      client.publish("all/stat", "NOT QUITE")
      return False
    else:
      client.publish("all/stat", "RETURNED GOOD")
      return query

def rules(serial, type, topic):
  result = verify(serial)
  if not result:
    return False
  row = result.fetchone()
  while row is not None:
    target = row[0]
    source = row[1]
    detail = row[2]
    active = row[3]
    typeT = row[4]
    print "Source: %s, Detail: %s, Active?: %s" %(source, detail, active)
    loops = len(detail) / 6
    for i in range(loops):
      if type == "016":
        event = detail[i:i+3]
        comm = detail[i+3:i+6]
        if event == "MD1":
          if comm[0] == 'D':
            executeD(typeT, comm, target)
          elif comm[0] == 'L':
            executeL(comm, target)
      elif type == "013":
    row = result.fetchone()

def executeD(type, comm, target):
  if type == "013":
    if comm[1:3] == "ON":
      mqttComm = "1"
    elif comm[1:3] == "OF":
      mqttComm = "0"
    else:
      mqttComm = "T"
    mqttTop = "{}/cm/{}/03".format(type, target)
    print "Publishing to: %s" % mqttTop
    client.publish(mqttTop, mqttComm)
    
#  if type == "018":
#    else:
#      for (user_name, id) in result:
#        print "User: %s, id: %d" % user_name, id
#  if serial == '1738927':
#    if (topic[15:20] == "butt1"):
#      print time.time() * 1000
#      print time.time() * 1000 - int(float(timeKeep[serial]))
#      if  (time.time() * 1000 - int(float(timeKeep[serial]))) < doubleTime:
#        client.publish("osh/" + serial + "/gpio/12", "TOG", 0, False)
#      else:
#        timeKeep[serial] = time.time() * 1000

doubleTime = 700
infile = open('assets/timeKeep.csv', 'r')
timeKeep = dict(csv.reader(infile))

db = mysql.connector.connect(user='pythonUser', password='24518000pythonUser', host='ha-records.cxdm8r7jhkbf.us-east-1.rds.amazonaws.com', database='ha_records')
query = db.cursor(buffered = True)

client = mqtt.Client(client_id="aws1", clean_session=False)
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("aws", "24518000aws")
client.connect("mqtt.oreillyj.com", 1883, 60)

client.loop_forever()
