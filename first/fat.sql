-- Sequences
CREATE SEQUENCE seq_docspec START WITH 1;
CREATE SEQUENCE seq_org START WITH 1;
CREATE SEQUENCE seq_address START WITH 1;
CREATE SEQUENCE seq_addfix START WITH 1;
CREATE SEQUENCE seq_holder START WITH 1;
CREATE SEQUENCE seq_account START WITH 1;
CREATE SEQUENCE seq_payment START WITH 1;

-- Table: MessageSpec
CREATE TABLE MessageSpec (
  SendingCompanyIN VARCHAR2(50),
  TransmittingCountry VARCHAR2(10),
  ReceivingCountry VARCHAR2(10),
  MessageType VARCHAR2(20)
);

INSERT INTO MessageSpec VALUES ('Y9N35.99999.SL.XXX', 'GG', 'US', 'FATCA');

-- Table: DocSpec
CREATE TABLE DocSpec (
  ID NUMBER PRIMARY KEY,
  DocTypeIndic VARCHAR2(20),
  DocRefId VARCHAR2(50)
);

INSERT INTO DocSpec VALUES (seq_docspec.NEXTVAL, 'FXXXX1', 'Y9888.99999.761.5645333233');

-- Table: Organization
CREATE TABLE Organization (
  ID NUMBER PRIMARY KEY,
  ReCountryCode VARCHAR2(10),
  TIN VARCHAR2(50),
  Name VARCHAR2(100)
);

INSERT INTO Organization VALUES (seq_org.NEXTVAL, 'GB', 'TIN123', 'OrgName Ltd');

-- Table: Address
CREATE TABLE Address (
  ID NUMBER PRIMARY KEY,
  OrgID NUMBER,
  CountryCode VARCHAR2(10),
  FOREIGN KEY (OrgID) REFERENCES Organization(ID)
);

INSERT INTO Address VALUES (seq_address.NEXTVAL, 1, 'GB');

-- Table: AddressFix
CREATE TABLE AddressFix (
  ID NUMBER PRIMARY KEY,
  AddressID NUMBER,
  Street VARCHAR2(100),
  PostalCode VARCHAR2(20),
  City VARCHAR2(50),
  FOREIGN KEY (AddressID) REFERENCES Address(ID)
);

INSERT INTO AddressFix VALUES (seq_addfix.NEXTVAL, 1, '7th cross , 5th main', 'GFE ELZ', 'Lancashire');

-- Table: AccountHolder
CREATE TABLE AccountHolder (
  ID NUMBER PRIMARY KEY,
  AccountHolderType VARCHAR2(20),
  OrgID NUMBER,
  FOREIGN KEY (OrgID) REFERENCES Organization(ID)
);

INSERT INTO AccountHolder VALUES (seq_holder.NEXTVAL, 'FXXXX104', 1);

-- Table: AccountReport
CREATE TABLE AccountReport (
  ID NUMBER PRIMARY KEY,
  AccountNumber VARCHAR2(20),
  AccountClosed VARCHAR2(5),
  DocSpecID NUMBER,
  HolderID NUMBER,
  FOREIGN KEY (DocSpecID) REFERENCES DocSpec(ID),
  FOREIGN KEY (HolderID) REFERENCES AccountHolder(ID)
);

INSERT INTO AccountReport VALUES (seq_account.NEXTVAL, '123456789', 'false', 1, 1);

-- Table: Payment
CREATE TABLE Payment (
  ID NUMBER PRIMARY KEY,
  ReportID NUMBER,
  PaymentType VARCHAR2(20),
  PaymentAmount NUMBER,
  FOREIGN KEY (ReportID) REFERENCES AccountReport(ID)
);

INSERT INTO Payment VALUES (seq_payment.NEXTVAL, 1, 'FAXXX301', 10000);
INSERT INTO Payment VALUES (seq_payment.NEXTVAL, 1, 'FAXXX501', 20000);

COMMIT;




