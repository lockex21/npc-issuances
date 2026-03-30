---
title: "2020-11-12: In re: Lisensya.Info (Cease and Desist Order)"
description: "Cease and Desist Order against Lisensya.Info and its owner/operators Jose Minao and Billy James Jimena for unauthorized processing and unauthorized access of personal information obtained from LTO.net.ph, directing them to file a comment, cease processing personal data, and enjoining the NTC to take down the website."
aliases:
  - "2020-11-12 Lisensya CDO"
  - "2020-11-12 lisensya cdo"
  - "In re: Lisensya.Info (Cease and Desist Order)"
  - "in re: lisensya.info (cease and desist order)"
tags:
  - "order"
  - "type/order"
  - "year/2020"
  - "npc-case"
date: "2020-11-12"
draft: false
---

## Source
- Reference: 2020-11-12
- Official PDF: http://privacy.gov.ph/wp-content/uploads/2023/05/Cease-And-Desist-Order-Re-In-Re-Lisensya.Info-11-12-20-Pseudonymized-17Dec20-ADJU1.pdf
- Source page: http://privacy.gov.ph/orders-2/
- Issue date: November 12, 2020
- Pages: 14

## Source Tags
- Unauthorized Processing
- Unauthorized Access
- NPC Circular 20-02
- Sensitive Personal Information

## Order Text

IN RE: LISENSYA.INFO, INITIATED AS AN INDEPENDENT NPC INVESTIGATION INTO THE POSSIBLE DATA PRIVACY VIOLATIONS COMMITTED BY THE WEBSITE LISENSYA.INFO.

x----------------------------------------------------x

**CEASE AND DESIST ORDER**

LIBORO, P.C.:

This resolves the Application for Issuance of Cease and Desist Order of the National Privacy Commission (NPC)'s Complaints and Investigation Division (CID)[^1] pursuant to a Sua Sponte Investigation against respondent Lisensya.Info for unauthorized processing and unauthorized access of personal information and sensitive personal information which are violations of the Data Privacy Act of 2012 (DPA).

### The Facts

The website Lisensya.Info depicts itself as one connected with the Land Transportation Office (LTO).

In an effort to inform the public of the fact that this website is not related to the LTO, on 05 November 2020, the LTO posted on its Facebook page a warning to the public stating, in part:

> "Ang lisensya.info website ay HINDI pinapatakbo o konektado sa ahensya ng LTO. Para sa kaligtasan ng lahat, huwag po tayong magbigay ng SENSITIBONG IMPORMASYON sa UNVERIFIED links o accounts."[^2]

On 08 November 2020, Manila Bulletin published an online article entitled "LTO exposes thousands of information due to misconfiguration"[^3]. The article is anchored on the independent investigation of AJ Dumanhug (Dumanhug), an independent cybersecurity analyst published on his blog.[^4]

Dumanhug, on his blog dated 08 November 2020, states that the website has two (2) main features, Driver's License Authenticator (DLA) and Motor Vehicle Authenticator (MVA). The DLA feature asks for user's license number and birthday and once those information are submitted, the name of the license's owner and the expiration date would be revealed. Meanwhile, the MVA asks users to submit just the Motor Vehicle File Number and would show sensitive information like the make, plate number, engine number, chassis number, registration expiry date and the name of the owner.[^5]

Dumanhug also mentioned how the acquired the personal data are stored by the said website. He further stated that one can see that the website is using the Application Programming Interface (API) endpoint of LTO.net.ph, an official website of LTO, by viewing the source code of the PHP files downloaded on the git repository of Lisensya.Info.[^6]

Upon knowledge, the CID commenced its investigation on the developing issue. In this initial data gathering, the CID found out that:

1. The website Lisensya.Info has been in existence as early as 15 September 2019; and
2. It has neither a privacy notice nor any contact details of its owner.[^7]

CID has communicated with the registered Data Protection Officer of the LTO – Atty. Romeo G. Vera Cruz (LTO Executive Director) for them to shed light on the incident considering that the information being provided by Lisensya.Info may be found on their database. The DPO committed to file a breach notification report with the NPC.

