import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(
                sorted( re.sub(r"\.md$", "", filename) for filename in filenames if filename.endswith(".md"))
                )


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

# -------------------------------------------------------------------------------------------------------------
# My functions
def delete_entry(title):
    """
    Delete entry by the title given
    """
    try:
        f = default_storage.delete(f"entries/{title}.md")
        return True
    except FileNotFoundError:
        return False

def suffix_search(title):
    """
    Retrieves encyclopedia entries by a suffix match.
    """
    _, filenames = default_storage.listdir("entries")

    searchResults = list(
                        re.sub(r"\.md$", "", filename) for filename in filenames if re.match(title, filename) is not None
                        )
    return searchResults

def save_in_storage(md_file, title):
    f = open(f"entries/{title}.md", "w")
    f.write(md_file)
    f.close()

def md_to_html(md_file, title):
    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Auxiliary functions
    
    def link_md_to_html(link_md, k):
        not_link_value_aux = k # saving original value of k (i.e. 'i' from the main loop) in case it's not a link
        k += 1 # Continue after the '['
        link_value = ""

        while k+1 < len(link_md) and link_md[k] != "\n":
            # Looking for boldtext inside link's value
            if (link_md[k] == '*' and link_md[k+1] == '*') or (char == '-' and link_md[k+1] == '-'):	
                strong, num_jumps = strong_md_to_html(link_md[k:])
                link_value += strong
                k += num_jumps

            # Looking for the end of the link's value and begining of it's href
            elif link_md[k] == ']' and link_md[k+1] == '(':
                md_href = ""
                k += 1 # So it can start at '('

                while link_md[k-1] != ')': # k-1 to concatenate ')' too
                    md_href += link_md[k]
                    k += 1

                link_p = re.compile(r"(\(https?://(www\.)?\w+\.\w+\)|\([^\)]+\)|\([^\)]+\))")

                # maybe this match is not really necessary but it gives m and n (have to think about it)
                if (link_match := link_p.match(md_href)): 
                    m, n = link_match.span()
                    
                    return ("<a href=\"" + md_href[m+1:n-1] + "\">" + link_value + "</a>", k-1)
                break
            else:
                link_value += link_md[k] # Acumulates until it finds "](" or not
             
            k += 1	
        
        return ("", not_link_value_aux-1) # just returns the text 

    def strong_md_to_html(strong_content_md):
        strong_p = re.compile(r"(\*\*[^*]+\*\*|--[^*]+--)")

        # Looking for a boldtext match
        if (strong_match := strong_p.match(strong_content_md)): 
            m, n = strong_match.span()
            
            return ("<strong>" + strong_content_md[m+2:n-2] + "</strong>", len(strong_content_md[m:n])-1)

        return ("**", 1)

    def header_md_to_html(header_md):
        # Pattern objects
        h1_p = re.compile(r"#\s+")
        h2_p = re.compile(r"##\s+")
        h3_p = re.compile(r"###\s+")
        h4_p = re.compile(r"####\s+")
        h5_p = re.compile(r"#####\s+")
        h6_p = re.compile(r"######\s+")
        hx_content_p = re.compile(r"[^\n]+(\n|$)", re.M) # Conteudo de um header
        
        if (hx_match:=h1_p.match(header_md)):
            num = 1
        elif (hx_match:=h2_p.match(header_md)):
            num = 2
        elif (hx_match:=h3_p.match(header_md)):
            num = 3
        elif (hx_match:=h4_p.match(header_md)):
            num = 4
        elif (hx_match:=h5_p.match(header_md)):
            num = 5
        elif (hx_match:=h6_p.match(header_md)):
            num = 6
    
        if (hx_match):
            _, n = hx_match.span()
            after_header = header_md[n:] # Getting everything after the #
            if (match_obj := hx_content_p.match(after_header)): 
                k, l = match_obj.span()
                header_content_md = after_header[k:l] # Getting actual header content

                # Looking for boldtext and links inside header
                is_header_content = False
                j = 0
                header_content_html = ""
                while j+1 < len(header_content_md): # To ignore the '\n'
                    char = header_content_md[j]
                    
                    if (char == "*" and header_content_md[j+1] == '*') or (char == '-' and header_content_md[j+1] == '-'):
                        strong_content, num_jumps = strong_md_to_html(header_content_md[j:]) 
                        header_content_html += strong_content 
                        
                        j += num_jumps
                    elif char == "[" and is_header_content == False:
                        link, aux = link_md_to_html(header_content_md, j)
                        
                        if aux == j-1:
                            is_header_content = True
                        else:
                            header_content_html += link	
                        j = aux
                    else:
                        header_content_html += char
                        is_header_content = False

                    j += 1
                
            return f"<h{num}>" + header_content_html + f"</h{num}>\n"
        else:
            return "\\\\"

    def ul_md_to_html(ul_md):
        ul_html = "<ul>\n"

        is_li_content = False
        li_html = "\t<li>"
        k = 0
        while k+1 < len(ul_md):
            c = ul_md[k]

            # If it reaches a break line without another list item symbol 
            # it means that's end of the list
            if c == '\n' and (ul_md[k+1] != "-" or ul_md[k+1] != "*"):
                li_html += "</li>\n"
                return "<ul>\n" + li_html + "</ul>\n", k
            elif k+2 == len(ul_md):
                li_html += c + ul_md[k+1] + "</li>\n"
                return "<ul>\n" + li_html + "</ul>\n", k+2
            elif c == '\n' and ul_md[k+1] == '-':
                li_html += "</li>\n\t<li>"
            elif (c == '*' and ul_md[k+1] == '*') or (c == '-' and ul_md[k+1] == '-'):
                strong, num_jumps = strong_md_to_html(ul_md[k:]) 
                li_html += strong
                k += num_jumps
            elif c == '[' and is_li_content == False:
                link, aux = link_md_to_html(ul_md, k)
    
                # if the value returned it's equal to k-1, it means it's not a link but a li content
                if aux == k-1:
                    is_li_content = True
                else:
                    li_html += link	
                k = aux		
            else:
                if c != '-' and c != '*':
                    li_html += c
                is_li_content = False

            k += 1
    
    def p_md_to_html(p_md):
        p_html = "<p>"

        not_link = False
        k = 0
        while k+1 < len(p_md) and p_md[k] != "\n":
            c = p_md[k]

            if (c == '*' and p_md[k+1] == '*') or (c == '-' and p_md[k+1] == '-'):
                strong, num_jumps = strong_md_to_html(p_md[k:]) 
                p_html += strong
                k += num_jumps
            elif c == '[' and not_link == False:
                link, aux = link_md_to_html(p_md, k)
    
                # if the value returned it's equal to k-1, it means it's not a link but a paragraph content
                if aux == k-1:
                    not_link = True
                else:
                    p_html += link	
                k = aux		
            else:
                p_html += c
                not_link = False

            k += 1

        # Obs.: In the main while loop, in order to check if it's a strong tag or just an ul tag 
        # I check the current charactere '*' and the next to make sure. However, by checking the next charactere
        # it's possible to reach and index out of range (e.g. if there's a '-' charactere at the very end of input file)
        # Therefore, the last character gets left out of the final html file, so in case the last tag is a paragraph
        # and contains a * ou - in the end of the string, that's why it's being concatened here (p_md[k])
        if p_md[k] != "\n":
            return p_html + p_md[k] + "</p>", k-1
        else:
            return p_html + "</p>", k-1
    # ---------------------------------------------------------------------------------------------------------------------------------------
    # 
    html_file = '''{% extends \"encyclopedia/layout.html\" %}

{% block title %}
    ''' + "{{ title }}" + '''
{% endblock %}

{% block body %}
    '''

    # Main loop to analyse the file
    isparagraph = False
    i = 0
    while i+1 < len(md_file):
        char = md_file[i]

        if char == '#':
            html_file += header_md_to_html(md_file[i:])

            while i < len(md_file)-1 and md_file[i] != "\n": # To continue from where the header ends
                i += 1

        elif (char == '*' and md_file[i+1] == '*') or (char == '-' and md_file[i+1] == '-'):
            strong, num_jumps = strong_md_to_html(md_file[i:]) 
            html_file += strong
            i += num_jumps 
        
        elif char == '[' and isparagraph == False:
            link, aux = link_md_to_html(md_file, i)
            
            # if the value returned it's equal to i-1, it means it's not a link but a paragraph
            if aux == i-1:
                isparagraph = True
            else:
                html_file += link
            i = aux

        elif char == '-' or char == '*':
            ul, num_jumps = ul_md_to_html(md_file[i:])
            html_file += ul

            i += num_jumps
        else:
            # If the character comes after a break line or if the paragraph is the first thing on file
            if (md_file[i-1] == "\n" and char != "\n") or re.match(r"^.", char):
                paragraph, num_jumps = p_md_to_html(md_file[i:])
                html_file += paragraph
                i += num_jumps
                isparagraph = False
            elif char != "\n":
                html_file += char

        i += 1

    html_file += '''
{% endblock %}

{% block nav %}
    <a href="{% url 'editpage' title %}">Edit Page</a><br>
    <a href="{% url 'deletepage' title %}">Delete Page</a>
{% endblock %}'''

    f = open("encyclopedia/templates/encyclopedia/entry.html", "w")
    f.write(html_file)
    f.close()

    # return html_file
