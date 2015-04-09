#!/usr/bin/python
import pyodbc
import base64



def getData(findServerName,serverName,DBName,Purpose):
    
    
    #--connction
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+serverName+';DATABASE='+DBName+';'+modd("yLWlpr6","zpWbqcPFgc6ZmKHPxYfFh6fDtK-G2r_K49_kmqp-eKyTpg=="))  #"zpWbqcPFgc6ZmKHPxYfFh6fDtK-G2r_K49_kmqp-eKyTpg==" #"zpWbqcO-d8KXkrzHtnPJrcrf5-Go3X2JjbCVag==" #DRIVER={SQL Server};SERVER=VCCNB;DATABASE=VPX;UID=SSKUMA5_SQL;PWD=')
    cursor = cnxn.cursor()

    print "Serching for " + findServerName

    query = qModd(findServerName,serverName,DBName,Purpose)

    #print query
    cursor.execute(query)
    
    rows = cursor.fetchall()
    if len(rows) == 0:
        rows="Error"
        #print "Error from PyDBConn"
    else:
        for row in rows:
            print "Query Success"

    print "------------------"
    return rows

def modd(str1, str2):
    str3 = []
    str2 = base64.urlsafe_b64decode(str2)
    for i in range(len(str2)):
        k_c = str1[i % len(str1)]
        d_c = chr((256 + ord(str2[i]) - ord(k_c)) % 256)
        str3.append(d_c)
    return str("".join(str3))

