---
title: "NPC SS 21-006: Wefund Lending Corporation and its Responsible Officers"
description: "Sua sponte investigation determining that Wefund Lending Corporation violated Section 25 of the DPA through unauthorized processing of personal information; case dismissed as to responsible officers for lack of substantial evidence."
aliases:
  - "NPC SS 21-006"
  - "npc ss 21-006"
  - "Wefund Lending Corporation and its Responsible Officers"
  - "wefund lending corporation and its responsible officers"
tags:
  - decision
  - type/decision
  - year/2021
  - npc-case
  - topic/breach-notification
  - topic/consent
  - topic/data-subject-rights
  - topic/legitimate-interest
  - topic/online-lending
  - topic/security
date: "2022-05-16"
draft: false
---

## Source
- Reference: NPC SS 21-006
- Official PDF: http://privacy.gov.ph/wp-content/uploads/2024/05/NPC-SS-21-006-2022.05.16-In-re-Wefund-Lending-Corporation-Decision-FinalP.pdf
- Source page: http://privacy.gov.ph/decisions-2/
- Issue date: May 16, 2022
- Published on NPC site: Fri, 24 May 2024 01:29:24 GMT
- Pages: 51

## Source Tags
- Unauthorized Processing (Section 25), Legitimate interest (Section 12 f)), Extent of Liability (Section 34), Substantial Evidence, Gross Negligence, Sua Sponte Investigation, Temporary Ban, Legitimate Purpose, Proportionality, Transparency

## Decision Text

IN RE: Wefund Lending Corporation (JuanHand) and its Responsible Officers

INITIATED AS A SUA SPONTE NPC INVESTIGATION ON THE POSSIBLE DATA PRIVACY VIOLATIONS COMMITTED BY WEFUND LENDING CORPORATION (JUANHAND)

x----------------------------------------------------x

AGUIRRE, D.P.C.:

Before this Commission is a Fact-Finding Report with Application for the Issuance of a Temporary Ban on the Processing of Personal Data (FFR) dated 09 June 2021 against Wefund Lending Corporation (JuanHand), the operator of the online lending application, JuanHand, and its responsible officers.

The Complaints and Investigation Division (CID) of the National Privacy Commission, pursuant to its power to conduct sua sponte investigations, filed an FFR against JuanHand. The FFR alleged that JuanHand committed violations of Republic Act No. 10173 or the Data Privacy Act of 2012 (DPA) and the Commission’s issuances. This concludes the sua sponte investigation conducted by the Commission.

### Facts

On 09 June 2021, the CID submitted its FFR against JuanHand following numerous reports of continuing privacy violations committed by several online lending applications (OLAs).[^1] The CID


initiated a sua sponte investigation against JuanHand[^2] pursuant to

