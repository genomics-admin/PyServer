#!/usr/bin/python
import pyodbc
import base64



def getData(findServerName,serverName,DBName,Purpose):
    
    
    #--connction
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+serverName+';DATABASE='+DBName+';'+modd("yLWlpr6","zpWbqcO-d8KXkrzHtnPJrcrf5-Go3X2JjbCVag=="))   #DRIVER={SQL Server};SERVER=VCCNB;DATABASE=VPX;UID=;PWD=')
    cursor = cnxn.cursor()

    print "Serching for " + findServerName

    query = qModd(findServerName,Purpose)

    #print query
    cursor.execute(query)
    
    rows = cursor.fetchall()
    if len(rows) == 0:
        rows="Error"
        #print "Error from PyDBConn"
    else:
        for row in rows:
            print row.VMID, row.NAME, row.DATASTORE_NAME,row.VMGROUPID, row.Mem_Resv

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
def qModd(findServerName,Purpose):

    #---condition VM
    if Purpose == "VM":
         query = """SELECT
                         @@SERVERNAME VCName
                         , [VMID]
                         , [VPX].[dbo].[VPXV_VMS].NAME
                         ,[VPX].[dbo].[VPXV_DATASTORE].NAME AS "DATASTORE_NAME"
                         , ((CONVERT(BIGINT,[VPX].[dbo].[VPXV_DATASTORE].[CAPACITY]))/(1024*1024*1024)) AS CapacityGB
                         , ((CONVERT(BIGINT,[VPX].[dbo].[VPXV_DATASTORE].[FREE_SPACE]))/(1024*1024*1024)) AS FreeGB
                         , [VMGROUPID] -- key into dbo.VPXV_VMGROUPS
                        -- , [HOSTID] -- ESXi host key into dbo.VPXV_HOSTS
                         ,(select dbo.VPXV_HOSTS.name from dbo.VPXV_HOSTS where dbo.VPXV_HOSTS.hostid=[VPX].[dbo].[VPXV_VMS].HOSTID) AS "ESH_HOSTNAME"
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
                        from [VPX].dbo.VPX_ENTITY 
                        where [VPX].dbo.VPX_ENTITY.ID in(
                        select PARENT_ID
                        from [VPX].dbo.VPX_ENTITY   
                        where [VPX].dbo.VPX_ENTITY.NAME in ((select dbo.VPXV_HOSTS.name from dbo.VPXV_HOSTS where dbo.VPXV_HOSTS.hostid=[VPX].[dbo].[VPXV_VMS].HOSTID)))
                         ) cluster_name
                         ,(
                         select NAME 
                        from [VPX].dbo.VPX_ENTITY 
                        where [VPX].dbo.VPX_ENTITY.ID in(
                        select PARENT_ID
                        from [VPX].dbo.VPX_ENTITY 
                        where [VPX].dbo.VPX_ENTITY.ID in(
                        select PARENT_ID
                        from [VPX].dbo.VPX_ENTITY 
                        where [VPX].dbo.VPX_ENTITY.ID in(
                        select PARENT_ID
                        from [VPX].dbo.VPX_ENTITY   
                        where [VPX].dbo.VPX_ENTITY.NAME in((select dbo.VPXV_HOSTS.name from dbo.VPXV_HOSTS where dbo.VPXV_HOSTS.hostid=[VPX].[dbo].[VPXV_VMS].HOSTID)))))
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
                         , ([MEMORY_OVERHEAD]/(1024*1024)) AS Mem_Ovhd
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
                         [VPX].[dbo].[VPXV_VMS] WITH (NOLOCK,NOWAIT)
                         INNER JOIN   [VPX].[dbo].[VPXV_VM_DATASTORE] WITH (NOLOCK,NOWAIT)
                         ON [VPX].[dbo].[VPXV_VMS].VMID = [VPX].[dbo].[VPXV_VM_DATASTORE].VM_ID
                         INNER JOIN [VPX].[dbo].[VPXV_DATASTORE] WITH (NOLOCK,NOWAIT)
                         ON [VPX].[dbo].[VPXV_DATASTORE].ID = [VPX].[dbo].[VPXV_VM_DATASTORE].DS_ID
                         where [VPX].[dbo].[VPXV_VMS].NAME='"""+ findServerName+"'"
         return query
        
    #---condition ESX
    elif Purpose == "ESX":
         query = """SELECT
                         @@SERVERNAME VCName
                         , [VMID]
                         , [VPX].[dbo].[VPXV_VMS].NAME
                         ,[VPX].[dbo].[VPXV_DATASTORE].NAME AS "DATASTORE_NAME"
                         , ((CONVERT(BIGINT,[VPX].[dbo].[VPXV_DATASTORE].[CAPACITY]))/(1024*1024*1024)) AS CapacityGB
                         , ((CONVERT(BIGINT,[VPX].[dbo].[VPXV_DATASTORE].[FREE_SPACE]))/(1024*1024*1024)) AS FreeGB
                         , [VMGROUPID] -- key into dbo.VPXV_VMGROUPS
                        -- , [HOSTID] -- ESXi host key into dbo.VPXV_HOSTS
                         ,(select dbo.VPXV_HOSTS.name from dbo.VPXV_HOSTS where dbo.VPXV_HOSTS.hostid=[VPX].[dbo].[VPXV_VMS].HOSTID) AS "ESH_HOSTNAME"
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
                        from [VPX].dbo.VPX_ENTITY 
                        where [VPX].dbo.VPX_ENTITY.ID in(
                        select PARENT_ID
                        from [VPX].dbo.VPX_ENTITY   
                        where [VPX].dbo.VPX_ENTITY.NAME in ((select dbo.VPXV_HOSTS.name from dbo.VPXV_HOSTS where dbo.VPXV_HOSTS.hostid=[VPX].[dbo].[VPXV_VMS].HOSTID)))
                         ) cluster_name
                         ,(
                         select NAME 
                        from [VPX].dbo.VPX_ENTITY 
                        where [VPX].dbo.VPX_ENTITY.ID in(
                        select PARENT_ID
                        from [VPX].dbo.VPX_ENTITY 
                        where [VPX].dbo.VPX_ENTITY.ID in(
                        select PARENT_ID
                        from [VPX].dbo.VPX_ENTITY 
                        where [VPX].dbo.VPX_ENTITY.ID in(
                        select PARENT_ID
                        from [VPX].dbo.VPX_ENTITY   
                        where [VPX].dbo.VPX_ENTITY.NAME in((select dbo.VPXV_HOSTS.name from dbo.VPXV_HOSTS where dbo.VPXV_HOSTS.hostid=[VPX].[dbo].[VPXV_VMS].HOSTID)))))
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
                         , ([MEMORY_OVERHEAD]/(1024*1024)) AS Mem_Ovhd
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
                         [VPX].[dbo].[VPXV_VMS] WITH (NOLOCK,NOWAIT)
                         INNER JOIN   [VPX].[dbo].[VPXV_VM_DATASTORE] WITH (NOLOCK,NOWAIT)
                         ON [VPX].[dbo].[VPXV_VMS].VMID = [VPX].[dbo].[VPXV_VM_DATASTORE].VM_ID
                         INNER JOIN [VPX].[dbo].[VPXV_DATASTORE] WITH (NOLOCK,NOWAIT)
                         ON [VPX].[dbo].[VPXV_DATASTORE].ID = [VPX].[dbo].[VPXV_VM_DATASTORE].DS_ID
                         where [VPX].[dbo].[VPXV_VMS].NAME='"""+ findServerName+"'"
         return query
        
    #---condition VM
    elif Purpose == "DS":
         query = """SELECT
                         @@SERVERNAME VCName
                         , [VMID]
                         , [VPX].[dbo].[VPXV_VMS].NAME
                         ,[VPX].[dbo].[VPXV_DATASTORE].NAME AS "DATASTORE_NAME"
                         , ((CONVERT(BIGINT,[VPX].[dbo].[VPXV_DATASTORE].[CAPACITY]))/(1024*1024*1024)) AS CapacityGB
                         , ((CONVERT(BIGINT,[VPX].[dbo].[VPXV_DATASTORE].[FREE_SPACE]))/(1024*1024*1024)) AS FreeGB
                         , [VMGROUPID] -- key into dbo.VPXV_VMGROUPS
                        -- , [HOSTID] -- ESXi host key into dbo.VPXV_HOSTS
                         ,(select dbo.VPXV_HOSTS.name from dbo.VPXV_HOSTS where dbo.VPXV_HOSTS.hostid=[VPX].[dbo].[VPXV_VMS].HOSTID) AS "ESH_HOSTNAME"
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
                        from [VPX].dbo.VPX_ENTITY 
                        where [VPX].dbo.VPX_ENTITY.ID in(
                        select PARENT_ID
                        from [VPX].dbo.VPX_ENTITY   
                        where [VPX].dbo.VPX_ENTITY.NAME in ((select dbo.VPXV_HOSTS.name from dbo.VPXV_HOSTS where dbo.VPXV_HOSTS.hostid=[VPX].[dbo].[VPXV_VMS].HOSTID)))
                         ) cluster_name
                         ,(
                         select NAME 
                        from [VPX].dbo.VPX_ENTITY 
                        where [VPX].dbo.VPX_ENTITY.ID in(
                        select PARENT_ID
                        from [VPX].dbo.VPX_ENTITY 
                        where [VPX].dbo.VPX_ENTITY.ID in(
                        select PARENT_ID
                        from [VPX].dbo.VPX_ENTITY 
                        where [VPX].dbo.VPX_ENTITY.ID in(
                        select PARENT_ID
                        from [VPX].dbo.VPX_ENTITY   
                        where [VPX].dbo.VPX_ENTITY.NAME in((select dbo.VPXV_HOSTS.name from dbo.VPXV_HOSTS where dbo.VPXV_HOSTS.hostid=[VPX].[dbo].[VPXV_VMS].HOSTID)))))
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
                         , ([MEMORY_OVERHEAD]/(1024*1024)) AS Mem_Ovhd
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
                         [VPX].[dbo].[VPXV_VMS] WITH (NOLOCK,NOWAIT)
                         INNER JOIN   [VPX].[dbo].[VPXV_VM_DATASTORE] WITH (NOLOCK,NOWAIT)
                         ON [VPX].[dbo].[VPXV_VMS].VMID = [VPX].[dbo].[VPXV_VM_DATASTORE].VM_ID
                         INNER JOIN [VPX].[dbo].[VPXV_DATASTORE] WITH (NOLOCK,NOWAIT)
                         ON [VPX].[dbo].[VPXV_DATASTORE].ID = [VPX].[dbo].[VPXV_VM_DATASTORE].DS_ID
                         where [VPX].[dbo].[VPXV_VMS].NAME='"""+ findServerName+"'"
         return query
    

#getData("win2k3")
