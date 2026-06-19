---
title: "NPC SS 21-008: Populus Lending Corporation (Pesopop) and its Responsible Officers"
description: "Sua sponte investigation against online lending application operator for unauthorized processing of personal data; found liable and recommended for prosecution."
aliases:
  - "NPC SS 21-008"
  - "npc ss 21-008"
  - "Populus Lending Corporation (Pesopop)"
  - "populus lending corporation (pesopop)"
tags:
  - "decision"
  - "type/decision"
  - "year/2021"
  - "npc-case"
  - "Unauthorized Processing (Section 25)"
  - "Incurring Criminal Liability"
  - "Gross Negligence"
  - "Consent"
  - "Online Lending Application"
  - "Legitimate Purpose"
  - "General Privacy Principles"
date: "2023-09-26"
draft: false
---

## Source

- Reference: NPC SS 21-008
- Official PDF: http://privacy.gov.ph/wp-content/uploads/2024/09/NPC-SS-21-008-2023.09.26-O.pdf
- Source page: http://privacy.gov.ph/decisions-2/
- Issue date: September 26, 2023
- Published on NPC site: September 21, 2024
- Pages: 59

## Source Tags

- Unauthorized Processing (Section 25)
- Incurring Criminal Liability
- Gross Negligence
- Consent
- Online Lending Application
- Legitimate Purpose
- General Privacy Principles

## Decision Text

IN RE: POPULUS LENDING CORPORATION (PESOPOP)

AND ITS RESPONSIBLE OFFICERS

INITIATED AS A SUA SPONTE NPC INVESTIGATION ON THE POSSIBLE DATA PRIVACY VIOLATIONS COMMITTED BY POPULUS LENDING CORPORATION (PESOPOP)

x----------------------------------------------------x

AGUIRRE, D.P.C.;

Before this Commission is a Fact-Finding Report with Application for the Issuance of a Temporary Ban on the Processing of Personal Data (FFR) dated 10 June 2021 against Populus Lending Corporation (Pesopop), the operator of the online lending application, Pesopop, and its responsible officers.

The Complaints and Investigation Division (CID) of the National Privacy Commission (NPC), pursuant to its power to conduct *sua sponte* investigations, filed an FFR against Pesopop. The FFR alleged that Pesopop committed violations of Sections 11, 16, and 25 of Republic Act No. 10173 or the Data Privacy Act of 2012 (DPA) and Section 3(D)(4) of NPC Circular 20-01 or the Guidelines on the Processing of Personal Data for Loan-Related Transactions (Loan-Related Transactions Circular).[^1] This concludes the *sua sponte* investigation conducted by the NPC.

### Facts

On 10 June 2021, the CID submitted its FFR against Pesopop following numerous reports of continuing privacy violations committed by several online lending applications (OLAs).[^2] The CID initiated a *sua sponte* investigation against Pesopop pursuant to Section 7(b) of the DPA that mandates the NPC to institute investigations in cases it deems appropriate, and NPC Circular 21-01 (2021 Rules of Procedure) that permits the NPC to initiate *sua sponte* investigations and file complaints for DPA violations.[^3] The FFR serves as the complaint, with the CID as the Nominal Complainant, in *sua sponte* investigations.[^4]

On 14 May 2021, the CID downloaded Pesopop (version 1.5.1) from the Google Play Store on an Android device and simulated the registration process.[^5]

Upon opening the Pesopop application (app), the user must provide a mobile number as the login credential.[^6] Once the user has logged in, a pop-up will appear with the following statement:

> Access permission – In order to check your credit score, you must grant permission to access Storage, Phone State, Contacts and Location info. Without these information, you can't use Pesopop.[^7]

To proceed, the user must click on the "Setting" button.[^8] The next pop-up messages will request access to the following: (1) device's location; (2) device's photos, media, and files; (3) contacts stored on the device; and (4) allow the app to make and manage phone calls.[^9] Each pop-up message gives the user an option to select either "DENY" or "ALLOW."[^10]

When the user clicks "DENY," he or she will be taken back to the previous "Access Permission" pop-up message.[^11] On the other hand, when the user selects "ALLOW," the user will be directed to the Main Screen, where he or she can proceed to the loan processing screen within the app.[^12]

The CID stated that the request for access to the phone contacts list will appear before the loan application process starts.[^13] The CID found that the loan application will not proceed to the next step without giving access to the entire phone contacts list.[^14] It added that there was no manual way of entering a character reference's phone number.[^15]

When the CID examined the source code of the app, it showed that the app utilized the Android software development kit (SDK) that provides coding for contacts retrieval, wherein an application will have the ability to collect data from contacts.[^16] The "AndroidManifest.xml" file explicitly contained a contacts permissions line ("android.permission.READ_CONTACTS").[^17] The CID explained that when this is enabled, it gives the app permission to read the user's contacts data.[^18]

The CID also stated that it was "unable to locate the Terms of Service or Loan Guarantee Agreement of Pesopop from the application, or from their website."[^19] Upon checking Pesopop's website, the CID, however, found Pesopop's Privacy Policy which stated the personal data collected and the purpose for which the collected information will be used:

**The Information We Collect**

To our beloved customer, to avoid fraud. When you sign up for Pesopop account, in addition to your login username and password, we will also ask for your **name, email address, birthday, gender**. Need your authorization to agree to provided **phone book, camera, internet, location, list of your applications and any other information**.

We also need to collect your contact information. **We will request the "Read Contacts" permission. If you agree to the authorization, we will scan and upload the contact list information to https://api.pesopop.com:18062** using the most secure data transfer protocol (HTTPS). We will store your personal information through DES and AES encryption. Storage time will not exceed your usage time.

The data is used only for the credit review process and will not be shared with third-party organizations without your permission. We are committed to encrypting the data and ensuring the security of the information. You click on the check the box below to indicate that you are fully aware of and agree to the application. Please feel free to use. If you do not agree to the authorization, the application will stop working and will not be able to serve you. Thank you for your understanding and cooperation.

If you do not have a successful loan, the information you leave will not be leaked, and the information you provide will only be used for loan review purposes, and the information will never be used for other purposes. **If you do not repay during the repayment period, we have the right to access and use your personal contact information, including FB, Instagram, Google+, etc.**

**Pesopop will Collect and Use of Information**

These clauses explain how we will use and share your information. By using the Services, you agree that we and members of Pesopop shall use Customer Information in accordance with such clauses.

Pesopop will collect your personally identifiable information when you register a Pesopop account, use other Pesopop products or services, access Pesopop webpages, or participate in promotional or prize winning games. Pesopop also collects personally identifiable information from our business partners. When you register a Pesopop account, we will ask for your name, birthday and gender, in addition to your email address. Once you are successfully registered with Pesopop, we will be able to identify you when you log in to the server.

**Information Collected by Third Parties**

Pesopop may allow third parties, including advertising partners, to display advertisements on the APP. These companies may use tracking technologies, including cookies, to collect information about users of the APP who view or interact with these advertisements. Pesopop does not provide Personally Identifiable Information to these third parties.

**Sharing Your Personally Identifiable Information**

Pesopop may share your Personally Identifiable Information (including, without limitation, your financial account information and social security number) with Payment Partners with whom Pesopop has a business relationship.

Any third parties with whom Pesopop shares Personally Identifiable Information may have their own policies which describe how they use and disclose your information. Those policies will govern the use, handling, and disclosure of your information once Pesopop has transferred or shared it with those third parties as described in this Policy or the Pesopop Terms and Conditions.

Pesopop will disclose your Personally Identifiable Information in response to a subpoena or similar investigative demand, a court order, or a request for cooperation from a law enforcement agency or other government agency; to establish or exercise our legal rights; to defend against legal claims; or as otherwise required by law. Pesopop will disclose your Personally Identifiable Information when Pesopop believes disclosure is necessary to investigate, prevent, or take action regarding illegal activity, suspected fraud, or other wrongdoing; to protect and defend the rights, property, or safety of Pesopop's parent company, its employees, its website users, or others; or to enforce the Terms and Conditions or other agreements or policies.

In addition, Pesopop may transfer Personally Identifiable Information to an entity acquiring all or substantially all of its parent company's stock or assets.[^20]

