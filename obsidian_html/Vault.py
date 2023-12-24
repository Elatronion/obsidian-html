import os
import shutil
from utils import find_files, slug_case, find_backlinks, md_link
from format import htmlify


class Vault:
    def __init__(self, vault_root, extra_folders=[], html_template=None):
        self.vault_root = vault_root
        self.notes = find_files(vault_root, extra_folders, no_extension=True)
        self.extra_folders = extra_folders
        self._add_backlinks()

        self.html_template = html_template
        if html_template:
            with open(html_template, encoding='utf-8') as f:
                self.html_template = f.read()

    def _add_backlinks(self):
        for note in self.notes:
            backlinks = find_backlinks(note["filename"], self.notes)
            if backlinks:
                note["content"] += "\n<div class=\"backlinks\" markdown=\"1\">\n## Backlinks\n\n"
                for backlink in backlinks:
                    note["content"] += f"- {md_link(backlink['text'], backlink['link'])}\n"
                note["content"] += "</div>"

    def directory_depth_to_root(self, path):
        # Count the number of forward slashes in the path
        depth = path.count('\\')
        
        # Generate the string with "../" repeated for each depth level
        return '../' * depth if depth > 0 else './'  # './' represents the current directory
    
    def create_directory_if_not_exists(self, directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Created directory: {directory_path}")
        else:
            print(f"Directory already exists: {directory_path}")

    def convert_to_html(self):
        notes_html = []
        for note in self.notes:
            filename_html = note["filename"] + ".html"
            content_html = htmlify(note["content"])

            notes_html.append(
                {"filename": filename_html, "content": content_html, "title": note["filename"]})

        return notes_html

    def copy_files(self, src_dir, dest_dir):
        for root, dirs, files in os.walk(src_dir):
            # Calculate the relative path from the source directory
            relative_path = os.path.relpath(root, src_dir)
            # Create the corresponding directory in the destination
            dest_path = os.path.join(dest_dir, relative_path)
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
    
            for file in files:
                # Skip files ending with .md
                if file.endswith('.md'):
                    continue
    
                # Copy the file to the new location
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_path, file)
                shutil.copy(src_file, dest_file)

    def export_html(self, out_dir):
        # Default location of exported HTML is "html"
        if not out_dir:
            out_dir = os.path.join(self.vault_root, "html")
        # Ensure out_dir exists, as well as its sub-folders.
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        for folder in self.extra_folders:
            if not os.path.exists(out_dir + "\\" + folder):
                os.makedirs(out_dir + "\\" + folder)

        notes_html = self.convert_to_html()

        for note in notes_html:
            if self.html_template:
                html = self.html_template.format(
                    title=note["title"], content=note["content"])
            else:
                html = note["content"]
            
            # Create the directory if it doesn't exist
            output_path = os.path.join(out_dir, note["filename"])
            output_path = output_path.replace(self.vault_root, "", 1)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            #file_path_encoded = os.path.join(out_dir, note["filename"]).encode('utf-8', 'replace').decode('utf-8')
            html_file_path = os.path.join(out_dir, note["filename"])
            html_file_path = html_file_path.replace("\\", "/")
            directory_path = os.path.dirname(html_file_path)
            self.create_directory_if_not_exists(directory_path)
            print("Writing file : " + html_file_path)
            
            with open(html_file_path, "w", encoding='utf-8') as f:
                f.write(html)
            
        self.copy_files(self.vault_root, out_dir)