On 09 November 2020, the CID further conducted an in-depth investigation regarding the blog post of Dumanhug dated 08 November 2020 regarding the website Lisensya.Info.

The examiners were able to get the dump files from the website Lisensya.Info, and captured sensitive information from the captured dump file of the website.

Through the source code, the examiners found the following information:[^8]

1. Author of the website is Jose Minao with email address joseminao@pm.me;
2. Project is named ValidateDL; and
3. The website is using the API endpoint from LTO.net.ph, one of the official website of LTO to retrieve some information.

Using the captured information, the examiners searched at github.com and found a repository result under user yoseminao updated on 14 September 2020. The date coincides from the gathered information on the creation of the website Lisensya.Info.

Under the _config.yml of ValidateDL, the examiners found that the owner of the URL of the website https://lto.pinoydev.org is also Jose Minao with email address joseminao@protonmail.com.

The examiners checked the Whois history of the url pinoydev.org and found the owner Billy James Jimena from Cagayan De Oro, Misamis Oriental, Philippines with email address billyjamesjimena@yahoo.ca.

After full extraction of the source code of the website Lisensya.Info, the examiners have validated the following:[^9]

1. There are 9,953 saved driver's license information on the developer's server;
2. There are 19,412 saved motor vehicle file number information on the developer's server; and
3. The website captures the following information:

   For the Driver's License Validation:
   - a. License Number;
   - b. Birthdate;
   - c. Sex;
   - d. First Name, Middle Name and Last Name; and
   - e. Expiry Date.

   For the Motor Vehicle Number Validation:
   - a. Motor Vehicle Number;
   - b. Plate Number;
   - c. Chassis Number;
   - d. Vehicle Make;
   - e. Vehicle Series;
   - f. First Name, Middle Name and Last Name of owner;
   - g. Registration Date; and
   - h. Classification of vehicle use whether private or public.

As of 11 November 2020, the LTO.net.ph website is no longer accessible, while Lisensya.Info is still fully accessible.

On the Application for Issuance of Cease and Desist Order dated 11 November 2020, the CID prays that its request for the issuance of a Cease and Desist Order against Lisensya.Info be granted by the Commission, and consequently require Lisensya.Info to stop processing the personal and sensitive personal information in its possession in order to preserve and protect public interest and the rights of the data subjects.

### Discussion

The NPC is an independent body created to administer and implement the provisions of the DPA. As provided in Section 7 of the DPA, the NPC has Rule Making, Advisory, Public Education, Compliance and Monitoring, Complaints and Investigation, and Enforcement powers[^10] to enable it to protect the fundamental human right of privacy while ensuring the free flow of information to promote innovation and growth.[^11]

Section 7(b) of the DPA specifically states that it is the mandate of the NPC to:

> "(b) Receive complaints, institute investigations, facilitate or enable settlement of complaints through the use of alternative dispute resolution processes, adjudicate, award indemnity on matters affecting any personal information, prepare reports on disposition of complaints and resolution of any investigation it initiates, and, in cases it deems appropriate, publicize any such report: *Provided*, That in resolving any complaint or investigation (except where amicable settlement is reached by the parties), the Commission shall act as a collegial body. For this purpose, the Commission may be given access to personal information that is subject of any complaint and to collect the information necessary to perform its functions under this Act;" (Emphasis supplied)

In the exercise of its rule-making power and to flesh out the provision above, the NPC issued NPC Circular 16-04 (NPC Rules of Procedure) on 15 December 2016. Section 3 thereof provides who may file complaints with the Commission:

> "SECTION 3. Who may file complaints. – The National Privacy Commission, sua sponte, or persons who are the subject of a privacy violation or personal data breach, or who are otherwise personally affected by a violation of the Data Privacy Act, may file complaints for violations of the Act."

Further, Section 23 of the NPC Rules of Procedure provides for the NPC's power of original inquiry:

