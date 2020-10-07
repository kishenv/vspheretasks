'''Module to fetch details of ESXi host/ vCenter'''
import atexit
from pyVim.connect import SmartConnectNoSSL, Disconnect


class ConnectObject:
    """
    Class ConnectObject
    Creates a SmartConnectNoSSL object to access the ESXi/vCenter inventory objects
    Parameters:
        hostip(str): The IP Address of the ESXi host/vCenter whose inventory details
                     are to be fetched.
        uname(str) : The username to login.
        passwd(str): The password to access the ESXi Host/vCenter
    Returns:
        Object to access the elements of the Inventory
    """

    def __init__(self, hostip, uname, passwd):
        self.hostip = hostip
        self.uname = uname
        self.passwd = passwd
        conn_obj = SmartConnectNoSSL(host=self.hostip, user=self.uname, pwd=self.passwd)
        self.content_object = conn_obj.RetrieveContent().rootFolder.childEntity[0]
        atexit.register(Disconnect, conn_obj)

    # def inventory_content(self, hostip, uname, passwd, port=443):
    def inventory_content(self):
        """
        inventory_contents(...)

        Retrieves and displays the details related to the ESXi Host / vCenter.
        (Resource Pools, VMs Hosted, Data-stores, Clusters configured (localhost for ESXi host))

        Parameters:
            self
        Returns:
            None

        """
        i = 0
        print("Displaying Details for ESXi Host/vCenter:", self.hostip)
        print("__" * 20)
        print("Resource Pools Configured on the host: ")
        for pools in self.content_object.hostFolder.childEntity[0].resourcePool.resourcePool:
            print(pools.name)
        print("__" * 20)
        print("VM's hosted:")
        for virtual_machines in self.content_object.vmFolder.childEntity:
            print(virtual_machines.name)
        print("__" * 20)
        print("Data-stores connected to host :")
        datastores = self.content_object.datastoreFolder.childEntity
        for datastore in datastores:
            print(datastore.name)
        print("__" * 20)
        print("Cluster/hosts")
        clusters = self.content_object.hostFolder.childEntity
        for cluster in clusters:
            print(cluster.name)
            hosts = self.content_object.hostFolder.childEntity[i].host
            for host in hosts:
                print("-->", host.name)
            i = i + 1

    def vms_hosted(self):
        """
        vms_hosted(...)

        Retrieves and displays the list of VM's provisioned on the ESXi host/vCenter

        Parameters:
            self
        Returns:
            None
        """

        print("VM's hosted:")
        for virtual_machine in self.content_object.vmFolder.childEntity:
            print(virtual_machine.name)
        print("__" * 20)

    def res_pools(self):
        """
        res_pools(...)

        Retrieves and displays the list of Resource Pools on the ESXi host/vCenter

        Parameters:
            self

        """
        print("Resource Pools Configured on the host: ")
        for pools in self.content_object.hostFolder.childEntity[0].resourcePool.resourcePool:
            print(pools.name)
        print("__" * 20)

    def dstores_connected(self):
        """

        vms_hosted(...)

        Retrieves and displays the list of datastores connected on the ESXi host/vCenter

        Parameters:
            self

        """
        print("Datastores connected to host :")
        datastores = self.content_object.datastoreFolder.childEntity
        for datastore in datastores:
            print(datastore.name)
        print("__" * 20)

    def clustered_hosts(self):
        """

        vms_hosted(...)

        Retrieves and displays the list clusters along with the ESXi Host IP's on the vCenter
        Displays localdomain.localhost in case of ESXi Host

        Parameters:
            self

        Returns:
            None

        """
        print("Cluster/hosts")
        i = 0
        clusters = self.content_object.hostFolder.childEntity
        for cluster in clusters:
            print(cluster.name)
            hosts = self.content_object.hostFolder.childEntity[i].host
            for host in hosts:
                print("-->", host.name)
            i = i + 1