Based on the foregoing, the CID argued that Pesopop violated Sections 11, 16, and 25 of the DPA and Section 3(D)(4) of the Loan-Related Transactions Circular.[^21]

First, the CID contended that Pesopop's processing of personal information does not adhere to the general privacy principles of transparency, legitimate purpose, and proportionality.[^22]

The CID stated that pursuant to the transparency principle, a data subject must be aware of the nature, purpose, and extent of processing of their personal data, including the risks and safeguards involved, the identity of the personal information controller (PIC), their rights as a data subject, and how these can be exercised.[^23] It elaborated that any information and communication relating to the processing of personal data should be accessible and easy to understand, using clear and plain language.[^24] It also explained that this is commonly done through a privacy notice or privacy policy.[^25]

The CID argued that Pesopop's Privacy Policy failed to "sufficiently and clearly inform the data subject of the extent of the processing of his/her personal data and how he/she can exercise his/her rights as a data subject."[^26]

Here, the Pesopop Privacy Policy's multiple declarations, "to avoid fraud"; "The data is used only for the credit review process and will not be shared with third-party organizations without your permission"; and "If you do not repay during the repayment period, we have the right to access and use the (sic) your personal contact information, including FB, Instagram, Google+, etc.", are contradictory phrases that do not conform with the general privacy of transparency.[^27]

On the legitimate purpose principle, the CID elaborated that the processing of information under the DPA must be compatible with a declared and specified purpose which must not be contrary to law, morals, or public policy.[^28] The CID explained that this principle is adhered to when there exists a lawful criterion to process personal data, such that the processing is grounded on at least one of the criteria provided under Sections 12 and 13 of the DPA.[^29]

According to the CID, the access, retention, and storage of a data subject's phone contacts are considered processing activities under the DPA, and "as such, it needs to have legitimate purpose as provided by Sections 12 and 13 of the DPA."[^30] Further, where consent is the basis of the processing, expressed consent must be freely given, specific, informed, and indication of will.[^31] Thus, for consent to be considered valid, it should be informed consent, where the information provided is accessible, clear, and easily understood.[^32] The CID elaborated that bundled consent does not meet the criteria for specific consent.[^33]

Further, where consent is the basis for processing, data subjects can object to the processing or withdraw consent.[^34]

The CID argued that Pesopop's Privacy Policy is written and presented in such a way that the data subject is not given an opportunity to make an informed choice:

> The Privacy Policy states that to avoid fraud, Pesopop "will scan and upload the contact list information… "; "will store your personal information …."; and that in case of non-payment of debt: "we have the right to access and use your personal contact information, including FB, Instagram, Google+, etc."
>
> Pesopop's Privacy Policy initially states that the data is used only for the credit review process and will not be shared with third-party organizations without the user's permission. However, a fine reading of the said policy shows that if the user, once he/she fails to repay during the repayment period, also consents or gives Pesopop the right to access and use the user's personal contact information, including FB, Instagram, Google+, etc. The stored personal information, including the phone contact list, are not only used to know the customer for credit review, but it will be weaponized later on for debt collection if the need arises.[^35]

The CID stressed that for data subjects to avail of the services of Pesopop, "they have no choice but to accept all the terms and conditions provided by [Pesopop] and give consent for all the purposes for which [Pesopop] intends to use the personal data"[^36] because otherwise, the data subject cannot obtain a loan. The CID argued that the consent was not freely given and did not serve as an indication of will of the data subjects.[^37] Thus, consent was not validly acquired.[^38]

Further, the CID saw no other reason for Pesopop to store the data subject's contacts list throughout the duration of the loan agreement other than for use in debt collection.[^39] The CID stated that Pesopop's Privacy Policy provides that "if you do not repay during the repayment period, we have the right to access and use your personal contact information, including FB, Instagram, Google+, etc."[^40]

Therefore, the CID asserted that Pesopop's processing of the data subjects' personal data was unauthorized because it did not have lawful basis to store the data subjects' phone contacts list and failed to validly acquire the data subjects' consent.[^41]

The CID further asserted that Pesopop's requirement that users grant Pesopop permission to access their phone contacts violates the principle of proportionality.[^42] The CID explained that it is "excessive and unnecessary in fulfilling its purpose of loan or debt collection, in the event that the information provided in the credit agreement is false, invalid or otherwise not responsive to its collection attempts."[^43]

Second, the CID asserted that Pesopop's requirement to grant it the "permission to access several phone capabilities, such as contacts, photos, media and files, in order to successfully install, register, and avail of its loan facilities, and failing to provide a separate interface for a user to provide character references or co-makers of his own choosing" is in violation of Section 3(D)(4) of the Loan-Related Transactions Circular.[^44] According to the CID, it is explicit in the Loan-Related Transactions Circular that processing of phone contacts list for use in debt collection is strictly prohibited.[^45] Further, it argued that "in all instances, online lending apps must have a separate interface where borrowers can provide character references and/or co-makers to their loan application, of their own choosing."[^46]

The CID reiterated that "Pesopop's processing of personal data does not adhere to the [general] privacy principles of transparency, legitimate purpose, and proportionality."[^47] The CID reiterated that the access, use, and storage of the phone contact list finds no legitimate basis under the DPA.[^48] Thus, there is unauthorized processing under Section 25 of the DPA.[^49]

The CID further argued that since Pesopop is a corporation, "it is its board of directors who decides and should have the duty of diligence."[^50] Thus, according to CID, "liability should fall upon the Board of Directors, as responsible officers, who by their gross negligence, allowed the commission of violation of the DPA."[^51]

Finally, the CID interposed that there is substantial evidence to warrant the issuance of a temporary ban on the processing of personal data against Pesopop through its app:

> From the discussion above, it was shown that Pesopop's processing of personal data is without adherence to the Data Privacy Principles enshrined in the DPA. It collects personal data without clearly informing the data subject the extent by which it will use the personal data. It also has no legitimate purpose from which it can anchor its personal data processing, particularly its storage and use of phone contacts, as free and informed consent was not validly acquired and there is no other basis in law. It likewise collects and processes more personal data in relation for the purposes it has expressed in its Privacy Policy.
>
> Further, there is sufficient information to support that Pesopop has the ability to access, store, and copy phone contact lists of its borrowers and utilizes that stored data for use in debt collection or to harass its borrowers, in direct violation of the issuance of this Commission in NPC Circular 20-01, Section 3 (D) (4).
>
> Hence, the issuance of a Temporary Ban on Pesopop is crucial to preserve and protect the rights of the data subject from further processing.[^52]

On 16 June 2021, the Commission issued an Order suspending the complaint proceedings until the resolution of the application for the issuance of a temporary ban.[^53] It directed Pesopop to submit a position paper on the application for the issuance of a temporary ban within ten (10) days from its receipt of the Order.[^54]

On 23 June 2021, the Commission attempted to personally serve the Order to Pesopop's office address.[^55] It was reported, however, that Pesopop had already moved out.[^56]

On 24 June 2021, the Commission served the Order by email to Pesopop's email address available on its official website.[^57] Thus, Pesopop had until 04 July 2021 to file its position paper.[^58] As of 12 August 2021, the Commission did not receive any position paper from Pesopop.[^59]

On 05 July 2021, the CID submitted a Supplemental Fact-Finding Report with Application for Issuance of Temporary Ban on the Processing of Personal Data, impleading specific responsible officers of Pesopop, namely RCJ, FLB, JIS, MM, and WL (collectively, individual respondents), in their official capacities as responsible officers of Pesopop in line with Section 34 of the DPA.[^60]

On 12 August 2021, the Commission issued an Order granting the application for the issuance of a temporary ban against Pesopop given that all the requisites for granting a temporary ban were satisfied:

