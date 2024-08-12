# scrape_confluence.py
import requests
from bs4 import BeautifulSoup

def scrape_confluence_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try different selectors based on the page's structure
        content_divs = soup.find_all('div', {'class': 'content'})
        
        text_content = ""
        for div in content_divs:
            text_content += div.get_text(separator='\n', strip=True) + "\n\n"
        
        # Fallback if specific divs aren't found
        if not text_content.strip():
            text_content = soup.get_text(separator='\n', strip=True)
        
        return text_content
    return None

def save_documents(documents, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for i, doc in enumerate(documents):
            f.write(f"Document {i+1}:\n{doc}\n\n")

urls = [
    "https://confluence.appstate.edu/display/ATKB/Appalachian+Technology+Knowledge+Base",
    "https://confluence.appstate.edu/display/ATKB/Appalachian+Technology+Knowledge+Base",
    "https://confluence.appstate.edu/display/ATKB/Appalachian+Technology+Knowledge+Base",
    "https://confluence.appstate.edu/display/ATKB/Knowledge+Base+Articles",
    "https://confluence.appstate.edu/display/ATKB/Accessibility",
    "https://confluence.appstate.edu/display/ATKB/Adobe+Creative+Cloud+Articles",
    "https://confluence.appstate.edu/display/ATKB/Android",
    "https://confluence.appstate.edu/display/ATKB/Apple",
    "https://confluence.appstate.edu/display/ATKB/AsULearn+Articles",
    "https://confluence.appstate.edu/display/ATKB/Atlassian",
    "https://confluence.appstate.edu/display/ATKB/Banner+Self-Service+Articles",
    "https://confluence.appstate.edu/display/ATKB/Confluence+Articles",
    "https://confluence.appstate.edu/display/ATKB/Docuware+Articles",
    "https://confluence.appstate.edu/display/ATKB/Domain+Protection",
    "https://confluence.appstate.edu/display/ATKB/Duo+-+2+Factor+Authentication",
    "https://confluence.appstate.edu/display/ATKB/FAQ+articles",
    "https://confluence.appstate.edu/display/ATKB/Google+Docs+Articles",
    "https://confluence.appstate.edu/display/ATKB/iOS+Articles",
    "https://confluence.appstate.edu/display/ATKB/Kaltura",
    "https://confluence.appstate.edu/display/ATKB/Library",
    "https://confluence.appstate.edu/display/ATKB/LinkedIn+Learning+Articles",
    "https://confluence.appstate.edu/display/ATKB/Mac+Articles",
    "https://confluence.appstate.edu/display/ATKB/Microsoft",
    "https://confluence.appstate.edu/display/ATKB/Other",
    "https://confluence.appstate.edu/display/ATKB/PaperCut+Print+Articles",
    "https://confluence.appstate.edu/display/ATKB/Print+and+Copy",
    "https://confluence.appstate.edu/display/ATKB/REDCap+Articles",
    "https://confluence.appstate.edu/display/ATKB/SAS+Software",
    "https://confluence.appstate.edu/display/ATKB/Security",
    "https://confluence.appstate.edu/display/ATKB/Student+PaperCut+Print+Articles",
    "https://confluence.appstate.edu/display/ATKB/Tech+Support",
    "https://confluence.appstate.edu/display/ATKB/uDesk+Virtual+Desktop+Articles",
    "https://confluence.appstate.edu/display/ATKB/University+Accounts",
    "https://confluence.appstate.edu/display/ATKB/VoIP+Phones",
    "https://confluence.appstate.edu/display/ATKB/VPN+and+Remote+Connections+to+Campus+Network",
    "https://confluence.appstate.edu/display/ATKB/Watermark+Faculty+Success+app",
    "https://confluence.appstate.edu/display/ATKB/Windows",
    "https://confluence.appstate.edu/display/ATKB/Workshop+Scheduler",
    "https://confluence.appstate.edu/display/ATKB/YoMart",
    "https://confluence.appstate.edu/display/ATKB/Zoom"
   
]

documents = []
for url in urls:
    content = scrape_confluence_page(url)
    if content:
        documents.append(content)

# Save documents to a text file
output_file = 'documents.txt'
save_documents(documents, output_file)
print(f"Documents saved to {output_file}")