[[laws/data-privacy-act-of-2012#section-7-functions-of-the-national-privacy-commission|Section 7 of the DPA]] that mandates the Commission to institute investigations in cases it deems appropriate[^3] and NPC Circular 21-01 (2021 Rules of Procedure) that permits the NPC to initiate sua sponte investigations and file complaints for DPA violations.[^4] The FFR serves as the complaint, with the CID as the Nominal Complainant, in sua sponte investigations.[^5]

In the CID’s technical investigation, it downloaded JuanHand installer version v.3.7.1 from Google Play Store and simulated JuanHand’s registration and loan application processes.[^6]

The permissions required by the application (app) were outlined in Google Play Store prior to its download and installation:[^7]

• read calendar events plus confidential information;

• add or modify calendar events and send email to guests without

owner’s knowledge;

• read your contacts;

• approximate location (network-based); and
• precise location (GPS and network-based).[^8]

Upon the installation and opening of the app, it immediately asked for permission to access contacts, thus, the CID stressed that “the permission to access contacts was required upon installation of the application, even without a loan being applied for.”[^9]

During the CID’s simulation, when the loan application form required character references, the app prompted the CID to: “[p]lease allow access to your contacts. This authorization will allow us to speed up your application process and prevent criminals from stealing your money.”[^10] Thus, the notification for permission to access contacts appeared when the app was opened and when inputting of character references were asked in the loan application process.[^11] The CID found


that there was no manual way of entering a phone number and it must be done through giving access to the contact list.[^12] Corollary, the loan application would not have progressed to the next step if the character references’ phone numbers were not given.[^13]

When the CID examined the source code of the app, it showed that the app utilized the Android software development kit (SDK) that provides coding for contacts retrieval, wherein an app will have the ability to collect data from contacts.[^14] The “AndroidManifest.xml” file explicitly contained a contacts permissions line as seen in the code “android.permissions.READ_CONTACTS”.[^15] The CID explained that, when this is enabled, it gives an app the ability to read the user’s phone contacts data.[^16]

The CID also disclosed that “no Privacy Policy was found on both JuanHand’s website and mobile application.”[^17] It searched for JuanHand’s Privacy Policy and instead found a link to the Service Agreement, which is “found only during the signup process in the [app] and the user will not be able to see or read the [S]ervice [A]greement again as there is no link of this agreement inside the application and no visible link on [JuanHand’s] website.”[^18]

The Service Agreement provided for the following pertinent

provisions:

[B. Limitation of Use]

[4. You agree to register with a username that does not to [sic]

violate the laws and social ethics and provide your real

information, and comply with the following requirements:]

[b].  You must provide true, up-to-date, valid and complete

information, and grant Juanhand a permanent right to use

the information you provide free-of-charge for the purpose

of using Juanhand service .


[K. Privacy]

[2. Source of Information]

[b].  In addition to the information provided to Juanhand by the

User voluntarily, User agrees that Juanhand and its partners

to collect and verify the User's information, including, but not

limited to the following manner:

iv. information related to personal communication

(including, but not limited to, contact list, geographical

location, device identification number, social networking

profiles) provided or authorized by the User, or

communication information relating to the activities and

logging in by the User provided to Juanhand by other Users

or third party, Juanhand can collect this information in the

User’s file.

[vi.] Juanhand will collect your Facebook platform

information through your authorization. Including but not

limited to: username, user ID, registered email, gender, etc.

[3. Use of Information]

[g]. I authorize the disclosure to and collection of my personal

data from Third Party Entities (‘Partners’) engaged by Juanhand

for the purposes stated under the heading Use of Personal Data.

These Partners shall refer to my employer (for auto-debit or other

auto-deduction mechanism) whether private or government,

telecommunication companies (e.g., Globe Telecom, Inc., PLDT,

Smart, Sun Cellular), utility companies (e.g., Meralco, Maynilad),

government agencies (e.g., SSS, GSIS, NSO, BIR), credit bureaus

(e.g., CIC, NFIS), remittance companies (e.g., Palawan Express,

Cebuana Lhuillier, etc.), insuran ce providers (e.g., Sun Life

Grepa Financial Inc., Insular Life, etc.), financial service

providers (e.g., CC Mobile Financial Services Philippines, etc.),

and other service providers. (2) I authorize Lending Company

Inc. to share my personal data with Len ding Company Inc.’s

parent, affiliate, subsidiaries even after my loan with Lending

Company Inc. is sold or assigned by it to another creditor for data

analytics, determination of insurable interest and amount

insured, statistical analysis and demographics , and business

development purposes, and fraud detection and investigation.

[h.] I authorize Juanhand to process Mobile device data (e.g.,

mobile phone number/s, mobile phone message data, SIM, IMEI,

or other device identifiers, type of device, device operating

system, device settings, user account information for your mobile

device or Google PlayStore account, information about mobile

network provider, device specifications), Location data (e.g.,

mobile device location, time zone setting); Phone data (e.g.,

contact lists, SMS metadata, types and nature of mobile NPC SS 21 -006

applications found on your mobile device); mobile app usage

data (e.g., traffic volume, mobile app usage) and

telecommunications usage data or ‘telco usage score’ .

[4. Disclosure of User’s Information by JuanHand]

[d.] When the Borrower is overdue for payment, Juanhand may

publish the personal information of such user for the purpose

of collecting debt. Juanhand shall not be held liable.

The Data Privacy Act (DPA) establishes that you have the

following rights as a data subject:

• You have the right to indicate your refusal to the collection

and processing of your personal data. You also have the

right to be informed and to withhold your consent to

further processing in case there are any changes or

amendments to information given t o you. Once you have

notified us of the withholding of your consent, further

processing of your personal data will no longer be done,

unless (i) the processing is required pursuant to a

subpoena, lawful order, or as required by law; or (ii) the

collection and processing is pursuant to any lawful criteria

indicated under the terms of this Policy.

• You have the right to reasonable access to your personal

data. Furthermore, you have the right to limit and prevent

disclosure of your personal data and to receive

notification of any possible breaches of your personal

data.

• You may also correct or remove any information that you

think is inaccurate. You have the right to dispute any

inaccuracy or error in your personal data. You may

request for the correction or removal of any inaccuracy or

error in your personal data by logg ing into your account

or making a formal request with our Data Privacy Officer.

• You have the right to the destruction of your personal

data;

• You have the right to damages; and

• You have the right to lodge a complaint with the National

Privacy Commission (NPC).

If you would like to make any request in relation to your rights

as a data subject, please contact our Data Protection Officer

(‘DPO’) with the contact details listed below . Please note that the

exercise of some of your rights as a data subject is subject to

review and may result in the denial of any application

currently pending .19


The CID , however, found through “JuanHand’s Permission

Information,” that JuanHand’s system can do the following:

1.  read the borrower’s calendar events plus confidential

information;

2.  add or modify calendar events;

3.  send email to guests without the owner’s knowledge;

4.  read borrower’s contacts;

5.  collect data from contacts; and

6.  pinpoint the borrower’s approximate and precise location

through its network and GPS. 20

As can be gleaned from the Service Agreement and the permissions

that CID discovered in its technical investigation , there are certain

permissions that were not disclosed at all in the Service Agreement,

particularly the ability to read and modify a borrower’s calendar

events and confidential information.

Based on the foregoing , the CID argued that JuanHand violated the

DPA and the Commission’s issuances.

First, the CID opined that the undisclosed permissions in JuanHand’s

app violated [[laws/data-privacy-act-of-2012#section-16-rights-of-the-data-subject|Section 16 of the DPA]]. 21  It found that:

The capabilities of JuanHand’s system to read the borrower’s

calendar events plus confidential information, add or modify

calendar events, send email to guests without the owner’s

knowledge, read borrower’s contacts, collect data from contacts

and pinpoint the borrower’s approximate and precise location

through its network and GPS are all unknown to the prospective

borrower. The permission information […] is not shown to the

users thru [sic] prompts or permissions when applying for a

loan but was discovered by the CID Technical Team from the

Google Play Store and not from the application itself .22

Since JuanHand’s data subjects were not informed that their personal

information have been processed, the CID argued that JuanHand

violated Section 16 of the DPA, which states that a data subject is


entitled to “[b]e informed whether personal information pertaining to

him or her shall be, are being or have been processed[.]” 23

Second, the CID asserted that JuanHand’s undisclosed permissions

violated the general privacy principles of transparency, legitimate

purpose, and proportionality. 24

The CID elaborate d that pursuant to the transparency principle , a data

subject must be aware of the nature, purpose, and extent of the

processing of his or her personal data, including the risks involved. 25

It argued that JuanHand “has the duty to inform its data subjects, by

clearly indicating in its privacy notice, the purpose/s for storage of the

personal information they access.” 26  Related to this, the CID elucidated

that “under NPC Circular 20 -01, access is allowed for [OLA] provided

[it] will use such information for [Know Your Customer (KYC)]

purposes, after accomplishing such purpose, the OLA should have

removed their access on the personal information it stored.” 27  Thus,

the CID claimed that JuanHand violated the principle of transparency

because the borrowers were not aware of the nature, extent, and risks

involved in granting access to his contacts. 28  The app “failed to provide

the purpose for the storage of the personal information accessed, and

such cannot be seen in the [a]pp’s Privacy Notice nor can [it] be

deduced from the permission it requires.” 29

As to the principles of proportionality and legitimate purpose, the CID

contended that JuanHand violated these general privacy principles

when it required access to borrowers’ contacts. 30

Legitimate purpose provides that “the processing of information shall

be compatible with a declared and specified purpose, which must not

be contrary to law, morals, or public policy.” 31


According to the CID’s technical investigation , when the permission

to access contacts is denied, a prompt is shown, stating: “Please allow

access to your contacts. This authorization will allow us to speed up

your application process and prevent criminals from stealing your

money.” 32  Thus, it argued that, “[h] arvesting contacts and data of

contacts are irrelevant, unnecessary and excessive in its declared

purpose of speeding up the processing of loan applications and

prevention of criminals from stealing money.” 33

The CID further opined that “the legitimate purpose principle requires

that the processing or [sic] personal information should meet one of

the criteria for the lawful processing of information as provided in

Sections 12 and 13 of the DPA[.]” 34  Valid consent or authority under

the DPA and other existing laws is necessary for the processing to be

authorized. 35  Given this, the CID alleged that JuanHand is without

valid consent or authority under the DPA to process and store the

borrowers’ phone contacts, which is in violation of the

abovementioned general privacy principles. 36

Third, the CID assert ed that “Juan[H]and’s requirement of having

access to phone book contacts even before the processing of the loan

clearly violates NPC Circular No. 20 -01” or the Guidelines on the

Processing of Personal Data for Loan -Related Transactions (Loan -

Related Transactions Circular ). 37  This is because , according to the CID,

the Loan -Related Transactions Circular “prohibits access to contact

details in whatever form, such as but not limited to phone contact list,

the harvesting of social media contacts, and/or copying or otherwise

saving these contacts.” 38  Further, it argued that “[i]n all instances,

online lending apps must have a separate interface where borrowers

can provide character references and/or co -makers of their own

choosing.” 39  Thus, the CID maintained that:

As discussed, JuanHand did not limit itself to a number of

character references of the borrower’s own choosing but required

access to all phone and social media contacts. It also failed to


comply with the required separate interface where borrowers

can provide character references and/or co -makers of their own

choosing. The availability of far less intrusive measures, such as

reliance on a limited number of reference contacts provided by

the borrower, demonstrates that the measures employed by

JuanHand were disproportionate to the aim of evaluation of the

loan application and/or loan collection purposes. 40

Fourth, the CID stated that the Privacy Policy violated the DPA and its

issuances:

JuanHand’s Privacy Policy, imbedded in the Service Agreement,

not only violates the general data privacy principles of

transparency, legitimate purpose and proportionality but makes

a mockery of the Data Privacy Act when it says that the exercise

of the privacy rights by the users is subject to review by

JuanHand and may result in the denial of any pe nding

application in violation of Section 16 of the DPA. The borrowers

are made to choose between their privacy and the much -needed

funds. The consent, therefore, that the borrowers granted to

JuanHand was not by will but thru [sic] coercion. 41

In addition, the CID pointed out irregularities in JuanHand’s Service

Agreement:

The Service Agreement of JuanHand provides that the borrower

must provide true, up-to-date, valid and complete information,

and grant JuanHand a permanent right to use the information the

borrower provided free-of-charge for the purpose of using

Juanhand s ervice. The permanent right to use the information

provided by the borrower free-of-charge for the purpose of using

JuanHand service is in violation of Rule IV of the [[laws/implementing-rules-and-regulations-of-the-data-privacy-act-of-2012|Implementing Rules and Regulations]] of the Data Privacy Act of 2012 which

states that the personal data should not be retained longer than

necessary. Personal data shall not be retained in perpetuity in

contemplation of a possible future use yet to be determined.

The provision in the Service Agreement which provides that:

‘When the Borrower is overdue for payment, Juanhand may

publish the personal information of such user for the purpose of

collecting debt. Juanhand shall not be held liable. ’ violates NPC Circular No. 20 -01 specifically Section 3, paragraph D4 of the

Circular which states:


‘Access to contact details in whatever form, such as but not

limited to phone contact list or e -mail lists, the harvesting of

social media contacts, and/or copying or otherwise saving these

contacts for use in debt collection or to harass in any way the

bor rower or his/her contacts, are prohibited. In all instances,

online lending apps must have a separate interface where

borrowers can provide character references and/or co -makers of

their own choosing. ’42

Again, the CID reiterated that undisclosed permissions in the app

exist, and that JuanHand did not acquire the consent of the data

subject s to process personal information arising from these

undisclosed permissions. 43  The CID considered these acts to be

unauthorized processing of personal informatio n in violation of

[[laws/data-privacy-act-of-2012#section-25-unauthorized-processing-of-personal-information-and-sensitive-personal-information|Section 25 of the DPA]] since JuanHand processed personal information

without valid consent or authority under the DPA and other existing

laws. 44

After having alleged violations of the DPA, the CID argued that

JuanHand ’s responsible officers should be held liable pursuant to

[[laws/data-privacy-act-of-2012#section-34-extent-of-liability|Section 34 of the DPA]] .45

Lastly, the CID interposed that:

Based on the initial results of the investigation conducted by the

CID, there is sufficient ground to warrant for the issuance of a

Temporary Ban on the processing of personal data against

WEFUND Lending Corporation, in relation to its online lending

appli cation, JuanHand. A review of its privacy policy shows that

JuanHand’s nature, purpose, and extent of accessing and

processing user’s personal information failed to adhere to the

principles of transparency, legitimate purpose and

proportionality. The simul ation of the installation of JuanHand’s

application and analysis of its source code show that its use of

dangerous permissions, is in direct violation of the prohibition

against the access of contacts, as provided in NPC Circular 20 -

01. 46


As such, it argued that substantial evidence had been established for

the issuance of a temporary ban against JuanHand .47

On 16 June 2021, the Commission issued an Order suspending the

complaint proceedings until the resolution of the application for the

issuance of a temporary ban. 48  JuanHand was ordered to submit a

position paper on the application for the issuance of a temporary ban

within ten (10 ) days from its receipt of the Order. 49

On 05 July 2021, the CID submitted a Supplement al Fact-Finding

Report with Application for Issuance of Temporary Ban on the

Processing of Personal Data , impleading specific responsible officers

of JuanHand in their official capacities as corporate officers and

members of the Board of Directors (Corporate Officers and Directors) ,

in line with Section 34 of the DPA .50

In a letter dated 02 August 2021, JuanHand acknowledged receipt of

the 16 June 2021 Order issued by the Commission and requested an

extension to submit its position paper since its change in physical office

caused its belated receipt of the Order .51

On 12 August 2021, JuanHand submitted a Motion to Properly Serve

Order with Motion to Admit Position Paper Ad Cautelam 52  and its

Position Paper on the application of the issuance of a temporary ban .53

It attached to the Position Paper a “standalone and rectified Privacy

Policy independent from the Service Agreement.” 54  JuanHand claimed

that the new Privacy Policy shall be shown and given consent to by the

borrowers upon registration and loan application. 55

Further, JuanHand clarified that it has not published any image or

information of its users for purposes of loan collection or harassment. 56


It will, however, continue to publish personal information of

delinquent users to the Credit Information Corporation for purposes

of creating a centralized credit information system. 57

As regards the undisclosed permission s in its app, JuanHand

explained that “[d]espite the embedded privacy policy in the Service

Agreement, which we undertake to rectify immediately, we would like

to clarify the corresponding consent sought and granted by our users

in relation to the permission information”:

• send email to

guests

Users are manually fill in his/her email

address. There is no way a user become

unaware of providing email address. Under

section 3(d) of the Service Agreement, we

stated clearly that Juanhand may use the User's

information to communicate with the User and

deliver information via SMS messages, email

and phone calls with respect to

communications relating to the use of

Juanhand by the User.

> •

read

borrower’s

contacts,

> •

collect data

from contacts

Under section 2(b)(iv) and 3(h) of the Service

Agreement, we stated clearly that Juanhand

will collect and process contact list. More

explanation about accessing contact list later.

• pinpoint the

borrower’s

approximate

and precise

location

through its

network and

GPS

Under section 2(b)(iv) and 3(h) of the Service

Agreement, we stated clearly that Juanhand

will collect and process geographical location

(e.g., mobile device location, time zone

setting). 58

. . .

Further, we do also read the borrower’s calendar events and

add or modify calendar events. We consider that accessing and

modifying user’s calendar is legitimate and proportional to the

purpose stated in the Service Agreement for two reasons:

(i) Credit Analysis and Scoring: by accessing the calendar,

we seek to identify due dates of other loans or payment

obligations of the users to determine whether or not to

provide loan services, and if so, his/her credit limits;


(ii) Due Day Reminder: by adding due date to the users’

calendar, it would be easier for the users to apprehend the

due date and, thus, repayment obligation.

Therefore, we consider that when users give consent to the

Service Agreement, users are materially informed the kind of

personal information shall be processed in compliance with

section 16(a) of the DPA and have given consent to the above

functions .59

Nevertheless, JuanHand acknowledged that it shall “enhance the

transparency and timeliness of obtaining user’s consent by

incorporatin g” certain prompts upon registering as a user in its app. 60

Lastly, JuanHand stressed that it does not use its users’ contact lists for

purpose s of collection or harassment but only for purposes of identity

verification, credit scoring, and fraud prevention. 61  It argued that

accessing the borrower’s contact list is necessary since, in certain

situations, it is the only means available to verify its users. 62  Thus,

“[v]erification by accessing users’ contact lists […] is a less -intrusive

and more reliable way for [ JuanHand ] to assess credit level and

risks.” 63

JuanHand prayed for the dismissal of the application for the issuance

of a temporary ban on its processing of personal data. 64

On 12 August 2021, the Commission issued an Order grant ing the

application for the issuance of a temporary ban against JuanHand

because all the requisites for granting a temporary ban were satisfied .65

The temporary ban would remain in effect until the final resolution of

the sua sponte investigation against JuanHand and its Corporate

Officers and Directors .66  Further, it ordered the following:

Further, pursuant to the TEMPORARY BAN , Respondent

Wefund Lending Corporation shall:


1.  Immediately take down its online lending application,

JuanHand, to ensure that it is no longer available for

download, installation or use by data subjects; and

2.  Stop personal data processing activities, including those

activities outsourced to third parties, where the processing

operations involves use of information from the phonebook,

directory, and contact list of data subjects, disclosure of false

or unwarranted information, and other undu ly intrusive

personal data processing methods. 67

The Commission also ordered JuanHand to file its comment on the

allegations in the FFR within ten (10) days from receipt of the Order .68

On 02 September 2021, JuanHand took down the app and submitted

its Comment to the Order and Temporary Ban dated 12 August 2021. 69

It emphasized that, pursuant to the 12 August 2021 Order, it has taken

down the JuanHand app from Google Play, Apple’s AppStore,

Huawei’s AppGallery , and Vivo Market, thereby making the app

unavailable for download by the public in any official platform. 70  It

also attached as annexes its revised Privacy Policy and Service

Agreement , as well as their respective correct hyperlinks. 71  Aside from

producing a separate Privacy Policy, JuanHand also began

incorporating the Privacy Policy in its user registration process. 72  Users

can now view the entire document and choose whether to agree to the

Privacy Policy before completing the registration. 73

As regards the permissions, JuanHand alleged that it deleted from its

app the access to its users’ calendar, location, contact list , and social

networking profile.  74  It also removed from its revised Privacy Policy

the permission s to access calendar, location, contact list , and social

networking profile .75  In order to make the prompts for these

permissions more “eye -catching,” it has shifted from using system

prompts to providing more intuitive and visible pop -up prompts


when the app attempts to access user’s personal information, wherein

the users may accept or deny such access. 76  Effectively, JuanHand

explained that these new alterations would ensure that :

[E] very time the data of a user is being accessed, such pop -up

prompt will trigger and will halt the entire process. This pop -up

prompt is now effective and live in JuanHand App during user

registration and loan application. We guarantee to the

Commission that there will be no hidden permissions in

JuanHand App and that we have implemented a more intuitive

design geared towards to providing actio nable knowledge to our

users and protection of the user's data. 77

JuanHand also included the “What’s New” feature in the app itself and

not merely in the download interface of platforms. 78  Any material

changes, such as the amendment of the Privacy Policy and Service

Agreement and other new functionalities, among other things, will be

shown in the “What’s New” interface. 79

Seeing, however, as the app is not available for the public market,

JuanHand explained that it re -created its app in a sandbox mode to

ensure that the app fully complies with all the requirements imposed

by law and by the Commissio n.80  It attached a quick response ( QR )

code for the Commission to download the testing version 4.1.1 of the

app since JuanHand strives to ensure full alignment with the

Commission’s regulations prior to the final re -deployment of its a pp

to the public. 81

Lastly, JuanHand attached as annexes its (1) Personal Privacy

Information Management Policy which serves as its comprehensive

corporate data protection policy and (2) Information Security

Emergency Response Management Directive which serves as its

structured approach in responding to incidents wherein the users’

data privacy may be breached or in any way compromised. 82  Thus, it

prayed that the Commission lift its temporary ban on the app and

allow its re -deployment to the public. 83


On 10 September 2021, it filed both the Entry of Appearance with

Motion to Admit [Supplemental Comment with Motion for Lifting of

Temporary Ban ]84  and the Supplemental Comment with Motion for

Lifting of Temporary Ban 85 .

Meanwhile, the Enforcement Division (EnD) of the Commission

continuously monitored the availability of the app pursuant to the

temporary ban. 86  It received, however, an email complaint which

included a link provided by the JuanHand Collection Department for

the downloading of the app. 87  Upon investigation, it found that the

direct download link (DDL) was for JuanHand app version 4.2.0 :88

To note, this version of the JuanHand APK file (v4.2.0) is different

from the one investigated by the Complaints and Investigation

Division (CID) which is v3.7.1 and the one [JuanHand] sent in an

email […], which is v.4.1.1, for compliance checking and

inv estigation. 89

Thus, o n 16 September 2021, the EnD issued a Letter to JuanHand

regarding its compliance with the Commission’s 12 August 2021

Order. 90  The EnD confirmed that, as of 06 September 2021, the

JuanHand app was no longer available for download on different

platforms. 91  The EnD, however, relayed that :

[T]he Commission received several reports from Juanhand’s

users. According to the reports, JuanHand’s Collection

Department sent them various links leading to the Direct

Download Links to the JuanHand application. Upon

investigation, the EnD was able to download the JuanHand

application through the Direct Download Links after

following the links provided in the reports.

As the Order dated 12 August 2021 directs JuanHand to

‘immediately take down its online lending application,


JuanHand, to ensure that it is no longer available for download,

installation or use by data subjects,’ JuanHand is instructed to

EXPLAIN the foregoing incident within FIVE DAYS (5) from

receipt of this letter. Such incident could be construed as a

violation of the Temporary Ban. 92

On 17 September 2021, the Commission issued an Order noting

JuanHand’s Comment and submissions. 93  In the Commission’s Order,

it emphasized that JuanHand was previously ordered to comment on

the FFR dated 09 June 2021 and not the issuance of the temporary

ban. 94  Nevertheless, it reiterated its order for JuanHand and its

Corporate Officers and Directors to comment on the FFR within a non-

extendible period of ten (10) days from receipt of the Order. 95

On 08 October 2021, JuanHand submitted its Reply and Explanation to

the National Privacy Commission Enforcement Division Letter dated

16 September 2021. 96  It countered that prior to the commencement of

the sua sponte investigation, it already prepared a template for the

repayment reminder Short Message Service (SMS) and emails it will

send out to its users that have availed themselves of loans. 97  The

template includes, among other things, a hyperlink to the JuanHand

app. 98  It explained that:

The sending of SMS and emails is an automatic process sent by

the JuanHand system, without human intervention , which

transmits repayment reminders to the Borrowers[.]

. . .

Based on the abovementioned template, the hyperlink or DDL

has always been part of the messages, both SMS and email, sent

to JuanHand users even before the issuance of the Temporary

Ban.

. . .


Unfortunately, after the removal or unavailability of the

JuanHand application on the Platforms for download, the

standardized or template repayment reminder SMS and emails,

which were inadvertently retained, automatically sent out,

without human intervention , to the JuanHand users, which still

contained the hyperlink or DDL to the JuanHand application. 99

JuanHand stressed that it only became aware of the situation on 17

September 2021, after which it conducted an internal investigation to

rectify the situation. 100  Apparently, the “template repayment

reminders were not updated or revised —the same unintentionally

retained the hyperlink or DDL” since the reminders were “system -

generated and automatically sent” to its users following certain

timelines or outstanding milestones. 101  After being made aware of the

situation, JuanHand immediately ordered the removal of the DDLs

from its repayment remind er s and instructed its designated personnel

to ensure that the DDLs that were sent out to users be inaccessible and

deactivated. 102  JuanHand posited that since its focus was solely to take

down its app from downloading platforms and prepar e responses to

the orders of the Commission, it committed a “complete and

unfortunate oversight” when the DDL to its app continued to be

included in its repayment reminder. 103

Nevertheless, despite the inadvertent sending of SMS and emails

containing the DDLs, JuanHand stressed that it never meant to

circumvent the prohibition under the temporary ban and that it

immediately took actions to rectify the matter. 104  Lastly, as a sign of

good faith and in immediate response to the EnD’s letter, JuanHand

sent messages to its six hundred thirty -two (632) users that were able

to use, access, or download the app during the period of the temporary

ban’s effectivity:

Dear Valued Client. We apologize to inform [you] that

Juan[H]and application is currently unavailable for

downloading in compliance to National Privacy Commission’s

order. If you have received Juan[H]and download links before,

please do not access it anymo re. We would like to express our

sincere gratitude to every Juan. Thank you. 105


On 11 October 2021, JuanHand submitted to the Commission its

Comment (on the Fact-Finding Report dated 09 June 2021) addressing

the allegations of the CID in its FFR .106

JuanHand stressed that there is more than one allowable basis for

processing in this case : (1) data subject’s consent; (2) contract of loan ;

and (3) legitimate interests pursued as lender. 107  Thereafter, it stated

that JuanHand has “already rectified any perceived violation” of the

DPA and that it has pursued “legitimate interests and purposes” in

processing the personal information of its users. 108  Moreover, it

asserted that the data it processed is only “personal information, which

can be collected for specified and legitimate purposes determined and

declared before, or as soon as reasonably practicable after collection ,

and later processed in a way compatible with such declared, specified

and legitimate purposes only.” 109  JuanHand argued that, aside from

the user’s acceptance of the terms and conditions in the pop -up

permissions, it considered, in good faith, the continuous use of its app

as the user’s express consent to the collection of personal

information. 110

JuanHand countered the contentions of the CID by alleging , first, that

it has already corrected the undisclosed permissions. 111  JuanHand

opined that , as regards the permission information claimed by the CID

to have been discovered through the Google Play Store and not the

JuanHand app itself, the “point of contention […] boils down to the

propriety of the format/manner upon which such permissions are to

be disclosed” since the “[p]ermission [i]nformation has already

prev ious ly existed, albeit in the Google Play Store and not in the OLA

itself.” 112  In any case, JuanHand emphasized that it has already revised

and addressed this particular issue by making the following changes:

33.1. Access to users’ calendar, location, contact list and social

networking profile have been removed and deleted from the

JuanHand OLA.


33.2. The Privacy Policy has been further revised, removing any

perceived Undisclosed Permissions to access users’ calendar,

location, contact list and social networking.

33.3. [ JuanHand ] reconfigured JuanHand OLA by providing

more visible pop -up prompts when there is an attempt to access

users’ personal information, subject to the user’s acceptance or

denial of such access. In case of the latter, no access or collection

will take place. These pop -up prompts effective even during user

registration and loan application. 113

In relation to this, JuanHand asserted that it similarly corrected and

revised the app to comply with the principles of transparency,

legitimate purpose, and proportionality. 114

Pertaining to the principle of transparency, JuanHand took into

consideration the findings of the CID and “[excluded] access to

calendar, location, contact list and social networking accounts of the

data subject” in its latest Privacy Policy. 115  Moreover, it reiterated that

it improved the prompts that will enable data subjects to modify their

permission or consent and ensured that the users can easily be

informed of the changes to the JuanHand app through the “What’s

New” feature. 116

As to the general privacy principle of legitimate purpose, JuanHand

argued that its processing of information was compatible with the

declared and specified purposes indicated for access to the user’s

contact list, which is: “(1) to speed up the application process, and (2)

to prevent criminals from stealing user’s money .” 117

In addition, JuanHand interposed that since the information is

personal information and not sensitive personal information, its

collection may still be subject to subsequent consent from the user s.118

JuanHand , however, “[conceded] that there were issues in the

operation and coding of its application, which failed to provide a

means to continue a loan application in cases where a user disagrees


to provide access to their contacts.” 119  Thus, to address the concerns of

the CID, it no longer request ed access to the user’s contact list in its

latest update of the app .120

As for the proportionality principle, JuanHand explained that :

[JuanHand ], in good faith, [was] of the belief that their

questioned action of requesting for the access of a user’s contact

list was in proportion to the purpose it declared.

[JuanHand ], in requesting for the access to the contact list of its

users, [was] hinged on the belief that it was a necessary means to

protect legitimate business interests and to serve the interests of

the user for credit approval.

Admitting that the purpose for which [ JuanHand ] requested for

the contact list may have been fulfilled by other means in a more

ideal scenario, the realities of the situation in the Philippines do

not make other options a reasonable means to achieve the

purpose sought to be addressed by [ JuanHand ]. 121

. . .

[T]he target market of the JuanHand application consists of the

individuals in the lower economic brackets. As such, these

realities were taken into consideration by [ JuanHand ] in its

decision to request for access to the user’s contact data. 122

Nevertheless, JuanHand acknowledged the concerns raised by the CID

and reiterated that it no longer requests for or uses the contact list of

its users. 123

Regarding the Loan -Related Transactions Circular , JuanHand stressed

that it interpreted the prohibition to access contacts as being qualified

by the statement “for use in debt collection or to harass in any way the

borrower or his/her contacts.” 124  It stated that it has never made use

of a user’s contact information to harass for debt collection .125  Instead ,

the information was merely used for purposes of identity verification,


credit scoring, and fraud prevention, and it was simply stored in its

system as a potential reference source. 126  In any case, it has now

removed its request to access and use its borrower s’ contacts. 127  The

supposed violations and concerns of the Commission , therefore, have

already been addressed. 128

JuanHand similarly revised its Service Agreement and remov ed the

contentious provisions raised by the CID to improve compliance with

the DPA and its issuances. 129

Lastly, JuanHand argued that its Corporate Officers and Directors

should not be held personally liable because they did not actively

participate in, nor by their own gross negligence, allow for the

commission of the crime. 130  As to the first category, it opined that i t

always acted in good faith when it executed the purported erroneous

acts. 131  It even acquired the advice of legal professionals to review the

legality of its documents and the process flows of the app since it

admits that its own interpretation of the DPA and its issuances,

particularly on OLAs, are inadequate. 132  As to the second category, it

asserted that assuming there was negligence, it did not amount to

“gross negligence” since JuanHand ma de efforts to comply with the

DPA and its issuances. 133

JuanHand prayed that the temporary ban be lifted and that it be

allowed to re -deploy the app to the public. 134

On 17 December 2021, JuanHand filed a Motion to Resolve the

imposition of the Temporary Ban on the Processing of Personal Data. 135

On 10 January 2022, it filed a Supplemental Motion to Resolve the

imposition of the Temporary Ban. 136


On 13 January 2022, the Commission issued a Resolution lifting the

Temporary Ban issued against JuanHand .137  Despite lifting the ban, the

Commission , in an Order dated 13 January 2022 , enjoined JuanHand

to address the issues it raised regarding the version 4.1.1, version 4.2.0,

its Privacy Manual, and its Security Incident Management Policy so

that it may fully comply with the DPA and the other issuances of the

Commission. 138  Thus, the Commission order ed the parties t o submit

their respective Memoranda within ten (10) days from the submission

of JuanHand’s proof of compliance to the mandated changes .139

On 28 February 2022, JuanHand filed its Compliance. 140  JuanHand

claimed that it only accesses its borrower s’ camera or photo gallery for

KYC, credit assessment, and fraud prevention at the beginning of loan

application processes. 141  It specified that both version 4.1.1 and version

4.2.0 of its app have been duly rectified to comply with Section 3(D)(3)

of the Loan -Related Transactions Circular on camera permissions. 142

Particularly, the app now contains prompts through its “Close Camera

Permission” feature informing its users when they may already turn

off or disallow permission to access their cameras or photo galleries. 143

Thus, upon uploading photos and successfully submitting their loan

applications, users may now deny camera access for the app. 144

Additionally, JuanHand submitted its rectified Privacy Manual that

includes organizational, physical, and technical measures. 145  It

provides for the procedure for appointing data privacy and

compliance officers, the conduct of annual privacy trainings, privacy

impact assessments, and review of data protection policies. 146  Physical

security measures such as storage, limitation of access, and modes of

transfer of personal data are included as well as technical security

measures involving encryption and authentication processes. 147  Lastly,

its submitted Privacy Manual discusses mechanism s in determining

the basis for lawful processing of personal data and mirrors the rights


of data subjects in accordance with Sections 12, 13, and 16 of the

DPA. 148  It also submitted its rectified Security Incident Management

Policy that complies with NPC Circular No. 16 -03 (Personal Data

Breach Management) in order to prevent or minimize the occurrence

of a personal data breach and assure the timely discover y of a security

incident. 149  It provides for an incident response procedure in case of

security incidents or breaches 150  and for a procedure that complies

with the requirements of personal data breach notification .151

On 10 March 2022, JuanHand filed its Memorandum. 152  The CID filed

its Memorandum on 16 March 2022. 153  Both parties reiterated the

arguments found in their respective pleadings.

### Issue

Whether JuanHand and its Corporate Officers and Directors

committed violations of the DPA and the Commission’s issuances that

warrant a recommendation for prosecution.

### Discussion

JuanHand ’s position mainly assert ed that it is no longer liable for

violations of the DPA and the Commission’s issuances since it already

incorporated and made changes to the app to align with the results of

the CID ’s investigation on undisclosed permissions:

There are no longer any ‘Undisclosed Permissions ’ in the

JuanHand OLA. Section 16 of the Data Privacy Act is not

violated. 154

. . .

[JuanHand has] already rectified and revised the [JuanHand]

OLA to comply with the principles of transparency, legitimate

purpose, and proportionality. 155


. . .

Thus, as it currently stands, the supposed violations by

[JuanHand ] and the concerns of the Honorable Commission have

already been addressed. 156

. . .

In any case, [JuanHand ’s] willingness to abide by all the

directives of this Honorable Commission is evident in the

rectifications made in the Service Agreement, the JuanHand OLA

itself, and the privacy policies. 157

. . .

Further, in [its] Compliance dated 28 February 2022, [ JuanHand ]

made the following rectifications pursuant to the Honorable

Commission’s Order dated 13 January 2022[.] 158

This argument is flawed. Rectification after the fact does not cure

violations that arose prior to the change s made . This was made clear

even in the Commission’s 13 January 2022 Order when it stated that :

Compliance with this Order shall not excuse [JuanHand] and its

responsible officers from any violations of the Data Privacy Act

of 2012 and its Implementing Rules and Regulations that may

have resulted from their previous actions before and during the

time the Temporary Ban was in place. 159

The Commission finds that JuanHand committed lapses in its actions

before and during the effectivity of the temporary ban. Nevertheless,

these lapses , even if taken together, are not sufficient to warrant a

recommendation for prosecution.

I.  JuanHand’s lapses in its actions result ed in a violation of

Section 25 of the DPA .

The root of the CID’s contentions stem med from the alleged

undisclosed permissions:


The capabilities of JuanHand’s system to read the borrower’s

calendar events plus confidential information, add or modify

calendar events, send email to guests without the owner’s

knowledge, read borrower’s contacts, collect data from contacts

and pinpoint the borrower’s approximate and precise location

through its network and GPS are all unknown to the prospective

borrower. The permission information for these capabilities is

not shown to the users thru [sic] prompts or permissions when

applying for a loan but was discovered by the Technical Team

from the google play store and not from the application itself.

Thus, the data subjects are uninformed that his or her

confidential personal information including that of his or her

contacts have been processed in violation of Section 16 of the DPA. 160

. . .

In the Fact-Finding Report, the CID said that the undisclosed

permissions in JuanHand’s Application also violated the

principles of transparency, legitimate purpose, and

proportionality, as described in Rule IV, Sections 17 and 18 of the

Implementing Rules and Regulations of the DPA[.] 161

. . .

JuanHand’s processing of personal information is in violation of

Sections 12 and 13 of the Data Privacy Act which requires consent

of the data subject prior to the processing. An undisclosed

permission did not acquire the consent of the data subject. Thus,

the processing of personal data by JuanHand did not adhere to

Sections 12 and 13 of the DPA, violating therefore Section 25 of the DPA being unauthorized processing of personal

information. 162

. . .

Moreover, without a valid consent, or authority under the DPA

and other existing laws, processing will be unauthorized in

violation of Section 25 of the Data Privacy Act of 2012. Where

information is used for purposes other than what the data subject

clearly agreed to, or otherwise authorized by law, the further

processing of the information may be considered processing for

unauthorized purpose. 163


JuanHand did not refute the results of the CID’s investigation

regarding its undisclosed permissions. Rather, to address this point, it

admitted that its app does “read the borrower’s calendar events and

add or modify calendar events.” 164  JuanHand’s arguments instead

attempted to address the conclusions the CID sought to derive from

these findings of fact by arguing that it considers the accessing and

modifying of its borrower’s calendar as “legitimate and proportional

to the purpose stated in the Service Agre ement. […] [t]herefore, [it]

consider[s] that when users give consent to the Service Agreement,

users are materially informed [of] the kind of personal information

[that] shall be processed in compliance with [S] ection 16(a) of the DPA

and have given consent to the above functions.” 165

Considering the foregoing, it is evident that JuanHand committed

lapses.

The results of the CID’s investigation on JuanHand’s Permission

Information demonstrated that the system can do the following:

1.  read the borrower’s calendar events plus confidential

information;

2.  add or modify calendar events;

3.  send email to guests without the owner’s knowledge;

4.  read borrower’s contacts;

5.  collect data from contacts; and

6.  pinpoint the borrower’s approximate and precise location

through its network and GPS. 166

Not all permissions, however, were indicated in the Service

Agreement, particularly the permission to access a borrower’s

calendar events and confidential information as well as read and

modify the calendar events. 167  This is an erroneous oversight because

“it is the Service Agreement that potential borrowers are asked to

consent to and is the one that governs the relationship between the

borrower and JuanHand.” 168  Moreover, as emphasized by the

Commission in its 12 August 2021 Order:


JuanHand does not have a clear understanding of the lawful

criteria for processing under the DPA that it is relying on. As

reflected in its Position Paper, JuanHand considers access to and

modification of a user’s calendar as legitimate and proportional

to the purpose stated in the Service Agreement. However,

JuanHand is unclear on which specific purpose it pertains to.

JuanHand subsequently states that ‘when users give consent to

the Service Agreement, users are materially informed [of] the

kind of personal information [that] shall be processed in

compliance with [S]ection 16(a) of the DPA and [users] have

given consent to the ab ove functions.’ This statement is, at best,

confusing.

The primary contract entered Into by JuanHand and its users is a

loan. When entering a loan, the borrower signifies consent to the

purposes necessary to deliver the services contemplated in the

contract, this necessarily includes the processing of relevant

personal information. JuanHand, in including the privacy

policies in its Service Agreement and in creating the revised

Privacy Policy, acknowledges that its main basis for processing

personal information is consent. In this case, however, for

matters where it did not request consent from its data subjects,

JuanHand erroneously attempts to fill in the gaps by

conveniently citing legitimate interest as its basis in processing

their personal information.

According to JuanHand, it considers accessing and modifying a

user’s calendar as legitimate and proportional to the purpose in

the Service Agreement[.]

. . .

In the next provision, JuanHand declares that users are

‘materially informed’ of the kind of personal information it

processes when users give consent[.]

. . .

The privacy provisions in the Service Agreement, however, do

not mention access to the user’s phone calendar. In fact, the

request for permission to access and modify the calendar is not

included among the disclosed permissions JuanHand requests

from its u sers, as presented in Annex 2 of the Position Paper. The

access and modification of the calendar that JuanHand claims to

be covered under its legitimate interest is not included in the

categories of personal information that will be collected and

processed , as set out in the Service Agreement. As a result, the

access and modification of the calendar could not have been

disclosed to the data subjects. JuanHand neither informed its

borrowers of the additional personal information that will be NPC SS 21 -006

processed nor acquired their consent to such processing. Having

failed to inform its borrowers of such processing, much less

acquired their consent, JuanHand cannot belatedly use

legitimate interest to cure this defect especially since its

borrowers could not have expected this at the time they gave

their consen t.169

Aside from this, the CID also pointed out that the clause in the Service

Agreement regarding publication is violative of the DPA and its

issuances. 170  Sections K(4)(c) and (d) of the Service Agreement provide:

c. After the repayment is overdue, [JuanHand] as the Facilitator

is entitled to disclose to the Investor the personal information of

the Borrower, and to or obtain by the Facilitator through this

Agreement and other lawful means and include the personal

in formation submitted by the Borrower or collected by

[JuanHand] into the blacklist of the [JuanHand] Website and the

national and local personal credit information systems. The

Facilitator is also entitled to share with any third parties the

personal inform ation of the Borrower, which was submitted by

the Borrower or collected by the Facilitator in public domain, so

that the Facilitator and the third parties can collect the overdue

amount and such personal information can be used for the

approval of other lo an applications made by the Borrower. All

the legal liabilities shall be borne by the Borrower and

[JuanHand] shall not take any responsibilities.

d. When the Borrower is overdue for payment, [JuanHand] may

publish the personal information of such user for the purpose

of collecting debt. [JuanHand] shall not be held liable .171

JuanHand contended that the limitation of liability does not pertain to

the DPA, but it is only connected to its publication in case of delinquent

users and where payment is overdue. 172  It argued that the contentious

provision should be read in conjunction with the provision of the

Service Agreement pertaining to disclosure in relation to credit

information systems. 173  The Commission previously pointed out that

the publication is accompanied by a categorical statement, thereby

putting into question its alleged non-limitation of liability:


The Commission understands that JuanHand’s disclosure of the

personal information of delinquent users to the [Credit

Information Corporation] is pursuant to Section K(4)(c) of the

Service Agreement[.]

. . .

However, Section K(4)(d) of the Service Agreement allows

JuanHand to ‘publish the personal information of such user for

the purpose of collecting debt ’. Further, JuanHand categorically

states that it ‘shall not be held liable ’ for such publication. 174

Lastly, while the temporary ban was in effect , the Commission

received several reports from JuanHand users who received various

messages from its Collection Department containing the DDL of the

app. 175  Upon investigation, the EnD was able to download the

JuanHand app through the provided DDL. 176  Thus, on 17 September

2021, the EnD sent a letter to JuanHand requiring it to explain the

foregoing incident. 177

On 08 October 2021, JuanHand responded to the EnD’s letter. 178  It

explained that the DDLs were inadvertently sent in an SMS and email

as part of an automatic process which transmits repayment reminders

to existing JuanHand users. 179  It reiterated this in its Memorandum,

stating that:

100.1. The dissemination of the DDL was done through

automatic, system -generated repayment reminder SMS and

emails , and therefore was done inadvertently, with no intention

to violate the Temporary Ban. The DDLs were inadvertently sent

through system -generated repayment reminders containing a

single hyperlink or DDL […], which automatically redirects users

to the lates t version of the JuanHand OLA, regardless of changes

and updates to the same.


100.2. Upon becoming aware of the incident, [JuanHand]

immediately made efforts to rectify the same. 180

Th us, the Commission finds that JuanHand violated Section 25 of the DPA or Unauthorized Processing of Personal or Sensitive Personal

Information .

Unauthorized Processing of Personal or Sensitive Personal

Information is committed when :

1.  The perpetrator processed the information of the data

subject;

2.  The information processed was personal information

or sensitive personal information; and

3.  The processing was done without the consent of the

data subject, or without being authorized under the

DPA or any existing law. 181

All three (3) requisites are present here. The circumstances when taken

together substantially demonstrate that JuanHand processed the

personal information of its data subjects, particularly their calendar

events, without their consent.

On the first requisite, JuanHand processed information of its data

subjects. [[laws/data-privacy-act-of-2012#section-3-definition-of-terms|Section 3 of the DPA]] defines processing as follows:

(j) Processing refers to any operation or any set of operations

performed upon personal information including, but not limited

to, the collection, recording, organization, storage, updating or

modification, retrieval, consultation, use, consolidation, bloc king,

erasure or destruction of data. 182

In its Position Paper dated 12 August 2021, JuanHand stated that it

“[does] also read the borrower’s calendar events and add or modify

calendar events.” 183  The first requisite of processing was admitted by

JuanHand.


As for the second requisite, the information that JuanHand processed

is personal information. Section 3 of the DPA defines personal

information:

(g) Personal information refers to any information whether

recorded in a material form or not, from which the identity of an

individual is apparent or can be reasonably and directly

ascertained by the entity holding the information, or when put

together with other information would directly and certainly

identify an individual. 184

In its Position Paper dated 12 August 2021, JuanHand admitted that it

considered the user’s calendar as a “ kind of personal information.” 185

Further, it stated that:

We consider that accessing and modifying user’s calendar is

legitimate and proportional to the purpose stated in the Service

Agreement for two reasons:

(i) Credit Analysis and Scoring: by accessing the calendar,

we seek to identify due dates of other loans or payment

obligations of the users to determine whether or not to

provide loan services, and if so, his/her credit limits;

(ii) Due Day Reminder: by adding due date to the users’

calendar, it would be easier for the users to apprehend the

due date and, thus, repayment obligation.

Therefore, we consider that when users give consent to the

Service Agreement, users are materially informed the kind of

personal information shall be processed in compliance with

section 16(a) of the DPA and have given consent to the above

functions. 186

As mentioned, JuanHand accessed and used the user’s calendar for

credit analysis and scoring and payment reminders. These information

allow it to “identify due dates of other loans or payment obligations of

the users.” 187  Clearly, t he identity of the borrower can be reasonably

and directly ascertained through the information contained in the

calendar. The calendar information , thus, is personal information

under the DPA.


As for the third requisite, JuanHand process ed personal information

without the consent of the data subjects or without lawful basis under

the DPA or any existing law .

The CID discussed in its FFR that :

After a thorough search, the CID Technical Team found

‘JuanHand’s Permission Information’ (Annex ‘B’) revealing that

JuanHand’s system, can do the following:

1.  read the borrower’s calendar events plus confidential

information;

2.  add or modify calendar events;

3.  send email to guests without the owner’s knowledge;

4.  read borrower’s contacts;

5.  collect data from contacts; and

6.  pinpoint the borrower’s approximate and precise

location through its network and GPS. 188

The CID, through its technical investigation, discovered that during

the time it conducted the investigation, JuanHand’s app was able to

utilize the abovementioned permissions. Apart from that, prior to the

CID’s downloading and installation of the app, t he permissions

required by the app were outlined in the Google Play Store: 189

• read calendar events plus confidential information;

• add or modify calendar events and send email to guests without

owner’s knowledge;

• read your contacts;

• approximate location (network-based); and

• precise location (GPS and network-based). 190

As previously discussed, however, JuanHand’s Service Agreement

does not indicate all of the abovementioned permissions outlined in

the Google Play Store and those discovered by the CID during its


technical investigation .191  The Service Agreement did not inform the

data subjects that it can and does access, read, and modify their

calendar events and other confidential information. 192

Thus, the Commission finds that JuanHand’s processing of personal

information was without consent of the data subjects.

The CID was able to prove, through its technical investigation, that

there were undisclosed permissions not mentioned in the Service

Agreement. This is a violation of the general privacy principle of

transparency, which  requires the Personal Information Controller

(PIC) to ensure that the data subject is aware of the nature, purpose,

and extent of the processing of his or her personal data. 193  The principle

of transparency similarly requires that these materials be easily

accessible and understandable by the data subjects and should be in

clear and plain language. 194  The requirement to use clear and plain

language means that information should be provided in as simple a

manner as possible. 195  In  NPC 19 -450, the Commission emphasized the

“clear and plain language ” requirement:

The requirement to use clear and plain language does not mean

using layman’s terms to substitute technical words at the risk of

not capturing the complex concepts they represent. Rather, this

requirement means that information should be provided in as

simple a manner as possible, avoiding sentence or language

structures that are complex. The information provided should

be concrete and definitive; it should not be phrased in abstract

or ambivalent terms or leave room for different interpretations

such as in the above -cited provision which uses the word ‘any’

several times, as well as wordings like ‘including but not limited

to’. 196

In NPC 19 -498, the Commission held that “vague, overbroad, and

confusing language cannot be said to comply with the requirements of

the transparency principle. ”197  Statements fail to satisfy the

transparency principle if data subjects are not informed of the nature,


purpose, and extent of the processing that the PIC is permitted to

undertake. 198  The Commission explained as follows:

This vague, overbroad, and confusing language cannot be said to

comply with the requirements of the transparency principle and

its objective of providing meaningful information to data

subjects to enable them to understand the purpose, scope,

nature, and extent of processing of their personal information .

Taken plainly, what Respondent obtained was blanket consent to

process the information they acquired from Complainant and not

informed consent to process specific information for a

specified and limited purpose .199

A PIC, therefore, should inform the data subject s that it will process

particular p ersonal information for a specific and limited purpose. 200

With these, it can be seen that JuanHand violated the principle of

transparency. To recall, “it is the Service Agreement that potential

borrowers are asked to consent to and is the one that governs the

relationship between the borrower and JuanHand.” 201  In failing to

include certain employed permissions in the Service Agreement,

JuanHand did not sufficiently inform its data subjects of its processing

pertaining to the undisclosed permissions in a manner that enables

them to understand the purpose, scope, nature, and extent of

processing of their personal information. 202

In effect, t his violation of the general privacy principle of transparency

result ed in a violation of Section 25 of the DPA. Since t he data subjects

were not informed in a way that they can properly understand the

specific nature, purpose, and extent of the processing the PIC is

permitted to undertake , t hey were not able to make an informed

decision regarding the processing of their personal information. Thus,

there can be no valid consent in JuanHand’s processing of their

personal information relating to the undisclosed permissions.


JuanHand, in its Position Paper, admitted that the undisclosed

permissions were being executed despite its glaring absence in the

Service Agreement :

[W]e do also read the borrower’s calendar events and add or

modify calendar events. We consider that accessing and

modifying user’s calendar is legitimate and proportional to the

purpose stated in the Service Agreement [.]

. . .

Therefore, we consider that when users give consent to the

Service Agreement, users are materially informed the kind of

personal information shall be processed in compliance with

section 16(a) of the DPA and have given consent to the above

functions .203

As previously discussed , JuanHand should have informed its data

subjects that it will process their personal information for a specific

and limited purpose. It cannot argue that its borrowers are materially

informed since it did not validly acquire its data subjects’ consent

specific to the nature, purpose, and extent of the particular processing

activity.

The Commission reminds PICs that regardless of the basis of

processing, the principle of transparency dictates that information

regarding the nature, pu rpose, and exten t of the processing of personal

information still has to be provided to the data subject.

Moreover, a perusal of JuanHand’s argument above shows that it

relie d on consent and contract for its processing. Nevertheless, it

attempted to argue that “ accessing and modifying user’s calendar is

legitimate and proportional to the purpose stated in the Service

Agreement.” 204  To recall, it stressed that there is more than one

allowable basis for processing in this case , such as consent, contract of

loan, and legitimate interest pursued as a lender .205  Therefore, it

alleged that it has pursued “legitimate interests and purposes” in

processing the personal information of its users. 206


Th e Commission stresses that legitimate interest cannot be used to

circumvent data subject rights. It cannot justify improper processing

that has already occurred on the basis of the lawful criteria of consent

or contract. Given that JuanHand relied on consent as its lawful criteria

for processing, then it must show and prove that it obtained proper

and specific consent.

This is not to say that legitimate interest cannot apply alongside

consent or contract.  Legitimate interest can apply in a contract or in a

processing related to consent if it can justify the processing of things

already agreed upon by the parties, which can be determined by the

type of contract entered into, the relationship of the parties, and other

similar circumstances. Thus,  legitimate interest can be used to fill in

gaps in the contract only if the processing involves something that the

data subject can reasonably expect from the terms stated in the

contract.

This is not the case for JuanHand since access and modification of a

borrower’ s calendar is not something that a user would reasonably

expect to fall under the terms stated in JuanHand’s Service Agreement,

particularly:

K. Privacy

. . .

2.  Source of information

. . .

b. In addition to the information provided to JuanHand by the

User voluntarily, User agrees that Juanhand and its partners to

collect and verify the User’s information, including, but not

limited to the following manner:

i. User’s information collected by Juanhand and its cooperating

party.

ii. User’s information authenticated by the third party.

iii. information relevant to such User collected by automatically

tracking by Juanhand based on the User’s behavior on this

Website.

iv. information related to personal communication (including,

but not limited to, contact list, geographical location, device

identification number, social networking profiles) provided or NPC SS 21 -006

authorized by the User, or communication information relating

to the activities and logging in by the User provided to Juanhand

by other User or third party, Juanhand can collect this

information in the User’s file.

v. Other information related to the use of Juanhand services by

the User.

vi. Juanhand will collect your Facebook platform information

through your authorization. Including but not limited to:

username, user ID, registered email, gender, etc. 207

To do something entirely different and not covered by the Service

Agreement is problematic and un fair since data subjects will be made

to believe that the processing will not go beyond the terms to which

they agreed; but in reality, the PIC crosses the boundary in processing

personal information.  Thus, JuanHand cannot use l egitimate interest

in the alternative to fill in the gaps of its contract.

Given the foregoing, JuanHand has no lawful basis under the DPA or

any existing laws to process the personal information of its data

subjects in relation to the undisclosed permissions.

Taking all the foregoing into consideration, JuanHand violated Section 25 of the DPA .

II.  Liability of responsible officers based on Section 34 of the DPA.

The DPA imposes criminal penalties on specific acts , which are

imposed by courts of law after the conduct of a criminal trial. 208  Upon

a finding of a violation, the Commission may recommend to the

Department of Justice the prosecution and imposition of penalties on

the violations enumerated under the DPA. 209  These unlawful acts

provided in Sections 25 to 32 are unauthorized processing of personal

or sensitive personal information, processing personal or sensitive

personal information for unauthorized purposes, accessing of

personal or sensitive personal information, unauthorized access or

intentional breach, imp roper disposal of personal or sensitive personal

information, concealment of security breaches involving sensitive

personal information, malicious disclosure, and unauthorized


disclosure. 210  If the PI C or Personal Information Processor (PIP) is a

juridical person, t he n the penalties are imposed on its responsible

officers. 211

Corporations and other juridical entities cannot be prosecuted for

crimes under Philippine law .212  It is an established principle in

criminal law that :

Only natural persons can be the active subject [the criminal]

because of the highly personal nature of the criminal

responsibility.

Since a felony is a punishable act or omission which produces or

tends to produce a change in the external world, it follows that

only a natural person can be the active subject [the criminal] of

a crime, because he alone by his act can set in motion a cause or

by his inaction can make possible the completion of a

developing modification in the external world .213

Specific to violations committed by a corporation, the Revised

Corporation Code provides  that:

Section 171. Liability of Directors, Trustees, Officers, or Other

Employees. If the offender is a corporation, the penalty may, at the

discretion of the court, be imposed upon such corporation

and/or upon its directors, trustees, stockholders, members,

officers, or employees responsible for the violation or

indispensable to its commission .214

Jurisprudence provides that corporations ha ve a separate and distinct

personality from its officers:

Bicol Gas is a corporation. As such, it is an entity separate and

distinct from the persons of its officers, directors, and

stockholders. It has been held, however, that corporate officers

or employees, through whose act, default or omission the


corporation commits a crime, may themselves be individually

held answerable for the crime .215

Thus, as held by the Supreme Court, “[a] corporation can act only

through its officers and agents, and where the business itself involves

a violation of the law, the correct rule is that all who participate in it

are liable. ”216  Certain special laws provide for the particular officers

who shall be held responsible for corporate crimes .217  In the DPA, this

is specified in Section 34.

Therefore, Section 34 supplies the gap in Sections 25 to 32 of the DPA

by specifying that the officers of erring corporations are the natural

persons that will be held responsible for such violations and will be

the accused in the criminal case that will be filed.

The Commission emphasizes that, for juridical entities, a violation of

Section 25 does not automatically result in a recommendation for

prosecution. Rather, there is a need to identify the proper responsible

officers that shall be the accused in the crimin al case. With this, the

standard for the identification of responsible officers is provided by

Section 34 of the DPA. Section 34, therefore, adds another layer for

violations of Sections 25 to 32 when juridical entities are involved.

Section 34 of the DP A explicitly states that a responsible officer can be

subject to the imposable penalties in two instances: (1) participation in

the commission of the crime , or (2) allowing the commission of the

violation through gross negligence:

Section 34. Extent of Liability. If the offender is a corporation,

partnership or any juridical person, the penalty shall be imposed

upon the responsible officers, as the case may be, who

participated in, or by their gross negligence , allowed the

commission of the crime. If the offender is a juridical person, the

court may suspend or revoke any of its rights under this Act. If

the offender is an alien, he or she shall, in addition to the

penalties herein prescribed, be deported withou t further

proceedings after serving the penalties presc ribed. If the offender

is a public official or employee and lie or she is found guilty of

acts penalized under Sections 27 and 28 of this Act, he or she

shall, in addition to the penalties prescribed herein, suffer


perpetual or temporary absolute disqualification from office, as

the case may be. 218

The Commission has previously expounded on an officer’s liability:

The DPA is clear, however, that the liability of the responsible

officers in cases where the offender is a corporation does not rely

on active participation alone. Gross negligence is explicitly stated

in the DPA as a ground for criminal liability. 219

In relation to this, the Commission stresses that the clause “who

participated in, or by their gross negligence” should be viewed in

relation to the acts of the responsible officers that reasonably cause d

the violation, without which the violation would not have occurred.

Ultimately, however, this shall be applied on a case -to -case basis.

Thus, t he Commission takes this opportunity to draw a distinction

between the different sections in Chapter VIII (Penalties) of the DPA,

namely Sections 25 to 32 and Section 34.

The evidence required for Sections 25 to 32 of the DPA is substantial

evidence demonstrating that all the elements of the respective

violations are present. Meanwhile, the evidence necessary to establish

Section 34 of the DPA is substantial evidence proving that the specific

responsible officers reasonably caused the violation by their

participation or allowed the commission of the violation through their

gross negligence.

III.  The case should be dismissed for lack of substantial

evidence supporting a recommendation for prosecution

based on Section 34 of the DPA.

The CID argued that the undisclosed permissions show that “there is

sufficient legal and factual basis” for the Commission to hold


JuanHand’s Corporate Officers and Directors , as the responsible

officers, liable .220  To further bolster its claim, it posited that:

First, Respondent Wefund admitted all the allegations in the

Fact-Finding Report. It in fact offered to rectify its shortcomings

identified in the Order and FFR and undertook to implement

immediate rectification and remedial actions. Finally, Wefund

warran ted that it shall also remain fully cooperative and

supportive with the NPC in the further investigation and will be

open to promptly rectify any issues and adopt any

recommendation made by the NPC.

Second, the responsible officers did not file any comment to the

Fact-Finding Report as ordered by the Commission. In Wefund’s

Position Paper, no defense was interposed as to why the

responsible officers should not be penalized if found guilty of the

viola tions of the DPA. 221

In arguing that the Corporate Officers and Directors of Juan Hand are

liable, t he CID discussed the abovementioned arguments to harp on

Section 34 which states that “liability shall be imposed upon the Board

of Directors, as responsible officers, who participated in, or by their

gross negligence, allowed the commission of the crime[.]” 222

In administrative proceedings, however, jurisprudence consistently

maintains that: “The burden to establish the charges rests upon the

complainant. […] The respondent is not even obliged to prove his

exception or defense .” 223

In line with this, the Commission held in NPC 19 -465 that:

[T]he Commission cannot recommend the criminal prosecution

of the responsible officers of [Respondent] based on the

weakness of their defense.

Ultimately, it is [Complainant ] that bears the burden of

proving the allegations in her Complaint with substantial

evidence. Jurisprudence is settled that if she ‘fail[s] to show in a

satisfactory manner the facts upon which [her] claims are


based, the [respondent is] not obliged to prove [its] exception

or defense.’ 224

Thus, the Commission stresses that, contrary to the CID’s argument,

the lack of any defense presented by JuanHand on possible violations

committed by its Corporate Officers and Directors is not enough basis

to recommend them for prosecution.

In any case, there is no evidence on record, despite the investigation

conducted and allegations made by the CID, that sufficiently

establish es in any way that JuanHand’s Corporate Officers and

Directors (1) participated in or (2) exercised gross negligence in

allowing the commission of the crime.

To reiterate, a recommendation for prosecution under Section 34

requires substantial evidence showing that the responsible officers

committed acts that reasonably caused the violation, without which

the violation would not have occurred, or allowed its commission

through their gross negligence.

In this case, there is nothing on record demonstrating that JuanHand’s

Corporate Officers and Directors either (1) participated in the violation

or (2) by their gross negligence, allowed the commission of the crime

in order to hold them liable based on Section 34 of the DPA . The lapses

pointed out are sufficient to demonstrate that JuanHand violated

Section 25 of the DPA. The lapses themselves do not, however,

automatically prove that the elements necessary to hold Corporate

Officers and Directors liable based on Section 34 of the DPA are

present. Given this, the Commission finds that the lapses in this case

are not tantamount to substantial evidence required to warrant a

recommenda tion for prosecution under Section 34 of the DPA.

There is no substantial evidence to prove that JuanHand’s Corporate

Officers and Directors participated in the violation. The term

“participated in ,” as found in Section 34 of the DPA, requires that the

responsible officers committed acts that reasonably caused the

violation, without which the violation would not have occurred. As

such, the instance of “participated in” contemplates a situation

wherein the officers and employees that will be recommended for


prosecution are “responsible” for and the root cause of the violation of

the DPA in such a way that if they had not committed certain acts, then

the violation would not have transpired. Examples of this instance

cover situations wherein the responsible officer directs the execution

of the act resulting in the violation or through his acts, reasonably

cause d the commission of the violation without which such violation

would not have occurred . Thus, a sense of causation is essential when

determining if the responsible officers may be held liable based on

participation .

Given the foregoing, the Commission finds that there is no substantial

evidence proving that JuanHand’s Corporate Officers and Directors

committed any acts that reasonably caused its violation of Section 25 of the DPA. In the absence of substantial evidence, JuanHand’s

Corporate Officers and Directors cannot be held liable based on

participation in Section 34 of the DPA.

As for gross negligence, the Commission finds that the second instance

of Section 34 is similarly not present in this case. It is settled that “he

who alleges has the burden of proving his allegation with the requisite

quantum of evidence.” 225  Absent substantial proof, an allegation of

gross negligence cannot be presumed. Here, there is no substantial

evidence on record demonstrating that JuanHand’s Corporate Officers

and Directors by their gross negligence , allowed the commission of the

crime.

The Supreme Court defines gross negligence as follows:

[G]ross negligence […] refers to negligence characterized by the

want of even slight care, or by acting or omitting to act in a

situation where there is a duty to act, not inadvertently but

wilfully and intentionally, with a conscious indifference to the

consequences, insofar as other persons may be affected. It is the

omission of that care that even inattentive and thoughtless men

never fail to give to their own property. It denotes a flagrant and

culpable refusal or unwillingness of a person to p erform a

duty. 226

The oversights committed by JuanHand do not demonstrate that its

Corporate Officers and Directors refused to perform their necessary

duties under the DPA. Moreover, the acts of JuanHand to rectify its


mistakes upon notification by the Commission show its willingness to

comply with its mandated duties.

Pertaining to the DDLs, after being alerted of the incident, JuanHand

immediately removed the DDLs from its repayment reminders and

ordered that the sent DDLs be inaccessible and deactivated. 227

Furthermore, it sent messages to its users that were able to use, access,

or download the app during the period of the temporary ban’s

effectivity, particularly stating that the app is “currently unavailable

for downloading in compliance [with the] Nation al Privacy

Commission’s order. If you have received Juan[H]and download links

before, please do not access it anymore.” 228

This was verified by the EnD when it declared that:

The alleged accessible links mentioned in the reports to the CID

included in the automated messages through the following links

are also no longer working, meaning, the mobile app is no

longer accessible through these links there were reported after

the effectivity of the temporary ban [.] 229

As for the app itself, JuanHand has revised it by (1) removing access

to users’ calendar, location, contact list and social networking profiles ;

(2) incorporating more visible pop -up prompts during the registration

and loan application procedure when there is an  attempt to access or

use its users’ personal information that would allow users to ask for or

modify the permissions that they have granted; and (3) adding a

“What’s New” feature that allows data subjects to be easily informed

of the changes in the app. 230

These were confirmed by the EnD in its assessment. It found that

versions 4.1.1 and 4.2.0 of the app are no longer functional and are now

unusable; rather, old users are prompted to update to the app’s latest

version 5.0.0. 231  Particularly, as regards the iOS version:


[W]hile there are still no prompts giving the user permission to

allow the application to access the phone’s contact list, it has an

option for manual entry of references. The iOS version now has

two options wherein users can input their contact references.

First, users can manually enter their contact references. Second,

users can choose their contact references from their contact list.

According to [JuanHand], this is solely for the purpose of

convenience of the users and the application cannot “read” the

entire contact lists of users.

. . .

[T]his claim was verified by EnD. In the generated iOS Privacy

Report, it was confirmed that the JuanHand OLA does not have

permission to access the users’ contacts .232

Further, it created a separate Privacy Policy excluding access to

calendar, location, contact list and social networking accounts of the

data subject. 233  Its Service Agreement, on the other hand, removed all

the alleged contentious provisions pointed out by the CID in order to

improve compliance with the DPA and its issuances. 234

As regards the alleged violations of the Loan -Related Transactions

Circular pointed out by the CID, JuanHand asserted that:

[I]n no instance has it ever used the contact information acquired

from the users’ contact list as a means of harassment in the

process of debt collection.

. . .

That said, in order to cooperate, comply, and address the

concerns of the CID, Respondent WeFund no longer requests for

access to the user’s contacts list. 235

The Commission takes this opportunity to clarify the Loan -Related

Transactions Circular, specifically Section 3(D)(4), which states that:

Access to contact details in whatever form, such as but not

limited to phone contact list or e -mail lists, the harvesting of


social media contacts, and/or copying or otherwise saving these

contacts for use in debt collection or to harass in any way the

borrower or his/her contacts, are prohibited. In all instances,

online lending apps must have a separate interface where

borrowe rs can provide character references and/or co -makers of

their own choosing. 236

The Commission emphasizes that the phrase “access to contact details

in whatever form” should be read in the context of the qualifying

phrase contained within the same paragraph, “for use in debt

collection or to harass in any way […] are prohibited.” 237  Thus, it is not

the collection of contacts nor its access per se that is prohibited,

especially since there are instances when the collection or processing

of contacts falls under lawful processing. Rather, what the Circular

strictly prohibits is the utilization of these contacts to unduly burden

borrowers when they ar e used for purposes of debt collection and

harassment.

The Loan -Related Transactions Circular similarly contains rules on

camera permissions. JuanHand has addressed the issues surrounding

camera permissions of both version 4.1.1 and version 4.2.0. 238  Through

the “Close Camera Permission” feature, users are now prompted that

they may turn off or disallow permission to access their cameras or

photo galleries upon uploading their pictures successfully and

submitting their loan application. 239  The EnD has validated that this

feature is present and functioning. 240

Lastly, it has now provided for organizational, physical, and technical

measures in both its revised Privacy Policy and Security Incident

Management Policy. 241  As confirmed by the EnD in its assessment,

these now align with the DPA and the Commission’s issuances. 242

The Commission notes that , in addition to JuanHand’s willingness to

comply with its Orders, its voluntary acts of changing key members of


its management team and legal counsel are inconsistent with gross

negligence .

JuanHand, in its Supplemental Motion to Resolve, stated that it has

now “initiated the appointment of a more senior and experienced legal

and compliance manager in the management team as the new data

privacy officer in due course, to better oversee the compliance and

protection of its users’ data privacy.” 243  The Commission considers the

efforts of JuanHand in diligently complying with its obligations as a

PIC by appointing more experienced members to its managerial team

in order to better protect the rights of its data subjects.

Moreover, the Commission recognizes its change in counsel as a badge

of its willingness to comply with the DPA and the Commission’s

issuances . JuanHand, through its former counsel, 244  attempted to

rectify the alleged errors pointed out by the CID by preparing and

attaching to its Position Paper a standalone Privacy Policy that was

independent from the Service Agreement and that complied with the

DPA. 245  Despite the rectifications made, the Commission was

unconvinced that there is no potential danger to data subjects, thus an

Order granting the temporary ban to preserve and protect the rights of

the data subjects was issued:

An analysis of JuanHand’s Position Paper, Service Agreement,

and revised Privacy Policy shows that the issuance of the

temporary ban is necessary to protect the rights of data subjects

for the following reasons: (1) JuanHand’s preparation and

submission of a ‘standalone and rectified Privacy Policy

independent from the Service Agreement’ does not necessarily

change the manner it processes personal data; (2) JuanHand’s

understanding and application of the criteria of lawful

processing personal data, as glean ed from its revised Privacy

Policy, is ambiguous; (3) JuanHand’s allegations in the Position

Paper are inconsistent with its Service Agreement and revised

Privacy Policy. 246

On 10 September 2021, JuanHand’s new counsel entered its

appearance. 247  Evidently, JuanHand, through its new counsel, was


able to properly address, to the satisfaction of the Commission, the

initial lapses discovered by the CID that resulted in the imposition of

the temporary ban. As a result, the Commission issued a Resolution

lifting the temporary ban. 248

Thus, taking into account the totality of the evidence and

circumstances, JuanHand clearly demonstrated that its dedication to

swiftly and substantially rectify its errors contradict the presence of

willful and conscious indifference. Thus, despite the lap ses present in

this case, it does not amount to gross negligence sufficient to

recommend JuanHand’s Corporate Officers and Directors for

prosecution based on Section 34 of the DPA.

Moreover, the Commission notes that the imposition of a temporary

ban against JuanHand would not automatically result in an eventual

recommendation for prosecution based on Section 34 of the DPA.

To recall, a temporary ban against JuanHand was granted on 12

August 2021 since all the requisite s for its issuance were satisfied .249

Nevertheless, the Commission eventually issued a Resolution on 13

January 2022 lifting the temporary ban. 250

The threshold for the issuance of a temporary ban is different from that

of a recommendation for prosecution. A temporary ban, being a

provisional remedy, is granted in order to prevent any potential harm

from arising as well as to deter any further harm t o data subjects from

proliferating. Thus, the existence of a clear and present potential harm

may result in the granting of a temporary ban. Its issuance, however,

is not definitive proof that warrants a recommendation for

prosecution. The Commission, in d etermining recommendation s for

prosecution, must still decide based on the totality of evidence

presented , since it is bound to adjudicate based on the following:


In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers

Section 3. Rendition of decision . The Decision of the Commission

shall resolve the issues on the basis of all the evidence presented

and its own consideration of the law. 251

Despite its investigation, the CID failed to present substantial evidence

with respect to the Corporate Officers and Directors of JuanHand to

support the allegations pertaining to Section 34 of the DPA . I t cannot

be assumed that JuanHand’s Corporate Officers and Directors can be

held liable based on Section 34 of the DPA simply because of their

position . Given the foregoing, the Commission is constrained to find

that there is no showing that JuanHand ’s Corporate Officers and

Directors participated in the violation nor allowed its commission by

their gross negligence . Without proof, JuanHand ’s Corporate Officers

and Directors cannot be recommend ed for prosecution under the DPA.

WHEREFORE, premises considered, this Commission resolves that

the case filed against Wefund Lending Corporation and its Corporate

Officers and Directors is hereby DISMISSED .

This is without prejudice to the filing of appropriate civil, criminal , or

administrative cases , if any, against Wefund Lending Corporation and

its Responsible Officers .

SO ORDERED.

City of Pasay, Philippines .

16  Ma y 2022 .

Sg d.

LEANDRO ANGELO Y. AGUIRRE

Deputy Privacy Commissioner

WE CONCUR:


In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers

Sgd.

JOHN HENRY D . NAGA

Privacy Commissioner

Sgd.

DUG CHRISTOPER B. MAH

Deputy Privacy Commissioner

Copy furnished:

Vasig Abarquez Lumauig Abarquez Puno

Counsel for Respondents

COMPLAINTS AND INVESTIGATION DIVISION

ENFORCEMENT DIVISION

GENERAL RECORDS UNIT

[^1]: Fact-Finding Report, 09 June 2021, at 1, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^2]: Id.

[^3]: Id. at 5.

[^4]: Id.

[^5]: Id.

[^6]: Id. at 1.

[^7]: Fact-Finding Report, 09 June 2021, at 2, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^8]: Technical Report, 17 May 2021, at 5 (Annex B), In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^9]: Fact-Finding Report, 09 June 2021, at 2, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022). Emphasis removed.

[^10]: Id. Emphasis removed.

[^11]: Id.

[^12]: Id.

[^13]: Id.

[^14]: Id.

[^15]: Fact-Finding Report, 09 June 2021, at 2, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^16]: Id.

[^17]: Id. at 3.

[^18]: Id.

[^19]: Id. at 3-4. Emphasis supplied; See Supplemental Report, 31 May 2021, Annex A (JuanHand User Agreement Web), In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^20]: Id. at 4-5.

[^21]: Fact-Finding Report, 09 June 2021, at 5, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^22]: Id. Emphasis supplied.

[^23]: An Act Protecting Individual Personal Information in Information and Communications Systems in the Government and the Private Sector, Creating for this purpose a National Privacy Commission, and For Other Purposes [Data Privacy Act of 2012], Republic Act No. 10173 § 16 (2012).

[^24]: Fact-Finding Report, 09 June 2021, at 6, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^25]: Id.

[^26]: Id. at 7.

[^27]: Id.

[^28]: Id.

[^29]: Id.

[^30]: Fact-Finding Report, 09 June 2021, at 7, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^31]: National Privacy Commission, Rules and Regulations Implementing the Data Privacy Act of 2012, Republic Act No. 10173, § 18 (2016).

[^32]: Fact-Finding Report, 09 June 2021, at 8, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^33]: Id. at 7.

