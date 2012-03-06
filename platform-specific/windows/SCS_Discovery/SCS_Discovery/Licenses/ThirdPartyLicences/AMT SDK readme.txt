
-------------------------------------------------------------------

  Copyright (C) Intel Corporation, 2004 - 2010 

  Readme file for
  - Intel(R) Active Management Technology (Intel AMT)
    Release 5.1 SDK  
  
-------------------------------------------------------------------

Table of contents:
1)  License
2)  System requirements
3)  Supported Intel AMT systems
4)  Installation instructions
5)  How to access the user guide
6)  New features and changes from Intel AMT release 3.0 SDK
7)  Notes
8)  Known issues list for Intel AMT release 4.0/5.0/5.1 SDK
9)  Known issues list from Intel AMT release 3.0 SDK
10) Integrated Development Environment (IDE) Known Limitations


1) INTEL SOFTWARE LICENSE AGREEMENT (SDK, Site License)
-------------------------------------------------------

IMPORTANT - READ BEFORE COPYING, INSTALLING OR USING.
Do not use or load this software and any associated materials (collectively,
the "Software") until you have carefully read the following terms and
conditions. By loading or using the Software, you agree to the terms of this
Agreement. If you do not wish to so agree, do not install or use the Software.

LICENSE:  Subject to the restrictions below, Intel Corporation ("Intel")
grants to you the following non-exclusive, non-assignable, royalty-free
copyright licenses in the Software. The Software may include portions offered
on terms in addition to those set out here, as set out in a license
accompanying those portions:

* Developer Tools include developer documentation, installation or development
  utilities, and other materials.  You may use them internally for the purposes
  of using the Software as licensed hereunder, but you may not redistribute
  them.

* Sample Source may include example interface or application source code.
  You may copy, modify and compile the Sample Source and distribute it in
  your own products in binary and source code form.

* End-User Documentation includes textual materials intended for end users.
  You may copy, modify and distribute them.

* Licensed Binaries are redistributable code provided in binary form.  You
  may copy and distribute Licensed Binaries with your product.

SITE LICENSE:  You may copy the Software onto your organization's computers
for your organization's use subject to and consistent with the terms of this
Agreement.

RESTRICTIONS:  You will make reasonable efforts to discontinue distribution
of the portions of the Software that you are licensed hereunder to distribute,
upon Intel's release of an update, upgrade or new version of the Software and
to make reasonable efforts to distribute such updates, upgrades or new versions
to your customers who have received the Software herein.
You may not reverse-assemble, reverse-compile, or otherwise reverse-engineer
any software provided solely in binary form.
Distribution of the Software is also subject to the following limitations:
you (i) are solely responsible to your customers for any update or support
obligation or other liability which may arise from the distribution,
(ii) do not make any statement that your product is "certified," or that its
performance is guaranteed, by Intel, (iii) do not use Intel's name or
trademarks to market your product without written permission, (iv) shall
prohibit disassembly and reverse engineering, and (v) shall indemnify, hold
harmless, and defend Intel and its suppliers from and against any claims or
lawsuits, including attorney's fees, that arise or result from your
distribution of any product.

OWNERSHIP OF SOFTWARE AND COPYRIGHTS. Title to all copies of the Software
remains with Intel or its suppliers. The Software is copyrighted and protected
by the laws of the United States and other countries, and international treaty
provisions. You may not remove any copyright notices from the Software.  Intel
may make changes to the Software, or to items referenced therein, at any time
without notice, but is not obligated to support or update the Software. Except
as otherwise expressly provided, Intel grants no express or implied right under
Intel patents, copyrights, trademarks, or other intellectual property rights.
You may transfer the Software only if the recipient agrees to be fully bound
by these terms and if you retain no copies of the Software.

LIMITED MEDIA WARRANTY.  If the Software has been delivered by Intel on physical
media, Intel warrants the media to be free from material physical defects for a
period of ninety days after delivery by Intel. If such a defect is found,
return the media to Intel for replacement or alternate delivery of the Software
as Intel may select.

