# CS50' Web Programming with Python and Javascript - Project 1 - Wiki

## Summary
- [Description](#description)
- [Requirements](#requirements)
- [How to Run](#how-to-run)
- [Submit Version](#submit-version-result)
    - [Main Page](#main-page)
    - [Create Page](#create-page)
    - [Entry Page](#entry-page)
    - [Edit Page](#edit-page)
    - [Search Page](#search-page)
    - [Random Page](#random-page)


## Description
Design a Wikipedia-like online encyclopedia.

## Requirements
Taken from the [project's page](https://cs50.harvard.edu/web/2020/projects/1/wiki/).
- Entry Page: Visiting /wiki/TITLE, where TITLE is the title of an encyclopedia entry, should render a page that displays the contents of that encyclopedia entry.
    - The view should get the content of the encyclopedia entry by calling the appropriate util function.
    - If an entry is requested that does not exist, the user should be presented with an error page indicating that their requested page was not found.
    - If the entry does exist, the user should be presented with a page that displays the content of the entry. The title of the page should include the name of the entry.
- Index Page: Update index.html such that, instead of merely listing the names of all pages in the encyclopedia, user can click on any entry name to be taken directly to that entry page.
- Search: Allow the user to type a query into the search box in the sidebar to search for an encyclopedia entry.
    - If the query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page.
    - If the query does not match the name of an encyclopedia entry, the user should instead be taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring. For example, if the search query were ytho, then Python should appear in the search results.
    - Clicking on any of the entry names on the search results page should take the user to that entry’s page.
- New Page: Clicking “Create New Page” in the sidebar should take the user to a page where they can create a new encyclopedia entry.
    - Users should be able to enter a title for the page and, in a textarea, should be able to enter the Markdown content for the page.
    - Users should be able to click a button to save their new page.
    - When the page is saved, if an encyclopedia entry already exists with the provided title, the user should be presented with an error message.
    - Otherwise, the encyclopedia entry should be saved to disk, and the user should be taken to the new entry’s page.
- Edit Page: On each entry page, the user should be able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a textarea.
    - The textarea should be pre-populated with the existing Markdown content of the page. (i.e., the existing content should be the initial value of the textarea).
    - The user should be able to click a button to save the changes made to the entry.
    - Once the entry is saved, the user should be redirected back to that entry’s page.
- Random Page: Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry.
- Markdown to HTML Conversion: On each entry’s page, any Markdown content in the entry file should be converted to HTML before being displayed to the user. You may use the python-markdown2 package to perform this conversion, installable via pip3 install markdown2.
    - Challenge for those more comfortable: If you’re feeling more comfortable, try implementing the Markdown to HTML conversion without using any external libraries, supporting headings, boldface text, unordered lists, links, and paragraphs. You may find using regular expressions in Python helpful.

## How to Run
In order to run the app, run the following commands in the root directory of the application.

```bash
    python -m venv .venv # you can use another virtual environment if you want (e.g.: virtualenv)
    source .venv/Scripts/activate # or source .venv/bin/activate for Linux users
    pip install -r requirements.txt
    python manage.py runserver
```

Now just access http://localhost:8000/.

## Submit Version Result
Here are the main pages required:

### Main Page

In the main page, you see a listing of all entries created so far.

![main page](/examples/main_page.jpg)

### Create Page

To create a new page, just add a title and insert some markdown to describe the entry.

![create page](/examples/new_page.jpg)

### Entry Page

The entry's page, shows it's Markdown contents parsed to HTML. It gives a options to edit or delete the page.

Note: the challenge to create your own parser was accepted :sunglasses:, however it's kinda limited :grimacing:.

![entry page](/examples/entry_page.jpg)

### Edit Page

The edit page is very similar to the create page.

![edit page](/examples/edit_page.jpg)

### Search Page
The search engine matches the preffixes of the titles as required.

![search page](/examples/search.jpg)

### Random Page
The random page works as expected, giving you a random entry page every time it's clicked :grin:.
