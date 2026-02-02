import json
import xml.etree.ElementTree as ET

XML_PATH = "static/data/tree/main.xml"
OUTPUT_PATH = "src/lib/data/tree-data.json"


def convert_xml_to_json():
    tree = ET.parse(XML_PATH)
    root = tree.getroot()

    nodes_data = []
    for node_element in root.findall(".//node"):
        node_id = node_element.get("id")
        title = (
            node_element.find("title").text
            if node_element.find("title") is not None
            else ""
        )

        body_element = node_element.find("body")
        body_content = ""
        if body_element is not None:
            # Serialize child elements of body to string
            body_content = "".join(
                ET.tostring(e, encoding="unicode", method="html") for e in body_element
            )

        children_refs = [
            child.get("ref") for child in node_element.findall("children/child")
        ]

        nodes_data.append(
            {
                "id": node_id,
                "title": title,
                "body": body_content,
                "children": children_refs,
            }
        )
    ids = set(n["id"] for n in nodes_data)
    childids = set()
    missing = set()
    childlesses = []
    for n in nodes_data:
        for c in n["children"]:
            childids.add(c)
            if c not in ids:
                missing.add(c)
        if not n["children"]:
            childlesses.append(n["id"])
    dangling = ids - childids
    if missing or len(dangling) > 1:
        print(
            f"{missing} ids are not defined\n{dangling} are dangling\n{childlesses} are childless"
        )
        return

    with open(OUTPUT_PATH, "w") as f:
        json.dump(nodes_data, f, indent=2)
    print(f"Successfully converted {XML_PATH} to {OUTPUT_PATH}")


if __name__ == "__main__":
    convert_xml_to_json()