EXCLUSION OF OTHER WARRANTIES. EXCEPT AS PROVIDED ABOVE, THE SOFTWARE IS
PROVIDED "AS IS" WITHOUT ANY EXPRESS OR IMPLIED WARRANTY OF ANY KIND INCLUDING
WARRANTIES OF MERCHANTABILITY, NONINFRINGEMENT, OR FITNESS FOR A PARTICULAR
PURPOSE.  Intel does not warrant or assume responsibility for the accuracy or
completeness of any information, text, graphics, links or other items
contained within the Software.

LIMITATION OF LIABILITY. IN NO EVENT SHALL INTEL OR ITS SUPPLIERS BE LIABLE
FOR ANY DAMAGES WHATSOEVER (INCLUDING, WITHOUT LIMITATION, LOST PROFITS,
BUSINESS INTERRUPTION, OR LOST INFORMATION) ARISING OUT OF THE USE OF OR
INABILITY TO USE THE SOFTWARE, EVEN IF INTEL HAS BEEN ADVISED OF THE
POSSIBILITY OF SUCH DAMAGES. SOME JURISDICTIONS PROHIBIT EXCLUSION OR
LIMITATION OF LIABILITY FOR IMPLIED WARRANTIES OR CONSEQUENTIAL OR INCIDENTAL
DAMAGES, SO THE ABOVE LIMITATION MAY NOT APPLY TO YOU. YOU MAY ALSO HAVE OTHER
LEGAL RIGHTS THAT VARY FROM JURISDICTION TO JURISDICTION.

TERMINATION OF THIS AGREEMENT. Intel may terminate this Agreement at any time
if you violate its terms. Upon termination, you will immediately destroy the
Software or return all copies of the Software to Intel.

APPLICABLE LAWS. Claims arising under this Agreement shall be governed by the
laws of California, excluding its principles of conflict of laws and the United
Nations Convention on Contracts for the Sale of Goods. You may not export the
Software in violation of applicable export laws and regulations. Intel is not
obligated under any other agreements unless they are in writing and signed by
an authorized representative of Intel.

GOVERNMENT RESTRICTED RIGHTS. The Software is provided with "RESTRICTED
RIGHTS." Use, duplication, or disclosure by the Government is subject to
restrictions as set forth in FAR52.227-14 and DFAR252.227-7013 et seq. or its
successor. Use of the Software by the Government constitutes acknowledgment of
Intel's proprietary rights therein. Contractor or Manufacturer is Intel
Corporation, 2200 Mission College Blvd., Santa Clara, CA 95052.

-------------------------------------------------------------------------------


2) System requirements
----------------------
System requirements are detailed in the Intel AMT SDK User Guide.


3) Supported Intel AMT systems
------------------------------

The Intel(R) AMT SDK is intended to support all presently shipping versions of
Intel(R) AMT (starting with the first official release 1.1.33).
Multiple versions of Intel(R) AMT firmware have shipped on different systems.
Although this SDK supports all versions of the firmware, there are bugs that 
have been fixed and features that have been added to later versions of the 
firmware. Developers should review the Versions.txt file on this CD to 
understand the different versions of the firmware that they can expect to 
encounter in shipping systems. See the Notes section below for more information.

4) Installation instructions
----------------------------
Simply copy the complete SDK directory structure to a location of your choosing.
Alternatively copy single components by copying just the component directory.

Note:   The SDK is designed to be copied as a single unit, as many samples 
        rely on common include files and code that is part of the SDK and 
        not replicated in each sample separately.

For details of components included in the Intel AMT SDK see the Overview section 
in the User Guide. 

5) How to access the user guide
-------------------------------
The documentation can be found in {CD ROOT}\Docs.

{CD ROOT}\Docs\index.htm serves as starting point to access and search
all of the documentation.

Documentation is supplied in Adobe PDF format. Viewing documents requires Adobe 
Reader* 5.0 or later. Searching the documents using the Search All Documents 
link requires Adobe Reader 7.0.

If you do not currently have Adobe Reader installed, it can be downloaded from:
http://www.adobe.com

6) New features and changes from Intel AMT release 3.0 SDK
-------------------------------------------------------------
- All the Windows software components were updated to Microsoft Visual Studio* 
  2005. The Storage library is also provided in Microsoft Visual Studio .NET 
  2003 project format.

- The SDK layout has changed. See the layout section in the User Guide.

- Linux operating systems versions were updated, see the user guide for details.

- All samples were updated to support new Intel AMT 4.0 features.
  Refer to the versions.txt file for a list of features available in various
  Intel AMT release versions.