> WHEREFORE, premises considered, this Commission GRANTS the Application for Temporary Ban on the processing of personal data filed by the Complaints and Investigation Division of the National Privacy Commission. A **TEMPORARY BAN ON PROCESSING OF PERSONAL DATA** is hereby issued against Respondent Populus Lending Corporation, as the operator of the online lending application, Pesopop.
>
> Further, pursuant to the ORDER FOR TEMPORARY BAN, Respondent Populus Lending Corporation shall:
>
> 1. Immediately take down its online lending application, Pesopop, to ensure that it is no longer available for download, installation or use by data subjects; and
>
> 2. Stop personal data processing activities, including those activities outsourced to third parties, where the processing operations involves use of information from the phonebook, directory, and contact list of data subjects, disclosure of false or unwarranted information, and other unduly intrusive personal data processing methods.
>
> This TEMPORARY BAN ON THE PROCESSING OF PERSONAL DATA shall remain in effect until the final resolution of the sua sponte investigation against Respondent and its responsible officers.
>
> . . .
>
> Furthermore, Respondent Populus Lending Corporation and its responsible officers are ORDERED, within ten (10) days from receipt of this Order, to file a COMMENT on the allegations in the attached Fact-Finding Report, pursuant to Section 6 of Rule X of NPC Circular No. 2021-01 (2021 NPC Rules of Procedure).[^61]

On 03 September 2021, Pesopop, through its counsel Zosa & Quijano Law Offices, submitted its Notice of Entry of Appearance with Motion for Reconsideration.[^62] The individual respondents also manifested that they are adopting the Motion as their comment in compliance with the Order to comment dated 12 August 2021.[^63]

In its Motion for Reconsideration, Pesopop argued that the Order granting the temporary ban "is not warranted [sic] and issued with grave abuse of discretion amounting to lack or excess of jurisdiction for having been issued without authority and in violation of Sec[tion] 3, Rule 9 of the 2021 NPC Rules of Procedure."[^64] It contended that the second and third requisites for the issuance of a temporary ban were absent.[^65] Pesopop stated that there was no mention in the assailed Order that the required motion has been filed to warrant the application.[^66] It further stated that the NPC does not have *motu proprio* authority to apply for a temporary ban because it cannot post the necessary bond required and the exemption pertains only to the payment of filing fees and not to the posting of the required bond.[^67]

Alternatively, Pesopop asserted that assuming the temporary ban was valid, the complete takedown of its application is "not warranted on the ground that the temporary ban only warrants a ban on the processing of personal data."[^68] It explained that a complete takedown [sic] of the application is prejudicial because that would include taking down areas not related to the processing of personal data.[^69]

Further, Pesopop explained that the inclusion of a request for the phone contacts list upon registration was "purely unintentional and a result of an inadvertent and honest mistake:"

> In this case, although respondent PesoPop requested for the inclusion of the phone contact list, the said list was limited to include five (5) persons from the contact list as character reference only. In other words, respondent PesoPop does not have access to the entire the [sic] phone contact list of its clients and/or its potential users.
>
> Moreover, although it was initially stated in the terms and conditions of use that, "If you do not repay during the repayment period, we have the right to access and use the [sic] your personal contact information, including FB, Instagram and Google+, etc.", respondent PesoPop never requested any of its clients to disclose their FB, Instagram and Google+ in the collection of debts or for whatever purpose.
>
> Therefore, respondents respectfully assert that although there could have been a mistake in the data terms and privacy of respondent PesoPop, the latter in good faith did not use and/or was able to obtain excess information considering that the request for access of the phone contact list was limited to only five (5) numbers solely used for character reference and that respondent PesoPop follows a strict collection policy without the use of harassment and/or excess of information.[^70]

Pesopop asserted that all elements of valid consent are present in this case.[^71] It argued that the consent it obtained from its clients were not bundled and were voluntarily requested as many times as the access to the information was requested.[^72] It stressed that its clients and potential users will "always have a choice in giving consent to the gathering, access, processing and storage of their personal data."[^73]

Citing the CID's technical and supplemental reports, Pesopop argued that users of the app were asked multiple requests for access to information.[^74] Absent the grant of access to such information, the users would not have any chance to provide information, use, or even obtain a loan.[^75]

Pesopop added that this is its first offense for a data privacy violation.[^76] It explained that it "has not received any data privacy complaint from any other party other than the instant case."[^77] For this purpose, Pesopop undertook "to immediately make a complete and thorough review and amendment of its existing data privacy terms and conditions and will revise the same to conform to the DPA."[^78]

Lastly, Pesopop argued that the individual respondents did not actively participate in the processing of personal data of Pesopop's clients.[^79] It asserted that there was no allegation and proof in the complaint that the individual respondents acted in gross negligence, fraud, bad faith, and malice.[^80]

On 17 September 2021, the Commission directed Pesopop and the individual respondents to appear for a clarificatory hearing on 28 September 2021.[^81]

On 28 September 2021, the Commission conducted the Clarificatory Hearing.[^82] As a result of the Clarificatory Hearing, the Commission directed Pesopop and the individual respondents to submit the following information and documents:

1. Revised Privacy Policy of Pesopop;
2. Revised Terms and Conditions or Terms of Service of Pesopop;
3. Revised Pesopop application;
4. Company Profile and a discussion of the business model of the corporation;
5. An explanation of the discrepancy between Counsel's representations in the Motion for Reconsideration on the access to the phone contact list and the Privacy Policy dated 10 September 2021;
6. A technical explanation on the purpose of the code "android.permission.READ_CONTACTS", which if enabled, gives the application permission to read the user's contacts data;
7. Collection Policy of the corporation;
8. An Agreement between the corporation and its third party collection partners or agents;
9. An Agreement between the corporation and its third party payment partners;
10. An explanation behind the drafting process of the Privacy Policy dated 10 September 2021;
11. Privacy Manual; and
12. Employee Manual, particularly on the provisions governing its employees' conduct of collecting debt and collection and usage of personal information.[^83]

On 20 October 2021, the Respondents filed its Motion to Admit with Compliance and submitted the following documents:

1. Revised Privacy Policy of Pesopop;
2. Revised Terms and Conditions or Terms of Service of Pesopop;
3. Revised Pesopop application;
4. Company Profile and a discussion of the business model of the corporation;
5. An explanation of the discrepancy between Counsel's representations in the Motion for Reconsideration on the access to the phone contact list and the Privacy Policy dated 10 September 2021;
6. A technical explanation on the purpose of the code "android.permission.READ_CONTACTS", which if enabled, gives the application permission to read the user's contacts data;
7. Collection Policy of the corporation;
8. An Agreement between the corporation and its third party collection partners or agents;
9. An Agreement between the corporation and its third party payment partners;
10. An explanation behind the drafting process of the Privacy Policy dated 10 September 2021;
11. Privacy Manual; and
12. Employee Manual, particularly on the provisions governing its employees' conduct of collecting debt and collection and usage of personal information.[^84]

Meanwhile, the Enforcement Division (EnD) of the NPC continuously monitored the availability of the app pursuant to the temporary ban.[^85]

The EnD confirmed that, as of 06 September 2021, the app was no longer available for download on different platforms.[^86]

Despite this, during the EnD's monitoring activity on 29 October 2021, it noticed that Pesopop was once again available for download in the Google Play Store and that it was last updated on 18 October 2021 to a new version (version 1.5.4).[^87] The EnD further stated that links to download the app can be found in Pesopop's official Facebook page and official website.[^88]

Thus, on 08 November 2021, the EnD issued a Letter to Pesopop regarding its compliance with the Commission's Order dated 12 August 2021.[^89] The EnD relayed that:

> [D]uring a monitoring activity on 29 October 2021, EnD noticed that Pesopop is again made available for download in the Google Play Store. Google Download Links of the mobile application can also be accessed on Pesopop's official Facebook page, through the "Use App" buttons and in its official website through the buttons "Get it on Google Play" and "Download Pesopop now."
>
> As the Temporary Ban on the Processing of Personal Data against Pesopop "shall remain in effect until the final resolution of the sua sponte investigation against Respondent and its responsible officers," Pesopop is instructed to EXPLAIN the foregoing incident within TEN (10) days from receipt of this letter.
>
> Populus Lending Corporation is also ORDERED to IMMEDIATELY ENSURE that Pesopop is no longer available for download, installation or use by the data subjects in any manner until the Temporary Ban is lifted.[^90]

