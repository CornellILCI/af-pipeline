""" 

This module is written as workaround for resolving some known
invalid tags in asreml result. This module is a temporary one which should be definitely
decomissioned and thrown away when Vsni fixes the issues with their asreml result xml file.

"""

def resolve_unmatched_tags(xml_file: str) -> str:
    resolved_xml_string = ""
    with open(xml_file, "r") as f:
        is_xml_definition = False
        in_start_tag = False
        in_end_tag = False
        tag = ""
        end_tag = ""
        value = ""
        tag_stack = []
        c = f.read(1)
        while c:
            if c == "<":
                c = f.read(1)
                if c == "/":
                    in_end_tag = True
                elif c == "?":
                    is_xml_definition = True
                else:
                    in_start_tag = True
                    tag += c
                pass
            elif is_xml_definition and c == "?":
                c == f.read(1)
                if c == ">":
                    is_xml_definition = False
                pass
            elif not in_start_tag and c == "":
                pass
            elif in_start_tag and c != ">":
                tag += c
            elif in_start_tag and c == ">":
                in_start_tag = False
                tag_stack.append(tag)
                resolved_xml_string += f"<{tag.strip()}>"
                tag = ""
            elif in_end_tag and c != ">":
                end_tag += c
            elif in_end_tag and c == ">":
                start_tag = tag_stack.pop()
                if start_tag.strip() != end_tag.strip():
                    if start_tag == "PredictTable" and end_tag == "Prow":
                        end_tag = ""
                        in_end_tag = False
                        tag_stack.append(start_tag)
                        continue
                    elif start_tag == "Prow" and end_tag == "PredictTable":
                        resolved_xml_string += "</Prow>"
                resolved_xml_string += f"{value.strip()}</{end_tag.strip()}>"
                value = ""
                end_tag = ""
                in_end_tag = False
            else:
                value += c
            c = f.read(1)
    return resolved_xml_string
