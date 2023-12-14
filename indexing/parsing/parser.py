# -------------------------------------------------------------------------
# FILENAME: parser.py
# SPECIFICATION: Read the Bio Faculty information, parse faculty members name, title, office, email, and website, and
#                persist this data in MongoDB collection.
# FOR: CS 4250- Group Project
# -----------------------------------------------------------*/

# importing some Python libraries
from bs4 import BeautifulSoup
from database.db_connection import *


def parsing_faculty_page(target_urls):
    # Connect to the database
    db = connectDataBase()
    pages = db.pages
    # Create a collection to store the professors' info
    faculty = db.faculty

    # faculty_urls = ['https://www.cpp.edu/faculty/alas',
    #                 'https://www.cpp.edu/faculty/parensburger/index.shtml',
    #                 'https://www.cpp.edu/faculty/nebuckley/',
    #                 'https://www.cpp.edu/faculty/jear/index.shtml',
    #                 'https://www.cpp.edu/faculty/junjunliu/',
    #                 'https://www.cpp.edu/faculty/ejquestad/index.shtml',
    #                 'https://www.cpp.edu/faculty/jaysonsmith/index.shtml',
    #                 'https://www.cpp.edu/faculty/jcsnyder/index.shtml',
    #                 'https://www.cpp.edu/faculty/adsteele/',
    #                 'https://www.cpp.edu/faculty/aavaldes/index.shtml']

    counter = 1
    # Retrieve the recorded page based on the provided URL
    for professor_url in target_urls:
        # print(professor_url)
        result = pages.find_one({'url': professor_url})

        # Check if the HTML content was found
        if not result:
            print('No matching records found')
        else:
            # Get the HTML content of the URL
            html = result['html']
            # print('1 HTML content extracted successfully!')
            bs = BeautifulSoup(html, 'html.parser')

            content = ''

            # The text is located in three main sections: section-text, section-menu, and accolades
            text_sections = bs.find_all('div', {'class': {'section-text', 'section-menu', 'accolades'}})

            # Get text in each section
            for section in text_sections:
                # Remove unrecognized characters (e.g. <0xa0>, Â)
                content += (section.get_text(' ', strip=True)
                                   .replace('Â', '')
                                   .replace('\xa0', ' '))
                # separate text sections by a space
                content += ' '

            # print(content)
            # print()

            professor = {'_id': counter, 'web': professor_url, 'text': content}
            faculty.insert_one(professor)
            counter += 1
