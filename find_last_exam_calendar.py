import requests
from bs4 import BeautifulSoup


def find_last_exam_calendar(url):
    base_url = url.split("/it/")[0]
    pdf_appelli = []

    try:
        # Fetch the page source using the requests library
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the first table row with class 'cat-list-row0'
            row = soup.find('tr', class_='cat-list-row0')

            # Find the link within the row
            if row:
                link = row.find('a', href=True)
                if link:
                    href = link['href']
                    print("Last exam calendar found: ", href.split("/")[-1])

                    # Fetch the page source of the linked page
                    linked_response = requests.get(str(base_url + href))

                    # Check if the request was successful (status code 200)
                    if linked_response.status_code == 200:
                        # Parse the HTML content of the linked page
                        linked_soup = BeautifulSoup(linked_response.text, 'html.parser')

                        # Find all links containing href to PDF files with "STUDENTI" and "Appello" in the name
                        pdf_links = linked_soup.find_all('a', href=True)
                        for pdf_link in pdf_links:
                            pdf_href = pdf_link['href']
                            if pdf_href.endswith('.pdf') and 'STUDENTI' in pdf_href and 'Appello' in pdf_href:
                                # print("Found PDF link:", pdf_href)
                                pdf_appelli.append(base_url + pdf_href)
                    else:
                        print(f"Failed to fetch page source from {href}. Status code: {linked_response.status_code}")
            else:
                print("Exam calendar not found")
        else:
            print(f"Failed to fetch page source from {url}. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return pdf_appelli


if __name__ == "__main__":
    url = 'https://www.ing.unipi.it/it/studenti/calendario-esami'
    pdf_links = find_last_exam_calendar(url)
    print("PDF Appelli:", pdf_links)