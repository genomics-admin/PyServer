#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi,os,sys,time,datetime
import PyDBConn_BUEWVCSQLPRD01 as PDC_BUEWVCSQLPRD01
import PyDBConn_MEUWVCSQLPRD01 as PDC_MEUWVCSQLPRD01
import PyDBConn_SINWVCSQLPRD01 as PDC_SINWVCSQLPRD01
import PyDBConn_STLWSQLVCEPRD01 as PDC_STLWSQLVCEPRD01
import PyDBConn_STLWSQLVCEPRD02 as PDC_STLWSQLVCEPRD02
import PyDBConn_STLWVCDBLAPRD01 as PDC_STLWVCDBLAPRD01
import PyDBConn_STLWVCSQLPRD03 as PDC_STLWVCSQLPRD03
import PyDBConn_STLWVCSQLPRD04 as PDC_STLWVCSQLPRD04
import PyDBConn_STLWVCSSDBPROD01 as PDC_STLWVCSSDBPROD01
import traceback

#-----------------Initiliseing values------

global PORT_NUMBER,htmlBuilderPre,htmlBuilderHeadStart,htmlBuilderHeadMid,htmlBuilderHeadStop,htmlBuilderBodyStart,htmlBuilderBodyMid1,htmlBuilderBodyMid2,htmlBuilderBodyMid3,htmlBuilderBodyStop,htmlbuilderPost,homeDIR

PORT_NUMBER = 8083

htmlBuilderPre='<html>'

htmlBuilderHeadStart='''
<head>'''

htmlBuilderHeadMid='''
<title>Monsanto: VM Search Page</title>
<link rel="stylesheet" type="text/css" media="screen" href="layout.css">
<style>
table, td, th {
    border: 1px solid black;
}

th {
    background-color: green;
    color: white;
	text-align: middle;
	height: 50px;
}
</style>'''

htmlBuilderHeadStop='''
</head>'''

htmlBuilderBodyStart='''
<body>
<div class="wrapper">'''

htmlBuilderBodyMid1='''
<div style="text-align: center;">
<a href="http://www.monsanto.com" title="Monsanto logo" style="margin-top:2px;margin-right:2px;margin-bottom:2px;margin-left:2px;" rel="" target="_blank"><img src="http://www.monsanto.com/SharedMonsantoLogos/media-kit/monsanto.png" alt="Monsanto Logo" style="border: 7px solid rgb(255, 255, 255); -webkit-box-shadow: rgba(0, 0, 0, 0.498039) 0px 15px 10px -10px, rgba(0, 0, 0, 0.298039) 0px 1px 4px; box-shadow: rgba(0, 0, 0, 0.498039) 0px 15px 10px -10px, rgba(0, 0, 0, 0.298039) 0px 1px 4px; border-top-left-radius: 7px; border-top-right-radius: 7px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px; float: none; margin: 2px; width: 600px; height: 201px;" /></a></div>
<div><br />
</div>
<form method="POST" action="/send" style="text-align: center;" id="clickMeId">  Search: 
	<input type="text" name="fsearch" id="clickMeId1"/>  
        <input type="submit" value="Search" onclick="toggleDisplay('loading', 'clickMeId')"/>
</form>
<img id="loading" src="http://bradsknutson.com/wp-content/uploads/2013/04/page-loader.gif" style="display:none;" alt="Please Wait..." height="40" width="40" align="right"/>
<div>&nbsp;</div>

<script>
function toggleDisplay (toBlock, toNone) {
    document.getElementById(toBlock).style.display = 'block';
    document.getElementById(toNone).style.display = 'none';
}
</script>'''

