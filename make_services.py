"""Create the PejWrite right-click Quick Action in ~/Library/Services.

It pipes the selected text to rewrite.py, which asks what to do and prints
the result; the output replaces the selection. Re-run after moving this folder.
"""

import plistlib
import shlex
import shutil
import subprocess
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
PYTHON = HERE / ".venv" / "bin" / "python"
SERVICES = Path.home() / "Library" / "Services"

# menu title -> rewrite.py mode
ACTIONS = {
    "PejWrite": "menu",
}


def info_plist(title):
    return {
        "NSServices": [{
            "NSBackgroundColorName": "background",
            "NSIconName": "NSActionTemplate",
            "NSMenuItem": {"default": title},
            "NSMessage": "runWorkflowAsService",
            "NSSendTypes": ["public.utf8-plain-text"],
            "NSReturnTypes": ["public.utf8-plain-text"],
        }]
    }


def document(command):
    action = {
        "AMAccepts": {"Container": "List", "Optional": True, "Types": ["com.apple.cocoa.string"]},
        "AMActionVersion": "2.0.3",
        "AMApplication": ["Automator"],
        "AMParameterProperties": {"COMMAND_STRING": {}, "CheckedForUserDefaultShell": {},
                                  "inputMethod": {}, "shell": {}, "source": {}},
        "AMProvides": {"Container": "List", "Types": ["com.apple.cocoa.string"]},
        "ActionBundlePath": "/System/Library/Automator/Run Shell Script.action",
        "ActionName": "Run Shell Script",
        "ActionParameters": {"COMMAND_STRING": command, "CheckedForUserDefaultShell": True,
                             "inputMethod": 0, "shell": "/bin/zsh", "source": ""},
        "BundleIdentifier": "com.apple.RunShellScript",
        "CFBundleVersion": "2.0.3",
        "CanShowSelectedItemsWhenRun": False,
        "CanShowWhenRun": True,
        "Category": ["AMCategoryUtilities"],
        "Class Name": "RunShellScriptAction",
        "InputUUID": str(uuid.uuid4()).upper(),
        "Keywords": ["Shell", "Script", "Command", "Run", "Unix"],
        "OutputUUID": str(uuid.uuid4()).upper(),
        "UUID": str(uuid.uuid4()).upper(),
        "UnlocalizedApplications": ["Automator"],
        "arguments": {
            "0": {"default value": 0, "name": "inputMethod", "required": "0", "type": "0", "uuid": "0"},
            "1": {"default value": False, "name": "CheckedForUserDefaultShell", "required": "0", "type": "0", "uuid": "1"},
            "2": {"default value": "", "name": "source", "required": "0", "type": "0", "uuid": "2"},
            "3": {"default value": "", "name": "COMMAND_STRING", "required": "0", "type": "0", "uuid": "3"},
            "4": {"default value": "/bin/sh", "name": "shell", "required": "0", "type": "0", "uuid": "4"},
        },
        "conversionLabel": 0,
        "isViewVisible": 1,
        "location": "309.000000:305.000000",
        "nibPath": "/System/Library/Automator/Run Shell Script.action/Contents/Resources/Base.lproj/main.nib",
    }
    return {
        "AMApplicationBuild": "534",
        "AMApplicationVersion": "2.10",
        "AMDocumentVersion": "2",
        "actions": [{"action": action, "isViewVisible": 1}],
        "connectors": {},
        "workflowMetaData": {
            "applicationBundleIDsByPath": {},
            "applicationPaths": [],
            "inputTypeIdentifier": "com.apple.Automator.text",
            "outputTypeIdentifier": "com.apple.Automator.text",
            "presentationMode": 11,
            "processesInput": False,
            "serviceInputTypeIdentifier": "com.apple.Automator.text",
            "serviceOutputTypeIdentifier": "com.apple.Automator.text",
            "serviceProcessesInput": False,
            "systemImageName": "NSActionTemplate",
            "useAutomaticInputType": False,
            "workflowTypeIdentifier": "com.apple.Automator.servicesMenu",
        },
    }


def main():
    # Remove the one-item-per-tone actions from earlier versions.
    for old in SERVICES.glob("AI - *.workflow"):
        shutil.rmtree(old)
    for title, mode in ACTIONS.items():
        contents = SERVICES / f"{title}.workflow" / "Contents"
        contents.mkdir(parents=True, exist_ok=True)
        command = f"{shlex.quote(str(PYTHON))} {shlex.quote(str(HERE / 'rewrite.py'))} {mode}"
        with open(contents / "Info.plist", "wb") as f:
            plistlib.dump(info_plist(title), f)
        with open(contents / "document.wflow", "wb") as f:
            plistlib.dump(document(command), f)
        print(f"Installed: {title}")
    # Ask macOS to re-scan the Services menu.
    subprocess.run(["/System/Library/CoreServices/pbs", "-update"], check=False)


if __name__ == "__main__":
    main()