[^34]: Id. at 8.

[^35]: Id. at 9.

[^36]: Id. at 10.

[^37]: Id.

[^38]: Fact-Finding Report, 09 June 2021, at 10, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^39]: Id. at 11.

[^40]: Id.

[^41]: Id.

[^42]: Id. at 13.

[^43]: Id. at 12.

[^44]: Fact-Finding Report, 09 June 2021, at 12, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^45]: Id. at 13.

[^46]: Id. at 15-16.

[^47]: Id. at 16.

[^48]: Order, 16 June 2021, at 1, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^49]: Id. at 2.

[^50]: Supplemental Fact-Finding Report, 05 July 2021, at 2, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^51]: JuanHand Letter, 02 August 2021, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^52]: Motion to Properly Serve Order with Motion to Admit Position Paper Ad Cautelam, 12 August 2021, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^53]: Position Paper, 12 August 2021, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^54]: Id. at 2.

[^55]: Id.

[^56]: Id. at 3.

[^57]: Id. at 3-4.

[^58]: Id. at 4.

[^59]: Position Paper, 12 August 2021, at 5, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022). Emphasis supplied.

[^60]: Id.

[^61]: Id. at 7.

[^62]: Id.

[^63]: Id. at 8.

[^64]: Id. at 10.

[^65]: Order, 12 August 2021, at 6-15, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^66]: Id. at 16.