htmlBuilderBodyMid2='''

<div><span style="font-weight: bold;">&nbsp;Data Grid:</span></div>
<div>
	<table style="border-collapse:collapse;width:100%;">
		<tbody>
			<tr>
				<th>VCNAME</th>
                                <th>VMID</th>
                                <th>NAME</th>
                                <th>DATASTORE_NAME</th>
                                <th>CAPACITYGB</th>
                                <th>FREEGB</th>
                                <th>VMGROUPID</th>
                                <th>ESH_HOSTNAME</th>
                                <th>CONFIGFILENAME</th>
                                <th>VMUNIQUEID</th>
                                <th>RESOURCE_GROUP_ID</th>
                                <th>MEM_SIZE_MB</th>
                                <th>NUM_VCPU</th>
                                <th>BOOTTIME</th>
                                <th>POWER_STATE</th>
                                <th>CLUSTER_NAME</th>
                                <th>VDATACENTER</th>
                                <th>GUESTOS</th>
                                <th>GUEST_STATE</th>
                                <th>MEM_RESV</th>
                                <th>MEM_OVHD</th>
                                <th>CPU_RESERVATION</th>
                                <th>DNS_NAME</th>
                                <th>IP_ADDRESS</th>
                                <th>VMMWARE_TOOL</th>
                                <th>TOOLS_VERSION</th>
                                <th>NUM_NIC</th>
                                <th>NUM_DISK</th>
                                <th>TEMPLATE</th>
                                <th>DESCRIPTION</th>
                                <th>ANNOTATION</th>
                                <th>AGG_COMMDISKMB</th>
                                <th>AGG_UNCOMMDISKMB</th>
                                <th>AGG_UNSHARDISKMB</th>
                                <th>STORUPDTIME</th>
			</tr>
'''
htmlBuilderBodyMid3='''
			<tr>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
				<td><br />
					</td>
			</tr>'''
htmlBuilderBodyMid4='''
          </tbody>
	</table><br />
	</div>'''

htmlBuilderBodyStop='''
	<div class="push"></div>

	</div>

	<div class="footer">
		<p class="copyright"><a href="http://www.monsanto.com/" title="Owner">Copyright &copy; Monsanto &mdash; <a href="http://mysites.monsanto.com/Person.aspx?accountname=ASIA%2DPACIFIC%5CSLAIK" title="Developer">Developed by: Sandeep kumar Laik</a> and <a href="http://mysites.monsanto.com/Person.aspx?accountname=ASIA%2DPACIFIC%5CSSKUMA5" title="Designer">Designed by: Santhosh Kumar N</a></p>
	</div>
</body>'''

htmlbuilderPost='''
</html>'''

homeDIR=str(os.path.dirname(os.path.realpath(sys.argv[0])))+'\\'

#print htmlBuilderPre+htmlBuilderHeadStart+htmlBuilderHeadMid+htmlBuilderHeadStop+htmlBuilderBodyStart+htmlBuilderBodyMid1+htmlBuilderBodyMid2+htmlBuilderBodyMid3+htmlBuilderBodyStop+htmlbuilderPost
#----------classes & functions
#----------this function loads any html sent as a filename existing in the code folder
def initHtml(self,filename):
    self.path="/" + filename
    #elif self.path=="/send":
        #self.path="/index_example3.html/f=Corn12"

    try:
        #Check the file extension required and
        #set the right mime type

        sendReply = False
        if self.path.endswith(".html"):
            mimetype='text/html'
            sendReply = True
        if self.path.endswith(".kml"):
            mimetype='application/vnd.google-earth.kml+xml'
            sendReply = True
        if self.path.endswith(".jpg"):
            mimetype='image/jpg'
            sendReply = True
        if self.path.endswith(".gif"):
            mimetype='image/gif'
            sendReply = True
        if self.path.endswith(".js"):
            mimetype='application/javascript'
            sendReply = True
        if self.path.endswith(".css"):
            mimetype='text/css'
            sendReply = True

        if sendReply == True:
            #Open the static file requested and send it
            f = open(curdir + sep + self.path) 
            self.send_response(200)
            self.send_header('Content-type',mimetype)
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
        return

    except IOError:
        self.send_error(404,'File Not Found: %s' % self.path)



