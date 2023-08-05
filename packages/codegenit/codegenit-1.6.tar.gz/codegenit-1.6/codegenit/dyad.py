import copy

import astor
import ast
import os
import shutil
from codegenit.print_in_color import PrintInColor

class Dyad(object):
    """ A class to update a dst with a src project
    """

    def __init__(self, src, dst):
        """ init the obj

        Args:
            src (Project): A src project
            dst (Project): A dst project

        """
        self.src = src
        self.dst = dst

    def copy_file(self, filen, clobber=False, check_mode=False):
        """ Copy a file

        Args:

            filen (str): The name of the file to copy
            clobber (bool): Clobber the destination
            check_mode (bool): Perforom or simply log

        """
        source = "%s/%s" % (self.src.directory, filen)
        destination = "%s/%s" % (self.dst.directory, filen)
        try:
            os.stat(source)
        except OSError:
            clobber = True
        if clobber:
            if not check_mode:
                shutil.copy(source, destination)
            PrintInColor.message(color='YELLOW', action="created", string=destination)

    def update_directory(self, directory, clobber=False, check_mode=False, update_args=False):
        """ update a directory from src to dst

        Args:
            directory (str): The directory to update between the Projects
            clobber (bool): Nuke the dst before updating
            check_mode (bool): Perforom or simply log
            update_args (bool): Update the args in the dest fn

        """
        source = "%s/%s" % (self.src.directory, directory)
        destination = "%s/%s" % (self.dst.directory, directory)
        if clobber:
            try:
                if not check_mode:
                    shutil.rmtree(destination)
                PrintInColor.message(color='YELLOW', action="deleted", string=destination)
            except OSError:
                pass
            if not check_mode:
                shutil.copytree(source, destination)
            PrintInColor.message(color='YELLOW', action="updated", string=destination)
        else:
            try:
                os.stat(destination)
            except OSError:
                PrintInColor.message(color='YELLOW', action="created", string=destination)
                if not check_mode:
                    os.mkdir(destination)
            for filen in os.listdir(source):
                if os.path.isfile("%s/%s" % (source, filen)):
                    try:
                        os.stat("%s/%s" % (destination, filen))
                        update_file(source=source, destination=destination,
                                    filen=filen, check_mode=check_mode,
                                    update_args=update_args)
                    except OSError:
                        if not check_mode:
                            source_tree = astor.code_to_ast.parse_file("%s/%s" % (source, filen))
                            source_tree = sort_defs(source_tree)
                            destination_contents = astor.to_source(source_tree)
                            with open("%s/%s" % (destination, filen), 'w') as fileh:
                                fileh.write(destination_contents)
                        PrintInColor.message(color='YELLOW', action="created",
                                             string="%s/%s" % (destination, filen))


def update_file(source, destination, filen, check_mode, update_args):
    """ update a python file

    Args:
        source (str): The source directory
        destination (str): The destination directory
        filen (str): The name of the file to be updated
        check_mode (bool): Perforom or simply log

    """
    source_tree = astor.code_to_ast.parse_file("%s/%s" % (source, filen))
    destination_tree = astor.code_to_ast.parse_file("%s/%s" % (destination, filen))
    for src_entry in source_tree.body:
        match = False
        for dst_entry in destination_tree.body:
            if astor.dump_tree(src_entry) == astor.dump_tree(dst_entry):
                match = True
                break
        if not match:
            if isinstance(src_entry, ast.Import):
                destination_tree = handle_import(destination_tree=destination_tree,
                                                 src_entry=src_entry)
            elif isinstance(src_entry, ast.ImportFrom):
                destination_tree = handle_import_from(destination_tree=destination_tree,
                                                      src_entry=src_entry)
            elif isinstance(src_entry, ast.FunctionDef):
                destination_tree = handle_function_def(filen=filen,
                                                       destination_tree=destination_tree,
                                                       src_entry=src_entry,
                                                       update_args=update_args)
            else:
                PrintInColor.message(color='RED', action="unhandled", string=filen)
                print("-> %s" % astor.to_source(src_entry))

    destination_tree = sort_defs(destination_tree)
    destination_contents = astor.to_source(destination_tree)
    with open("%s/%s" % (destination, filen)) as fileh:
        source_contents = fileh.read()
    if source_contents != destination_contents:
        PrintInColor.message(color='YELLOW', action="updated",
                             string="%s/%s" % (destination, filen))
        PrintInColor.diff(left=source_contents, right=destination_contents)
        if not check_mode:
            with open("%s/%s" % (destination, filen), 'w') as fileh:
                fileh.write(destination_contents)
    else:
        PrintInColor.message(color='GREEN', action="unmodified",
                             string="%s/%s" % (destination, filen))