- WS-Management sample C++ classes are provided in addition to the C# classes.

- Some WS-Management samples are provided in C++ using OpenWSMAN. These samples
  can easily be changed to use WinRM or gSOAP instead of OpenWSMAN by using the 
  WS-Management abstraction layer provided in the SDK. 

- A WS-Management sample is provided for Linux.

- AMT new features:
  * Secure Audit Log - Configuration and samples (4.0 & 5.0).
  * Client Initiated Remote access (CIRA) - Manageability Presence Server (MPS)
    sample provided, configuration support & most samples updated to support 
    working remotely (4.0 & 5.0).
  * Network Access Protection (NAP) - System Health Validator (SHV) sample 
    (4.0 & 5.0).
  * Samples for additional DASH 1.0 profiles - 'Role Based authorization (ACL)',
    WS-Eventing & DASH Discovery support (3.2 - apart from WS-Eventing, 4.0 & 
    5.0).
  * USB configuration has been updated to support many configuration options.
  * Wireless configuration WS-Management support (4.0).
  * New event log interface (3.2, 4.0 & 5.0).
  * Alarm clock feature (5.1).
  * DASH 1.0 compliance (5.1). This change has caused some backward 
    compatability issues. Additional information can be found in Intel AMT 
    WS-Management Capabilities Comparison.pdf document, in the DOCS folder.


7) Notes
--------
- The following Microsoft hotfixes are required to work correctly in some 
  situations:
  KB889388 - Digest DLL crash when connecting to an Intel AMT machine from 2 
  	     applications simultaneously.
  KB899900 - For using Kerberos authentication to connect to an Intel AMT 
             device.
  KB908209 - For using Kerberos authentication to connect to an Intel AMT 
             device using Internet Explorer.
  KB842773 - For using digest authentication from a Windows application to
             connect to an Intel AMT device on which Kerberos users are 
             configured.
             Note: this is included in Windows XP* SP2 and in Windows Server 
                   2003* SP1.
   
  See Intel AMT SDK User Guide for more details on some of these fixes.

- Several previously existing SOAP commands are now deprecated. The samples in 
  this SDK release only use new API calls. This means that the samples in this 
  SDK release (or applications developed using them) might not work with 
  machines using Intel AMT releases older than 4.0. SOAP commands supported 
  from Intel AMT 1.0 and deprecated in Intel AMT 2.0 are not supported by
  Intel AMT 4.0 devices. These functions are supported by the WSDL files for 
  working with previous generations of Intel AMT.

  Exceptions to this are the Discovery sample and the Configuration Server
  sample, which demonstrate, respectively, how to find Intel AMT machines
  and how to configure them. Both of these samples will work with Intel AMT
  machines regardless of their release version.

  For samples demonstrating the usage of older (deprecated) SOAP API, please
  refer to older releases of the Intel AMT SDK.

  See the Intel AMT SDK Network Interface Guide for detailed information on
  which SOAP commands are supported by which Intel AMT release versions.

- Most of the C++ SOAP samples in the SDK (with the exception of the Discovery
  and Configuration samples) might fail to operate against an Intel AMT
  Release 1.0 device, even when using non-deprecated API calls.

  This is because of the way in which the C++ samples use gSOAP to generate C++
  code from the WSDL files. The makewsdls.bat script uses the relevant gSOAP
  utilities on all the WSDL files relevant for the various SDK samples. As a
  result, gSOAP creates a namespace table which contains all the namespaces of
  all the WSDLs. All of these namespaces are then placed in the HTTP header of
  any SOAP request sent by gSOAP.

  The Intel AMT Release 1.0 device's HTTP server will not accept such a large
  HTTP header. To send SOAP commands to such a device, initialize gSOAP with
  a shorter list of namespaces (just the ones you need for the particular SOAP
  request you are sending). See the Discovery and Configuration samples for
  examples on how to set gSOAP namespaces in order to communicate with an
  Intel AMT Release 1.0 device.

- The C# & C++ classes derived from the MOF files are meant as samples only. The
  actual interface is defined by the MOF files, not the classes. Those classes 
  not used by any of the SDK's WS-Management samples were not tested.

8) Known issues for Intel AMT release 4.0/5.0/5.1 SDK
-------------------------------------------------