[^67]: Id.

[^68]: Id.

[^69]: Order, 12 August 2021, at 9, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^70]: Comment to the Order and Temporary Ban dated 12 August 2021, 01 September 2021, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^71]: Id. at 1.

[^72]: Id. at 2.

[^73]: Id.

[^74]: Id. at 3.

[^75]: Comment to the Order and Temporary Ban dated 12 August 2021, 01 September 2021, at 3, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^76]: Id.

[^77]: Id. at 3-4.

[^78]: Id. at 4.

[^79]: Id.

[^80]: Id.

[^81]: Comment to the Order and Temporary Ban dated 12 August 2021, 01 September 2021, at 4, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^82]: Id. at 5.

[^83]: Id. at 7.

[^84]: Entry of Appearance with Motion to Admit [Supplemental Comment with Motion for Lifting of Temporary Ban], 10 September 2021, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^85]: Supplemental Comment with Motion for Lifting of Temporary Ban, 10 September 2021, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^86]: Enforcement Division Memorandum, 14 September 2021, at 1, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^87]: Id.

[^88]: Id. at 3.

[^89]: Enforcement Division Letter of Compliance with Order dated 12 August 2021 in NPC SS 21-006 entitled "In re: Wefund Lending Corporation (JuanHand)", 16 September 2021, at 1, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^90]: Id. at 2.