> "SECTION 23. Own initiative. – Depending on the nature of the incident, in cases of a possible serious privacy violation or personal data breach, taking into account the risks of harm to a data subject, the Commission may investigate on its own initiative the circumstances surrounding the possible violation. Investigations may include on-site examination of systems and procedures. If necessary, the Commission may use its enforcement powers to order cooperation of the personal information controller or other persons, with the investigation or to compel appropriate action to protect the interests of data subjects."

In addition, the DPA explicitly provides for the Commission's power to issue Cease and Desist Orders:

> "Section 7 (c). Issue cease and desist orders, impose a temporary or permanent ban on the processing personal information, upon finding that the processing will be detrimental to national security and public interest."

This was reiterated in the Implementing Rules and Regulations (IRR) of the DPA:

> "Section 9. Functions. The National Privacy Commission shall have the following functions:
>
> xxx
>
> f. Enforcement. The Commission shall perform all acts as may be necessary to effectively implement the Act, these Rules, and its other issuances, and to enforce its Orders, Resolutions, or Decisions, including the imposition of administrative sanctions, fines, or penalties. This includes:
>
> xxx
>
> 3. Issuing cease and desist orders, or imposing a temporary or permanent ban on the processing of personal data, upon finding that the processing will be detrimental to national security or public interest, or if it is necessary to preserve and protect the rights of data subjects." (Emphasis supplied)

Furthermore, Section 4 of the recently issued NPC Circular No. 20-02 (Rules on the Issuance of Cease and Desist Orders) provides that the grounds for the issuance of Cease and Desist Order are the following:

> "Section 4. Grounds for the Issuance of Cease and Desist Order. – No CDO shall be issued unless it is established by substantial evidence that all of the following concur:
>
> A. the Adverse Party is doing, threatening or is about to do, is procuring to be done, some act or practice in violation of the DPA, its IRR, or other related issuances;
>
> B. such act or practice is detrimental to national security or public interest, or the CDO is necessary to preserve and protect the rights of a data subject; and
>
> C. the commission or continuance of such act or practice, unless restrained, will cause grave and irreparable injury to a data subject."

From the foregoing, it can be seen that three (3) elements are required for this Commission to validly exercise its power to issue a Cease and Desist Order, to wit:

1. There must be a finding of a practice or act that an entity is doing, threatening, or about to do, which constitute a violation of the DPA, its IRR, or other related issuances;
2. Such act or practice is or will be detrimental to national security or public interest, or the issuance is necessary to preserve and protect the rights of the data subject; and
3. The commission or continuance of such act or practice, unless restrained, will cause grave and irreparable injury to a data subject.

Based on the facts and initial result of the technical investigation, the Commission finds that substantial evidence has established the concurrence of the grounds for the issuance of a Cease and Desist Order against Lisensya.Info.

#### On the Violation of the DPA and Its IRR

In sum, there is sufficient ground to support the finding that Lisensya.Info violated the following penal provisions of law:

> SEC. 25. Unauthorized Processing of Personal Information and Sensitive Personal Information. – (a) The unauthorized processing of personal information shall be penalized by imprisonment ranging from one (1) year to three (3) years and a fine of not less than Five hundred thousand pesos (Php500,000.00) but not more than Two million pesos (Php2,000,000.00) shall be imposed on persons who process personal information without the consent of the data subject, or without being authorized under this Act or any existing law.
>
> (b) The unauthorized processing of personal sensitive information shall be penalized by imprisonment ranging from three (3) years to six (6) years and a fine of not less than Five hundred thousand pesos (Php500,000.00) but not more than Four million pesos (Php4,000,000.00) shall be imposed on persons who process personal information without the consent of the data subject, or without being authorized under this Act or any existing law.
>
> xxx
>
> SEC. 29. Unauthorized Access or Intentional Breach. – The penalty of imprisonment ranging from one (1) year to three (3) years and a fine of not less than Five hundred thousand pesos (Php500,000.00) but not more than Two million pesos (Php2,000,000.00) shall be imposed on persons who knowingly and unlawfully, or violating data confidentiality and security data systems, breaks in any way into any system where personal and sensitive personal information is stored.