- NAP SHV sample:
  * 2687118: When using the SCS-Plugin sample to Validate signature and using 
             TLS, for the first 2-4 times SHV returns Non-Compliant answer 
             although the posture is compliant. 
  * 2308066: The NAP SHV sample has a potential memory leak of ~40 KB per hour
             when under constant stress of validating SoH postures from several
             machines. 
  * 2794868  The NAC PVS server sample in the SDK doesn’t work with the latest 
	     Apache server 2.2.x. the development sample works in Apache 2.0.x.

- Manageability Presence Server (MPS) sample:
  * 2686942: Configuration of Apache Proxy to support Kerberos in CIRA is not 
             documented. In order to support this, the 'httpd.conf' file should 
             be modified by un-commenting the line 'LoadModule headers_module 
             modules/mod_headers.so' and adding the following line 'Header set 
             Proxy-support Session-Based-Authentication'.
  * 2686939: Errors and warnings show in the log even when ERROR or WARNING are 
             removed from 'TraceLevel'.
  * 2686940: No indication is given for an invalid 'TraceLevel'.
  * 2621655: Configuring MPS to send notifications to a non-existent service 
             slows down MPS notifications to other services which might also be 
             configured.
  * 2621884: Supplying the wrong address when using MPS as a SOCKS proxy results
             with a "Connection refused" error number 5, instead of "Host
             unreachable" error number 4.
  * 2621887: Wrong error message printed to the log when trying to connect to a 
             non-existing authentication server.
  * 2621888: Log time stamp may be older than the records included in it.

- Redirection Library:
  * 2621744: Linux redirection library function 'IMR_Close' fails after ~1000 
             cycles of 'IMR_Init' and 'IMR_Close'.

- WS-Management client:
  * 2308079: Calling enumerate with selectors always returns all instances.
  * 2308083: Calling enumerate on a class with no instances using the WinRM 
             client causes a 'WsmanClientException'.

- AssetDisplay samples:
  * 2687191: SOAP sample: Memory size isn't parsed to determine if in MB or KB.
  * 2687196: Several Processor and Memory types are unknown by the samples,
             therefore the samples do not display them properly when
             enumerating these types.

- Linux EventLogReader WS-Management sample:
  * 2622430: Sample doesn't support TLS authentication.
  * 2687236: Sample usage includes Kerberos & TLS options incorrectly.

- Documentation:
  * 2686924: Permitted realms of CIM_SystemDevice.Get missing 
             ADMIN_SECURITY_EVENT_MANAGER_REALM.
  * 2622348: System Defense event names displayed by the secure audit log sample
             are not the same as in the Network Design Guide and Audit Log 
             Documents.

- Linux samples general:
  * 2567657: If swap partition is not activated, compilation may fail in Red Hat
             Enterprise Linux 5 x64. The OS may freeze for a long time and 
             eventually return an error. This is fixed if swap partition is 
             activated.

- Intel AMT 5.0:
  * 2737391: Voltage and current sensors reported incorrectly by WS-Management 
             API, with sensor type of 0. 
  * 2737433: CIM_Memory can display the wrong value as the cumulative memory
             available in the system. Instead, sum up the available memory in
             all CIM_physicalMemory instances.