[^91]: Order, 17 September 2021, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^92]: Id. at 3.

[^93]: Id. at 3-4.

[^94]: Reply and Explanation to the National Privacy Commission Enforcement Division Letter dated 16 September 2021, 08 October 2021, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^95]: Id. at 2.

[^96]: Id. at 3.

[^97]: Enforcement Division Memorandum, 1 4 September 2021, at 1, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^98]: Reply and Explanation to the National Privacy Commission Enforcement Division Letter dated 16 September 2021, 08 October 2021, at 4, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^99]: Id. at 5.

[^100]: Id.

[^101]: Id. at 6. Emphasis removed.

[^102]: Comment on the Fact-Finding Report dated 09 June 2021, 11 October 2021, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^103]: Id. at 5.

[^104]: Id. at 6.

[^105]: Id. at 7. Emphasis supplied.

[^106]: Id.

[^107]: Id. at 8.

[^108]: Comment on the Fact-Finding Report dated 09 June 2021, 11 October 2021, at 8-9, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^109]: Id. at 9.

[^110]: Id. at 12.

[^111]: Id.

[^112]: Id. at 13.

[^113]: Comment on the Fact-Finding Report dated 09 June 2021, 11 October 2021, at 14, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^114]: Id. at 15.

[^115]: Id.