On 15 November 2021, Pesopop submitted its Reply to the EnD's letter dated 08 November 2021.[^91] Pesopop stressed that it has already filed its Motion for Reconsideration to the Order dated 12 August 2021 in which it argued that the temporary ban imposed is void ab initio:

> In the meantime, please be advised that my client has already filed a motion for reconsideration to the order dated 12 August 2021 which is now pending for resolution. Kindly note that one of the arguments raised by my client in their motion is that the Temporary Ban imposed is void ab initio on the ground that the same cannot be filed motu propio and that the same was issued without posting the required bond. As such, the said motion for reconsideration filed maybe treated as a motion to lift and/or cancel the temporary ban. In other words, when the motion for reconsideration will be granted it will have the same effect of nullifying the temporary ban ordered against my client.[^92]

Nevertheless, Pesopop stressed that it has already manifested to the Commission that it will comply with all its orders.[^93] It explained that it has already "modified its data privacy policy, modified its app to conform to its data privacy policy and submitted other compliance documents directed to be submitted by this Honorable Commission."[^94]

On 19 November 2021, the EnD once again simulated downloading the app, account registration, and attempted a loan application.[^95] It found that "based on the simulations of the two (2) versions, versions 1.5.1 and 1.5.4, no evident changes were present."[^96] According to the EnD "the processes were similar, and the data being requested by the forms provided are still the same."[^97] The EnD observed that the permissions requested during the registration and loan application processes in both versions were also the same:

> The "AndroidManifest.xml" file of the two (2) versions were also checked for comparison. Derived from the files [ANNEX D], the dangerous permissions (Contacts, Location, Storage, Telephone and Camera) were still present in the current version 1.5.4 which is available for download to the public.[^98]

On 25 November 2021, the EnD issued a second Letter to Pesopop regarding its compliance with the Order dated 12 August 2021.[^99] The EnD reiterated that the temporary ban against Pesopop remains in effect until the final resolution of the main case or upon further orders by the Commission or other lawful authority.[^100] The EnD explained that the Motion for Reconsideration filed by Pesopop does not in any way lift or suspend the effectivity of the temporary ban, as the case is still pending with the Commission.[^101]

Further, the EnD confirmed that as of date, despite the Commission's Order, the app is still available for download, installation, and use by the data subjects, in clear violation of the Order dated 12 August 2021.[^102] The EnD ordered Pesopop to "immediately ensure that Pesopop is no longer available for download, installation or use by the data subjects in any manner until the temporary ban is lifted."[^103]

As of 26 November 2021, the EnD reported that the app was no longer available for download in the Google Play Store and other platforms.[^104] On 06 December 2021, however, the EnD found that a new version of the app (version 1.5.5) was once again made available on the Google Play Store.[^105] The EnD observed that the same permissions were still present when compared to the previous versions:

Below is a summary of the app permissions present in the different versions of Pesopop:[^106]

| App Permissions | Version 1.5.1 (Investigated by CID) | Version 1.5.4 | Version 1.5.5 | Proposed revised version from the Motion |
|---|---|---|---|---|
| Location | Present and required | Present and required | Present and required | Present and required |
| Camera | Present and required | Present and required | Present and required | Present and required |
| Contacts | Present and required | Present and required | Present and required | Present and required |
| Phone | Present and required | Present and required | Present and required | Present and required |
| Storage | Present and required | Present and required | Present and required | Present and required |

On 28 December 2021, the EnD issued a third Letter to Pesopop regarding its compliance with the Order dated 12 August 2021.[^107] The EnD stated that during its conduct of regular monitoring, it found that the app was again available for download on Google Play Store.[^108] The EnD reiterated that the temporary ban against Pesopop remains in effect until the final resolution of the main case, or upon further orders by the Commission or other lawful authority.[^109] It ordered the immediate take down of the app:

> Consequently, Populus Lending Corporation is hereby, **ORDERED, for the last time to IMMEDIATELY TAKE DOWN the Pesopop application from Google Play Store and ENSURE that it is no longer available for download, installation, or use by the data subjects in any manner until the Temporary Ban is lifted.**
>
> Further, Pesopop is instructed to EXPLAIN the foregoing incident within FIVE (5) days from receipt of this letter. Failure to comply with these orders shall be dealt with accordingly.[^110]

On 02 January 2022, Pesopop replied to the EnD and informed the latter that it already removed the app from the Google Play Store.[^111] It also reiterated that the temporary ban imposed is void ab initio for failure to post the required bond and claimed that it exposes the Commission to liability for damages if the temporary ban is not lifted.[^112] It also prayed for the resolution of the pending Motion for Reconsideration.[^113]

On 27 January 2022, the Commission issued a Resolution denying the Motion for Reconsideration and maintaining the temporary ban:

> WHEREFORE, premises considered, the Commission ADMITS the compliance documents submitted by Populus Lending Corporation and its responsible officers.
>
> The Commission DENIES the Motion for Reconsideration and MAINTAINS the Temporary Ban on the processing of personal data issued against Populus Lending Corporation and its responsible officers.
>
> Further, the Commission orders Populus Lending Corporation and its responsible officers and the Complaints and Investigation Division of the National Privacy Commission to SUBMIT within ten (10) days from the receipt of this Order their respective Memoranda on their respective arguments on the facts and issues for the resolution of this Commission.
>
> **SO ORDERED.**[^114]

The Commission stated that Pesopop has not sufficiently addressed the reasons for the issuance of the temporary ban.[^115] Pesopop continued to make the app available for download while the temporary ban was in effect.[^116] In addition, Pesopop did not submit all the documents and information required by the Order dated 28 September 2021.[^117] The Commission also found that Pesopop has not rectified its operations to comply with the DPA and the issuances of the Commission.[^118]

On 01 March 2022, Pesopop submitted its Memorandum.[^119]

Pesopop reiterated its arguments in its Motion for Reconsideration. First, Pesopop contended that the temporary ban is void ab initio because there is no showing that it is necessary to protect national security, or public interest, or to preserve and protect the rights of data subjects, and no posting of the required bond.[^120] It argued that "the initiation of a sua sponte investigation is unwarranted because there was no actual or threatened violation of the rights of data subjects."[^121]

Pesopop stated that at the time the CID initiated its investigation, there was no complaint filed by any of its customers against its practices.[^122] Thus, Pesopop contended that the CID exceeded its authority.[^123]

Second, Pesopop argued that its Revised Privacy Policy complies with the general privacy principles of transparency, legitimate purpose, and proportionality.[^124]

Pesopop explained that the Revised Privacy Policy "sufficiently informs the data subject of the nature, purpose, and extent of the data processing activity."[^125] It provides:

> The Revised Privacy Policy of the respondents expressly provides that personal information will be stored through DES and AES encryption and will be used primarily to prevent fraud, credit risk evaluation management, debt collection, identity verification, anti-money laundering, and to ensure compliance with laws, rules, and regulations.
>
> In addition, the Revised Privacy Policy provides for specific and concrete instances when personal information collected by respondents, including contact details, will be used.
>
> Specifically, contact details will be used for purposes including character reference and identification, such as instances of suspected fraud or identity theft. Hence, not only are respondents' declared purposes fully compliant with the law, but they are also clearly meant to protect the rights of the data subject.
>
> Likewise, prior versions of the respondents' Privacy Policy's failure to specify a retention period for collected data has already been rectified in the latest version of respondents' Revised Privacy Policy, which now clearly specifies the period within which respondents can retain the information collected from the data subject. Thus, the Revised Privacy Policy sufficiently provides the extent to which personal data is processed.[^126]

Pesopop argued that its Revised Privacy Policy "expressly declares that the processing of personal information is necessary for all purposes not prohibited by applicable law."[^127] It stressed that there is no law which prohibits the collection of personal data for the purpose of facilitating online lending services.[^128] It states:

> The Revised Privacy Policy also expressly provides that the purpose for collecting personal information is to facilitate the use of the service as an online lending application and other related services, including sharing information to third-party Payment Partners to help in facilitating online payments and who third-parties are even bound by the same Privacy Policy.
>
> . . .
>
> As a matter of fact, the respondents' declared purpose for collecting personal information is expressly regulated by the National Privacy Commission under NPC Circular 20-01 (Guidelines on Processing Personal Data for Loan-Related Transactions). In other words, the Honorable Commission itself recognizes that the respondents' declared purpose is legitimate because the Commission has even issued rules regulating Respondents' service. Therefore, the respondents' declared purpose complies with the principle that the collection of personal data must be for a legitimate purpose.[^129]

