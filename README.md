# ese407Project
1) Install the 32 bit Mininet 2.2.2 Ubuntu image from https://github.com/mininet/mininet/wiki/Mininet-VM-Images
2) Import the VM image into a VM. 
3) Log into the account "mininet" with the password "mininet". 
4) Insert a flash drive with a copy of our project or pull our project off github.
5) Navigate into the ese407Project folder.
6) Run "sudo python RUNME.py"
7) Launch wireshark
To view control traffic using the OpenFlow Wireshark dissector, first open wireshark in the background:

$ sudo wireshark &
In the Wireshark filter box, enter this filter, then click Apply:

of
In Wireshark, click Capture, then Interfaces, then select Start on the loopback interface (lo).

For now, there should be no OpenFlow packets displayed in the main window.

Note: Wireshark is installed by default in the Mininet VM image. If the system you are using does not have Wireshark and the OpenFlow plugin installed, you may be able to install both of them using Mininet’s install.sh script as follows:

$ cd ~
$ git clone https://github.com/mininet/mininet  # if it's not already there
$ mininet/util/install.sh -w
If Wireshark is installed but you cannot run it (e.g. you get an error like $DISPLAY not set, please consult the FAQ: https://github.com/mininet/mininet/wiki/FAQ#wiki-x11-forwarding.)

Setting X11 up correctly will enable you to run other GUI programs and the xterm terminal emulator, used later in this walkthrough.

