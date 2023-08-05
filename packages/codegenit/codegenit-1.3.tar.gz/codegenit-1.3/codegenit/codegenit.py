import os, sys
from argparse import ArgumentParser, RawTextHelpFormatter
from codegenit.codegen_package import CodegenPackage
from codegenit.project import Project
from codegenit.dyad import Dyad

def parse_args():
    """ Parse the cli args

        Returns:
            args (namespace): The args

    """
    # pwd = os.path.dirname(os.path.realpath(sys.argv[0]))
    # pwd = os.path.dirname(os.path.abspath(__file__))
    pwd = os.getcwd()
    parser = ArgumentParser(description='Generate a python project from a swagger file.',
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('-c', '--codegen_dir', action="store", dest="codegen_dir",
                        required=False,
                        help=("A folder in which to place the codegend project."
                              " (default: ./swagger_codegen/)"),
                        default="%s/swagger_codegen" % pwd)
    parser.add_argument('-p', '--project_dir', action="store", dest="project_dir",
                        required=False,
                        help="A folder in which to place the codegend project. (default: ./)",
                        default="%s" % pwd)
    parser.add_argument('-s', '--swagger_file', action="store", dest="swagger_file",
                        required=False,
                        help="A folder in which to place the codegend project. (default ./api.yml)",
                        default="%s/api.yml" % pwd)

    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    codegen_package = CodegenPackage(directory=args.codegen_dir,
                                     swagger_file=args.swagger_file)
    codegen_package.generate()

    current_project = Project(directory=args.project_dir)
    current_project.make_directory(directory='swagger_server', clobber=False)
    current_project.remove_trailing_whitespace()

    codegen_project = Project(directory=codegen_package.directory)
    codegen_project.remove_trailing_whitespace()

    dyad = Dyad(src=codegen_project, dst=current_project)
    dyad.copy_file(filen='requirements.txt', clobber=False)
    dyad.update_directory(directory='swagger_server', clobber=False)
    dyad.update_directory(directory='swagger_server/swagger', clobber=True)
    dyad.update_directory(directory='swagger_server/models', clobber=True)
    dyad.update_directory(directory='swagger_server/controllers', clobber=False)

if __name__ == '__main__':
    main()
