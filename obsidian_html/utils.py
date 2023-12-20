import regex as re
import os
import sys


def slug_case(text):
    text = text.replace(".", "dot")
    text = text.replace("_", "-")
    return re.sub(r'[^\w\-/]+', '-', text).lower()


def md_link(text, link):
    return "[" + text + "](" + link + ")"


def find_files(vault_root, extra_folders, no_extension=False):
    # Find all markdown-files in vault root.
    md_files = []
    
    for root, dirs, files in os.walk(vault_root):
        for directory in dirs:
            #print(os.path.join(root, directory))
            md_files += find_md_files(os.path.join(root, directory), no_extension, is_extra_folder=False)

    # Find all markdown-files in each extra folder.
    for folder in extra_folders:
        md_files += find_md_files(os.path.join(vault_root, folder),
                                  no_extension, is_extra_folder=True)

    return md_files


def find_md_files(root, no_extension, is_extra_folder=False):
    md_files = []
    for md_file in os.listdir(root):
        if not md_file.endswith(".md"):
            continue

        with open(os.path.join(root, md_file), encoding='utf-8') as f:
            content = f.read()

        if no_extension:
            md_file = md_file.replace(".md", "")

        if is_extra_folder:
            md_file = os.path.join(os.path.split(root)[-1], md_file)
        
        # TODO: Support both Windows & UNIX file structures
        md_file = root + "\\" + md_file
        md_file = md_file.replace("../", "")
        # Split the path into parts
        parts = md_file.split('\\')
        # Remove the first directory and rejoin the remaining parts
        md_file = '\\'.join(parts[1:])
        md_files.append({"filename": md_file, "content": content})

    return md_files


def extract_links_from_file(document):
    matches = re.finditer(r"\[{2}([^\]]*?)[|#\]]([^\]]*?)\]+", document)

    links = []
    for match in matches:
        link = match.group(1)
        links.append(link)

    return links


def find_backlinks(target_note_name, all_notes):
    backlinks = []
    for note in all_notes:
        links = extract_links_from_file(note["content"])
        if target_note_name in links:
            backlinks.append({"text": note["filename"].replace(".md", ""),
                              "link": slug_case(note["filename"].replace(".md", ""))})

    backlinks = sorted(backlinks, key=lambda x: x['text'])

    return backlinks