[^116]: Id. at 16.

[^117]: Id. at 17.

[^118]: Id.

[^119]: Id.

[^120]: Id. at 22.

[^121]: Id.

[^122]: Id.

[^123]: Id. at 23.

[^124]: Motion to Resolve, 17 December 2021, In re: Wefund Lending Corporation and its Responsible Officers, NPC SS 21-006, (NPC 2022).

[^125]: Supplemental Motion to Resolve, 10 January 2022, In re: Wefund Lending Corporation and its Responsible Officers, NPC SS 21-006, (NPC 2022).

[^126]: Resolution, 13 January 2022, at 6-7, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^127]: Order, 13 January 2022, at 9, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^128]: Id. at 10.

[^129]: Memorandum (for Respondents), 10 March 2022, at 5, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^130]: Compliance, 28 February 2022, at 3, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^131]: Id. at 2.

[^132]: Id.

[^133]: Id. at 3.

[^134]: Id.

[^135]: Id.

[^136]: Compliance, 28 February 2022, at 3, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^137]: Id. at 4.

[^138]: Id.

[^139]: Id. at 5.

[^140]: Memorandum (for Respondents), 10 March 2022, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^141]: Memorandum, 16 March 2022, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^142]: Memorandum (for Respondents), 10 March 2022, at 8, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^143]: Id. at 10.

