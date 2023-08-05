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
    parser.add_argument('-u', '--update_args', action="store_true", dest="update_args",
                        required=False,
                        help=("Update the function arguments in the project_dir."
                              " (default: warn only)"))
    parser.add_argument('--check', action="store_true", dest="check_mode",
                        required=False,
                        help=("Run in check mode, no changes to PROJECT_DIR."
                              " (except trailing whitespace removal)"))

    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    codegen_package = CodegenPackage(directory=args.codegen_dir,
                                     swagger_file=args.swagger_file)
    codegen_package.generate()

    current_project = Project(directory=args.project_dir)
    current_project.make_directory(directory='swagger_server',
                                   clobber=False,
                                   check_mode=args.check_mode)
    current_project.remove_trailing_whitespace()

    codegen_project = Project(directory=codegen_package.directory)
    codegen_project.remove_trailing_whitespace()

    dyad = Dyad(src=codegen_project, dst=current_project)
    dyad.copy_file(filen='requirements.txt', clobber=False, check_mode=args.check_mode)
    dyad.update_directory(directory='swagger_server', clobber=False, check_mode=args.check_mode)
    dyad.update_directory(directory='swagger_server/swagger',
                          clobber=True,
                          check_mode=args.check_mode)
    dyad.update_directory(directory='swagger_server/models',
                          clobber=True,
                          check_mode=args.check_mode)
    dyad.update_directory(directory='swagger_server/controllers',
                          clobber=False,
                          check_mode=args.check_mode,
                          update_args=args.update_args)

if __name__ == '__main__':
    main()
