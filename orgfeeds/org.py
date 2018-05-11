from PyOrgMode.PyOrgMode import OrgDataStructure, OrgDrawer
from PyOrgMode.PyOrgMode import OrgNode, OrgElement

import shutil


def load_file(path):
    base = OrgDataStructure()
    base.load_from_file(path)
    return base


def get_entries(feed_header):
    for entry in feed_header.content:
        if isinstance(entry, OrgElement) and entry.level == 2:
            yield entry


def get_feeds(doc):
    for feed_header in doc.root.content:
        if isinstance(feed_header, OrgElement):
            yield feed_header


def get_properties_drawer(header):
    for node in header.content:
        if (isinstance(node, OrgDrawer.Element) and
                node.name == 'PROPERTIES'):
            return node


def get_properties(header):
    drawer = get_properties_drawer(header)
    r = {}
    for property in drawer.content:
        r[property.name] = property.value
    return r


def make_entry_header(entry_id, title, link, datestr, new_tag):
    org_entry = OrgNode.Element()
    # NOTE: space at the end of the title is neccesary to
    # properly place the tag
    org_entry.heading = title + ' '
    org_entry.level = 2
    org_entry.tags = ['NEW']
    org_entry.todo = "UNREAD"

    _props = OrgDrawer.Element("PROPERTIES")
    _props.append(OrgDrawer.Property("ENTRY_ID", entry_id))
    _props.append(OrgDrawer.Property("LINK", link))
    _props.append(OrgDrawer.Property("DATE", datestr))
    org_entry.append_clean(_props)

    return org_entry


def save_file(doc, path):
    backup_path = path + '.bak'
    shutil.copyfile(path, backup_path)
    try:
        doc.save_to_file(path)
    except Exception as e:
        shutil.copyfile(backup_path, path)
        raise e
