import subprocess
import sys
import os

from collections import namedtuple

from tkinter.messagebox import showinfo
from thonny import get_workbench
from thonny.running import get_front_interpreter_for_subprocess

name = "thonny-black-formatter"

ErrorMessage = namedtuple("ErrorMessage", ["error_type", "description"])  # NOSONAR

SUCCESS = "All done!"

NO_TEXT_TO_FORMAT = ErrorMessage("Nothing to do here", "There is no text to format.")
PACKAGE_NOT_FOUND = ErrorMessage(
    "Package not found",
    "Could not find Black package. Is it installed and on your PATH?",
)
NOT_COMPATIBLE = ErrorMessage(
    "File not compatible!",
    "Looks like this is not a python file. Did you already save it?",
)


class BlackFormat:
    """
    Apply black format to the current loaded file.

    Using subprocess, black is executed to format .py files displayed in
    Thonny. Whenever this plugin is executed, format_black is called. Depending
    on the result, final_title and final_message is displayed through
    tkinter.messagebox.showinfo().
    """

    def __init__(self) -> None:
        """Get the workbench to be later used to detect the file to format."""
        self.workbench = get_workbench()

    def prepare_run_environment(self):
        plugins_folders = [folder for folder in sys.path if "plugins" in folder]
        plugins_folder = os.path.join(plugins_folders[0])
        binfolder = plugins_folder.replace("lib/python/site-packages", "bin")

        os.environ["PYTHONPATH"] = plugins_folder + (
            ":" + os.environ["PYTHONPATH"] if os.environ["PYTHONPATH"] else ""
        )
        os.environ["PATH"] = binfolder + ":" + plugins_folder + ":" + os.environ["PATH"]

    def format_black(self) -> None:
        """Handle the plugin execution."""
        self.editor = self.workbench.get_editor_notebook().get_current_editor()

        try:
            self.filename = self.editor.get_filename()
        except AttributeError:
            final_title = NO_TEXT_TO_FORMAT.error_type
            final_message = NO_TEXT_TO_FORMAT.description
        else:
            if self.filename is not None and self.filename[-3:] == ".py":
                self.editor.save_file()

                self.prepare_run_environment()

                format_code = subprocess.run(
                    [
                        get_front_interpreter_for_subprocess(),
                        "-m",
                        "black",
                        self.filename,
                    ],
                    capture_output=True,
                    text=True,
                )

                if format_code.stderr.find("No module named black") != -1:
                    final_title = PACKAGE_NOT_FOUND.error_type
                    final_message = PACKAGE_NOT_FOUND.description
                else:
                    # Emojis are not supported in Tkinter.
                    message_without_emojis = format_code.stderr.encode(
                        "ascii", "ignore"
                    ).decode()
                    if format_code.returncode != 0:
                        """
                        Black error message structure:
                            1. error: cannot format file_name.py: ... (Error detail)
                            2. Oh no!
                            3. 1 file failed to reformat.
                        """

                        final_title = "Oh no!"
                        final_message = "\n".join(
                            message_without_emojis.splitlines()[::2]
                        )

                        final_message = final_message[0].upper() + final_message[1:]

                    else:
                        self.editor._load_file(self.filename, keep_undo=True)

                        """
                        Black success message structure:
                            A) When a file is reformatted:
                                1. reformatted file_name.py
                                2. All done!
                                3. 1 file reformatted.
                            * A.1 is not shown in final_message.

                            B) When the file is not changed:
                                1. All done!
                                2. 1 file left unchanged.
                        """

                        final_title = "All done!"
                        final_message = message_without_emojis.splitlines()[-1]

            else:
                final_title = NOT_COMPATIBLE.error_type
                final_message = NOT_COMPATIBLE.description

        showinfo(title=final_title, message=final_message)

    def load_plugin(self) -> None:
        """
        Load the plugin on runtime.

        Using self.workbench.add_command(), the plugin is registered in Thonny
        with all the given arguments.
        """
        self.workbench.add_command(
            command_id="format_black",
            menu_name="tools",
            command_label="Format with Black",
            handler=self.format_black,
            default_sequence="<Control-Alt-c>",
            extra_sequences=["<<CtrlAltCInText>>"],
        )


if get_workbench() is not None:
    run = BlackFormat().load_plugin()
