# -------------------------------------------------------------------------
# AUTHOR: Kenny Santanu, Harry Nguyen, Nathan Pham, Chi Le, Ismael Garcia
# FILENAME: main.py
# SPECIFICATION:    This program is a Web/Topical search engine that will crawl the CPP Biology Dept Web until until 10 Faculty Professors' pages with the required format are found.
#                   Next, this information will be collected, transformed, and saved in a database to enabling searching.
#                   Finally, the user will be able to search for a query and the results will be displayed in the order of most relevant.
# FOR: CS 4250 - Group Project
# TIME SPENT: 50 hours
# -----------------------------------------------------------*/

from indexing.crawling import crawler
from indexing.parsing import parser
from indexing.transforming import transform
from indexing import indexer
from querying import ir_model


def main():
    # Text Acquisition
    print("Crawler starting...")
    base_url = "https://www.cpp.edu/sci/biological-sciences/index.shtml"
    frontier = crawler.Frontier()
    frontier.add_url(base_url)
    target_urls = crawler.crawler_thread(frontier)
    print("Crawler finished!")

    print("Start parsing faculty page...")
    parser.parsing_faculty_page(target_urls)
    print("Parsing finished!")

    # Text Transformation
    print("Start transforming text...")
    transform.transform()
    print("Transforming finished!")

    # Index Creation
    print("Creating index...")
    indexer.create_index()
    print("Index created!")

    # Ranking
    while True:
        userQuery = input("Enter a query: ")
        print("Searching...")
        results = ir_model.search(userQuery)

        print("Results:")
        menu = "y"
        count = 0
        while menu == "y":
            for i in range(5):
                if count < len(results):
                    print("=====================================")
                    print(count + 1)
                    print("Website:", results[count][0])
                    print("Score:", results[count][1])
                    count += 1
                else:
                    break
            if count >= len(results):
                break

            print("\nThere are", len(results) - count, "more results.")
            while True:
                menu = input("Do you want to see more results? (y/n): ")
                if menu == 'y' or menu == 'n':
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

        print("=====================================\n")

if __name__ == '__main__':
    main()