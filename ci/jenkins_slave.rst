Jenkins slave
**************

Jenkins slave instance are used to have more parallel builds using different machines on the network. Small setup is needed to let the node to be online:

-  Install network machine
-  Generate ssh key with minimum enforce and copy in .ssh authorized_keys the public key part
-  Setup Jenkins user
-  Add in Jenkins master credential the private key and connect to a new node
-  Run from the interface of Jenkins the installation of the agent required to connect the node

.. _Jenkinsslave-GenerateSSHkey:

Generate SSH key
================

Jenkins will connect to the slave using SSH. The first step is thus to setup the Jenkins server to be able to connect to the slave via SSH. To do so, first connect to your Jenkins server via SSH and then generate an SSH key:

::

         # switch user to the user used by Jenkins (jenkins by default)
         $ sudo su jenkins
         # generate the SSH key
         $ ssh-keygen -t ed25519 -b 4096 -C "jenkins@example.com"
         Generating public/private rsa key pair.  
         Enter file in which to save the key (/var/lib/jenkins/.ssh/id_ed25519):  
         Enter passphrase (empty for no passphrase):  
         Enter same passphrase again:  
         Your identification has been saved in /var/lib/jenkins/.ssh/id_ed25519.  
         Your public key has been saved in /var/lib/jenkins/.ssh/id_ed25519.pub.  
         The key fingerprint is:  
         7f:87:09:b8:44:0d:1a:c0:f0:d2:6c:45:83:ea:b9:1a jenkins@example.com  
         The key's randomart image is:

**Deprecated way (NOT USE ANYMORE):**

::

         # switch user to the user used by Jenkins (jenkins by default)
         $ sudo su jenkins
         # generate the SSH key
         $ ssh-keygen -t rsa -C "jenkins@example.com"
         Generating public/private rsa key pair.  
         Enter file in which to save the key (/var/lib/jenkins/.ssh/id_rsa):  
         Enter passphrase (empty for no passphrase):  
         Enter same passphrase again:  
         Your identification has been saved in /var/lib/jenkins/.ssh/id_rsa.  
         Your public key has been saved in /var/lib/jenkins/.ssh/id_rsa.pub.  
         The key fingerprint is:  
         7f:87:09:b8:44:0d:1a:c0:f0:d2:6c:45:83:ea:b9:1a jenkins@example.com  
         The key's randomart image is:

Public key should be copied and install in the slave machine after Jenkins user creation

.. _Jenkinsslave-SetupJenkinsuser:

Setup Jenkins user
==================

Jenkins user needs to be selected in a way that it can unique and mapping to docker building image. Our docker image are created to have jenkins user mapped to 20000

::

         $ groupadd -g 20000 jenkins  
         $ useradd -d /home/jenkins -u 20000 -g 20000 -m -s /bin/bash jenkins

Then add the public key in the authorized_keys file and disable password login for the user jenkins:

::

         # switch user to jenkins
         $ sudo su jenkins
         # add the key to authorized_keys
         $ mkdir ~/.ssh
         $ echo "CONTENT_OF_PUBLIC_KEY" > ~/.ssh/authorized_keys
         $ chmod 600 ~/.ssh/authorized_keys
         # disable password login for the user jenkins
         $ sudo vim /etc/ssh/sshd_config

**Node administrator must remove** the access using password and allow only access using the key

.. _Jenkinsslave-GradlebuildonJenkinsnode:

Gradle build on Jenkins node
============================

Since Gradle 3.0, we enable Daemon by default and recommend using it for both developers' machines and Continuous Integration servers. However, if you suspect that Daemon makes your CI builds unstable, you can disable it to use a fresh runtime for each build since the runtime is completely isolated from any previous builds.

https://docs.gradle.org/current/userguide/gradle_daemon.html#when_should_i_not_use_the_gradle_daemon

::

         Add org.gradle.daemon=false to the «GRADLE_USER_HOME»/gradle.properties file

         Note, «GRADLE_USER_HOME» defaults to «USER_HOME»/.gradle, where «USER_HOME» is the home directory of the current user.
         This location can be configured via the -g and --gradle-user-home command line switches, as well as by the GRADLE_USER_HOME
         environment variable and org.gradle.user.home JVM system property.

         Create an .m2 directory for artifacts download

.. _Jenkinsslave-Jenkinsnodednstrouble:

Jenkins node dns trouble
========================

Setting up the node resolver according to the vpn endpoint. Add add daemon.json in /etc/docker directory

::

         {
           "dns": ["10.105.6.1"]
         }

| 

.. _Jenkinsslave-Jenkinsnodelimitbandwidth:

Jenkins node limit bandwidth
============================

AWS plugin can consume all the bandwidth in upload. Service provider does not guarantee  it.

::

         # Limit bandwidth of Jenkins user suppose source address 192.168.77.202
         tc qdisc del dev eth1 root htb
         tc qdisc add dev eth1 root handle 1:0 htb
         tc class add dev eth1 parent 1:0 classid 1:1 htb rate 12Mbit ceil 12Mbit prio 1
         iptables -t mangle -A POSTROUTING -o eth1 -s 192.168.77.202 -m owner --uid-owner 20000 -j CLASSIFY --set-class 1:1