Pesopop posited that its Revised Privacy Policy provides that it will only collect information that are necessary, material, and relevant in its dealings with the data subject.[^130] It provides:

> A cursory reading of the respondents' Revised Privacy Policy readily shows that the respondents' access to the data subject's contact details is not being used to collect debt, much less to harass in any way the borrower or his/her contacts. On the contrary, the respondents' Revised Privacy Policy expressly provides:
>
> [Respondents] will request contact list limited to five (5) phone contacts for character reference purpose and identity verification. By giving us your home and/or mobile phone number, we have your permission to contact you or the phone contacts you provided us. This shall allow us to use text messaging, artificial or prerecorded voice messages, and automatic dialing technology, for all purposes not prohibited by applicable law.
>
> In other words, the collection of the data subject's contact list is required only when the purpose is not contrary to law, such as for the purpose of character reference and identity verification, including instances of suspected fraud or identity theft, or for the servicing the account of the data subject. Therefore, the respondents' processing of personal information is adequate, relevant, suitable, necessary, and not excessive in relation to its declared and specified purpose.[^131]

Third, Pesopop contended that the data subjects validly consented to the agreement entered into with Pesopop.[^132] It argued that prior to accepting the terms and conditions, the data subject is given the opportunity to read its Privacy Policy in full.[^133]

Fourth, Pesopop maintained that a temporary ban applies only against the processing of personal data.[^134] Thus, according to Pesopop, the Commission "acted in excess or with grave abuse discretion in issuing the temporary ban against the online lending activities of (Pesopop)":

> [A]ssuming arguendo that a Temporary Ban is proper under the circumstances, the Temporary Ban should have only covered the data processing activities of Populus Lending Corporation and not its online lending services, such as its online lending application. Data processing and online lending services are two activities which exist independently of each other and are entirely separate and distinct from the other. To impose a blanket ban against any other activity other than data processing is beyond the scope of the powers and authority of this Honorable Commission.[^135]

Fifth, Pesopop argued that the individual respondents, as directors and officers of Pesopop, should not be held personally liable because there is no allegation that they acted with bad faith, malice, or gross negligence.[^136] It interposed that the fact that the individual respondents have continuously revised the Privacy Policy to comply with the Commission's Orders negates any allegation of bad faith.[^137]

Lastly, Pesopop maintained that there is no longer any legal basis for the continued imposition of the temporary ban because its Revised Privacy Policy already complies with all the principles of proper data collection:

> Firstly, the Revised Privacy Policy sufficiently informs the data subjects of the nature, purpose, and extent of the data processing activity. The data subject is given the opportunity to read in full the Privacy Policy prior to accepting its terms and conditions. The party who seeks to adhere to the agreement is free to reject it entirely.
>
> Secondly, the Revised Privacy Policy expressly declares that the processing of personal information is necessary for all purposes not prohibited by applicable law. The declared purpose in collecting personal information for online lending application is not prohibited by law, morals, or public policy. There is no law which prohibits the collection of personal information for the purpose of facilitating online lending services.
>
> Lastly, the collection of personal information is not excessive because it adheres to well-defined standards in order to protect the rights of the data subject. The collection of the data subject's contact list is required only when the purpose is not contrary to law, such as for the purpose of character reference and identity verification, including instances of suspected fraud or identity theft, or for servicing the account of the data subject.[^138]

Pesopop prayed that the Commission nullify and set aside the temporary ban.[^139]

On 11 March 2022, the CID filed its Memorandum.[^140] It reiterated the arguments found in its FFR.[^141] The CID stated that the Revised Privacy Policy submitted by Pesopop still does not conform with the principles of transparency, legitimate purpose, and proportionality.[^142]

In addition, the CID argued that if found liable, the penalty shall be imposed upon the responsible officers, who by their gross negligence, allowed the commission of the violations.[^143] The CID stressed that Pesopop continued to make the app available during the pendency of the temporary ban on the processing of personal information imposed upon Pesopop.[^144] Further, the CID stated that based on their submissions and the EnD's findings, Pesopop has not rectified its operations to comply with the DPA, its Implementing Rules and Regulations (IRR), the Loan-Related Transactions Circular, and the lawful orders and issuances of the Commission.[^145]

As to the individual respondents' liability, the CID explained that Pesopop's Board of Directors, despite their assertion that they have not actively participated in the processing of the data, have the duty to decide for the corporation, and as such, carry the duty of diligence.[^146]

Thus, the CID argued that "the violation of the corporation is a violation of the persons behind it, which are its officers or board."[^147]

Lastly, the CID interposed that there is sufficient legal and factual basis for the issuance of an order for a permanent ban on processing of personal data against Pesopop for the following reasons:

> First, Respondent willfully and deliberately violated the issuance of the Order for Temporary Ban on 12 August 2021, when Respondent still made available for download its application on several instances.
>
> Second, despite the Respondent's assertions that it does not have any intention to violate any data privacy law, rules and regulations, issuances and will always consider the privacy rights of its customer supreme, it failed to rectify its Privacy Policy's provisions to comply with the DPA and its IRR, and Circular 2020-01.
>
> In light of the Respondent Corporation's continued and willful violation of the Temporary Ban issued against it during the pendency of this case, and in order to preserve and protect the rights of the Respondent's Corporation's data subject from further processing, the CID respectfully recommends for an issuance of a Permanent Ban on processing of personal data, against the Respondent Corporation.[^148]

The CID prayed that the Commission find Pesopop liable for violations of Sections 11, 12, 13, 16, and 25 of the DPA.[^149] Further, it prayed that the Commission find sufficient legal and factual basis for the issuance of an order for a permanent ban on processing of personal data against Pesopop.[^150]

On 31 March 2022, the Commission ordered Pesopop to show cause in writing why it should not be subject to contempt proceedings for failure to comply with its Order dated 12 August 2021 within ten (10) days from receipt of the Order.[^151] The Commission stated that:

> Despite repeated orders from the Commission to take down the application, the application kept re-appearing on the list of applications available for download in the Google Play Store. The Commission stresses that this is a blatant recurring violation of the Temporary Ban against Pesopop.[^152]

On the same day, the Commission directed the EnD to coordinate with Google LLC (Google), which operated Google Play, to determine the number of users who may have downloaded the app during the pendency of the temporary ban.[^153]

On 28 June 2022, Pesopop, through its new counsel, Vasig Abarquez Lumauig Abarquel Puno (VAL Law), filed its Entry of Appearance with Motion for Additional Time to File Reply/Comment.[^154] Pesopop requested for an additional period of ten (10) days within which to file its Reply/Comment to the Show Cause Order.[^155]

On 11 July 2022, Pesopop replied to the Show Cause Order.[^156] Pesopop manifested that the app was no longer available for download, installation, or use in the Google Play Store, Apple Store, and Huawei App Gallery.[^157] It also reiterated its arguments from its previous submissions.[^158]

With regard to its alleged recurring violations, Pesopop explained that it had no intention to violate the temporary ban and it only allowed a limited launch of the app for its existing users upon the advice of its previous counsel:

> Respondents, upon legal advice by previous counsel, allowed a limited launch of the PESOPOP application for existing users only for purposes of processing loans of EXISTING users, especially those who had pending obligations, and avoid incurring further losses from pre-existing liabilities. With no malicious intent to violate the Temporary Ban, Respondents only sought to ensure that EXISTING users can access the necessary information in order to fulfill their outstanding obligations. Otherwise put, new users could not have used the PESOPOP application. PESOPOP no longer processed any new information/data from new applicants in compliance with the Temporary Ban.[^159]

On 28 July 2022, the Commission issued an Order to the CID and Pesopop to appear for a clarificatory hearing on the alleged Pesopop's limited launch, on 11 August 2022.[^160]

