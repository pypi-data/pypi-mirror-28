# Elem
Welcome to the Enterprise Linux Exploit Mapper.  The purpose of the **elem** tool is to assist with assessments known exploits on an enterprise Linux host.  Initially the [STRIDE](https://msdn.microsoft.com/en-us/library/ee823878%28v=cs.20%29.aspx) threat scoring model will be used though this tool is designed to support additional models.

## Requirements
There are two components necessary to use all the features of **elem**.
1. The **elem** repository: https://github.com/fedoraredteam/elem
1. The curation information stored in the **elem-curation** repository: https://github.com/fedoraredteam/elem-curation

The current version of **elem** requires that the curation repository be cloned separately.  The rationale is that because exploit POC's are now included with the curation data, the act of downloading the exploits to a host must be due to a conscious and deliberate act by the user.  For more information as to what information is stored in the curation repo, please see the **elem-curation** README.md.

## Getting Started

### Obtain the Curation Data
We recommend cloning the data via git.
```terminal
git clone https://github.com/fedoraredteam/elem-curation.git
```
You'll need to note the location. ;-)

### Install the ELEM tool
There are a couple ways to accomplish this.  First is to clone via git.  The second is to insall bia Pypi.  We recommend that latter as **elem** has some dependencies that will automatically be installed via **pip**.  Furthermore, we recommend the use of Python Virtualenv.  This will ensure that **elem** is installed in an isolated Python environment.

#### Clone the Repository
```terminal
git clone https://github.com/fedoraredteam/elem
```
#### Pypi
```terminal
pip install elem
```
#### Virtualenv
```terminal
sudo easy_install virtualenv
virtualenv elem
cd elem
source bin/activate
pip install elem
```
**NOTE** This is a known issue in Python 2.6 where the version of **wheel** causes some conflicts.  This can be resolved with:
```terminal
pip install wheel==0.29.0
```
## General Usage
Executing **elem** with the ***--help*** argument will provide some basic guidance.
```terminal
(elem) [admin@localhost elem]$ elem --help
usage: elem [-h] [--notlsverify] {host,cve,score,exploit} ...

Cross Reference CVE's against a Exploit-DB entries for Enterprise Linux.

positional arguments:
  {host,cve,score,exploit}

optional arguments:
  -h, --help            show this help message and exit
  --notlsverify
```
### Assessing a Host
The first action you probably want to perform is an assessment.  This is acheived with the **host** subcommand.  The only required argument here is the location of the curation data.  For example:
```terminal
(elem) [admin@localhost elem]$ elem host assess --curation /home/admin/elem-curation
```
By default, this will result in a comma separated value list of exploits based on the CVE's applicable to the host.  For example:
```
exploit-database,40003,CVE-2016-0728,cpe:/o:redhat:enterprise_linux:7.0:ga:server,stride,000000
exploit-database,1602
```
The values are as follows:
1. Source of the exploit
2. Source specific identifier
3. Applicable CVE (only listed if exploit hsa been scored)
4. CPE against which the exploit was tested (only listed if exploit hsa been scored)
5. Score name (only listed if exploit hsa been scored)
6. Score value (only listed if exploit hsa been scored)

#### Filtering Assessment Results
It is possible to filter the results of **elem host assess** by certain values.  For example, perhaps we want to only list results where the efficacy of a privilage escallation exploit is very high.  The following would help us achieve this:
```terminal
(elem) [admin@localhost elem]$ elem host assess --curation /mnt/hgfs/elem-curation/ --kind stride --score 00000[8,9]
```
### Testing an Exploit
The next major step is to test an exploit on a host.  For this, we use the **exploit** subcommand.
#### Copy the Exploit to a Location on the Host
The **elem exploit copy** command will copy an exploit to the user's home directory by default:
```terminal
elem exploit copy --source exploit-database --id 37706 --curation /mnt/hgfs/elem-curation/
```
From here, you can examine the exploit file and manually stage it.  If the staging information is configured, the **--stage** will take the necessary actions to prepare the exploit for execution.
#### Score the Exploit
While not required, you may wish to score the exploit.
```terminal
(elem) [admin@localhost elem]$ elem exploit score --id 37706 --source exploit-database --kind stride --value 000009 --curation /mnt/hgfs/elem-curation/
```
### Patching a Host
In testing an exploit, it may be useful to test the exploit against a host that has been patched.  The elem tool assists with this, though this must be executed with escallated privileges.  We return to the **elem host** command/sub-command and use the **patch** sub-sub-command:
```terminal
(elem) [root@localhost elem]# elem host patch exploits --curation /mnt/hgfs/elem-curation/ --source exploit-database --ids 37706
```