9) Known issues list from Intel AMT release 3.0 SDK
---------------------------------------------------
* General

  -Title: Failure to connect to Intel(R) AMT device over TLS while
          OS is down, and DHCP options 81 & 12 are not supported
  -ID: 42466
  -Symptoms: When the enterprise's DHCP configuration does not support
             DHCP options 81 and 12, it won't be possible to connect to
             the Intel AMT device over a TLS connection after DNS
             tables refresh.
  -Cause: The certificate used for TLS is based on host name. If these DHCP
          options are disabled, the Intel AMT device has no means to
          update the DNS. Thus, DNS will remove the Intel AMT device
          entry upon tables refresh.
  -Impact On developer: None
  -Resolution: See Name Resolve Sample readme.

  -Title: Partial Unprovision performed although essential data is missing.
  -ID: b2443699
  -Symptoms: On several Intel AMT release versions (e.g. 3.0), the command
             PartialUnprovision() will succeed even if Remote Configuration
             is disabled and there is no PID/PPS set in the firmware. This
             means that in order to complete the configuration, the PID/PPS
             will have to be set manually via the MEBx or using a USB key
             (i.e. by physically touching the machine).
             This issue does not affect machines that have no support for
             Remote Configuration, i.e. Intel AMT releases 1.0, 2.0, 2.1
             and 2.5.
  -Cause: Implementation defect.
  -Impact On developer: Don't rely on the PartialUnprovision() command to
                        return PT_STATUS_NOT_PERMITTED when Remote
                        Configuration is disabled and no PID/PPS are set.
  -Resolution: Before calling the PartialUnprovision() command, verify that
               if Remote Configuration is disabled (by using the command
               GetZeroTouchConfigurationMode()), then PID/PPS is set (by
               using the command GetProvisioningPID()).
               Alternatively, if Remote Configuration is enabled, verify
               that the machine has active certificate hash entries (by
               using the commands EnumerateCertificateHashEntries() and
               GetCertificateHashEntry()).

  -Title: 802.1x server certificate, when added to CRL, does not cause Intel
          AMT to fail the authentication.
  -ID: b2445112
  -Symptoms: Adding to the CRL (Certificate Revocation List) the certificate
             that is used by the server will not fail the next authentications
             if session resuming is used, because in this case, certificates
             will not be re-sent.
  -Cause: Implementation defect
  -Impact On developer: Use the following suggested workaround.
  -Resolution: Adding the same 802.1x profile again (by calling the command
               Set8021XWiredProfile()) will clear the TLS session cache.

  -Title: In WS-Management, nested EndpointReferences (EPR) are not formatted as
          expected in selector set.
  -ID: b2448550
  -Symptoms: Intel AMT release 3.0 does not currently support the option of
             passing a Selector (key) of type EndpointReference. (These types of
             keys would typically be used for association objects).
             Consequently, when performing a WS-Management routine on an object
             which has a key of type EndpointReference, you may not pass its EPR
             key (or keys) as selectors, or the routine will fail and return a
             wsa:DestinationUnreachable fault.
  -Cause: Implementation defect
  -Impact On developer: Use the following suggested workaround.
  -Resolution: EndpointReferences that are returned by Intel AMT itself never
               include selectors of type EndpointReference. They are always
               returned with 1 selector with a hidden key property (GUID) that
               uniquely identifies all instances. The EndpointReference of an
               instance is received after creation (using command “Create”), or
               as fields of associations that are connected to the instance.
               Wherever possible, use these EndpointReferences as identifiers,
               instead of constructing your own EndpointReference from the
               object’s keys.
               Alternatively, if Intel AMT has only a single instance of the
               object (which is very often the case), you can pass an empty
               selector set.

  -Title: Intel AMT returns a "destination unreachable" fault when it was sent a
          WS-Management Enumerate command with an invalid selector in a filter.
  -ID: b2437295
  -Symptoms: When sending the Enumerate command with a selector that is not
             a key, Intel AMT will return a "destination unreachable" fault
             instead of "cannot process filter" fault.
  -Cause: Implementation defect
  -Impact On developer: Minimal - follow recommendation below.
  -Resolution: Make sure to use only keys as selectors when enumerating
               resources.

  -Title: Getting ProvisioningAuditRecord during in-provisioning state fails
          with undocumented/wrong error codes.
  -ID: b2442999
  -Symptoms: 1) When sending the GetProvisioningAuditRecord SOAP command during
                in-provisioning state, PT_STATUS_NOT_READY is returned, despite
                it not being documented in the Network Interface Guide as one of
                the possible return values.
             2) When invoking the GetProvisioningAuditRecord() method of the
                WS-Management AMT_SetupAndConfigurationService class during
                in-provisioning state, PT_STATUS_INTERNAL_ERROR is returned.
  -Cause: Implementation/documentation defect
  -Impact On developer: Minimal - follow recommendation below.
  -Resolution: Make sure not to call the GetProvisioningAuditRecord command
               during in-provisioning state.
               Alternatively, be prepared to handle the above mentioned return
               codes.

  -Title: Sending WS-Management packets encoded with an unsupported encoding
          type returns error code 401 instead of 415.
  -ID: b2438588
  -Symptoms: When sending a WS-Management request which is encoded with an
             unsupported encoding type (e.g. UTF-16), Intel AMT returns HTTP
             error code 401 ("unauthorized") instead of 415 ("unsupported media
             type").
  -Cause: Implementation defect.
  -Impact On developer: Follow recommendation below.
  -Resolution: Make sure to only use the supported encoding type: UTF-8.

  -Title: Calling the host interface command CFG_GetCertificateHashEntry with a
          handle that is not associated to any certificate hash, Intel AMT
          returns the error AMT_STATUS_INVALID_HANDLE.
  -ID: b2445816 
  -Symptoms: Calling the host interface command CFG_GetCertificateHashEntry
             (relevant for developing a Remote Configuration local agent) with
             a handle that is not associated to any certificate hash, returns
             AMT_STATUS_INVALID_HANDLE instead of AMT_STATUS_NOT_FOUND.
  -Cause: Implementation/documentation defect.
  -Impact On developer: Follow recommendation below.
  -Resolution: Treat an error code of AMT_STATUS_INVALID_HANDLE in this command as
               if it was AMT_STATUS_NOT_FOUND.

  -Title: When creating alert subscriptions with an invalid Address or Policy
          ID, PT_STATUS_UNSUPPORTED error is returned.
  -ID: b2443702
  -Symptoms: When creating SOAP or WS-Management alert subscription with an
             invalid Address or Policy ID, PT_STATUS_UNSUPPORTED error is
             returned instead of error status PT_STATUS_INVALID_PARAMETER.
             This is relevant for Intel AMT release 3.0 machines for the
             following commands:
                SubscribeForGeneralAlert SOAP command of UserNotification WSDL,
                SubscribeForGeneralAlert SOAP command of EventManager WSDL,
                Create WS-Management command of class AMT_SNMPEventSubscriber,
                Create WS-Management command of class AMT_SOAPEventSubscriber.
  -Cause: Implementation defect.
  -Impact On developer: Follow recommendation below.
  -Resolution: When creating an alert subscription, handle PT_STATUS_UNSUPPORTED
               and PT_STATUS_INVALID_PARAMETER error codes by checking if
               an invalid address or Policy ID was provided as a parameter.

  -Title: The firmware prevents setting more than 3 URLs inside a CRL.
  -ID: b2444568
  -Symptoms: The Certificate Revocation List (CRL) is constructed of a list of
             URLs, each URL followed by a list of serial numbers. The CRL can be
             empty, i.e. no URLs and no serial numbers. If the CRL is not empty,
             it should contain at least one URL followed by at least one serial
             number.
             When sending the SetCRL SOAP command of the Security Administration
             Interface or sending the AddCRL WS-Management command of the class
             AMT_PublicKeyManagementService to an Intel AMT release 3.0
             machine, if the CRL list contains more than 3 URLs, the operation
             will fail.
  -Cause: Implementation defect.
  -Impact On developer: Follow recommendation below.
  -Resolution: When sending SOAP or WS-Management commands to set or add CRL,
               the final CRL list should contain at most 3 URLs.


* Security Administration

  -Title: AddUserAclEntry() and UpdateUserAclEntry() fail when run by an
          application using ATLSOAP.
  -ID: 46074
  -Symptoms: The Firmware returns Internal Server Error (HTTP 500) when an
             application using ATLSOAP calls AddUserAclEntry() and
             UpdateUserAclEntry().
  -Cause: The SOAP/XML request created by ATLSOAP isn't parsed correctly by
          the firmware.
  -Impact On developer: Don't call AddUserAclEntry() and UpdateUserAclEntry()
                        from an ATLSOAP application.
  -Resolution: Use other SOAP libraries. C# and gSOAP are known to work
               correctly.


* ISV Storage

  -Title: Compiling the storage library with WSDL files using gSOAP will fail
  -ID: 45788
  -Symptoms: Trying to link an application which includes the storage library
             and other WSDL files using the gSOAP library will fail.
  -Cause: The storage library uses gSOAP and this situation creates multiple
          definitions.
  -Impact on developer: Use following instructions for compiling.
  -Resolution: (instructions are for Windows; the same applies similarly to
               Linux)
      1) Run wsdl.exe using the -n option
         e.g. wsdl2h.exe -e -t typemap.dat -o RemoteControlInterface.h -n
           remotecontrol RemoteControlInterface.wsdl
      2) Run soapcpp2.exe using the -p and -n options
         e.g. soapcpp2.exe -p remotecontrol -n RemoteControlInterface.h
      3) Link your application with the Intel AMT storage library
      3a) Don't include the gSOAP main files (e.g., soapstd2.cpp) and "SOAP
          Header and Fault serializers" since they are already included in the
          library.
      3b) Add "LIBC.lib" to "Ignore Specific Library" in Linker->Input.
          (Windows only)
      Your project should then compile successfully. In your application,
      make sure you set the correct namespaces before using soap calls. You
      should do that by using "soap_set_namespaces(soap*,<name>_namespaces)".
      You can check the namespaces names in the .nsmap file.
      NOTE (Windows only): openSSL use is not supported in this mode. Use
                           the WinHTTP extension for TLS support.