[^144]: Memorandum, 16 March 2022, at 2, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022). Emphasis removed.

[^145]: Id. at 3.

[^146]: Id. at 7.

[^147]: Id.

[^148]: Order, 13 January 2022, at 10, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022). Emphasis supplied.

[^149]: Fact-Finding Report, 09 June 2021, at 4-5, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^150]: See Supplemental Report, 31 May 2021, Annex A (JuanHand User Agreement Web), In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^151]: Order, 12 August 2021, at 9, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^152]: See NPC Case No 19-498, 09 June 2020, at 8 (NPC 2020) (unreported).

[^153]: Rules and Regulations Implementing the Data Privacy Act of 2012, § 18.

[^154]: See JRG v. CXXX Lending Corporation, NPC Case No. 19-450, 09 June 2020, at 6, available at https://www.privacy.gov.ph/wp-content/uploads/2022/01/Decision_NPC-19-450-JRG-v.-CXXX.pdf (last accessed 30 May 2022).

[^155]: Id. Emphasis supplied.

[^156]: NPC Case No 19-498, 09 June 2020, at 8 (NPC 2020) (unreported).

[^157]: Id. Emphasis supplied.

[^158]: See id.

[^159]: Memorandum (for Respondents), 10 March 2022, at 19, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^160]: Id.

