# -------------------------------------------------------------------------
# FILENAME: parser.py
# SPECIFICATION: Read the Bio Faculty information, parse faculty members name, title, office, email, and website, and
#                persist this data in MongoDB collection.
# FOR: CS 4250- Group Project
# TIME SPENT: 2 hours
# -----------------------------------------------------------*/

# importing some Python libraries
from bs4 import BeautifulSoup
from db_connection import *


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
        print(professor_url)
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

            text_sections = len(bs.find_all('div', {'class': 'section-text'}))

            # Get the sections of each professor data
            section_element = bs.find('div', {'class': 'section-text'})

            while section_element.find_next('h2') and text_sections != 0:
                section_element = section_element.find_next('h2')

                for section in section_element:
                    if section.get_text().strip() != '':
                        content += section.get_text().strip().replace('\n', ' ')
                content += ' '

                section_element = section_element.find_next()
                for section in section_element:
                    if section.get_text().strip() != '':
                        content += section.get_text().strip().replace('\n', ' ')
                content += ' '

                text_sections -= 1

            print(content)
            print()

            professor = {'_id': counter, 'web': professor_url, 'text': content}
            faculty.insert_one(professor)
            counter += 1
