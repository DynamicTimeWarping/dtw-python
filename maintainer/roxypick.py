#!/usr/bin/env python3
"""
roxypick.py - Roxygen to Python Documentation Converter

This script automates the process of converting R package documentation (roxygen comments)
to Python docstrings, maintaining consistency between the R and Python versions of the dtw package.

Logic Overview:
1. Parse R source files in ../dtw/R/ using roxygen2 to extract structured documentation
2. Convert R-specific syntax to Python equivalents (e.g., TRUE/FALSE -> True/False, . -> _)
3. Transform roxygen tags into RST-formatted docstrings with sections like Parameters, Returns, etc.
4. Generate Python example files from R examples by converting R syntax to Python
5. Process Python files in dtw/ directory, replacing IMPORT_RDOCSTRING placeholders with converted docstrings

Usage:
- Run this script from the dtw-python root directory
- Requires rpy2, pypandoc, and roxygen2 R package
- Input: R files with roxygen documentation in ../dtw/R/
- Output: Updated Python files with docstrings, example drafts in maintainer/examples/

The script preserves the original Python files by creating backups with ~ suffix before modification.

Run with:   uv run --with rpy2 --with pypandoc maintainer/roxypick.py
"""

from rpy2.robjects.packages import importr

import glob
import re
import os
import pypandoc



# ==================================================
# Misc functions

def indent_as(l):
    """Extract the indentation (whitespace) before the first '#' character in a line.
    
    Used to preserve indentation when inserting docstrings into Python code.
    
    Args:
        l (str): The line of code containing a comment marker
        
    Returns:
        str: The whitespace characters before the '#' symbol
    """
    c = l.find('#')
    return l[:c]

def dot_underscore(s):
    """Convert R naming conventions to Python equivalents.
    
    Replaces dots with underscores in identifiers and converts R boolean
    literals (TRUE/FALSE) to Python (True/False).
    
    Args:
        s (str): String containing R-style identifiers
        
    Returns:
        str: String with Python-style identifiers
    """
    rex = r"([a-zA-Z])\.([a-zA-Z])"
    s = re.sub(rex,r"\1_\2",s)
    s = s.replace("TRUE","True")
    s = s.replace("FALSE","False")
    return s

def sanitize_rd_commands(s):
    """Convert R documentation (Rd) markup commands to markdown equivalents.
    
    Handles common Rd commands like \\url{} and \\doi{} by converting them
    to appropriate markdown/link formats.
    
    Args:
        s (str): String containing Rd markup commands
        
    Returns:
        str: String with markdown-formatted links
    """
    import re
    s = re.sub('\\\\url{(.+?)}','<\\1>',s)
    s = re.sub('\\\\doi{(.+?)}','[doi:\\1](https://doi.org/\\1)',s)
    return s



def unarrow(s):
    """Convert R assignment operator to Python assignment operator.
    
    Replaces R's <- with Python's = for code examples.
    
    Args:
        s (str): String containing R assignment operators
        
    Returns:
        str: String with Python assignment operators
    """
    s=s.replace("<-"," = ")
    return s


def getParameters(k):
    """Format parameter documentation from roxygen tags into RST format.
    
    Extracts parameter names and descriptions from the parsed roxygen data
    and formats them as a Parameters section in RST (reStructuredText) format.
    
    Args:
        k (dict): Dictionary containing parsed roxygen documentation tags
        
    Returns:
        str: Formatted parameter documentation in RST format, or empty string if no parameters
    """
    o=[]

    if "param" not in k:
        return ""
    
    for p in k['param']:
        pn = dot_underscore(p.rx2('name')[0])
        pd = dot_underscore(p.rx2('description')[0])
        pd = pd.replace("\n"," ")
        o.append(pn + " : ")
        o.append( "    " + pd )
    if len(o) > 0:
        out =  "Parameters\n"
        out += "----------\n"
        out += ("\n".join(o))
        return out
    else:
        return ""