* Redirection Library

  -Title: An existing IDER session may be closed while trying to open a session
          to an unreachable Intel AMT system.
  -ID: b2196623
  -Symptoms: An existing IDER session will close.
  -Cause: Implementation defect.
  -Impact On developer: Verify machine is reachable prior to opening an IDER 
                        session.
  -Resolution: Verify machine is reachable prior to opening an IDER session.

  -Title: Adding tens of thousands of clients could overload system memory
  -ID: 43806
  -Symptoms: High memory consumption by the Redirection SDK process.
  -Cause:      When user adds a client to the Redirection SDK, some memory is
               allocated in order to create appropriate data structures and store
          client's data.
  -Impact On developer: None
  -Resolution: Mean memory consumption when adding many clients is about 1K per
               each new client added.  Adding tens of thousands of clients can
               consume a significant amount of memory. Limitations will change,
               depending on the amount of RAM available and other system
               configurations. On typical desktop system (Windows XP with 256 MB
               of RAM) the adding of 50,000 - 70,000 clients should be possible
               without a problem.

  -Title: Linux Redirection library: SOL session is sometimes terminated under
          stress
  -ID: 47537
  -Symptoms: When sending a lot of SOL data to the console, the SOL session is
             sometimes terminated with the message of "Session Timeout".
  -Cause: Implementation defect
  -Impact On developer: The SOL session is terminated.
  -Resolution: Restart the SOL session.

  -Title: SOL Transmit from console without open terminal in the host causes SOL 
          session to close
  -ID: b2138953
  -Symptoms: SOL Transmit from console without open terminal in the host causes 
  	     SOL session to close.
  -Cause: Implementation defect.
  -Impact On developer: None.
  -Resolution: Make sure terminal (or BIOS) is open on host for SOL session.

  -Title: SOL Receive stress (from host to MC) in FIFO mode causes SOL session
          to close.
  -ID: b2139367
  -Symptoms: SOL Receive stress may cause SOL session to close.
  -Cause: Implementation defect.
  -Impact On developer: Session may close under stress. This doesn't occur on 
                        normal BIOS redirection.
  -Resolution: SOL Receive stress shouldn't be used in FIFO mode.

  -Title: Linux Redirection library: The application sometimes hangs when
          closing an SOL or IDER session.
  -ID: 47538
  -Symptoms: When closing an SOL or IDER session (either by user command, link
             loss or when detecting no activity from the Intel AMT device)
             the application can sometimes hang.
  -Cause: Implementation defect
  -Impact On developer: The application hangs.
  -Resolution: Terminate the application's process and restart the application.

  -Title: Closing an IDER session during IDER stress might generate an error.
  -ID: b1685993, b2211199
  -Symptoms: Closing an IDER session during IDER stress sometimes results with
             the IMR_RES_SESSION_CLOSED error code (in the IMRGUI sample
             application, a message will be displayed stating:
             "Failed to Close IDER Session. Status: Session Closed").
             The session itself is closed normally, despite the operation
             returning an error code. In rare occasions, the sample application
             crashes as a result.
  -Cause: Implementation defect.
  -Impact On developer: Closing the session appears to have failed, although it
             has succeeded.
  -Resolution: Ignore this error value when closing an IDER session.

  -Title: Access to read only floppy image by IDER may cause loop (5 times) of
          write protect errors.
  -ID: b2171453
  -Symptoms: When trying to access a read only image write protect errors may 
             occur.
  -Cause: Implementation defect.
  -Impact On developer: Don't use a read only floppy image.
  -Resolution: Don't use a read only floppy image.

  -Title: No keyboard arrow keys redirection in OS selection screen
  -ID: b2332300
  -Symptoms: Using SOL and booting the Intel AMT machine, when in the Windows
             Vista OS selection menu, the keyboard arrow keys might not be
             redirected through the terminal emulator.
  -Cause: Implementation defect.
  -Impact On developer: Not every terminal emulator might be sufficient for
                        SOL usage.
  -Resolution: When using a terminal emulator for SOL, make sure it can send
               the arrow key presses.

  
