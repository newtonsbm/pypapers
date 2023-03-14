import pyscript
import asyncio
import json
from request import request  # import our request function.

async def fetch_doi(doi):
    Element("title").element.innerText = "Loading..." 
    url = f"https://api.crossref.org/works/{doi}"
    response = await request(url, method="GET")
    return response 

def show_loading():
    Element("loading").element.style.display = "flex"
    Element("results").element.style.display = "none"

def hide_loading():
    # Hide the loading div and show the results div
    Element("loading").element.style.display = "none"
    Element("results").element.style.display = "block"

async def search_doi(*args, **kwargs):
    """Search for a DOI"""
    doi = Element("doi").element.value
    if not doi:
        return None

    # make a fetch request to the DOI Crossref API
    show_loading()
    response = await fetch_doi(doi)
    hide_loading()
    if response.status != 200:
        Element("title").element.innerText = "Error loading DOI. Try again."
        return None
    
    # parse the response as JSON
    data = await response.json()
    js.console.log(json.dumps(data))
    if not data:
        Element("title").element.innerText = "DOI not found. Try again."
        return None
    
    # get metadata from doi response json
    title = data["message"]["title"][0]
    authors = data["message"]["author"]
    referencesCount = data["message"]["reference-count"]
    references = data["message"]["reference"]

    # set the title and author in the page
    Element("title").element.innerText = title
    # set authors as list
    Element("authors").element.innerText = ", ".join([f"{author['given']} {author['family']}" for author in authors])
    # set references count
    Element("references-count").element.innerText = str(referencesCount)
    # set references as list
    Element("references").element.innerText = ", ".join([f"{reference['title']}" for reference in references])


def search_doi_event():
    asyncio.create_task(search_doi()) 
    # asyncio.ensure_future(search_doi())