import os
import random
import re
import ntpath

#Expected Citation ML Output from API call
CITATION_OUTPUT_PATTERN = '{0}> :=  TYPE:{1}SUBTYPE:{2}ANAPHORIC:{3}CO-REF:{4}NAME:{5} ##{6}#{7}#'
CITATION_REGX = CITATION_OUTPUT_PATTERN.format('(?P<CITATIONID>.*)', '(?P<TYPE>.*)', '(?P<SUBTYPE>.*)', '(?P<ANAPHORIC>.*)', '(?P<COREF>.*)', '(?P<NAME>.*)', '(?P<OFFSETSTART>.*)', '(?P<OFFSETEND>.*)')

#Represents Citation Detail with data from ML API Response and derevied properties
class citationDetail:
    
    def __init__(self):
        self.citationFileAndId = ''
        self.citationtype = ''
        self.subtype = ''
        self.anaphoric = False
        self.coref = ''
        self.name = ''
        self.offsetStart = 0
        self.offsetEnd = 0
        
        #Generates Random Color
        r = lambda: random.randint(50,225)
        self.color = '#%02X%02X%02X' % (r(),r(),r())

    #Gets the file name from Composite Key
    def CitationFileId(self):
        return self.citationFileAndId[0:self.citationFileAndId.rfind('-')]

    #Gets the Citation Id from Composite Key  
    def CitationId(self):
        return self.citationFileAndId[self.citationFileAndId.rfind('-') + 1:len(self.citationFileAndId)]

    #Gets the Co-ref Citation Id from Composite Key
    def CorefCitationId(self):
        if(len(self.coref) > 4):
            return self.coref[self.coref.rfind('-') + 1:len(self.coref)]
        else:
            return ''

#Represents Citation HtmlDocument
class citationHtmlDocument:
    def __init__(self, citationDetails, citatation_raw_content):
        self.citationDetails = citationDetails
        self.sourceText = citatation_raw_content

    def createDocument(self):
        self.citationDetails.sort(key=lambda x: x.offsetEnd, reverse=True)
        #Generates HTMl Conetent for passed in Citation Offset Details
        #Decorate all the citations with Span Tag with Unique color per related citations
        for citationDetail in self.citationDetails:
            #self.sourceText = self.sourceText.replace(citationDetail.name, f'<span style="background-color: {citationDetail.color}">{citationDetail.name}</span>')
            self.sourceText = insert_text(self.sourceText,citationDetail.offsetEnd, f'</span>')
            self.sourceText = insert_text(self.sourceText,citationDetail.offsetStart, f'<span style="background-color: {citationDetail.color}">')
        return self.sourceText

#Method to get citation details based on file input
def getCitationHtmlDetailsbyFile(citation_raw_file, citation_ml_output, citation_output_html):
    rawFileContent = open(citation_raw_file, 'r').read()
    mlOutputFileContent = open(citation_ml_output, 'r').read()
    citationHtmlContent = getCitationHtmlDetails(rawFileContent, mlOutputFileContent)
    
#    if not os.path.exists(os.path.dirname(citation_output_html)):
#        os.makedirs(os.path.dirname(citation_output_html))
        
    htmlFile = open(citation_output_html, 'w')
    htmlFile.write(citationHtmlContent)
    htmlFile.close()
    
#Method to get citation details based on content input
def getCitationHtmlDetails(rawFileContent, mlOutputFileContent):
    citationHtml = citationHtmlDocument(getCitationDetails(mlOutputFileContent), rawFileContent)
    
#    if not os.path.exists(os.path.dirname(citation_output_html)):
#        os.makedirs(os.path.dirname(citation_output_html))

    return citationHtml.createDocument()

#Parse Citation ML output
def getCitationDetails(citationContent):
    outputDetails = citationContent.replace('\r', '').replace('\n', '').replace('\t', '').split('<CITATION-')

    citationDetails = []

    for output in outputDetails:
        citationRegex = re.compile(CITATION_REGX)
        match = citationRegex.search(output)

        if match == None:
            continue

        citationDetailOutput = citationDetail()
        citationDetailOutput.citationFileAndId = match.group('CITATIONID').strip()
        citationDetailOutput.citationtype = match.group('TYPE').strip()
        citationDetailOutput.subtype = match.group('SUBTYPE').strip()
        citationDetailOutput.anaphoric = bool(match.group('ANAPHORIC').strip())
        citationDetailOutput.coref = match.group('COREF').strip()
        citationDetailOutput.name = rreplace(match.group('NAME').replace('"', ''),'"', '', 0).strip()
        citationDetailOutput.offsetStart = int(match.group('OFFSETSTART').strip())
        citationDetailOutput.offsetEnd = int(match.group('OFFSETEND').strip())

        citationDetails.append(citationDetailOutput)

    for indCitationDetail in [x for x in citationDetails if x.CorefCitationId() != '']:
        indCitationDetail.color = next(x for x in citationDetails if x.CitationId() == indCitationDetail.CorefCitationId()).color
    
    return citationDetails

#Replace Last Occurance of the string
def rreplace(input, old, new, occurrence):
    output = input.rsplit(old, occurrence)
    return new.join(output)

#Inserts text at the given index
def insert_text(input, index, text):
    return input[:index] + text + input[index:]

#if __name__ == "__main__":
def htmlgeneration(path):
    #    CURRENT_FOLDER_PATH = os.path.dirname(os.getcwd())
    citation_raw_file = path
    path = ntpath.basename(citation_raw_file)
    path = path.replace('.txt','')
    citation_ml_output = 'outputs/'+path+'-text.txt'
    citation_output_html = 'outputs/'+path+'-Html.html'

    getCitationHtmlDetailsbyFile(citation_raw_file, citation_ml_output, citation_output_html)

    #For content based call use below code
    #citationHtmlContent = getCitationHtmlDetails(rawFileContent, mlOutputFileContent)

    print('Html Generation completed. Files available @ ' + citation_output_html)