The initial investigation and the technical report have clearly shown that the processing of the personal data on Lisensya.Info is without the consent of the affected data subject, or without authority under the DPA or any existing law, which is a blatant and complete violation of the DPA.

Lisensya.Info displays the logo of the LTO prominently in its website pretending to be an official government website. It processed the personal data of the data subjects, the owners of the driver's license and motor vehicle file number, by storing the unlawfully obtained information from LTO in its website and using them to "verify" entries by the public without their consent or authority of law, as defined under Section 13 of the DPA.

The license number, birthday, sex, and plate number are sensitive personal information that are generally prohibited to be processed except under the circumstances provided under Section 13 of the DPA, which provides:

> "SEC. 13. Sensitive Personal Information and Privileged Information. – The processing of sensitive personal information and privileged information shall be prohibited, except in the following cases:
>
> (a) The data subject has given his or her consent, specific to the purpose prior to the processing, or in the case of privileged information, all parties to the exchange have given their consent prior to processing;
>
> (b) The processing of the same is provided for by existing laws and regulations: *Provided*, That such regulatory enactments guarantee the protection of the sensitive personal information and the privileged information: *Provided, further*, That the consent of the data subjects are not required by law or regulation permitting the processing of the sensitive personal information or the privileged information;
>
> (c) The processing is necessary to protect the life and health of the data subject or another person, and the data subject is not legally or physically able to express his or her consent prior to the processing;
>
> (d) The processing is necessary to achieve the lawful and noncommercial objectives of public organizations and their associations: *Provided*, That such processing is only confined and related to the bona fide members of these organizations or their associations: *Provided, further*, That the sensitive personal information are not transferred to third parties: *Provided, finally*, That consent of the data subject was obtained prior to processing;
>
> (e) The processing is necessary for purposes of medical treatment, is carried out by a medical practitioner or a medical treatment institution, and an adequate level of protection of personal information is ensured; or
>
> (f) The processing concerns such personal information as is necessary for the protection of lawful rights and interests of natural or legal persons in court proceedings, or the establishment, exercise or defense of legal claims, or when provided to government or public authority.

As quoted above, there is a set of criteria provided in the DPA for the lawful processing of sensitive personal information. To rely on consent as the lawful basis for processing, an examination must be made whether such consent was freely given, specific, informed, and an indication of will, whereby the data subject agrees to the collection and processing of personal information about and/or relating to him or her.[^12]

Consent is considered freely given, specific and informed when it adheres to the principles to the general data privacy principles of transparency, legitimate purpose and proportionality.

As the IRR of the DPA explains:

> The data subject must be aware of the nature, purpose, and extent of the processing of his or her personal data, including the risks and safeguards involved, the identity of personal information controller, his or her rights as a data subject, and how these can be exercised. Any information and communication relating to the processing of personal data should be easy to access and understand, using clear and plain language.[^13]

There is no informed consent in this instance considering that said website does not provide any specific and legitimate purpose for the collection and processing of the involved personal data.

Further, the website accessed the personal information from LTO.net.ph without authority. Through the use an Application Programming Interface (API), it acquired the personal data from LTO.net.ph, an official website of LTO and stored the same in its own database.

#### On Detriment to National Security and Public Interest

The act of accessing a government website's stored data is detrimental to national security or public interest, and the practice of storing the unlawfully collected personal data on its database without any authority or statement of purpose is in gross disregard and violation of the rights of data subjects.

As of 11 November 2020, a total of 9,953 driver's license information and 19,412 motor vehicle file number information were saved on the server of Lisensya.Info.

Until its recent discovery, it has been masquerading itself as a website of the LTO and has been unlawfully processing personal data without the consent and knowledge of data subjects.

Lisensya.Info accessed a government website LTO.net.ph, used the information stored therein without authority, and stored it in its own website. This unlawful acquisition of sensitive personal information exposes the affected data subjects to real risks of serious harm.

The protection of the data subjects from these imminent threats or harm is a matter of public interest and issuance of a cease and desist order is crucial in order to preserve and protect the rights of the data subject.

#### On Grave and Irreparable Injury to Data Subjects

