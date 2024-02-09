from kerberos_config import config
# for rocky linux, step 1 is dnf -y install realmd sssd oddjob oddjob-mkhomedir adcli samba-common-tools krb5-workstation
client_commands = [
    "******* On the client ********",
    "1. dnf install sssd realmd oddjob oddjob-mkhomedir adcli samba-common samba-common-tools krb5-workstation openldap-clients policycoreutils-python nfs-utils -y", #If RHEL9 python3-policycoreutils
    "2. Confirm /etc/resolv.conf is pointing to the right domain and DNS server",
    "3. realm join --user=" + config["domain-admin"] + " " + config["realm"],
    "\n******** Go to Powershell on the DC and run the following: ********",
    "\t4. Set-ADComputer " + config["client-computer-name"] + "$ -KerberosEncryptionType aes128,aes256",
    "\t5. Add-DnsServerResourceRecordA -Name " + config["client-computer-name"] + " -ZoneName " + config[
        "realm"] + " -IPv4Address " + config["client-ip"] + " -CreatePtr",
    "\n******* Back on the client *******",
    "6. Edit /etc/sssd/sssd.conf so the following lines look like this:",
    "\tuse_fully_qualified_names = False",
    "\tfallback_homedir = /home/%u",
    "7.  systemctl restart sssd",
    "8.  systemctl enable sssd",
    "9.  systemctl start nfs-secure", #Not needed if RHEL7.1+
    "10. systemctl enable nfs-secure",
    ]

ontap_commands = [
    "nfs server modify -vserver " + config["svm"] + " -permitted-enc-types aes-*",
    "dns create -vserver " + config["svm"] + " -domains " + config["realm"] + " -name-servers " + config["dns-ip"],
    "kerberos realm create -vserver " + config["svm"] + " -realm " + config[
        "realm"] + " -kdc-vendor Microsoft -kdc-ip " + config[
        "dc-ip"] + " -kdc-port 88 -clock-skew 5 -adminserver-ip " + config[
        "dc-ip"] + " -adminserver-port 749 -passwordserver-ip " + config[
        "dc-ip"] + " -passwordserver-port 464 -adserver-name " + config["dc-name"] + " -adserver-ip " + config["dc-ip"],
    "kerberos interface enable -vserver " + config["svm"] + " -lif " + config["data-lif"] + " -spn nfs/" + config[
        "dns-name-of-lif"] + "@" + config["realm"] + " -admin-username " + config["domain-admin"],
    "FROM POWERSHELL ON DC:",
    "\tSet-ADComputer nfs-" + config["dns-name-of-lif"] + "$ -KerberosEncryptionType aes128,aes256",
    "\tAdd-DnsServerResourceRecordA -Name " + config["dns-name-of-lif"] + " -ZoneName " + config[
        "realm"] + " -IPv4Address " + config["data-lif-ip"] + " -CreatePtr",
    "vserver name-mapping create -vserver " + config["svm"] + " -direction krb-unix -position 1 -pattern (.+)\\$@" +
    config["realm"] + " -replacement root",
    "vserver name-mapping create -vserver " + config["svm"] + " -direction krb-unix -position 2 -pattern nfs/" + config["dns-name-of-lif"] + "@" + config["realm"] + " -replacement pcuser",
    "vserver name-mapping create -vserver " + config["svm"] + " -direction krb-unix -position 3 -pattern (.+)@" + config["realm"] + " -replacement \\1",
    "nfs server modify -vserver " + config["svm"] + " -v4.0 enabled -v4.1 enabled -v3 disabled -v4-id-domain " + config["realm"] + " -v4.1-pnfs disabled",]


for command in client_commands:
    print(command)

print("\n\n************ Following are ONTAP CLI commands ***************")

for command in ontap_commands:
    print(command)