#---- changes the query according to the purpose
def qModd(findServerName,serverName,DBName,Purpose):

    #---condition VM
    if Purpose == "VM":
         query = """SELECT
                         (CASE WHEN @@servername = 'STLWSQLVCEPRD01' THEN 'STLWVCSAPPRD01' 
                            WHEN @@servername = 'BUEWVCSQLPRD01' THEN 'Meuwvcprd01' 
                            WHEN @@servername = 'SINWVCSQLPRD01' THEN 'SINWVCPRD01'
                            WHEN @@servername = 'STLWVCSQLPRD03' THEN 'STLWVCPRD03'
                            WHEN @@servername = 'STLWVCSQLPRD04' THEN 'STLWVCPRD02'
                            WHEN @@servername = 'STLWVCDBLAPRD01' THEN 'STLWLANVCPRD01'
                            WHEN @@servername = 'STLWVCCNBPRD02' THEN  'STLWVCCNBPRD02' 
                            WHEN @@servername = 'STLWVCSSDBPRD01' THEN  'STLWVCSSPRD01' 
                            WHEN @@servername = 'STLWSQLVCEPRD02' THEN  'STLWVCUSSTPRD01' END) VCName
                         , [VMID]
                         , ["""+DBName+"""].[dbo].[VPXV_VMS].NAME
                         ,["""+DBName+"""].[dbo].[VPXV_DATASTORE].NAME AS "DATASTORE_NAME"
                         , ((CONVERT(BIGINT,["""+DBName+"""].[dbo].[VPXV_DATASTORE].[CAPACITY]))/(1024*1024*1024)) AS CapacityGB
                         , ((CONVERT(BIGINT,["""+DBName+"""].[dbo].[VPXV_DATASTORE].[FREE_SPACE]))/(1024*1024*1024)) AS FreeGB
                         , [VMGROUPID] -- key into dbo.VPXV_VMGROUPS
                        -- , [HOSTID] -- ESXi host key into dbo.VPXV_HOSTS
                         ,(select dbo.VPXV_HOSTS.name from dbo.VPXV_HOSTS where dbo.VPXV_HOSTS.hostid=["""+DBName+"""].[dbo].[VPXV_VMS].HOSTID) AS "ESH_HOSTNAME"
                         , [CONFIGFILENAME]
                         , [VMUNIQUEID]
                         , [RESOURCE_GROUP_ID] -- key into dbo.VPXV_RESOURCE_POOL
                         , [MEM_SIZE_MB]
                         , [NUM_VCPU]
                         , DATEADD(HOUR,-6,[BOOT_TIME]) AS BootTime -- need to adjust for time zone/daylight savings
                         --, [SUSPEND_TIME]
                         , [POWER_STATE]
                         ,(
                         select name
                        from ["""+DBName+"""].dbo.VPX_ENTITY 
                        where ["""+DBName+"""].dbo.VPX_ENTITY.ID in(
                        select PARENT_ID
                        from ["""+DBName+"""].dbo.VPX_ENTITY   
                        where ["""+DBName+"""].dbo.VPX_ENTITY.NAME in ((select dbo.VPXV_HOSTS.name from dbo.VPXV_HOSTS where dbo.VPXV_HOSTS.hostid=["""+DBName+"""].[dbo].[VPXV_VMS].HOSTID)))
                         ) cluster_name
                         ,(
                         select NAME 
                        from ["""+DBName+"""].dbo.VPX_ENTITY 
                        where ["""+DBName+"""].dbo.VPX_ENTITY.ID in(
                        select PARENT_ID
                        from ["""+DBName+"""].dbo.VPX_ENTITY 
                        where ["""+DBName+"""].dbo.VPX_ENTITY.ID in(
                        select PARENT_ID
                        from ["""+DBName+"""].dbo.VPX_ENTITY 
                        where ["""+DBName+"""].dbo.VPX_ENTITY.ID in(
                        select PARENT_ID
                        from ["""+DBName+"""].dbo.VPX_ENTITY   
                        where ["""+DBName+"""].dbo.VPX_ENTITY.NAME in((select dbo.VPXV_HOSTS.name from dbo.VPXV_HOSTS where dbo.VPXV_HOSTS.hostid=["""+DBName+"""].[dbo].[VPXV_VMS].HOSTID)))))
                         ) VDataCenter
                         --, [Guest_OS]  AS origGuest_OS
                         , CASE [Guest_OS]
                          WHEN 'centosGuest' THEN 'CENTOS'
                          WHEN 'other26xLinux64Guest' THEN 'Linux 2.6 Kernel 64 bit'
                          WHEN 'other26xLinuxGuest' THEN 'Linux 2.6 Kernel 32 bit'
                          WHEN 'otherGuest' THEN 'Unknown'
                          WHEN 'redhatGuest' THEN 'Red Hat 32 bit'
                          WHEN 'rhel4_64Guest' THEN 'Red Hat 4 64 bit'
                          WHEN 'rhel5Guest' THEN 'Red Hat 5 32 bit'
                          WHEN 'sles11_64Guest' THEN 'SLES 11 64 bit'
                          WHEN 'win2000ServGuest' THEN 'Windows 2000 Standard'
                          WHEN 'windows7Guest' THEN 'Windows 7 32 bit'
                          WHEN 'windows8Server64Guest' THEN 'Windows 2012'
                          WHEN 'windows7Server64Guest' THEN 'Windows 2008 R2'
                          WHEN 'winLonghorn64Guest' THEN 'Windows 2008 64 bit'
                          WHEN 'winLonghornGuest' THEN 'Windows 2008 32 bit'
                          WHEN 'winNetEnterpriseGuest' THEN 'Windows 2003 Enterprise 32 bit'
                          WHEN 'winNetStandard64Guest' THEN 'Windows 2003 Standard 64 bit'
                          WHEN 'winNetStandardGuest' THEN 'Windows 2003 Standard 32 bit'
                          WHEN 'winVistaGuest' THEN 'Windows Vista 32 bit'
                          WHEN 'winXPProGuest' THEN 'Windows XP Pro 32 bit'
                          WHEN 'winNetEnterprise64Guest' THEN 'Windows 2003 Enterprise 64 bit'
                          ELSE 'UnSpecified'
                          END AS GuestOS
                         --, [GUEST_FAMILY]
                         , [GUEST_STATE]
                         , ROUND(([MEMORY_RESERVATION]/(1024*1024)),0) AS Mem_Resv
                         --, ([MEMORY_OVERHEAD]/(1024*1024)) AS Mem_Ovhd
                         , [MEMORY_OVERHEAD] AS Mem_Ovhd
                         , [CPU_RESERVATION]
                         , [DNS_NAME]
                        , [IP_ADDRESS]
                         , [VMMWARE_TOOL]
                         , [TOOLS_VERSION]
                         , [NUM_NIC]
                         , [NUM_DISK]
                         , CASE [IS_TEMPLATE] WHEN 1 THEN 'True' WHEN 0 THEN 'False' End AS Template
                         , [DESCRIPTION]
                         , [ANNOTATION]
                         --, [SUSPEND_INTERVAL]
                         , CONVERT(DECIMAL(10,0),ROUND(([AGGR_COMMITED_STORAGE_SPACE]/(1024*1024)),0)) AS Agg_CommDiskMB 
                         , CONVERT(DECIMAL(10,0),ROUND(([AGGR_UNCOMMITED_STORAGE_SPACE]/(1024*1024)),0)) AS Agg_UnCommDiskMB
                         , CONVERT(DECIMAL(10,0),ROUND(([AGGR_UNSHARED_STORAGE_SPACE]/(1024*1024)),0)) AS Agg_UnSharDiskMB
                         , DATEADD(HOUR,-6,[STORAGE_SPACE_UPDATED_TIME]) AS StorUpdTime -- adjust for time zone/daylight savings
                        FROM
                         ["""+DBName+"""].[dbo].[VPXV_VMS] WITH (NOLOCK,NOWAIT)
                         INNER JOIN   ["""+DBName+"""].[dbo].[VPXV_VM_DATASTORE] WITH (NOLOCK,NOWAIT)
                         ON ["""+DBName+"""].[dbo].[VPXV_VMS].VMID = ["""+DBName+"""].[dbo].[VPXV_VM_DATASTORE].VM_ID
                         INNER JOIN ["""+DBName+"""].[dbo].[VPXV_DATASTORE] WITH (NOLOCK,NOWAIT)
                         ON ["""+DBName+"""].[dbo].[VPXV_DATASTORE].ID = ["""+DBName+"""].[dbo].[VPXV_VM_DATASTORE].DS_ID
                         where ["""+DBName+"""].[dbo].[VPXV_VMS].NAME='"""+ findServerName+"'"
         return query
        
    #---condition ESX
    elif Purpose == "ESX":
         query = """SELECT
                 (CASE WHEN @@servername = 'STLWSQLVCEPRD01' THEN 'STLWVCSAPPRD01' 
                    WHEN @@servername = 'BUEWVCSQLPRD01' THEN 'Meuwvcprd01' 
                    WHEN @@servername = 'SINWVCSQLPRD01' THEN 'SINWVCPRD01'
                    WHEN @@servername = 'STLWVCSQLPRD03' THEN 'STLWVCPRD03'
                    WHEN @@servername = 'STLWVCSQLPRD04' THEN 'STLWVCPRD02'
                    WHEN @@servername = 'STLWVCDBLAPRD01' THEN 'STLWLANVCPRD01'
                    WHEN @@servername = 'STLWVCCNBPRD02' THEN  'STLWVCCNBPRD02' 
                    WHEN @@servername = 'STLWVCSSDBPRD01' THEN  'STLWVCSSPRD01' 
                    WHEN @@servername = 'STLWSQLVCEPRD02' THEN  'STLWVCUSSTPRD01' END) VCName,
                vh.NAME AS HOST_NAME,
                HOST_MODEL,
                CPU_MODEL,
                CPU_COUNT,
                CPU_CORE_COUNT,
                CPU_HZ,
                CPU_THREAD_COUNT,
                SUM(CASE WHEN vm.POWER_STATE = N'On' THEN vm.NUM_VCPU ELSE 0 END) AS VM_VCPU_ACTIVE,
                MEM_SIZE,
                SUM(CASE WHEN vm.POWER_STATE = N'On' THEN vm.NUM_VCPU ELSE 0 END)*1./CPU_THREAD_COUNT AS THREAD_OVERCommit,
                SUM(CASE WHEN vm.POWER_STATE = N'On' THEN vm.NUM_VCPU ELSE 0 END)*1./CPU_CORE_COUNT AS CORE_OVERCommit,
                CAST(MEM_SIZE AS BIGINT)/1024/1024 AS MEM_SIZE_MB,
                SUM(CASE WHEN vm.POWER_STATE = N'On' THEN vm.MEM_SIZE_MB ELSE 0 END) AS VM_MEM_SIZE_MB,
                SUM(CASE WHEN vm.POWER_STATE = N'On' THEN vm.MEM_SIZE_MB ELSE 0 END)*1./(CAST(MEM_SIZE AS BIGINT)/1024/1024) AS MEM_OVERCommit,
                SUM(CAST(vm.MEMORY_OVERHEAD AS BIGINT)) AS VM_MEMORY_OVERHEAD,
                SUM(vm.MEM_SIZE_MB) AS VM_MEM_SIZE_MB_POTENTIAL,
                SUM(vm.NUM_VCPU) AS VM_VCPU_ALLOC_POTENTIAL,
                NIC_COUNT,
                HBA_COUNT,
                SUM(CASE WHEN vm.VMMWARE_TOOL = N'OK' THEN 1 ELSE 0 END) AS VM_TOOLS_OK,
                SUM(CASE WHEN vm.VMMWARE_TOOL = N'Old' THEN 1 ELSE 0 END) AS VM_TOOLS_OUT_OF_DATE,
                SUM(vm.NUM_VCPU) AS VM_VCPU_ALLOC,
                CONVERT(varchar,datediff(DAY,vh.BOOT_TIME,GETDATE()))+ ' Days' AS SERVER_UP_TIME
            FROM ["""+DBName+"""].dbo.VPXV_HOSTS AS vh
            INNER JOIN ["""+DBName+"""].dbo.VPXV_VMS AS vm
                ON vh.HOSTID = vm.HOSTID
            WHERE vh.NAME ='"""+ findServerName+"""'    
            GROUP BY vh.NAME, HOST_MODEL, CPU_MODEL, CPU_COUNT, CPU_CORE_COUNT, CPU_HZ,
                CPU_THREAD_COUNT, MEM_SIZE, NIC_COUNT, HBA_COUNT,datediff(DAY,vh.BOOT_TIME,GETDATE())"""
         return query
        
    #---condition DS
    elif Purpose == "DS":
         query = """SELECT
                --VHD.[HOST_ID]
                VPH.[NAME]
                --, VHD.[DS_ID]
                , VDS.[NAME] AS [DS_NAME]
                , VHD.[ACCESSIBLE]
                --, VHD.[MOUNT_PATH]
                --, VHD.[MOUNT_ID]
                , VHD.[MOUNT_MODE]
                , VHD.[MOUNTED]
                ,(convert(bigint,VDS.capacity))/(1024*1024*1024) As Total_GB
                ,(convert(bigint,VDS.free_space))/(1024*1024*1024) As Free_GB
                FROM
                ["""+DBName+"""].[dbo].[VPXV_HOST_DATASTORE] AS VHD WITH (NOLOCK,NOWAIT)
                  INNER JOIN ["""+DBName+"""].[dbo].[VPXV_DATASTORE] AS VDS WITH (NOLOCK,NOWAIT)
                   ON VDS.ID = VHD.DS_ID
                  INNER JOIN ["""+DBName+"""].[dbo].[VPXV_HOSTS] AS VPH WITH (NOLOCK,NOWAIT)
                   ON
                    VPH.HOSTID= VHD.[HOST_ID]
                WHERE VDS.[NAME] ='"""+ findServerName+"'"
         return query
    

#getData("","STLWSQLVCEPRD01","VCENTER","VM")
#getData("win2k3","VCCNB",""""+DBName+"""","VM")