def p(k,w,h=None):
    """Extract and format a documentation section from roxygen data.
    
    Retrieves a specific section (like 'title', 'description', etc.) from the
    parsed roxygen dictionary, converts it to RST format using pandoc, and
    optionally adds a header.
    
    Args:
        k (dict): Dictionary containing parsed roxygen documentation tags
        w (str): The section name to extract (e.g., 'title', 'description')
        h (str, optional): Header text to add above the section
        
    Returns:
        str: Formatted documentation section in RST format, or empty string if section not found
    """
    try:
        txt = "\n".join(k[w])
        txt = dot_underscore(txt)
        txt = sanitize_rd_commands(txt)
        txt_m = pypandoc.convert_text(txt,'rst',format="md")
        out = ""
        if h is not None:
            out = h + "\n"
            out += ("-" * len(h)) + "\n\n"
        out += txt_m + "\n\n"
        return out
    except:
        return ""


    
def getdoc(n):
    """Generate a complete Python docstring from parsed roxygen documentation.
    
    Assembles all documentation sections (title, description, details, parameters,
    returns, notes, references, examples) into a properly formatted Python docstring.
    
    Args:
        n (str): Function name to generate documentation for
        
    Returns:
        str: Complete Python docstring with all available documentation sections
    """
    k=roxy[n]

    o=f"""\"\"\"{p(k,'title')}

{p(k,'description')}

**Details**

{p(k,'details')}

{getParameters(k)}

{p(k,'return','Returns')}

{p(k,'note','Notes')}

{p(k,'references','References')}

{getex(n)}
\"\"\"
"""
    o=sanitize_whitespace(o)
    return o

def sanitize_whitespace(o):
    """Clean up excessive whitespace in documentation strings.
    
    Removes duplicated empty lines to ensure clean, readable formatting
    in the generated docstrings.
    
    Args:
        o (str): Documentation string that may contain excessive whitespace
        
    Returns:
        str: Documentation string with normalized whitespace
    """
    return re.sub(r'\n\s*\n', '\n\n', o)


def convex(txt):
    """Convert R example code to Python interactive session format.
    
    Transforms R code examples by:
    - Converting comments (## -> #)
    - Converting R syntax to Python (dots, booleans, assignment)
    - Adding >>> prompts for interactive examples
    - Preserving empty lines as paragraph breaks
    
    Args:
        txt (str): R code example as a string
        
    Returns:
        str: Python-formatted example code with >>> prompts
    """
    o = []
    for l in txt.split("\n"):
        if l.startswith("##"):
            l = l.replace("#","")
            l = l.lstrip()
        elif re.match(r'^ *$',l):
            l = "\n"
        else:
            l = l.lstrip()
            l = dot_underscore(l)
            l = unarrow(l)
            l = ">>> "+l
        o.append(l)
    return "\n".join(o)


def getex(n):
    """Retrieve pre-processed Python examples for a function.
    
    Reads the Python example file (ex_{n}.py.txt) from the maintainer/examples
    directory and formats it as an Examples section for the docstring.
    
    Args:
        n (str): Function name to get examples for
        
    Returns:
        str: Formatted Examples section, or empty string if no examples found
    """
    o=""
    try:
        with open(f"maintainer/examples/ex_{n}.py.txt") as f:
            o =  "Examples\n"
            o += "--------\n"
            o += f.read()
            o += "\n\n"
    except:
        print(f"No examples for {n}")
    return o



# ========================================
# ========================================