def datamodifier_1(self,string,data):
    string=string+'''
        <tr>
                <td>'''+str(data.VCName)+'''<br />
                        </td>
                <td>'''+str(data.VMID)+'''<br />
                                                        </td>
                <td>'''+str(data.NAME)+'''<br />
                                                        </td>
                <td>'''+str(data.DATASTORE_NAME)+'''<br />
                                                        </td>
                <td>'''+str(data.CapacityGB)+'''<br />
                                                        </td>
                <td>'''+str(data.FreeGB)+'''<br />
                                                        </td>
                <td>'''+str(data.VMGROUPID)+'''<br />
                                                        </td>
                <td>'''+str(data.ESH_HOSTNAME)+'''<br />
                                                        </td>
                <td>'''+str(data.CONFIGFILENAME)+'''<br />
                                                        </td>
                <td>'''+str(data.VMUNIQUEID)+'''<br />
                                                        </td>
                <td>'''+str(data.RESOURCE_GROUP_ID)+'''<br />
                                                        </td>
                <td>'''+str(data.MEM_SIZE_MB)+'''<br />
                                                        </td>
                <td>'''+str(data.NUM_VCPU)+'''<br />
                                                        </td>
                <td>'''+str(data.BootTime)+'''<br />
                                                        </td>
                <td>'''+str(data.POWER_STATE)+'''<br />
                                                        </td>
                <td>'''+str(data.cluster_name)+'''<br />
                                                        </td>
                <td>'''+str(data.VDataCenter)+'''<br />
                                                        </td>
                <td>'''+str(data.GuestOS)+'''<br />
                                                        </td>
                <td>'''+str(data.GUEST_STATE)+'''<br />
                                                        </td>
                <td>'''+str(data.Mem_Resv)+'''<br />
                                                        </td>
                <td>'''+str(data.Mem_Ovhd)+'''<br />
                                                        </td>
                <td>'''+str(data.CPU_RESERVATION)+'''<br />
                                                        </td>
                <td>'''+str(data.DNS_NAME)+'''<br />
                                                        </td>
                <td>'''+str(data.IP_ADDRESS)+'''<br />
                                                        </td>
                <td>'''+str(data.VMMWARE_TOOL)+'''<br />
                                                        </td>
                <td>'''+str(data.TOOLS_VERSION)+'''<br />
                                                        </td>
                <td>'''+str(data.NUM_NIC)+'''<br />
                                                        </td>
                <td>'''+str(data.NUM_DISK)+'''<br />
                                                        </td>
                <td>'''+str(data.Template)+'''<br />
                                                        </td>
                <td>'''+str(data.DESCRIPTION)+'''<br />
                                                        </td>
                <td>'''+str(data.ANNOTATION)+'''<br />
                                                        </td>
                <td>'''+str(data.Agg_CommDiskMB)+'''<br />
                                                        </td>
                <td>'''+str(data.Agg_UnCommDiskMB)+'''<br />
                                                        </td>
                <td>'''+str(data.Agg_UnSharDiskMB)+'''<br />
                                                        </td>
                <td>'''+str(data.StorUpdTime)+'''<br />
                                                        </td>
        </tr>'''
    return string



