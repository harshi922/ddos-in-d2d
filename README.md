# ddos-in-d2d

Link to our Simulated Dataset:
https://drive.google.com/file/d/1-2_nuhtI-C3NM37nSXart8DFVT5rGtha/view?usp=sharing

Data Directory:<br />
Contains our custom dataset with the attacks that we have simulated. We use Wireshark to perform packet capture and pass the resulting .pcap file through CiCFlowMeter to mimic the attacks’ format present in the CiCDoS2019 dataset. 

The complete dataset (Custom_dataset) was labelled as follows:
|Class|	Label|
|-----|------|
|Benign	|0|
|TFTP|1|
|UDP+SSDP|	2|
|LDAP	|3|
|Syn	|4|
|MSSQL|	5|
|Hulk	|6|
|Rudy	|7|
|GoldenEye|	8|
|HTTP|9|
|SQLi|10|
|MITM|11|
|Dictionary|12|

Models Directory:<br />
Contains the model along with the weights that were used for each layer in .h5 files.

Training Directory:<br />
Contains the notebook which shows our training process. We create separate labels for each layer based on how the attack is categorized. The layers are explained along with their labels below:<br />
<br />
Layer 1:<br />
Layer 1 was a binary classifier which was trained to classify attack and benign values.
| Class	 | Label | 
|--------|-------|
| Benign |	0    |
| Attack |	1    |

Layer 2:<br />
Layer 2 was a multi-class classifier which was trained to classify DDoS and other non-DDoS attacks.
| Class |	Label |
|-------|-------|
| DDoS |	0     |
| SQLi |	1 |
| MITM	| 2 |
| Dictionary|	3 |

Layer 3:<br />
Layer 3 was a multi-class DDoS attack classifier.
|Class|	Label|
|-----|------|
|TFTP	|0|
|UDP+SSDP|	1|
|LDAP	|2|
|NetBIOS + Portmap|	3|
|Syn	|4|
|MSSQL|	5|
|Hulk	|6|
|Rudy	|7|
|GoldenEye|	8|

double_filter.py: <br />
Contains the double feature selection mechanism that we have used. We use a correlation based feature selector followed by k best features ranked by the Mutual Information. In our model we have used the 20 best features as it has given us optimum performance. 

Inference.py: <br />
Contains code that allows you to perform prediction with the option to use each layer seperately or with all layers as a whole.


