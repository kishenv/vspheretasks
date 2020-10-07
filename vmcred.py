"""Module to create and edit VM's on ESXi host
   Provision resources carefully
   Default VM architecture = ubuntu64"""

import atexit
from pyVmomi import vim
from pyVim import connect
from vmwc import VMWareClient


def get_obj(content, vim_type, name):
    """
    Create a container view to manage the Infrastructure
    Parameters:
        content: The container object.
        vim_type(List): The kind of object to be searched for
        name(str): The name of the object to be retrieved
    """
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vim_type, True)
    for container in container.view:
        if container.name == name:
            obj = container
            break
    return obj


class Management:

    def __init__(self, ip, uname, pwd):
        self.ip = ip
        self.uname = uname
        self.pwd = pwd
        instance = connect.SmartConnectNoSSL(host=ip, user=uname, pwd=pwd)
        self.content = instance.RetrieveContent()
        atexit.register(connect.Disconnect, instance)
        print("Object Created")

    def edit_vm(self):
        """
            Modify the vCPU and Memory Parameters for a Particular VM
            Returns:
                None
        """
        cpu = int(input("Enter the number of CPUs to Reconfigure to (1-8):  0-to leave unchanged "))
        memory = int(input("Enter the memory configuration in GB (1-3): 0- to leave unchanged"))
        memory = memory * 1024
        if memory == 0:
            memory = None
        if cpu == 0:
            cpu = None
        print("vCPUs = " + str(cpu))
        print("Memory in MB = " + str(memory))
        v_name = input("Enter the name of VM to be configured: ")
        vm = get_obj(self.content, [vim.VirtualMachine], v_name)
        if vm:
            print("Instance Found")
            if cpu and memory:
                cspec = vim.vm.ConfigSpec()
                cspec.numCPUs = cpu
                cspec.memoryMB = memory
                vm.Reconfigure(cspec)
                print("CPU and Memory Reconfigured to", cpu, "vCPU and ", memory, "GB")

            elif cpu:
                cspec = vim.vm.ConfigSpec()
                cspec.numCPUs = cpu
                vm.Reconfigure(cspec)
                print("vCPU's Configured to ", cpu)

            elif memory:
                cspec = vim.vm.ConfigSpec()
                cspec.memoryMB = memory
                vm.Reconfigure(cspec)
                print("Memory configured to ", memory)

            elif cpu is None and memory is None:
                print("Invalid Inputs to configure VM")

    def create_vm(self):
        """
                Module to create a VM with basic settings and provisions only vCPU and Memory
                Default arch: ubuntu64
                Network : e1000
                Scsi: LSI logic SAS
                Disk Type : Thin provisioned
                ISO to be mounted using vSphere Client
        """
        with VMWareClient(self.ip, self.uname, self.pwd) as client:
            name = input("Enter VM Name")
            vm = get_obj(self.content, [vim.VirtualMachine], name)
            if vm:
                print("A VM already exists with the same name, choose a different name")
            else:

                cpu = int(input("Enter the number of vCPUs to add: "))
                ram = int(input("Enter memory in GB: "))
                ram = ram * 1024
                disk_size = int(input("Enter the size of the Hard disk"))
                print("Provisioning resources on ESXi, Please wait")
                vm = client.new_virtual_machine(name, cpus=cpu, ram_mb=ram, disk_size_gb=disk_size)
                vm.configure_bios(boot_delay=5000, boot_order=['network', 'disk'])
                print("VM {0}  has been provisoned with:".format(name))
                print("{0} CPUs and {1} MB Memory ".format(cpu, ram))
                print("{0}GB of HDD(Thin provisoned)".format(disk_size))