* Configuration Sample

  -Title: Configuration Sample returns error after its folder name was renamed 
          in Windows Vista
  -ID: b2139230
  -Symptoms: Configuration Sample returns socket error in 2nd run after the 
             folder name was renamed in Windows Vista.
  -Cause: Implementation defect.
  -Impact on developer: Don't rename directory after running sample.
  -Resolution: Don't rename directory after running sample. 

  -Title: Sample configuration server doesn't report a "missing PKI certificate"
          when the path for the certificate is wrong.
  -ID: b2443006
  -Symptoms: The sample configuration server does not check the validity of the
             specified path to a PKI configuration full chain certificate file.
             As a result, if trying to configure a machine using the Remote
             Configuration flow, the SSL handshake will fail.
  -Cause: Implementation defect.
  -Impact on developer: None.
  -Resolution: Don't provide a wrong path to a PKI configuration full chain
               certificate file when using the Remote Configuration flow.

  -Title: SetTLSCredentials fails to disassociate key and certificate in IN_PROV
          mode
  -ID: b2448310
  -Symptoms: Before completing a Remote Configuration flow (by calling the
             CommitChanges function), trying to disassociate an already existing
             TLS certificate (by calling the SetTLSCredentials function with a
             NULL certificate) might fail with a PT_STATUS_NOT_PERMITTED error.
             When using the configuration sample in the SDK, if the Remote
             configuration flow has failed at a point after setting the TLS
             certificate, the next configuration (after fixing the bad settings)
             will fail, because the sample configuration server first tries to
             clear the existing certificates (by passing a NULL certificate to
             SetTLSCredentials, which will fail) and then tries to re-add the
             TLS certificate (which will fail with a PT_STATUS_DUPLICATE error,
             since the certificate was never removed after being added in the
             first configuration attempt).
  -Cause: Implementation defect.
  -Impact on developer: None.
  -Resolution: When developing a configuration server that uses the Remote
               Configuration flow, note that calling SetTLSCredentials with a
               NULL certificate might fail. If you try to re-add a certificate
               be aware that it might not have been removed, and don't fail the
               configuration if CertStoreAddCertificate returns with the error
               code PT_STATUS_DUPLICATE.