[^161]: National Privacy Commission, Guidelines on the Processing of Personal Data for Loan-Related Transactions, Circular No. 01, Series of 2020 [NPC Circ. No. 20-01], § 3 (D)(4) (28 January 2021).

[^162]: Id.

[^163]: Memorandum (for Respondents), 10 March 2022, at 20, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^164]: Id. at 20-21.

[^165]: Enforcement Division Enforcement Assessment Report, 28 April 2022, at 4, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^166]: Memorandum (for Respondents), 10 March 2022, at 21, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^167]: Enforcement Division Enforcement Assessment Report, 28 April 2022, at 2, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^168]: Supplemental Motion to Resolve, 10 January 2022, at 5, In re: Wefund Lending Corporation and its Responsible Officers, NPC SS 21-006, (NPC 2022).

[^169]: Entry of Appearance of the Former Counsel was on 10 August 2021.

[^170]: Position Paper, 12 August 2021, at 2, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No 21-006 (NPC 2022).

[^171]: Order, 12 August 2021, at 7, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^172]: Entry of Appearance with Motion to Admit [Supplemental Comment with Motion for Lifting of Temporary Ban], at 1, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^173]: Resolution, 13 January 2022, at 6, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^174]: Order, 12 August 2021, at 6-15, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^175]: Resolution, 13 January 2022, at 6, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^176]: In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, Section 3. Rendition of decision. The Decision of the Commission shall resolve the issues on the basis of all the evidence presented and its own consideration of the law. National Privacy Commission, 2021 Rules of Procedure of the National Privacy Commission [NPC 2021 Rules of Procedure], rule VIII, § 3 (28 January 2021). Emphasis supplied.

[^177]: Memorandum, 16 March 2022, at 9, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022); See Supplementary Fact-Finding Report (with Application for Issuance of Temporary Ban on the Processing of Personal Data), 05 July 2021, at 2-3, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^178]: Memorandum, 16 March 2022, at 9, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^179]: Id.

[^180]: National Bureau of Investigation v. Conrado M. Najera, G.R. No. 237522 (2020). Emphasis supplied.

[^181]: [[decisions/2022/npc-19-465-gjj-v-easy-peso|NPC 19-465]], 03 March 2022, at 10 (NPC 2022) (unreported). Emphasis supplied.

[^182]: Reply and Explanation to the National Privacy Commission Enforcement Division Letter dated 16 September 2021, 08 October 2021, at 4, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^183]: Id. at 6. Emphasis removed.

[^184]: Enforcement Division Memorandum, 03 November 2021, at 3, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022). Emphasis supplied.

[^185]: Memorandum (for Respondents), 10 March 2022, at 9 & 13, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^186]: Enforcement Division Enforcement Assessment Report, 28 April 2022, at 3, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^187]: Enforcement Division Letter of Compliance with Order dated 12 August 2021 in NPC SS 21-006 entitled "In re: Wefund Lending Corporation (JuanHand)", 16 September 2021, at 2, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^188]: Id.

[^189]: Id.

[^190]: Id. Emphasis supplied.

[^191]: See Supplemental Report, 31 May 2021, Annex A (JuanHand User Agreement Web), In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^192]: See id.

[^193]: Tacis v. Shields Security Services, Inc., G.R. No. 234575 (2021).

[^194]: Securities and Exchange Commissioner v. Commission on Audit, G.R. No. 252198 (2021). Emphasis supplied.

[^195]: Memorandum (for Respondents), 10 March 2022, at 8, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^196]: Id.

[^197]: Id.

[^198]: Id. Emphasis supplied.

[^199]: Memorandum (for Respondents), 10 March 2022, at 9 & 13, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^200]: Memorandum (for Respondents), 10 March 2022, at 12, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^201]: Id. at 17.

[^202]: Id. at 15.

[^203]: Id.

[^204]: Supplemental Report, 31 May 2021, Annex A (JuanHand User Agreement Web) at 9, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022). Emphasis supplied.

[^205]: Data Privacy Act of 2012, § 34. Emphasis supplied.

[^206]: In Re: FLI Operating ABC Online Lending Application, NPC 19-910, 17 December 2020, at 35, available at https://www.privacy.gov.ph/wp-content/uploads/2021/02/NPC-19-910-In-re-FLI-Decision-LYA-Final-pseudonymized-17Dec2020-.pdf (last accessed 30 May 2022).

[^207]: [[decisions/2021/npc-19-134-vvc-v-cjb|NPC 19-134]], 10 December 2021, at 12 (NPC 2021) (unreported).

[^208]: Data Privacy Act of 2012, § 3 (j).

[^209]: Position Paper, 12 August 2021, at 5, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022). Emphasis supplied.

[^210]: Id.

[^211]: Id.

[^212]: Data Privacy Act of 2012, § 3 (g).

[^213]: Position Paper, 12 August 2021, at 5, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^214]: Id.

[^215]: Fact-Finding Report, 09 June 2021, at 5, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022). Emphasis supplied.

[^216]: Technical Report, 17 May 2021, at 5 (Annex B), In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022).

[^217]: See People v. Tan Boon Kong, G.R. L-35262 (1930).

[^218]: Luis B. Reyes, The Revised Penal Code, Criminal Law, Book 1 Articles 1-113 505 (2012). Emphasis removed. Emphasis supplied.

[^219]: An Act Providing for the Revised Corporation Code of the Philippines [Revised Corporation Code], Republic Act No. 11232, §171 (2019). Emphasis supplied.

[^220]: Espiritu Jr. v. Petron Corporation, G.R. No. 170891 (2009). Emphasis supplied.

[^221]: People v. Tan Boon Kong, G.R. L-35262 (1930).

[^222]: Jose R. Sundiang, Sr. & Timoteo B. Aquino, Reviewer on Commercial Law 60 (2019).

[^223]: National Privacy Commission, Rules and Regulations Implementing the Data Privacy Act of 2012, Republic Act No. 10173, § 18 (2016).

[^224]: Rules and Regulations Implementing the Data Privacy Act of 2012, § 18.

[^225]: Memorandum, 16 March 2022, at 2, In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers, NPC SS Case No. 21-006 (NPC 2022). Emphasis removed.