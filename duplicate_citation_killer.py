import xml.etree.ElementTree as ET
import re

def clean_title(title):
    cleaned_title = re.sub(r'[^\w]', '', title).strip().lower()
    return cleaned_title

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    titles = {}
    duplicates = []
    readable_duplicates = []

    for record in root.findall('./records/record'):
        title_element = record.find('titles/title')
        title = re.sub(r'[^\w]', '', title_element.text).strip().lower()
        readble_title = re.sub(r'[\n]', '', title_element.text).strip().lower()

        if title in titles:
            if title not in duplicates:
                duplicates.append(title)
                readable_duplicates.append(readble_title)
        else:
            titles[title] = True

    return readable_duplicates


def remove_duplicates(file_path, output_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Build a set of unique titles
    unique_titles = set()

    # Construct a new XML tree containing only non-duplicate nodes
    new_root = ET.Element(root.tag)
    records_element = ET.SubElement(new_root, 'records')

    for record in root.findall('./records/record'):
        title_element = record.find('titles/title')
        title = re.sub(r'[^\w]', '', title_element.text).strip().lower()

        # Add the title if is new to the tree
        if title not in unique_titles:
            records_element.append(record)
            unique_titles.add(title)

    # Building a new XML tree with the new root
    new_tree = ET.ElementTree(new_root)

    # Write the tree to the output file
    new_tree.write(output_path)


if __name__ == "__main__":
    input_file_path = "input.xml"
    output_file_path = "output.xml"

    duplicates = parse_xml(input_file_path)

    num_duplicates = len(duplicates)
    if num_duplicates > 0:
        print(f"\n {num_duplicates} duplicate titles have been found:\n")
        i = 1
        for i in range(0, num_duplicates):
            print(f"{i+1}: {duplicates[i]}")
        
        remove_duplicates(input_file_path, output_file_path)
        print(f"\nFile {output_file_path} has been created without duplicates\n")

    else:
        print(f"No duplicate titles found")