On 11 August 2022, the Commission conducted the Clarificatory Hearing.[^161] Pesopop, through its counsel, explained that the limited launch was only for the purposes of servicing old users, and if a new user applies, the loan application will automatically be denied.[^162]

During the Clarificatory Hearing, the Commission ordered Pesopop and the individual respondents to submit the following information and documents:

1. Proof in relation the alleged process of automatically rejecting new loan applications during the "limited launch" that occurred while the Temporary Ban issued by the Commission was in effect;
2. Proof that the version of the Pesopop mobile application launched on a "limited" basis was for the sole purpose of processing payments for existing loan obligations;
3. Android Package Kit (APK) files for versions 1.5.1, 1.5.4, and 1.5.5 of the Pesopop mobile application;
4. Total number of users of the Pesopop mobile application;
5. Total number of users of the Pesopop mobile application with existing loan obligations;
6. Number of new users who downloaded the Pesopop application during the "limited launch";
7. Records of new loan applications filed during the "limited launch";
8. Records and statistics of the number of existing loan accounts that were processed and serviced during the "limited launch";
9. Logs of the IP addresses of all users who accessed the application during the "limited launch" period, if such logs are maintained;
10. Cloud-based storage data for new and existing users;
11. Explanation of the rationale, process, and decision-making leading to the "limited launch"; and
12. Proof of compliance with the Commission's previous orders through screenshots and submission of the complete customer database containing the names and contact information of all existing users of Pesopop.[^163]

On 14 September 2022, Pesopop, through its counsel VAL Law, submitted its Compliance dated 14 September 2022.[^164] Pesopop provided submissions with the following information and documents:

1. Proof of the alleged process of automatically rejecting new loan applications;
2. Proof of Pesopop's Decision on "Limited Launch";
3. Android Package Kit (APK) files for versions 1.5.1, 1.5.4, and 1.5.5;
4. Total number of users (5,633 users) and number of existing users (1,373 users);
5. Number of new users who downloaded the app during the "limited launch" (4,260 new users);
6. Records of new loan applications filed during the "limited launch" (none);
7. Records and statistics of new loan accounts processed and serviced during the "limited launch" (95 existing accounts);
8. Email logs of the IP addresses of users who accessed the application during the "limited launch" period;
9. Cloud-based storage data for new and existing users;
10. Explanation of the rationale, process, and decision-making leading to the "limited launch"; and
11. Proof of compliance with the Commission's previous orders through screenshots and a copy of the customer database.[^165]

On the same day, Pesopop submitted its 2022 Compliance Monitoring Report dated 14 September 2022.[^166]

However, in response to the CID's contention that the app's permissions were still present in version 1.5.5, Pesopop in its Revised Application screenshots submitted during the Clarificatory Hearing dated 10 September 2021, it was shown that a step labelled as "Step 4" where users can choose character references from their phone contact list was present. However, in its 2022 Compliance Monitoring Report dated 14 September 2022, Pesopop in the newly uploaded screenshots for version 1.5.5, indicated that the "Step 4" character reference selection interface was removed.[^167]

Notwithstanding these submissions and the apparent removal of the contact list permission in the revised screenshots, the fact remains that Pesopop, even with its alleged revision of the app, will still indeed have access to the contacts of the user's phone, as stated:

> We will request you to 'Read Contacts' permission. If you agree to the authorization, we will scan and upload the contact list information to https://api.pesopop.com:18062 using the most secure data transfer protocol (HTTPS). We will store your personal information through DES and AES encryption.
>
> Storage time will not exceed your usage time.
>
> We will request contact list limited to five (5) phone contacts for character reference purpose and identity verification. By giving us your home and/or mobile phone number, we have your permission to contact you or the phone contacts you provided us. This shall allow us to use text messaging, artificial or prerecorded voice messages, and automatic dialing technology, for all purposes not prohibited by applicable law. We may also send an email to any address where we reasonably believe we can contact you (include the contact list). Some of the purposes for calls and messages include suspected fraud or identity theft; obtaining information; transactions on or servicing of your account; and collecting on your account or collecting the delinquent account.[^168]

This practice does not only violate the Loan-Related Transactions Circular but also Memorandum Circular 18, Series of 2019 of the Securities and Exchange Commission (SEC).

The SEC Memorandum Circular prohibits unfair debt collection practices of financial and lending companies.[^169] Section 1(h) of the SEC Memorandum Circular states:

> **Section 1. *Unfair Collection Practices.*** [Financing] C[ompanie]s, [Lending] C[ompanie]s, and T[hird] P[arty] S[ervice] P[rovider]s hired by them may resort to all reasonable and legally permissible means to collect amounts due them under the loan agreement, provided that, in the exercise of their rights and performance of their duties, they must observe good faith and reasonable conduct and refrain from engaging in unscrupulous and untoward acts. Without limiting the general application of the foregoing, the following conduct shall constitute unfair collection practices, which shall be subject to the penalties provided herein:
>
> . . .
>
> **h. Notwithstanding the borrower's consent, contacting the persons in the borrower's contact list other than those who were named as guarantors or co-makers shall also constitute unfair debt collection practice.**[^170]

To reiterate, the legitimate purpose principle requires that the purpose for processing be within the limitations of the law.[^171] This should be understood to include the entire body of laws, rules, and regulations, and not just the DPA, its IRR, and the Commission's issuances.[^172]

Pesopop's access and use of the phone contacts list is an unfair debt collection practice, which is prohibited by the SEC Memorandum Circular. Pesopop's violation of the SEC Memorandum Circular, even if it is an issuance from a different government agency, and the Loan-Related Transactions Circular, renders its purpose for processing as illegitimate. Thus, Pesopop's access and use of the phone contacts list go against the general privacy principle of legitimate purpose.

Given all these, despite the changes to its app and Privacy Policy, Pesopop still blatantly violated the DPA and the Loan-Related Transactions Circular.

### Issue

Whether Pesopop's violation of the DPA warrants a recommendation for prosecution and whether the responsible officers of Pesopop are liable under Section 34 of the DPA.

### Discussion

#### On Pesopop's Violation of the DPA and Recommendation for Prosecution

Having established that Pesopop committed Unauthorized Processing before and during the effectivity of the temporary ban, the Commission proceeds to determine whether Pesopop's Board of Directors and corporate officers are liable based on Section 34 of the DPA.

The DPA imposes criminal penalties on specific offenses, which are imposed by courts of law after the conduct of a criminal trial.[^173] Upon finding of a violation, the Commission may recommend to the Department of Justice the prosecution and imposition of penalties on the violations enumerated under the DPA.[^174] These unlawful acts provided in Sections 25 to 32 are unauthorized processing of personal or sensitive personal information, processing personal or sensitive personal information for unauthorized purposes, accessing of personal or sensitive personal information, unauthorized access or intentional breach, improper disposal of personal or sensitive personal information, concealment of security breaches involving sensitive personal information, malicious disclosure, and unauthorized disclosure.[^175] If the PIC or Personal Information Processor (PIP) is a juridical person, then the penalties are imposed on its responsible officers.[^176]

Corporations and other juridical entities cannot be prosecuted for crimes under Philippine law.[^177] It is an established principle in criminal law that:

> Only natural persons can be the active subject [the criminal] because of the highly personal nature of the criminal responsibility.
>
> Since a felony is a punishable act or omission which produces or tends to produce a change in the external world, it follows that only a natural person can be the active subject [the criminal] of a crime, because he alone by his act can set in motion a cause or by his inaction can make possible the completion of a developing modification in the external world.[^178]

Specific to violations committed by a corporation, the Revised Corporation Code provides that:

> **Section 171. *Liability of Directors, Trustees, Officers, or Other Employees.*** If the offender is a corporation, the penalty may, at the discretion of the court, be imposed upon such corporation and/or upon its directors, trustees, stockholders, members, officers, or employees **responsible for the violation or indispensable to its commission.**[^179]

Jurisprudence provides that corporations have a separate and distinct personality from its officers:

> Bicol Gas is a corporation. As such, it is an entity separate and distinct from the persons of its officers, directors, and stockholders. It has been held, however, that **corporate officers or employees, through whose act, default or omission the corporation commits a crime, may themselves be individually held answerable for the crime.**[^180]