def handle_import(destination_tree, src_entry):
    """ Add a missing import statement

    Args:
        destination_tree (ast): An ast generated from the destination file
        src_entry (ast node): An ast node found missing from the destination_tree

    """
    destination_tree.body.insert(0, src_entry)
    return destination_tree

def handle_import_from(destination_tree, src_entry):
    """ Add or modify a 'from' statement

    Args:
        destination_tree (ast): An ast generated from the destination file
        src_entry (ast node): An ast node found missing from the destination_tree

    """
    modified_import_from = False
    for i, dst_entry in enumerate(destination_tree.body):
        if isinstance(dst_entry, ast.ImportFrom):
            if dst_entry.module == src_entry.module:
                destination_tree.body[i] = src_entry
                modified_import_from = True
    if not modified_import_from:
        destination_tree.body.insert(0, src_entry)
    return destination_tree

def handle_function_def(filen, destination_tree, src_entry, update_args):
    """ Add or modify a 'def'

    Args:
        filen (str): The nname of the file being modified
        destination_tree (ast): An ast generated from the destination file
        src_entry (ast node): An ast node found missing from the destination_tree

    """
    found_by_name = False
    for i, dst_entry in enumerate(destination_tree.body):
        if isinstance(dst_entry, ast.FunctionDef):
            if dst_entry.name == src_entry.name:
                found_by_name = True
                if astor.to_source(dst_entry.args) != astor.to_source(src_entry.args):
                    if update_args:
                        dst_entry.args = src_entry.args
                    else:
                        log_src = copy.copy(src_entry)
                        log_src.body = []
                        log_dst = copy.copy(dst_entry)
                        log_dst.body = []
                        PrintInColor.message(color='RED', action="warning", string=filen)
                        PrintInColor.diff(left=astor.to_source(log_src),
                                          right=astor.to_source(log_dst),
                                          fromfile="Codegen package",
                                          tofile="Project")
                elif astor.to_source(dst_entry.body[0]) != astor.to_source(src_entry.body[0]):
                    if isinstance(src_entry.body[0], ast.Expr):
                        if isinstance(dst_entry.body[0], ast.Expr):
                            destination_tree.body[i].body[0] = src_entry.body[0]
                        else:
                            destination_tree.body[i].body.insert(0, src_entry.body[0])
    if not found_by_name:
        destination_tree.body.append(src_entry)
    return destination_tree

def sort_defs(destination_tree):
    """ Sort the fns in a tree

    Args:
        destination_tree (ast): An ast generated from the destination file

    Returns:
        destination_tree (ast): An ast generated from the destination file

    """
    defs = []
    for i in reversed(range(len(destination_tree.body))):
        if isinstance(destination_tree.body[i], ast.FunctionDef):
            defs.append(destination_tree.body[i])
            destination_tree.body.pop(i)
    defs = sorted(defs, key=lambda k: k.name)
    added = False
    for i in range(len(destination_tree.body)):
        if (not isinstance(destination_tree.body[i], ast.Import) and
                not isinstance(destination_tree.body[i], ast.ImportFrom)):
            destination_tree.body[i:i] = defs
            added = True
    if not added:
        destination_tree.body.extend(defs)
    return destination_tree