Lisensya.Info's continued operation is a palpable risk that can cause grave and irreparable injury to affected data subjects.

Lisensya.Info's website is still active as of date. Its continued existence poses a threat to unsuspecting individuals who may use its services by surrendering their sensitive personal information.

Identity theft is the most likely consequence, but there is no telling what other acts and further damage can be done to the stored data on Lisensya.Info's database as surveillance and threats to security may be among them. Allowing it to continue its operations increases the risk of exposing the personal data to identity fraud, and other grave and irreparable damage and/or injury.

As discussed by the Commission in the case of *In re: Philippine Seven Corporation* (CID BN 18-081),[^14] viz:

> Identity theft occurs when individual/s wrongfully acquired, use, misuse, transfer, possession, alteration or deletion of identifying information without right. In *Jose Disini, Jr., et al., vs. Secretary of Justice*, the Supreme Court had this to say on the crime of Identity Theft:
>
>> 'The usual identifying information regarding a person includes his name, his citizenship, his residence address, his contact number, his place and date of birth, the name of his spouse if any, his occupation, and similar data. The law punishes those who acquire or use such identifying information without right, implicitly to cause damage.'
>
> The Court rightly recognizes that a combination of personal information can be used by online imposter to access or take over existing personal accounts or open new accounts in the name of unsuspecting data subjects. x x x. A simple online search in search engines and/or social media accounts of these franchise applicants may already give enough ammunition for these online wrong doers to commit the crime of Identity Theft. Thus, considering the above, this breach might entail real risk of serious harm to the affected data subjects. (Emphasis Supplied)

Hence based on the foregoing, it is clear that grounds for the issuance of a Cease and Desist Order are present in the instant case.

WHEREFORE, premises considered, Lisensya.Info and its owner/operator, JOSE MINAO, BILLY JAMES JIMENA and other responsible officers are hereby ordered to:

1. File a **COMMENT**, within ten (10) days from receipt of this Order, on the allegations in the attached Application for Issuance of Cease and Desist Order, pursuant to Section 9 of the NPC Circular No. 20-02; and
2. **CEASE AND DESIST** from the processing the personal and sensitive personal information in its possession, until the Commission issues a decision on the submission of the Comment, which shall be made no more than thirty (30) days from the expiration of the period to file a Comment or of the termination of the clarificatory hearing if one is held, pursuant to NPC Circular No. 20-02.

Furthermore, the NATIONAL TELECOMMUNICATIONS COMMISSION is hereby enjoined to take down the website Lisensya.Info immediately upon receipt of this Order.

**SO ORDERED.**

City of Pasay, Philippines;
12 November 2020.

RAYMUND ENRIQUEZ LIBORO
Privacy Commissioner

WE CONCUR:

LEANDRO ANGELO Y. AGUIRRE
Deputy Privacy Commissioner

JOHN HENRY D. NAGA
Deputy Privacy Commissioner

[^1]: Application For Issuance of Cease and Desist Order dated 11 November 2020.
[^2]: https://www.facebook.com/lto.cdmpao/photos/a.1589028444448324/4945107912173677/ (last accessed 09 November 2020).
[^3]: https://mb.com.ph/2020/11/08/lto-exposes-thousands-of-information-due-to-misconfiguration/.
[^4]: *Ibid.*
[^5]: https://atom.hackstreetboys.ph/lisensya-website-and-why-you-should-never-useit/?fbclid=IwAR0meSLYGlpSib0h-WioJKo_V_94GBgrM8-bzx7gkn_uGHmHi3jlaNzQni0 (last accessed 09 November 2020).
[^6]: *Ibid.*
[^7]: Preliminary Report on Lisensya.Info/LTO dated 09 November 2020.
[^8]: Technical Report dated 10 November 2020.
[^9]: Supplemental Technical Report dated 11 November 2020.
[^10]: See, RA 10173, Section 7.
[^11]: See, *Id.*, Section 2.
[^12]: See Republic Act No. 10173, Section 3(b).
[^13]: Implementing Rules and Regulations of the Data Privacy Act, Section 18(a).
[^14]: Resolution dated 21 May 2020.