#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    #Handler for the GET requests
    def do_GET(self):
        if self.path=="/":
            initHtml(self,"index.html")


    #Handler for the POST requests
    def do_POST(self):
         #-- For VM's
        if self.path=="/send":
            form = cgi.FieldStorage(
                    fp=self.rfile, 
                    headers=self.headers,
                    environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
            })
            print "================================"
            print "Requested by : "+str(self.client_address[0])
            print "TimeStamp : " + str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) 
            print str(form)
            #--if someone search nothing just for fun throw a try except at them
            try:
                rValue = form["fsearch"].value
                print "Search Value: %s" % form["fsearch"].value
                #--single value or multivalue search?
                rValueArr = rValue.split(',')
                print str(rValueArr[0])


                #--modify the content
                dnf ="Data Not Found For : "
                htmlBuilderBodyMid33=htmlBuilderBodyMid3
                for rValue in rValueArr:
                    #---Cascading if else condition No : 1
                    print "Cascading if else condition No : 1"
                    rows = PDC_BUEWVCSQLPRD01.getData(str(rValue))
                    if rows <> "Error":
                              if htmlBuilderBodyMid33  == htmlBuilderBodyMid3:
                                        htmlBuilderBodyMid33=""
                              for row in rows:
                                        print row.VMID, row.NAME, row.DATASTORE_NAME,row.VMGROUPID, row.Mem_Resv
                                        htmlBuilderBodyMid33=datamodifier_1(self,htmlBuilderBodyMid33,row)
                                        
                    else:
                        #---Cascading if else condition No : 2
                        print "Cascading if else condition No : 2"
                        rows = PDC_BUEWVCSQLPRD01.getData(str(rValue))
                        if rows <> "Error":
                                  if htmlBuilderBodyMid33  == htmlBuilderBodyMid3:
                                            htmlBuilderBodyMid33=""
                                  for row in rows:
                                            print row.VMID, row.NAME, row.DATASTORE_NAME,row.VMGROUPID, row.Mem_Resv
                                            htmlBuilderBodyMid33=datamodifier_1(self,htmlBuilderBodyMid33,row)
                                            
                        else:
                            #---Cascading if else condition No : 3
                            print "Cascading if else condition No : 3"
                            rows = PDC_BUEWVCSQLPRD01.getData(str(rValue))
                            if rows <> "Error":
                                      if htmlBuilderBodyMid33  == htmlBuilderBodyMid3:
                                                htmlBuilderBodyMid33=""
                                      for row in rows:
                                                print row.VMID, row.NAME, row.DATASTORE_NAME,row.VMGROUPID, row.Mem_Resv
                                                htmlBuilderBodyMid33=datamodifier_1(self,htmlBuilderBodyMid33,row)
                                                
                            else:
                                #---Cascading if else condition No : 4
                                print "Cascading if else condition No : 4"
                                rows = PDC_BUEWVCSQLPRD01.getData(str(rValue))
                                if rows <> "Error":
                                          if htmlBuilderBodyMid33  == htmlBuilderBodyMid3:
                                                    htmlBuilderBodyMid33=""
                                          for row in rows:
                                                    print row.VMID, row.NAME, row.DATASTORE_NAME,row.VMGROUPID, row.Mem_Resv
                                                    htmlBuilderBodyMid33=datamodifier_1(self,htmlBuilderBodyMid33,row)
                                                    
                                else:
                                    #---Final Else
                                    print "Final Else"
                                    dnf=dnf+rValue+","

                    #print dnf[:-1]

                #--report error on UI
                if dnf <>"Data Not Found For : ":
                          htmlBuilderBodyMid22='<div><span style="font-weight: bold;Color: Red">&nbsp;'+dnf[:-1]+'</span></div>'+htmlBuilderBodyMid2
                else:
                          htmlBuilderBodyMid22=htmlBuilderBodyMid2
                          
                #--build the html on the fly
                with open(homeDIR+"index"+str(rValueArr[0])+".html", "w") as text_file:
                #--write the content
                    text_file.write(htmlBuilderPre+htmlBuilderHeadStart+htmlBuilderHeadMid+htmlBuilderHeadStop+htmlBuilderBodyStart+htmlBuilderBodyMid1+htmlBuilderBodyMid22+htmlBuilderBodyMid33+htmlBuilderBodyMid4+htmlBuilderBodyStop+htmlbuilderPost)
                #--return the html
                #time.sleep(100)
                initHtml(self,"index"+str(rValueArr[0])+".html")
                #--clear the file once html rendered
                try:
                    with open(homeDIR+"index"+str(rValueArr[0])+".html") as existing_file:
                        existing_file.close()
                        os.remove(homeDIR+"index"+str(rValueArr[0])+".html")
                except:
                    print "delete failed"
            except Exception, err:
                print traceback.format_exc()
                initHtml(self,"index.html")
try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER

    #Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()




                                                  

    
