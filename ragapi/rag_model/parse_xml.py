import xml.etree.ElementTree as ET

class Parse_XML:
    def __init__(self, input_file):
        self.input_file = input_file

    def extract_text_from_recommendation_sections(self):
        # Parse the XML file
        tree = ET.parse(self.input_file)
        root = tree.getroot()

        # Find all <recommendation> elements
        recommendation_elements = root.findall('.//recommendation')

        # List to hold the extracted text content
        text_list = []

        i = 0

        # Iterate through all <recommendation> elements
        for recommendation_element in recommendation_elements:
            # Get the content of the <recommendation> element as a string
            recommendation = recommendation_element.findall('.//text')

            # Add the text to the list
            text_list.append(recommendation[0].text)

        return text_list


# Example usage
# input_file = 'rag_model/cpg-corpus-cms.xml'
# input_file = 'cpg-corpus-cms.xml'
# pxml = Parse_XML(input_file)
# text_list = pxml.extract_text_from_recommendation_sections()

# # Print out the first bottom section's text for demonstration
# print(len(text_list))
# print(text_list[11])