def parse_roxygen_headers():
    """Parse R source files and extract roxygen documentation.
    
    Scans all .R files in the ../dtw/R/ directory using roxygen2 to extract
    structured documentation. Builds a global dictionary (roxy) mapping function
    names to their parsed documentation tags.
    
    The parsing handles different roxygen versions and extracts tags like
    @title, @description, @param, @return, @examples, etc. Functions are
    identified by their alias or @name tag.
    
    Returns:
        dict: Dictionary mapping function names to their documentation data
    """
    global roxy
    roxy = {}
    
    # For roxygen 7.1.1 this became elts[0].rx2("tags")[2].rx2("val")
    rlist = glob.glob("../dtw/R/*.R")
    r2 = importr("roxygen2")
    
    for rfile in rlist:
        print(f"Parsing {rfile}...")
        
        elts = r2.parse_file(rfile)
        for i, k in enumerate(elts):
            tagdict = {}
            for tag_r in k.rx2("tags"):
                tag = tag_r.rx2("tag")[0]
                val = tag_r.rx2("val")
                if tag not in tagdict:
                    tagdict[tag] = []
                if tag == "param":
                    tagdict[tag].append(val)
                else:
                    tagdict[tag].append(val[0])
            
            # Extract function name from alias or @name tag
            try:
                ex = k.rx2('object').rx2('alias')[0]
                wh = "alias"
            except:
                try:
                    ex = tagdict['name'][0]
                    wh = "@name"
                except:
                    print(f"  {i} NOT FOUND")
                    continue
            
            print(f"  {i} found {wh}... " + ex)
            roxy[ex] = tagdict
    
    print("\n\n")
    return roxy



def write_examples():
    """Generate example files from R documentation.
    
    For each function with examples in the roxygen data, creates:
    1. Raw R example file (ex_{name}.R)
    2. Python draft example file (ex_{name}.py.draft) with converted syntax
    
    Uses the convex() function to convert R syntax to Python interactive format.
    """
    for k in roxy:
        try:
            ex = roxy[k]["examples"][0]
        except:
            continue
        
        # Write raw R example
        with open(f"maintainer/examples/ex_{k}.R", "w") as f:
            print(f"Writing example: {k}")
            f.write(ex)
        
        # Write Python draft with converted syntax
        with open(f"maintainer/examples/ex_{k}.py.draft", "w") as f:
            print(f"Writing draft: {k}")
            f.write(convex(ex))
    
    print("\n\n")


def process_python_files():
    """Update Python source files with generated docstrings.
    
    Scans all .py files in the dtw/ directory for IMPORT_RDOCSTRING placeholders.
    For each placeholder found, replaces it with the corresponding generated
    docstring while preserving indentation.
    
    Creates backup files with ~ suffix before modification. Skips to ENDIMPORT
    tag after inserting docstring to avoid processing the placeholder content.
    """
    plist = glob.glob("dtw/*.py")
    
    for pfile in plist:
        print(f"Modifying {pfile}...")
        
        # Create backup
        pfile_back = pfile + "~"
        os.rename(pfile, pfile_back)
        
        with open(pfile_back, "r") as fin, open(pfile, "w") as fout:
            for l in fin:
                if "IMPORT_RDOCSTRING" in l:
                    fout.write(l)  # Copy the tag
                    
                    # Preserve indentation for docstring
                    fout.write(indent_as(l))
                    
                    # Extract function name and insert docstring
                    n = l.split()[2]
                    print(f" Inserting {n}")
                    ds = getdoc(n)
                    fout.write(ds)
                    
                    # Skip until ENDIMPORT tag
                    while True:
                        l = fin.readline()
                        if "ENDIMPORT" in l:
                            fout.write(l)
                            break
                else:
                    fout.write(l)


def main():
    """Main execution function coordinating the documentation conversion process.
    
    Orchestrates the three main phases:
    1. Parse R documentation from source files
    2. Generate example files in both R and Python formats
    3. Update Python source files with converted docstrings
    
    This maintains consistency between R and Python versions of the dtw package
    by automatically syncing documentation and examples.
    """
    parse_roxygen_headers()
    write_examples()
    process_python_files()


# ========================================
# Script execution
# ========================================

roxy = {}
pyex = {}

if __name__ == "__main__":
    main()
