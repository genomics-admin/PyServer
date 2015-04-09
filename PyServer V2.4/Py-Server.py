#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi,os,sys,time,datetime
import PyDBConn as PDC
import LogFile as LOG
import traceback

#-----------------Initiliseing values------

global PORT_NUMBER,htmlBuilderPre,htmlBuilderHeadStart,htmlBuilderHeadMid,htmlBuilderHeadStop,htmlBuilderBodyStart,htmlBuilderBodyMid1,htmlBuilderBodyMid2,htmlBuilderBodyMid3,htmlBuilderBodyStop,htmlbuilderPost,homeDIR

PORT_NUMBER = 8083

htmlBuilderPre='<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">'

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
	</style>
	
	
    <style type="text/css">
      body { font-size: 80%; font-family: 'Lucida Grande', Verdana, Arial, Sans-Serif; }
      ul#tabs { list-style-type: none; margin: 30px 0 0 0; padding: 0 0 0.3em 0; }
      ul#tabs li { display: inline; }
      ul#tabs li a { color: #42454a; background-color: #dedbde; border: 1px solid #c9c3ba; border-bottom: none; padding: 0.3em; text-decoration: none; }
      ul#tabs li a:hover { background-color: #f1f0ee; }
      ul#tabs li a.selected { color: #000; background-color: #f1f0ee; font-weight: bold; padding: 0.7em 0.3em 0.38em 0.3em; }
      div.tabContent { border: 1px solid #c9c3ba; padding: 0.5em; background-color: #f1f0ee; }
      div.tabContent.hide { display: none; }
    </style>

    <script type="text/javascript">
    //<![CDATA[

    var tabLinks = new Array();
    var contentDivs = new Array();

    function init() {

      // Grab the tab links and content divs from the page
      var tabListItems = document.getElementById('tabs').childNodes;
      for ( var i = 0; i < tabListItems.length; i++ ) {
        if ( tabListItems[i].nodeName == "LI" ) {
          var tabLink = getFirstChildWithTagName( tabListItems[i], 'A' );
          var id = getHash( tabLink.getAttribute('href') );
          tabLinks[id] = tabLink;
          contentDivs[id] = document.getElementById( id );
        }
      }

      // Assign onclick events to the tab links, and
      // highlight the first tab
      var i = 0;

      for ( var id in tabLinks ) {
        tabLinks[id].onclick = showTab;
        tabLinks[id].onfocus = function() { this.blur() };
        if ( i == 0 ) tabLinks[id].className = 'selected';
        i++;
      }

      // Hide all content divs except the first
      var i = 0;

      for ( var id in contentDivs ) {
        if ( i != 0 ) contentDivs[id].className = 'tabContent hide';
        i++;
      }
    }

    function showTab() {
      var selectedId = getHash( this.getAttribute('href') );

      // Highlight the selected tab, and dim all others.
      // Also show the selected content div, and hide all others.
      for ( var id in contentDivs ) {
        if ( id == selectedId ) {
          tabLinks[id].className = 'selected';
          contentDivs[id].className = 'tabContent';
        } else {
          tabLinks[id].className = '';
          contentDivs[id].className = 'tabContent hide';
        }
      }

      // Stop the browser following the link
      return false;
    }

    function getFirstChildWithTagName( element, tagName ) {
      for ( var i = 0; i < element.childNodes.length; i++ ) {
        if ( element.childNodes[i].nodeName == tagName ) return element.childNodes[i];
      }
    }

    function getHash( url ) {
      var hashPos = url.lastIndexOf ( '#' );
      return url.substring( hashPos + 1 );
    }

    //]]>
    </script>'''

htmlBuilderHeadStop='''
</head>'''

htmlBuilderBodyStart='''
<body onload="init()">
<div class="wrapper">
<h1>Monsanto: VM Search 2.4</h1>'''

htmlBuilderBodyMid1_1='''
<div style="text-align: center;"><a href="http://www.monsanto.com" title="Monsanto logo" style="margin-top:2px;margin-right:2px;margin-bottom:2px;margin-left:2px;" rel="" target="_blank"><img src="http://www.monsanto.com/SharedMonsantoLogos/media-kit/monsanto.png" alt="Monsanto Logo" style="border: 7px solid rgb(255, 255, 255); -webkit-box-shadow: rgba(0, 0, 0, 0.498039) 0px 15px 10px -10px, rgba(0, 0, 0, 0.298039) 0px 1px 4px; box-shadow: rgba(0, 0, 0, 0.498039) 0px 15px 10px -10px, rgba(0, 0, 0, 0.298039) 0px 1px 4px; border-top-left-radius: 7px; border-top-right-radius: 7px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px; float: none; margin: 2px; width: 600px; height: 201px;" /></a></div>
	
	<div><br />
	</div>

    <ul id="tabs">
      <li><a href="#VM">VM Search</a></li>
      <li><a href="#ESX">Physical ESX Host Search</a></li>
      <li><a href="#DS">Data Store Search</a></li>
    </ul>
'''

htmlBuilderBodyMid1_1_1='''
    <div class="tabContent" id="VM">
      <h2>VM Search</h2>
      <div>
			<form method="POST" action="/send1" style="text-align: center;" id="clickMeId">  Search: 
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
			</script>
      </div>
'''

htmlBuilderBodyMid1_2='''
<div style="text-align: center;"><a href="http://www.monsanto.com" title="Monsanto logo" style="margin-top:2px;margin-right:2px;margin-bottom:2px;margin-left:2px;" rel="" target="_blank"><img src="http://www.monsanto.com/SharedMonsantoLogos/media-kit/monsanto.png" alt="Monsanto Logo" style="border: 7px solid rgb(255, 255, 255); -webkit-box-shadow: rgba(0, 0, 0, 0.498039) 0px 15px 10px -10px, rgba(0, 0, 0, 0.298039) 0px 1px 4px; box-shadow: rgba(0, 0, 0, 0.498039) 0px 15px 10px -10px, rgba(0, 0, 0, 0.298039) 0px 1px 4px; border-top-left-radius: 7px; border-top-right-radius: 7px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px; float: none; margin: 2px; width: 600px; height: 201px;" /></a></div>
	
	<div><br />
	</div>

    <ul id="tabs">
      <li><a href="#ESX">Physical ESX Host Search</a></li>
      <li><a href="#DS">Data Store Search</a></li>
      <li><a href="#VM">VM Search</a></li>
    </ul>
'''

htmlBuilderBodyMid1_2_1='''
    <div class="tabContent" id="ESX">
      <h2>Physical ESX Host Search</h2>
      <div>
			<form method="POST" action="/send2" style="text-align: center;" id="clickMeId">  Search: 
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
			</script>
      </div>'''

htmlBuilderBodyMid1_3='''
<div style="text-align: center;"><a href="http://www.monsanto.com" title="Monsanto logo" style="margin-top:2px;margin-right:2px;margin-bottom:2px;margin-left:2px;" rel="" target="_blank"><img src="http://www.monsanto.com/SharedMonsantoLogos/media-kit/monsanto.png" alt="Monsanto Logo" style="border: 7px solid rgb(255, 255, 255); -webkit-box-shadow: rgba(0, 0, 0, 0.498039) 0px 15px 10px -10px, rgba(0, 0, 0, 0.298039) 0px 1px 4px; box-shadow: rgba(0, 0, 0, 0.498039) 0px 15px 10px -10px, rgba(0, 0, 0, 0.298039) 0px 1px 4px; border-top-left-radius: 7px; border-top-right-radius: 7px; border-bottom-right-radius: 7px; border-bottom-left-radius: 7px; float: none; margin: 2px; width: 600px; height: 201px;" /></a></div>
	
	<div><br />
	</div>

    <ul id="tabs">
      <li><a href="#DS">Data Store Search</a></li>
      <li><a href="#VM">VM Search</a></li>
      <li><a href="#ESX">Physical ESX Host Search</a></li>
    </ul>
'''

htmlBuilderBodyMid1_3_1='''
    <div class="tabContent" id="DS">
      <h2>Data Storage Search</h2>
      <div>
			<form method="POST" action="/send3" style="text-align: center;" id="clickMeId">  Search: 
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
			</script>
      </div>'''


htmlBuilderBodyMid2_VM='''

    <div><span style="font-weight: bold;">&nbsp;Data Grid:</span></div>
    <div>
	<table style="border-collapse:collapse;width:100%;">
		<tbody>
			<tr>
				<th> VCNAME </th>
                                <th> VMID </th>
                                <th> NAME </th>
                                <th> DATASTORE_NAME </th>
                                <th> CAPACITYGB </th>
                                <th> FREEGB </th>
                                <th> VMGROUPID </th>
                                <th> ESH_HOSTNAME </th>
                                <th> CONFIGFILENAME </th>
                                <th> VMUNIQUEID </th>
                                <th> RESOURCE_GROUP_ID </th>
                                <th> MEM_SIZE_MB </th>
                                <th> NUM_VCPU </th>
                                <th> BOOTTIME </th>
                                <th> POWER_STATE </th>
                                <th> CLUSTER_NAME </th>
                                <th> VDATACENTER </th>
                                <th> GUESTOS </th>
                                <th> GUEST_STATE </th>
                                <th> MEM_RESV </th>
                                <th> MEM_OVHD </th>
                                <th> CPU_RESERVATION </th>
                                <th> DNS_NAME </th>
                                <th> IP_ADDRESS </th>
                                <th> VMMWARE_TOOL </th>
                                <th> TOOLS_VERSION </th>
                                <th> NUM_NIC </th>
                                <th> NUM_DISK </th>
                                <th> TEMPLATE </th>
                                <th> DESCRIPTION </th>
                                <th> ANNOTATION </th>
                                <th> AGG_COMMDISKMB </th>
                                <th> AGG_UNCOMMDISKMB </th>
                                <th> AGG_UNSHARDISKMB </th>
                                <th> STORUPDTIME </th>
			</tr>
'''
htmlBuilderBodyMid3_VM='''
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


htmlBuilderBodyMid2_ESX='''

    <div><span style="font-weight: bold;">&nbsp;Data Grid:</span></div>
    <div>
	<table style="border-collapse:collapse;width:100%;">
		<tbody>
			<tr>
				<th> VCNAME </th>
                                <th> HOST_NAME </th>
                                <th> HOST_MODEL </th>
                                <th> CPU_MODEL </th>
                                <th> CPU_COUNT </th>
                                <th> CPU_CORE_COUNT </th>
                                <th> CPU_HZ </th>
                                <th> CPU_THREAD_COUNT </th>
                                <th> VM_VCPU_ACTIVE </th>
                                <th> MEM_SIZE </th>
                                <th> THREAD_OVERCommit </th>
                                <th> CORE_OVERCommit </th>
                                <th> MEM_SIZE_MB </th>
                                <th> VM_MEM_SIZE_MB </th>
                                <th> MEM_OVERCommit </th>
                                <th> VM_MEMORY_OVERHEAD </th>
                                <th> VM_MEM_SIZE_MB_POTENTIAL </th>
                                <th> VM_VCPU_ALLOC_POTENTIAL </th>
                                <th> NIC_COUNT </th>
                                <th> HBA_COUNT </th>
                                <th> VM_TOOLS_OK </th>
                                <th> VM_TOOLS_OUT_OF_DATE </th>
                                <th> VM_VCPU_ALLOC </th>
			</tr>
'''
htmlBuilderBodyMid3_ESX='''
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
			</tr>'''


htmlBuilderBodyMid2_DS='''

    <div><span style="font-weight: bold;">&nbsp;Data Grid:</span></div>
    <div>
	<table style="border-collapse:collapse;width:100%;">
		<tbody>
			<tr>
				<th> NAME </th>
                                <th> DS_NAME </th>
                                <th> ACCESSIBLE </th>
                                <th> MOUNT_MODE </th>
                                <th> MOUNTED </th>
                                <th> Total_GB </th>
                                <th> Free_GB </th>
			</tr>
'''
htmlBuilderBodyMid3_DS='''
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
			</tr>'''


htmlBuilderBodyMid4='''
          </tbody>
	</table><br />
	</div>
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


#---Modified the Table data for VM groups from DB outputs
def datamodifier_VM(self,string,data):
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

#---Modified the Table data for ESX groups from DB outputs
def datamodifier_ESX(self,string,data):
    string=string+'''
        <tr>
                <td>'''+str(data.VCName)+'''<br />
                                                        </td>
                <td>'''+str(data.HOST_NAME)+'''<br />
                                                        </td>
                <td>'''+str(data.HOST_MODEL)+'''<br />
                                                        </td>
                <td>'''+str(data.CPU_MODEL)+'''<br />
                                                        </td>
                <td>'''+str(data.CPU_COUNT)+'''<br />
                                                        </td>
                <td>'''+str(data.CPU_CORE_COUNT)+'''<br />
                                                        </td>
                <td>'''+str(data.CPU_HZ)+'''<br />
                                                        </td>
                <td>'''+str(data.CPU_THREAD_COUNT)+'''<br />
                                                        </td>
                <td>'''+str(data.VM_VCPU_ACTIVE)+'''<br />
                                                        </td>
                <td>'''+str(data.MEM_SIZE)+'''<br />
                                                        </td>
                <td>'''+str(data.THREAD_OVERCommit)+'''<br />
                                                        </td>
                <td>'''+str(data.CORE_OVERCommit)+'''<br />
                                                        </td>
                <td>'''+str(data.MEM_SIZE_MB)+'''<br />
                                                        </td>
                <td>'''+str(data.VM_MEM_SIZE_MB)+'''<br />
                                                        </td>
                <td>'''+str(data.MEM_OVERCommit)+'''<br />
                                                        </td>
                <td>'''+str(data.VM_MEMORY_OVERHEAD)+'''<br />
                                                        </td>
                <td>'''+str(data.VM_MEM_SIZE_MB_POTENTIAL)+'''<br />
                                                        </td>
                <td>'''+str(data.VM_VCPU_ALLOC_POTENTIAL)+'''<br />
                                                        </td>
                <td>'''+str(data.NIC_COUNT)+'''<br />
                                                        </td>
                <td>'''+str(data.HBA_COUNT)+'''<br />
                                                        </td>
                <td>'''+str(data.VM_TOOLS_OK)+'''<br />
                                                        </td>
                <td>'''+str(data.VM_TOOLS_OUT_OF_DATE)+'''<br />
                                                        </td>
                <td>'''+str(data.VM_VCPU_ALLOC)+'''<br />
                                                        </td>
        </tr>'''
    return string




#---Modified the Table data for DS groups from DB outputs
def datamodifier_DS(self,string,data):
    string=string+'''
        <tr>
                <td>'''+str(data.NAME)+'''<br />
                                                        </td>
                <td>'''+str(data.DS_NAME)+'''<br />
                                                        </td>
                <td>'''+str(data.ACCESSIBLE)+'''<br />
                                                        </td>
                <td>'''+str(data.MOUNT_MODE)+'''<br />
                                                        </td>
                <td>'''+str(data.MOUNTED)+'''<br />
                                                        </td>
                <td>'''+str(data.Total_GB)+'''<br />
                                                        </td>
                <td>'''+str(data.Free_GB)+'''<br />
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
        if self.path=="/send1":
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
                execCount=  LOG.filelog(homeDIR+"TestLog.txt",str(self.client_address[0]),str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) ,form["fsearch"].value)
                htmlBuilderBodyStart1=htmlBuilderBodyStart+'<p align="right">Hits: '+str(execCount)+'</p>'
                #--single value or multivalue search?
                rValueArr = rValue.split(',')
                print str(rValueArr[0])


                #--modify the content
                dnf ="Data Not Found For : "
                htmlBuilderBodyMid33=htmlBuilderBodyMid3_VM
                for rValue in rValueArr:
                    rValue = str(rValue).strip()
                    #---Cascading if else condition No : 1
                    print "Cascading if else condition No : 1"
                    rows = PDC.getData(rValue,"STLWSQLVCEPRD01","VCENTER","VM")
                    if rows <> "Error":
                              if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_VM:
                                        htmlBuilderBodyMid33=""
                              for row in rows:
                                        print row.VMID, row.NAME, row.DATASTORE_NAME,row.VMGROUPID, row.Mem_Resv
                                        htmlBuilderBodyMid33=datamodifier_VM(self,htmlBuilderBodyMid33,row)
                                        
                    else:
                        #---Cascading if else condition No : 2
                        print "Cascading if else condition No : 2"
                        rows = PDC.getData(rValue,"STLWSQLVCEPRD02","VCENTER","VM")
                        if rows <> "Error":
                                  if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_VM:
                                            htmlBuilderBodyMid33=""
                                  for row in rows:
                                            print row.VMID, row.NAME, row.DATASTORE_NAME,row.VMGROUPID, row.Mem_Resv
                                            htmlBuilderBodyMid33=datamodifier_VM(self,htmlBuilderBodyMid33,row)
                                            
                        else:
                            #---Cascading if else condition No : 3
                            print "Cascading if else condition No : 3"
                            rows = PDC.getData(rValue,"STLWVCSQLPRD03","vcprd55","VM")
                            if rows <> "Error":
                                      if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_VM:
                                                htmlBuilderBodyMid33=""
                                      for row in rows:
                                                print row.VMID, row.NAME, row.DATASTORE_NAME,row.VMGROUPID, row.Mem_Resv
                                                htmlBuilderBodyMid33=datamodifier_VM(self,htmlBuilderBodyMid33,row)
                                                
                            else:
                                #---Cascading if else condition No : 4
                                print "Cascading if else condition No : 4"
                                rows = PDC.getData(rValue,"STLWVCSQLPRD04","NPVC55DB","VM")
                                if rows <> "Error":
                                          if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_VM:
                                                    htmlBuilderBodyMid33=""
                                          for row in rows:
                                                    print row.VMID, row.NAME, row.DATASTORE_NAME,row.VMGROUPID, row.Mem_Resv
                                                    htmlBuilderBodyMid33=datamodifier_VM(self,htmlBuilderBodyMid33,row)
                                                    
                                else:
                                    #---Cascading if else condition No : 5
                                    print "Cascading if else condition No : 5"
                                    rows = PDC.getData(rValue,"STLWVCDBLAPRD01","VPX","VM")
                                    if rows <> "Error":
                                              if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_VM:
                                                        htmlBuilderBodyMid33=""
                                              for row in rows:
                                                        print row.VMID, row.NAME, row.DATASTORE_NAME,row.VMGROUPID, row.Mem_Resv
                                                        htmlBuilderBodyMid33=datamodifier_VM(self,htmlBuilderBodyMid33,row)
                                                        
                                    else:
                                        #---Cascading if else condition No : 6
                                        print "Cascading if else condition No : 6"
                                        rows = PDC.getData(rValue,"stlwvcssdbprd01","vcenter","VM")
                                        if rows <> "Error":
                                                  if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_VM:
                                                            htmlBuilderBodyMid33=""
                                                  for row in rows:
                                                            print row.VMID, row.NAME, row.DATASTORE_NAME,row.VMGROUPID, row.Mem_Resv
                                                            htmlBuilderBodyMid33=datamodifier_VM(self,htmlBuilderBodyMid33,row)
                                                            
                                        else:
                                            #---Cascading if else condition No : 7
                                            print "Cascading if else condition No : 7"
                                            rows = PDC.getData(rValue,"meuwvcsqlprd01","lasvc55","VM")
                                            if rows <> "Error":
                                                      if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_VM:
                                                                htmlBuilderBodyMid33=""
                                                      for row in rows:
                                                                print row.VMID, row.NAME, row.DATASTORE_NAME,row.VMGROUPID, row.Mem_Resv
                                                                htmlBuilderBodyMid33=datamodifier_VM(self,htmlBuilderBodyMid33,row)
                                                                
                                            else:
                                                #---Cascading if else condition No : 8
                                                print "Cascading if else condition No : 8"
                                                rows = PDC.getData(rValue,"SINWVCSQLPRD01","VPX","VM")
                                                if rows <> "Error":
                                                          if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_VM:
                                                                    htmlBuilderBodyMid33=""
                                                          for row in rows:
                                                                    print row.VMID, row.NAME, row.DATASTORE_NAME,row.VMGROUPID, row.Mem_Resv
                                                                    htmlBuilderBodyMid33=datamodifier_VM(self,htmlBuilderBodyMid33,row)
                                                                    
                                                else:
                                                    #---Cascading if else condition No : 9
                                                    print "Cascading if else condition No : 9"
                                                    rows = PDC.getData(rValue,"STLWVCSQLPRD03","vcprd55","VM")
                                                    if rows <> "Error":
                                                              if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_VM:
                                                                        htmlBuilderBodyMid33=""
                                                              for row in rows:
                                                                        print row.VMID, row.NAME, row.DATASTORE_NAME,row.VMGROUPID, row.Mem_Resv
                                                                        htmlBuilderBodyMid33=datamodifier_VM(self,htmlBuilderBodyMid33,row)
                                                                        
                                                    else:
                                                        #---Final Else
                                                        print "Final Else"
                                                        dnf=dnf+rValue+","

                    #print dnf[:-1]

                #--report error on UI
                if dnf <>"Data Not Found For : ":
                          htmlBuilderBodyMid22='<div><span style="font-weight: bold;Color: Red">&nbsp;'+dnf[:-1]+'</span></div>'+htmlBuilderBodyMid2_VM
                else:
                          htmlBuilderBodyMid22=htmlBuilderBodyMid2_VM
                          
                #--build the html on the fly
                with open(homeDIR+"index"+str(rValueArr[0])+".html", "w") as text_file:
                #--write the content                    
                    text_file.write(htmlBuilderPre+htmlBuilderHeadStart+htmlBuilderHeadMid+htmlBuilderHeadStop+htmlBuilderBodyStart1+htmlBuilderBodyMid1_1+htmlBuilderBodyMid1_1_1+htmlBuilderBodyMid22+htmlBuilderBodyMid33+htmlBuilderBodyMid4+htmlBuilderBodyMid1_2_1+htmlBuilderBodyMid2_ESX+htmlBuilderBodyMid3_ESX+htmlBuilderBodyMid4+htmlBuilderBodyMid1_3_1+htmlBuilderBodyMid2_DS+htmlBuilderBodyMid3_DS+htmlBuilderBodyMid4+htmlBuilderBodyStop+htmlbuilderPost)
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



                
        #-- For ESX's
        if self.path=="/send2":
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
                execCount=  LOG.filelog(homeDIR+"TestLog.txt",str(self.client_address[0]),str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) ,form["fsearch"].value)
                htmlBuilderBodyStart1=htmlBuilderBodyStart+'<p align="right">Hits: '+str(execCount)+'</p>'
                #--single value or multivalue search?
                rValueArr = rValue.split(',')
                print str(rValueArr[0])


                #--modify the content
                dnf ="Data Not Found For : "
                htmlBuilderBodyMid33=htmlBuilderBodyMid3_ESX
                for rValue in rValueArr:
                    rValue = str(rValue).strip()
                    #---Cascading if else condition No : 1
                    print "Cascading if else condition No : 1"
                    rows = PDC.getData(rValue,"STLWSQLVCEPRD01","VCENTER","ESX")
                    if rows <> "Error":
                              if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_ESX:
                                        htmlBuilderBodyMid33=""
                              for row in rows:
                                        print row.HOST_NAME
                                        htmlBuilderBodyMid33=datamodifier_ESX(self,htmlBuilderBodyMid33,row)
                                        
                    else:
                        #---Cascading if else condition No : 2
                        print "Cascading if else condition No : 2"
                        rows = PDC.getData(rValue,"STLWSQLVCEPRD02","VCENTER","ESX")
                        if rows <> "Error":
                                  if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_ESX:
                                            htmlBuilderBodyMid33=""
                                  for row in rows:
                                            print row.HOST_NAME
                                            htmlBuilderBodyMid33=datamodifier_ESX(self,htmlBuilderBodyMid33,row)
                                            
                        else:
                            #---Cascading if else condition No : 3
                            print "Cascading if else condition No : 3"
                            rows = PDC.getData(rValue,"STLWVCSQLPRD03","vcprd55","ESX")
                            if rows <> "Error":
                                      if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_ESX:
                                                htmlBuilderBodyMid33=""
                                      for row in rows:
                                                print row.HOST_NAME
                                                htmlBuilderBodyMid33=datamodifier_ESX(self,htmlBuilderBodyMid33,row)
                                                
                            else:
                                #---Cascading if else condition No : 4
                                print "Cascading if else condition No : 4"
                                rows = PDC.getData(rValue,"STLWVCSQLPRD04","NPVC55DB","ESX")
                                if rows <> "Error":
                                          if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_ESX:
                                                    htmlBuilderBodyMid33=""
                                          for row in rows:
                                                    print row.HOST_NAME
                                                    htmlBuilderBodyMid33=datamodifier_ESX(self,htmlBuilderBodyMid33,row)
                                                    
                                else:
                                    #---Cascading if else condition No : 5
                                    print "Cascading if else condition No : 5"
                                    rows = PDC.getData(rValue,"STLWVCDBLAPRD01","VPX","ESX")
                                    if rows <> "Error":
                                              if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_ESX:
                                                        htmlBuilderBodyMid33=""
                                              for row in rows:
                                                        print row.HOST_NAME
                                                        htmlBuilderBodyMid33=datamodifier_ESX(self,htmlBuilderBodyMid33,row)
                                                        
                                    else:
                                        #---Cascading if else condition No : 6
                                        print "Cascading if else condition No : 6"
                                        rows = PDC.getData(rValue,"stlwvcssdbprd01","vcenter","ESX")
                                        if rows <> "Error":
                                                  if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_ESX:
                                                            htmlBuilderBodyMid33=""
                                                  for row in rows:
                                                            print row.HOST_NAME
                                                            htmlBuilderBodyMid33=datamodifier_ESX(self,htmlBuilderBodyMid33,row)
                                                            
                                        else:
                                            #---Cascading if else condition No : 7
                                            print "Cascading if else condition No : 7"
                                            rows = PDC.getData(rValue,"meuwvcsqlprd01","lasvc55","ESX")
                                            if rows <> "Error":
                                                      if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_ESX:
                                                                htmlBuilderBodyMid33=""
                                                      for row in rows:
                                                                print row.HOST_NAME
                                                                htmlBuilderBodyMid33=datamodifier_ESX(self,htmlBuilderBodyMid33,row)
                                                                
                                            else:
                                                #---Cascading if else condition No : 8
                                                print "Cascading if else condition No : 8"
                                                rows = PDC.getData(rValue,"SINWVCSQLPRD01","VPX","ESX")
                                                if rows <> "Error":
                                                          if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_ESX:
                                                                    htmlBuilderBodyMid33=""
                                                          for row in rows:
                                                                    print row.HOST_NAME
                                                                    htmlBuilderBodyMid33=datamodifier_ESX(self,htmlBuilderBodyMid33,row)
                                                                    
                                                else:
                                                    #---Cascading if else condition No : 9
                                                    print "Cascading if else condition No : 9"
                                                    rows = PDC.getData(rValue,"STLWSQLVCEPRD01","VCENTER","ESX")
                                                    if rows <> "Error":
                                                              if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_ESX:
                                                                        htmlBuilderBodyMid33=""
                                                              for row in rows:
                                                                        print row.HOST_NAME
                                                                        htmlBuilderBodyMid33=datamodifier_ESX(self,htmlBuilderBodyMid33,row)
                                                                        
                                                    else:
                                                        #---Final Else
                                                        print "Final Else"
                                                        dnf=dnf+rValue+","

                    #print dnf[:-1]

                #--report error on UI
                if dnf <>"Data Not Found For : ":
                          htmlBuilderBodyMid22='<div><span style="font-weight: bold;Color: Red">&nbsp;'+dnf[:-1]+'</span></div>'+htmlBuilderBodyMid2_ESX
                else:
                          htmlBuilderBodyMid22=htmlBuilderBodyMid2_ESX
                          
                #--build the html on the fly
                with open(homeDIR+"index"+str(rValueArr[0])+".html", "w") as text_file:
                #--write the content
                    text_file.write(htmlBuilderPre+htmlBuilderHeadStart+htmlBuilderHeadMid+htmlBuilderHeadStop+htmlBuilderBodyStart1+htmlBuilderBodyMid1_2+htmlBuilderBodyMid1_2_1+htmlBuilderBodyMid22+htmlBuilderBodyMid33+htmlBuilderBodyMid4+htmlBuilderBodyMid1_3_1+htmlBuilderBodyMid2_DS+htmlBuilderBodyMid3_DS+htmlBuilderBodyMid4+htmlBuilderBodyMid1_1_1+htmlBuilderBodyMid2_VM+htmlBuilderBodyMid3_VM+htmlBuilderBodyMid4+htmlBuilderBodyStop+htmlbuilderPost)
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




                
        #-- For DS's
        if self.path=="/send3":
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
                execCount=  LOG.filelog(homeDIR+"TestLog.txt",str(self.client_address[0]),str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) ,form["fsearch"].value)
                htmlBuilderBodyStart1=htmlBuilderBodyStart+'<p align="right">Hits: '+str(execCount)+'</p>'
                #--single value or multivalue search?
                rValueArr = rValue.split(',')
                print str(rValueArr[0])


                #--modify the content
                dnf ="Data Not Found For : "
                htmlBuilderBodyMid33=htmlBuilderBodyMid3_DS
                for rValue in rValueArr:                    
                    rValue = str(rValue).strip()

                    #---Query All DS database for the given value
                    
                    rows1 = PDC.getData(rValue,"STLWSQLVCEPRD01","VCENTER","DS")
                    rows2 = PDC.getData(rValue,"STLWSQLVCEPRD02","VCENTER","DS")
                    rows3 = PDC.getData(rValue,"STLWVCSQLPRD03","vcprd55","DS")
                    rows4 = PDC.getData(rValue,"STLWVCSQLPRD04","NPVC55DB","DS")
                    rows5 = PDC.getData(rValue,"STLWVCDBLAPRD01","VPX","DS")
                    rows6 = PDC.getData(rValue,"stlwvcssdbprd01","vcenter","DS")
                    rows7 = PDC.getData(rValue,"meuwvcsqlprd01","lasvc55","DS")
                    rows8 = PDC.getData(rValue,"SINWVCSQLPRD01","VPX","DS")
                    rows9 = PDC.getData(rValue,"STLWSQLVCEPRD01","VCENTER","DS")
                    
                    #---Check if the data was not found anywhere
                    if rows1 == "Error" and rows2 == "Error" and rows3 == "Error" and rows4 == "Error" and rows5 == "Error" and rows6 == "Error" and rows7 == "Error" and rows8 == "Error" and rows9 == "Error":
                        print "Final Else"
                        dnf=dnf+rValue+","
                    else:
                        #---Cascading if else condition No : 1
                        print "Cascading if else condition No : 1"
                        if rows1 <> "Error":
                              if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_DS:
                                        htmlBuilderBodyMid33=""
                              for row in rows1:
                                        print row.NAME
                                        htmlBuilderBodyMid33=datamodifier_DS(self,htmlBuilderBodyMid33,row)
                        
                        #---Cascading if else condition No : 2
                        print "Cascading if else condition No : 2"
                        if rows2 <> "Error":
                              if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_DS:
                                        htmlBuilderBodyMid33=""
                              for row in rows2:
                                        print row.NAME
                                        htmlBuilderBodyMid33=datamodifier_DS(self,htmlBuilderBodyMid33,row)
                        
                        #---Cascading if else condition No : 3
                        print "Cascading if else condition No : 3"
                        if rows3 <> "Error":
                              if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_DS:
                                        htmlBuilderBodyMid33=""
                              for row in rows3:
                                        print row.NAME
                                        htmlBuilderBodyMid33=datamodifier_DS(self,htmlBuilderBodyMid33,row)
                                        

                        #---Cascading if else condition No : 4
                        print "Cascading if else condition No : 4"
                        if rows4 <> "Error":
                              if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_DS:
                                        htmlBuilderBodyMid33=""
                              for row in rows4:
                                        print row.NAME
                                        htmlBuilderBodyMid33=datamodifier_DS(self,htmlBuilderBodyMid33,row)
                                        

                        #---Cascading if else condition No : 5
                        print "Cascading if else condition No : 5"
                        if rows5 <> "Error":
                              if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_DS:
                                        htmlBuilderBodyMid33=""
                              for row in rows5:
                                        print row.NAME
                                        htmlBuilderBodyMid33=datamodifier_DS(self,htmlBuilderBodyMid33,row)
                                        

                        #---Cascading if else condition No : 6
                        print "Cascading if else condition No : 6"
                        if rows6 <> "Error":
                              if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_DS:
                                        htmlBuilderBodyMid33=""
                              for row in rows6:
                                        print row.NAME
                                        htmlBuilderBodyMid33=datamodifier_DS(self,htmlBuilderBodyMid33,row)
                                        

                        #---Cascading if else condition No : 7
                        print "Cascading if else condition No : 7"
                        if rows7 <> "Error":
                              if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_DS:
                                        htmlBuilderBodyMid33=""
                              for row in rows7:
                                        print row.NAME
                                        htmlBuilderBodyMid33=datamodifier_DS(self,htmlBuilderBodyMid33,row)
                                        

                        #---Cascading if else condition No : 8
                        print "Cascading if else condition No : 8"
                        if rows8 <> "Error":
                              if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_DS:
                                        htmlBuilderBodyMid33=""
                              for row in rows8:
                                        print row.NAME
                                        htmlBuilderBodyMid33=datamodifier_DS(self,htmlBuilderBodyMid33,row)
                                        

                        #---Cascading if else condition No : 9
                        print "Cascading if else condition No : 9"
                        if rows9 <> "Error":
                              if htmlBuilderBodyMid33  == htmlBuilderBodyMid3_DS:
                                        htmlBuilderBodyMid33=""
                              for row in rows9:
                                        print row.NAME
                                        htmlBuilderBodyMid33=datamodifier_DS(self,htmlBuilderBodyMid33,row)
                                        

                                        

                    #print dnf[:-1]

                #--report error on UI
                if dnf <>"Data Not Found For : ":
                          htmlBuilderBodyMid22='<div><span style="font-weight: bold;Color: Red">&nbsp;'+dnf[:-1]+'</span></div>'+htmlBuilderBodyMid2_DS
                else:
                          htmlBuilderBodyMid22=htmlBuilderBodyMid2_DS
                          
                #--build the html on the fly
                with open(homeDIR+"index"+str(rValueArr[0])+".html", "w") as text_file:
                #--write the content
                    text_file.write(htmlBuilderPre+htmlBuilderHeadStart+htmlBuilderHeadMid+htmlBuilderHeadStop+htmlBuilderBodyStart1+htmlBuilderBodyMid1_3+htmlBuilderBodyMid1_3_1+htmlBuilderBodyMid22+htmlBuilderBodyMid33+htmlBuilderBodyMid4+htmlBuilderBodyMid1_1_1+htmlBuilderBodyMid2_VM+htmlBuilderBodyMid3_VM+htmlBuilderBodyMid4+htmlBuilderBodyMid1_2_1+htmlBuilderBodyMid2_ESX+htmlBuilderBodyMid3_ESX+htmlBuilderBodyMid4+htmlBuilderBodyStop+htmlbuilderPost)
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




                                                  

    