Thus, as held by the Supreme Court, "[a] corporation can act only through its officers and agents, and where the business itself involves a violation of the law, the correct rule is that all who participate in it are liable."[^181] Certain special laws provide for the particular officers who shall be held responsible for corporate crimes.[^182] In the DPA, this is specified in Section 34:

> **Section 34. *Extent of Liability.*** If the offender is a corporation, partnership or any juridical person, **the penalty shall be imposed upon the responsible officers, as the case may be, who participated in, or by their gross negligence, allowed the commission of the crime.** If the offender is a juridical person, the court may suspend or revoke any of its rights under this Act. If the offender is an alien, he or she shall, in addition to the penalties herein prescribed, be deported without further proceedings after serving the penalties prescribed. If the offender is a public official or employee and lie or she is found guilty of acts penalized under Sections 27 and 28 of this Act, he or she shall, in addition to the penalties prescribed herein, suffer perpetual or temporary absolute disqualification from office, as the case may be.[^183]

Therefore, Section 34 supplies the gap in Sections 25 to 32 of the DPA by specifying that the officers of erring corporations are the natural persons that may be held responsible for such violations and will be the accused in the criminal case that will be filed.[^184]

As the Commission has emphasized in previous decisions, for juridical entities, a violation of Section 25 does not automatically result in a recommendation for prosecution.[^185] Rather, there is a need to identify the proper responsible officers that shall be accused in the criminal case.[^186]

Section 34 of the DPA explicitly states that a responsible officer can be subject to the imposable penalties in two instances: (1) participation in the commission of the crime, or (2) allowing the commission of the violation through gross negligence.[^189]

The clause "who participated in, or by their gross negligence" should be viewed in relation to the acts of the responsible officers that reasonably caused the violation, without which the violation would not have occurred.[^190] Ultimately, however, this shall be applied on a case-to-case basis.[^191]

The Commission has previously defined the phrase "participated in" as follows:

> The term "participated in," as found in Section 34 of the DPA, **requires that the responsible officers committed acts that reasonably caused the violation, without which the violation would not have occurred.** As such, the instance of "participated in" contemplates a situation wherein the officers and employees that will be recommended for prosecution are "responsible" for and the root cause of the violation of the DPA in such a way that **if they had not committed certain acts, then the violation would not have transpired.** Examples of this instance cover situations wherein the responsible officer directs the execution of the act resulting in the violation or through his acts, reasonably caused the commission of the violation without which such violation would not have occurred. Thus, a sense of causation is essential when determining if the responsible officers may be held liable based on participation.[^192]

Given these, the first ground or "participation in the commission of the crime" has three elements:

1. There is an act that reasonably caused the violation;
2. The violation would not have occurred without the act;
3. The person:
   a. exercised a certain degree of responsibility over the act that caused the violation; or
   b. whose actions were indispensable to the commission of the crime.[^193]

In this case, individual respondents RCJ, FLB, JIS, MM, and WL, in Pesopop's Motion for Reconsideration, argued that they did not actively participate in the processing of personal data of its clients.[^194] They claimed that upon discovery of the Order dated 12 August 2021, they "immediately set a meeting to discuss and instruct the management of Pesopop to immediately review and amend the data privacy terms and conditions to conform to the provision of the Data Privacy Act of 2012."[^195] Further, they asserted that there was no allegation nor proof of gross negligence, fraud, bad faith and malice.[^196]

It can no longer be said, however, that the individual respondents, as Pesopop's officers and directors, did not participate in the commission of these violations Pesopop repeated violating the temporary ban by making its app available for download in several instances during the effectivity of the temporary ban.

Applying the elements discussed earlier, there were acts that caused the violation, which was making the app available for download or the "limited launch" during the effectivity of the temporary ban and the revision of the app and policies. These acts were necessary for the violation to occur. Finally, it is the officers and directors who exercised a certain degree of responsibility over the limited launch and revisions which caused the violation of the temporary ban.

First, as stated by Pesopop in its Compliance, Mr. JIS, one of the individual respondents, as incorporator and director, approved and implemented the so-called "limited launch" which it argued was the reason why the app was made available for download during the temporary ban.[^197]

Second, Pesopop explained that upon discovery of the individual respondents of the Commission's Order imposing the temporary ban, they "immediately set a meeting to discuss and instruct the management of Pesopop to immediately review and amend the data privacy terms and conditions to conform to the provision of the DPA."[^198] Pesopop also stated that the individual respondents have continuously revised the Privacy Policy to comply with the Commission's Orders.[^199] As earlier established, however, the Commission found the Revised Application and Privacy Policy not only wanting but violative of the DPA and the Loan-Related Transactions Circular.

These show that the individual respondents, as directors and officers of Pesopop, directed both the relaunching of the app and revision of the app and policies during the temporary ban. The only conclusion then is that they allowed the repeated violations to happen which led to the commission of Unauthorized Processing during the effectivity of the temporary ban.

Even assuming that the individual respondents did not directly participate in the commission of Unauthorized Processing, their failure to prevent these acts, given the repeated nature and gravity of the violations, is tantamount to gross negligence.

The Supreme Court has consistently defined gross negligence as:

> [N]egligence characterized by the want of even slight care, or by acting or omitting to act in a situation where there is a duty to act, **not inadvertently but willfully and intentionally, with a conscious indifference to the consequences, insofar as other persons may be affected.** It is the omission of that care that even inattentive and thoughtless men never fail to give to their own property.[^200]

Despite the imposition of the temporary ban and the repeated reminders from the EnD, the app remained continuously accessible. This continuous availability demonstrates the inaction of the individual respondents, which amounts to gross negligence. Thus, they could still be held liable for Unauthorized Processing based on their gross negligence.

Given the totality of the evidence presented, the Commission finds that the present case warrants a recommendation for prosecution.

The Commission emphasizes that PICs are accountable for the protection of the personal information of individuals and for the observation of the obligations under the DPA. At the core of these obligations are the general privacy principles. Following this, any person or entity that processes information should process information only for legitimate purposes that have been made known to the data subject.[^201] They should only process as much information as is needed to achieve their clearly defined and stated business purposes or to comply with the provisions of law or regulation.[^202]

**WHEREFORE**, premises considered, this Commission:

1. **FINDS** that Respondents Populus Lending Corporation (Pesopop) and its directors and officers, namely RCJ, FLB, JIS, MM, and WL, as responsible officers, violated Section 25 of Republic Act No 10173 or the Data Privacy Act of 2012 (DPA); and

2. **FORWARDS** this Decision and a copy of the pertinent case records to the Secretary of Justice and **RECOMMENDS** the prosecution of the responsible officers for Unauthorized Processing of Personal or Sensitive Personal Information under Section 25 of the DPA.

**SO ORDERED.**

City of Pasay, Philippines.
26 September 2023.

LEANDRO ANGELO Y. AGUIRRE
Deputy Privacy Commissioner

WE CONCUR:

JOHN HENRY D. NAGA
Privacy Commissioner

NERISSA N. DE JESUS
Deputy Privacy Commissioner

Copy furnished:

VASIG ABARQUEZ LUMAUIG ABARQUEZ PUNO LAW OFFICES
Counsel for Respondents

COMPLAINTS AND INVESTIGATION DIVISION
ENFORCEMENT DIVISION
GENERAL RECORDS UNIT
National Privacy Commission

[^1]: Fact-Finding Report, 10 June 2021, at 13, *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^2]: *Id.* at 1.

[^3]: *Id.* at 4-5.

[^4]: *Id.* at 5.

[^5]: *Id.* at 2.

[^6]: *Id.*

[^7]: Fact-Finding Report, 10 June 2021, at 2, *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^8]: *Id.*

[^9]: *Id.*

[^10]: *Id.*

[^11]: *Id.*

[^12]: *Id.*

[^13]: Fact-Finding Report, 10 June 2021, at 2, *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^14]: *Id.*

[^15]: *Id.*

[^16]: *Id.*

[^17]: *Id.* at 3.

[^18]: *Id.*

[^19]: Fact-Finding Report, 10 June 2021, at 3, *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^20]: *Id.* at 3-4.

[^21]: *Id.* at 13.