* WS-Management samples

  -Title: Incorrect XML representation of AMT_EthernetPortSettings.LinkPolicy
  -ID: b2447178
  -Symptoms: When using the AMT_EthernetPortSettings class using the .NET
             XmlSerializer, the LinkPolicy field is a byte array (byte[])
             and is sent with each array element in its own <LinkPolicy> XML
             tag. However, the .NET XmlSerializer expects byte arrays to be
             either hex-binary or Base-64 encoded, and would return a zero
             length array for the list of <LinkPolicy> tags.
  -Cause: .NET XmlSerializer behavior.
  -Impact On developer: When using the AMT_EthernetPortSettings class using
                        the .NET XmlSerializer, can't get or set the
                        LinkPolicy field.
  -Resolution: The type of the LinkPolicy field can be modified to be an
               int array (int[]) instead of a byte array. The .NET
               XmlSerializer can then get/put this array, with each array
               element in its own <LinkPolicy> XML tag.


10) Integrated Development Environment (IDE) Known Limitations
--------------------------------------------------------------

* When running C# SOAP client through the Microsoft Visual Studio .NET debugger,
  the debugger sends debug information which is not recognized by the Intel
  AMT device. The debug information can be disabled by adding the following
  section to the App.config file:

  <configuration>
    <system.diagnostics>
      <switches>
        <add name="Remote.Disable" value="1" />
      </switches>
    </system.diagnostics>
  </configuration>


-------------------------------------------------------------------
 * Other names and brands may be claimed as the property of others.
