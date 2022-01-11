# TaxDocumentXMLInterface

  Hello, this is a tool for the Polytechnic for parsing through, specifically, tax documentation. Although, generally, no assumption is made of the content for the input XML files. Essentially, this acts as an interface with XML etree for Pytthon to simplify data extraction.

  It is best viewed as a explorer for the tree formed by the XML file. For the uninitiated, with the example of a tax document, one could have different supporting documentation such as a Schedule A. Within this document, there exists multiple sections with subsections each. And, only at some depth of this categorization of the inital filling does any desired piece of information reside. So, this just makes it a bit easier for end users to not worry about the explicit tree data structure in extracting the data. 