[^22]: *Id.* at 11.

[^23]: *Id.* at 6.

[^24]: *Id.*

[^25]: Fact-Finding Report, 10 June 2021, at 6, *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^26]: *Id.* at 6-7.

[^27]: *Id.* at 6.

[^28]: *Id.* at 7.

[^29]: *Id.*

[^30]: *Id.* at 8.

[^31]: *Id.*

[^32]: *Id.*

[^33]: *Id.*

[^34]: *Id.*

[^35]: *Id.* at 8-9. Emphasis supplied.

[^36]: *Id.* at 9.

[^37]: Fact-Finding Report, 10 June 2021, at 9 *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^38]: *Id.*

[^39]: *Id.* at 9.

[^40]: *Id.*

[^41]: *Id.*

[^42]: *Id.*

[^43]: Fact-Finding Report, 10 June 2021, at 9, *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^44]: *Id.* at 10.

[^45]: *Id.*

[^46]: *Id.*

[^47]: *Id.* at 11.

[^48]: *Id.*

[^49]: Fact-Finding Report, 10 June 2021, at 11, *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^50]: *Id.* at 12.

[^51]: *Id.* at 11.

[^52]: *Id.* at 12.

[^53]: Order, 16 June 2021, at 1, *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^54]: *Id.*

[^55]: Order, 12 August 2021, at 2, *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^56]: *Id.*

[^57]: *Id.*

[^58]: *Id.* at 3.

[^59]: *Id.*

[^60]: Supplemental Fact-Finding Report, 05 July 2021, at 2, *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^61]: Order, 16 June 2021, at 1, *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^62]: *Id.*

[^63]: *Id.*

[^64]: Order, 12 August 2021, at 2, *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^65]: *Id.*

[^66]: *Id.*

[^67]: Notice of Entry of Appearance with Motion for Reconsideration, 03 September 2021, at 5-6, *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^68]: *Id.* at 6.

[^69]: *Id.*

[^70]: Motion to Admit with Compliance, 20 October 2021, in *In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^71]: Enforcement Division Memorandum, 03 November 2021, in *In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^72]: *Id.*

[^73]: Letter Re: Compliance with Order dated 12 August 2021 in NPC SS 21-008 entitled "In re: Populus Lending Corporation (Pesopop) and its Responsible Officers", 08 November 2021, at 2, in *In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^74]: Enforcement Division Memorandum, 03 November 2021, at 1, in *In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^75]: *Id.*

[^76]: Letter Re: Compliance with Order dated 12 August 2021 in NPC SS 21-008 entitled "In re: Populus Lending Corporation (Pesopop) and its Responsible Officers", 08 November 2021, in *In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^77]: *Id.*

[^78]: *Id.*

[^79]: *Id.*

[^80]: *Id.*

[^81]: *Id.*

[^82]: *Id.*

[^83]: *Id.*

[^84]: *Id.*

[^85]: *Id.*

[^86]: *Id.*

[^87]: *Id.*

[^88]: *Id.*

[^89]: *Id.*

[^90]: *Id.*

[^91]: *Id.*

[^92]: *Id.*

[^93]: *Id.*

[^94]: *Id.*

[^95]: *Id.*

[^96]: *Id.*

[^97]: *Id.*

[^98]: *Id.*

[^99]: *Id.*

[^100]: *Id.*

[^101]: *Id.*

[^102]: *Id.*

[^103]: *Id.*

[^104]: *Id.*

[^105]: *Id.*

[^106]: *Id.*

[^107]: *Id.*

[^108]: *Id.*

[^109]: *Id.*

[^110]: *Id.*

[^111]: *Id.*

[^112]: *Id.*

[^113]: *Id.*

[^114]: *Id.*

[^115]: *Id.*

[^116]: *Id.*

[^117]: *Id.*

[^118]: *Id.*

[^119]: *Id.*

[^120]: *Id.*

[^121]: *Id.*

[^122]: *Id.*

[^123]: *Id.*

[^124]: *Id.*

[^125]: *Id.*

[^126]: *Id.*

[^127]: *Id.*

[^128]: *Id.*

[^129]: *Id.*

[^130]: *Id.*

[^131]: *Id.*

[^132]: *Id.*

[^133]: *Id.*

[^134]: *Id.*

[^135]: *Id.*

[^136]: *Id.*

[^137]: *Id.*

[^138]: *Id.*

[^139]: *Id.*

[^140]: *Id.*

[^141]: *Id.*

[^142]: *Id.*

[^143]: *Id.*

[^144]: *Id.*

[^145]: *Id.*

[^146]: *Id.*

[^147]: *Id.*

[^148]: *Id.*

[^149]: *Id.*

[^150]: *Id.*

[^151]: *Id.*

[^152]: *Id.*

[^153]: *Id.*

[^154]: *Id.*

[^155]: *Id.*

[^156]: *Id.*

[^157]: *Id.*

[^158]: *Id.*

[^159]: *Id.*

[^160]: *Id.*

[^161]: *Id.*

[^162]: *Id.*

[^163]: *Id.*

[^164]: *Id.*

[^165]: *Id.*

[^166]: *Id.*

[^167]: *Id.*

[^168]: *Id.* at 15-16. Emphasis supplied.

[^169]: Securities and Exchange Commission, Prohibition on Unfair Debt Collection Practices or Financing Companies (FC) and Lending Companies (LC), Memorandum Circular No. 18, Series of 2019 [SEC MC. No. 19-18 (19 August 2019)].

[^170]: *Id.* § 1 (h).

[^171]: MLF v. Grab Philippines, NPC 19-142, at 8.

[^172]: *Id.*

[^173]: Data Privacy Act of 2012, §§ 25-37.

[^174]: *Id.* § 7 (i).

[^175]: *Id.* §§ 23-32.

[^176]: *Id.* § 34.

[^177]: See *People v. Tan Boon Kong*, G.R. L-35262 (1930).

[^178]: LUIS B. REYES, THE REVISED PENAL CODE CRIMINAL LAW BOOK 1 505 (2012). Emphasis removed. Emphasis supplied.

[^179]: An Act Providing for the Revised Corporation Code of the Philippines [Revised Corporation Code], Republic Act No. 11232, § 171 (2019). Emphasis supplied.

[^180]: *Espiritu Jr. v. Petro Corporation*, G.R. No. 170891 (2009). Emphasis supplied.

[^181]: *People v. Tan Boon Kong*, G.R. L-35262 (1930).

[^182]: *In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers*, NPC SS 21-006, at 40.

[^183]: *Id.*

[^184]: *Id.*

[^185]: *Id.*

[^186]: *Id.*

[^187]: *Id.* at 41.

[^188]: *Id.*

[^189]: Data Privacy Act of 2012, § 34.

[^190]: *In re: Wefund Lending Corporation (JuanHand) and its Responsible Officers*, NPC SS 21-006, at 41.

[^191]: *Id.*

[^192]: *Id.* at 43-44. Emphasis supplied.

[^193]: See *Revised Corporation Code*, § 171; *Data Privacy Act of 2012*, § 34.

[^194]: Notice of Entry of Appearance with Motion for Reconsideration, 03 September 2021, at 5, *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^195]: *Memorandum of the Respondents*, 01 March 2022, at 15, *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2022).

[^196]: *Id.* at 5-6.

[^197]: *Compliance*, 02 September 2022, at 3, *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2022).

[^198]: *Notice of Entry of Appearance with Motion for Reconsideration*, 03 September 2021, at 5-6, *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2021).

[^199]: *Memorandum of the Respondents*, 01 March 2022, at 15, *in In re: Populus Lending Corporation and its Responsible Officers*, NPC SS 21-008 (NPC 2022).

[^200]: *Fernandez v. Office of the Ombudsman*, G.R. No. 193983, 14 March 2012. Emphasis supplied.

[^201]: KGR v. BB, et. al., CID 18-E-040, 12 May 2020, at 5, *available at* https://privacy.gov.ph/wp-content/uploads/2023/05/CID-18-E-040-KGR-v.-BB-et-al.-Decision-2020.05.12.pdf (last accessed 04 December 2023)

[^202]: *Id.*