SELECT XMLELEMENT("FATCA_OECD",  
         XMLAttributes('2.0' AS "version"),
         -- MessageSpec
         (
           SELECT XMLELEMENT("MessageSpec",
                    XMLFOREST(
                      SendingCompanyIN,
                      TransmittingCountry,
                      ReceivingCountry,
                      MessageType
                    )
           ) 
           FROM MessageSpec
         ),
         -- FATCA
         XMLELEMENT("FATCA",
           -- ReportingFl
           (
             SELECT XMLELEMENT("ReportingFl",
                      XMLFOREST(
                        o.ReCountryCode AS "ResCountryCode",
                        o.Name
                      ),
                      XMLELEMENT("TIN", XMLAttributes('US' AS "issuedBy"), 'Y9YN35.999999.SL.XXX'),
                      CURSOR(
                        SELECT XMLELEMENT("Address",
                                 XMLFOREST(a.CountryCode),
                                 (
                                   SELECT XMLELEMENT("AddressFix",
                                            XMLFOREST(af.Street, af.PostalCode, af.City)
                                   )
                                   FROM AddressFix af
                                   WHERE af.AddressID = a.ID
                                 )
                               )
                        FROM Address a
                        WHERE a.OrgID = o.ID
                      ),
                      XMLELEMENT("FilerCategory", 'FXXX2'),
                      (
                        SELECT XMLELEMENT("DocSpec",
                                 XMLFOREST(d.DocTypeIndic, d.DocRefId)
                               )
                        FROM DocSpec d
                        WHERE d.ID = ar.DocSpecID
                      )
             )
             FROM Organization o
             JOIN AccountHolder ah ON ah.OrgID = o.ID
             JOIN AccountReport ar ON ar.HolderID = ah.ID
             WHERE o.ID = 1
           ),
           -- ReportingGroup
           XMLELEMENT("ReportingGroup",
             CURSOR(
               SELECT XMLELEMENT("AccountReport",
                        XMLFOREST(
                          ar.AccountNumber,
                          ar.AccountClosed
                        ),
                        (
                          SELECT XMLELEMENT("DocSpec",
                                   XMLFOREST(d.DocTypeIndic, d.DocRefId)
                                 )
                          FROM DocSpec d
                          WHERE d.ID = ar.DocSpecID
                        ),
                        (
                          SELECT XMLELEMENT("AccountHolder",
                                   XMLFOREST(ah.AccountHolderType),
                                   (
                                     SELECT XMLELEMENT("Organization",
                                              XMLELEMENT("TIN", XMLAttributes('GB' AS "issuedBy"), o.TIN),
                                              XMLFOREST(o.Name, o.ReCountryCode),
                                              CURSOR(
                                                SELECT XMLELEMENT("Address",
                                                         XMLFOREST(a.CountryCode),
                                                         (
                                                           SELECT XMLELEMENT("AddressFix",
                                                                    XMLFOREST(af.Street, af.PostalCode, af.City)
                                                           )
                                                           FROM AddressFix af
                                                           WHERE af.AddressID = a.ID
                                                         )
                                                       )
                                                FROM Address a
                                                WHERE a.OrgID = o.ID
                                              )
                                     )
                                     FROM Organization o
                                     WHERE o.ID = ah.OrgID
                                   )
                          )
                          FROM AccountHolder ah
                          WHERE ah.ID = ar.HolderID
                        ),
                        CURSOR(
                          SELECT XMLELEMENT("Payment",
                                   XMLFOREST(p.PaymentType, p.PaymentAmount)
                                 )
                          FROM Payment p
                          WHERE p.ReportID = ar.ID
                        )
               )
               FROM AccountReport ar
             )
           )
         )
       ).getClobVal() AS final_xml
FROM dual;



CREATE TABLE fatca_xml_log (
  id NUMBER PRIMARY KEY,
  generated_on DATE DEFAULT SYSDATE,
  fatca_payload XMLTYPE
);

CREATE SEQUENCE seq_fatca_xml_log START WITH 1;

SELECT id, generated_on, fatca_payload.getClobVal()
FROM fatca_xml_log
ORDER BY generated_on DESC;
