import requests
import subprocess
import rich
import rich.table
import rich.panel
from rich import print as rprint

binAddress = "https://gtfobins.org/api.json"
downloadedBins = []

scanDone = {
    "done": False,
    "unprivileged": False,
    "sudo": False,
    "suid": False,
    "capabilities": False
}

def intro():
    print("\033[0;31m░░░░░░▀\033[0;37m   \033[0;90m▄▄▄\033[0;37m▄▄▄\033[0;90m▄\033[0;37m \033[0;31m░░░\033[0;37m \033[0;90m▄▄▄▄▄▄▄▄▄▄▄▄▄\033[0;37m▄▄▄\033[0;90m▄\033[0;37m \033[0;31m░░░░░░▀\033[0;37m   \033[0;90m▄▄▄\033[0;37m▄▄▄\033[0;90m▄\033[0;37m \033[0;31m░░░░░░░░░▀\033[0;37m   \033[0;90m▄▄▄\033[0;37m▄\033[0;90m▄\033[0;37m \033[0;31m▀▓▒░░\033[0m")
    print("\033[0;31m░░░░\033[0;37m \033[0;90m▄▄█▀▀░░▓\033[0;90;47m▓░▓\033[0;90m▌\033[0;37m \033[0;31m▐▀\033[0;37m \033[0;90m█▓▒░\033[0;37m  \033[0;90m▄▄█▀▀░░▓\033[0;90;47m▓░▓\033[0;90m▌\033[0;37m \033[0;31m░░░░\033[0;37m \033[0;90m▄▄█▀▀░░▓\033[0;90;47m▓░▓\033[0;90m▌\033[0;37m \033[0;31m▐▀\033[0;37m \033[0;31m░░░░\033[0;37m \033[0;90m▄▄█▀▀░░▓\033[0;90;47m▓░▓\033[0;90m▄\033[0;37m \033[0;31m▐▒▒\033[0m")
    print("\033[0;31m▒▒\033[0;37m \033[0;90m▄▀\033[0;37m \033[0;90m▄▄\033[0;90;47m▀\033[0;90m▀\033[0;90;47m▀▀\033[0;37m█\033[0;97;47m▄▌\033[0;90m█\033[0;37m  \033[0;90m▄▄▀▀▄█▄\033[0;37m \033[0;90m▀\033[0;37m \033[0;90m▄▄\033[0;90;47m▀\033[0;90m▀\033[0;90;47m▀▀\033[0;37m█\033[0;97;47m▄▌\033[0;90m█\033[0;37m \033[0;31m░▒▒\033[0;37m \033[0;90m▄▀\033[0;37m \033[0;90m▄▄\033[0;90;47m▀\033[0;90m▀\033[0;90;47m▀▀\033[0;37m█\033[0;97;47m▄▌\033[0;90m█\033[0;37m  \033[0;90m▄▄▀\033[0;31m▒▒\033[0;37m \033[0;90m▄▀\033[0;37m \033[0;90m▄▄\033[0;90;47m▀\033[0;90m▀\033[0;90;47m▀▀\033[0;37m█\033[0;97;47m▄▌\033[0;90m█▀▄\033[0;37m \033[0;31m░░\033[0m")
    print("\033[0;31m▓\033[0;37m \033[0;90;47m▓\033[0;90m▌\033[0;37m \033[0;90m█\033[0;37m█▀   █\033[0;97;47m█▓\033[0;90;47m▐\033[0;90m▀▄█\033[0;90;47m▓\033[0;37m \033[0;31m░▄\033[0;37m \033[0;90m██▌\033[0;37m \033[0;90m█\033[0;37m█▀   █\033[0;97;47m█▓\033[0;90;47m▐\033[0;90m▀\033[0;37m \033[0;31m█▓\033[0;37m \033[0;90;47m▓\033[0;90m▌\033[0;37m \033[0;90m█\033[0;37m█▀   █\033[0;97;47m█▓\033[0;90;47m▐\033[0;90m▀▄█\033[0;90;47m▓\033[0;37m \033[0;31m░▓\033[0;37m \033[0;90;47m▓\033[0;90m▌\033[0;37m \033[0;90m█\033[0;37m█▀   █\033[0;97;47m█▓\033[0;90;47m▐\033[0;90m▀▄█▄\033[0;31m░░\033[0m")
    print("\033[0;31m▌\033[0;37m▐\033[0;90m█\033[0;37m \033[0;90m█\033[0;90;47m░\033[0;37m▌ \033[0;91;41m▄\033[0;31m▌\033[0;37m ▐█\033[0;90;47m▄▀▀ \033[0;37m▓\033[0;90;47m░\033[0;37m \033[0;31m░█▌\033[0;37m▐\033[0;90m█▓█\033[0;90;47m░\033[0;37m▌ \033[0;91;41m▄\033[0;31m█\033[0;37m ▐█\033[0;90;47m▄\033[0;37m  \033[0;31m██▌\033[0;37m▐\033[0;90m█\033[0;37m \033[0;90m█\033[0;90;47m░\033[0;37m▌ \033[0;91;41m▄\033[0;31m█\033[0;37m ▐█\033[0;90;47m▄▀▀ \033[0;37m▓\033[0;90;47m░\033[0;37m \033[0;31m░▌\033[0;37m▐\033[0;90m█\033[0;37m \033[0;90m█\033[0;90;47m░\033[0;37m▌ \033[0;91;41m▄\033[0;31m▌\033[0;37m ▐█\033[0;90;47m▄▀▀ \033[0;37m▓\033[0;90m█\033[0;37m \033[0;31m░\033[0m")
    print("\033[0;31m▌\033[0;37m▐\033[0;90;47m░\033[0;90m█\033[0;90;47m▓\033[0;37m█ \033[0;31m▒▓\033[0;37m \033[0;90m▀\033[0;37m▀▀ \033[0;31m▄▄▄▄▄▄▓█▌\033[0;37m▐\033[0;90;47m░\033[0;90m█\033[0;90;47m▓\033[0;37m█ \033[0;31m▐██░\033[0;90m▀\033[0;37m▀ \033[0;31m▄▄██▌\033[0;37m▐\033[0;90;47m░\033[0;90m█\033[0;90;47m▓\033[0;37m█  \033[0;31m██░\033[0;90m▀\033[0;37m▀ \033[0;31m▄▄▄▄▄▄░▌\033[0;37m▐\033[0;90;47m░\033[0;90m█\033[0;90;47m▓\033[0;37m█  \033[0;31m██\033[0;37m \033[0;90m▀\033[0;37m▓███\033[0;90;47m░▓\033[0;90m▓▌\033[0;31m▒\033[0m")
    print("\033[0;37m ██\033[0;90;47m▓░\033[0;37m█ ▄▄▄▄▄▄\033[0;97m▄▄▄\033[0;37m▄▄ \033[0;31m▀▐█\033[0;37m ██\033[0;90;47m▓░\033[0;37m█ \033[0;31m█▓███████▓▓\033[0;37m ██\033[0;90;47m▓░\033[0;37m█\033[0;90m▄\033[0;37m▄▄\033[0;90m▄\033[0;37m \033[0;31m█████▓▓▓▓░\033[0;37m ██\033[0;90;47m▓░\033[0;37m█ \033[0;31m████\033[0;37m \033[0;90m▀\033[0;90;47m▄\033[0;37m█\033[0;90;47m░▓\033[0;90m▓█▓\033[0;31m▐\033[0m")
    print("\033[0;37m ██\033[0;90;47m░\033[0;37m██ ▀▀▀▀\033[0;90;47m░\033[0;37m█\033[0;90;47m░░\033[0;97;47m░▀▄\033[0;90;47m░\033[0;90m▄\033[0;31m▐█\033[0;37m ██\033[0;90;47m░\033[0;37m██ \033[0;31m▒▓██████▓▓▓\033[0;37m ██\033[0;90;47m░\033[0;37m███\033[0;90;47m▄\033[0;90m▀\033[0;37m \033[0;31m░████▓▓▓▓▒░\033[0;37m ██\033[0;90;47m░\033[0;37m██ \033[0;31m█▓██▀\033[0;37m \033[0;90m█\033[0;90;47m▓▓█▓▀▓\033[0;31m▐\033[0m")
    print("\033[0;37m █\033[0;97;47m░\033[0;90;47m░\033[0;37m██ \033[0;31m█\033[0;91;41m█▓\033[0;31m▌\033[0;37m \033[0;90;47m░▒▒▒▒\033[0;97;47m▒\033[0;37m█\033[0;90;47m▄\033[0;90m▌\033[0;31m█\033[0;37m █\033[0;97;47m░\033[0;90;47m░\033[0;37m██  \033[0;91m▄\033[0;91;41m▓\033[0;31m▒███▓▓▓▓\033[0;37m █\033[0;97;47m░\033[0;90;47m░\033[0;37m██  \033[0;91m▄\033[0;91;41m▓\033[0;31m▒███▓▓▓▓▓▓░\033[0;37m █\033[0;97;47m░\033[0;90;47m░\033[0;37m██ \033[0;31m█\033[0;91m▄\033[0;91;41m▓\033[0;31m▒\033[0;37m  \033[0;90m█\033[0;90;47m▓▒▓░\033[0;37m█\033[0;90;47m▄\033[0;90m▌\033[0m")
    print("\033[0;37m \033[0;90;47m░\033[0;97;47m▓▄\033[0;37m██ \033[0;31m▀\033[0;91;41m▀\033[0;31m██▌\033[0;90m▐\033[0;37m█\033[0;90;47m▓▓▓▓▒\033[0;90m▌▒\033[0;31m▒\033[0;37m \033[0;90;47m░\033[0;97;47m▓▄\033[0;37m██  \033[0;91;41m▀\033[0;31m█░███████\033[0;37m \033[0;90;47m░\033[0;97;47m▓▄\033[0;37m██  \033[0;91;41m▀\033[0;31m█░███████▓▒░\033[0;37m \033[0;90;47m░\033[0;97;47m▓▄\033[0;37m██\033[0;90m▌\033[0;37m \033[0;91;41m▀\033[0;31m█░\033[0;37m \033[0;90m▐\033[0;37m█\033[0;90;47m░░░▄█\033[0;90m▌▐\033[0m")
    print("\033[0;37m \033[0;90;47m░\033[0;37m█\033[0;97;47m▀██\033[0;37m█▄   ▄▄\033[0;90;47m░▓█\033[0;90m█▀\033[0;90;47m▓\033[0;37m \033[0;90m▓\033[0;31m░\033[0;37m \033[0;90;47m░\033[0;37m█\033[0;97;47m▀██\033[0;37m█▄ \033[0;31m▀████████\033[0;37m \033[0;90;47m░\033[0;37m█\033[0;97;47m▀██\033[0;37m█▄ \033[0;31m▀█████████▒░\033[0;37m \033[0;90;47m░\033[0;37m█\033[0;97;47m▀██\033[0;37m█\033[0;90m▄\033[0;37m   \033[0;90m▄\033[0;90;47m▀░▓█\033[0;90m█▀▀▐▓\033[0m")
    print("\033[0;90m▐\033[0;90;47m▓░\033[0;37m█\033[0;97;47m \033[0;37m██\033[0;90;47m▄▄▄▄▄\033[0;90m▀░▀\033[0;90;47m▓\033[0;90m▄▀▄▀█\033[0;37m \033[0;90m▐\033[0;90;47m▓░\033[0;37m█\033[0;97;47m \033[0;37m██\033[0;90;47m▄\033[0;90m█▄\033[0;37m \033[0;31m███████\033[0;90m▐\033[0;90;47m▓░\033[0;37m█\033[0;97;47m \033[0;37m██\033[0;90;47m▄\033[0;90m█▄\033[0;37m \033[0;31m███████▓▒░\033[0;37m \033[0;90;47m▓░\033[0;37m█\033[0;97;47m \033[0;37m██\033[0;90;47m▄▄▄▄▄\033[0;90m▀▀▀\033[0;37m  \033[0;90m▄▄█▀\033[0m")

    rprint("\n Unofficial GTFO Bins advisor by [bold cyan]26Diesel[/bold cyan] from [bold dark_orange]T[/bold dark_orange][bold]ITAN Security\n")


def getBins():
    try:
        res = requests.get(binAddress)
        rprint("[bold green]Successfully fetched the GTFO Bins![/bold green]")

    except Exception as e:
        rprint("[bold red]Error! I am unable to fetch the GTFO Bins.[/bold red]")
        rprint(f"[orange1]I tried to get the latest GTFO Bins from [green]{binAddress}[/green], but an error occurred. More info below.[/orange1]")
        print(e)
        exit()

    raw = res.json()["executables"]
    for bin, data in raw.items():
        for function, variants in (data.get("functions") or {}).items():
            downloadedBins.append({
                "id": len(downloadedBins) + 1,
                "bin": bin,
                "function": function,
                "description": data.get("comment"),
                "variants": variants
            })

def runbash(command):
    output = subprocess.run(
        ["/bin/bash", "-c", command],
        capture_output=True,
        text=True,
        check=True
    )
    return output.stdout.strip()


def getUnpriv():
    try:
        output = runbash("compgen -ac").splitlines()
        scanDone["unprivileged"] = True
        return output
    except Exception:
        rprint("[bold yellow]Error! I am unable to fetch the unprivileged binaries.[/bold yellow]")
        return []


def getSudo():
    try:
        output = runbash("sudo -l").splitlines()
        scanDone["sudo"] = True
        return output
    except Exception:
        rprint("[bold yellow]Error! I am unable to fetch the sudo binaries.[/bold yellow]")
        return []


def getSuid():
    try:
        output = runbash("find / -perm -4000 -type f 2>/dev/null | xargs -r -n1 basename | sort -u").splitlines()
        scanDone["suid"] = True
        return output
    except Exception:
        rprint("[bold yellow]Error! I am unable to fetch the SUID binaries.[/bold yellow]")
        return []


def getCapabilities():
    try:
        output = runbash("getcap -r / 2>/dev/null").splitlines()
        scanDone["capabilities"] = True
        return output
    except Exception:
        rprint("[bold yellow]Error! I am unable to fetch the capability binaries.[/bold yellow]")
        return []


def binInLines(binName, lines):
    for line in lines:
        if binName in line:
            return True
    return False


def autoScan():
    rprint("[bold yellow]Automatically scanning for usable GTFO bins...[/bold yellow]")
    scanDone["done"] = True

    unpriv = getUnpriv()

    answer = input("Do you know the password for the current user? [Y/n] > ").strip().lower()
    if answer in ("n", "no"):
        rprint("[bold yellow]Skipping sudo scan.[/bold yellow]")
        sudo = []
    else:
        sudo = getSudo()

    suid = getSuid()
    caps = getCapabilities()

    countUnpriv = 0
    countSudo = 0
    countSuid = 0
    countCaps = 0

    for bin in downloadedBins:
        binName = bin["bin"]

        bin["unprivileged"] = binName in unpriv
        bin["sudo"] = binInLines(binName, sudo)
        bin["suid"] = binName in suid
        bin["capabilities"] = binInLines(binName, caps)

        if bin["unprivileged"]: countUnpriv += 1
        if bin["sudo"]: countSudo += 1
        if bin["suid"]: countSuid += 1
        if bin["capabilities"]: countCaps += 1

        contexts = set()
        for variant in bin["variants"]:
            for context, value in variant["contexts"].items():
                if value is not None:
                    contexts.add(context)

        if not contexts:
            contexts.add("unprivileged")

        availableContexts = [context for context in contexts if bin.get(context)]

        if not availableContexts:
            bin["available"] = "none"
        elif len(availableContexts) == len(contexts):
            bin["available"] = "all"
        else:
            bin["available"] = "only " + ", ".join(sorted(availableContexts))

    counterTable = rich.table.Table(title="GTFO Bins Scan Results", show_header=True, header_style="bold magenta")
    counterTable.add_column("Category", style="dim", width=20)
    counterTable.add_column("Count", style="bold cyan", width=10)
    counterTable.add_row("Unprivileged", str(countUnpriv))
    counterTable.add_row("Sudo", str(countSudo))
    counterTable.add_row("SUID", str(countSuid))
    counterTable.add_row("Capabilities", str(countCaps))
    rprint(counterTable)

def printEveryBin(onlyAvailable):
    if onlyAvailable and not scanDone["done"]:
        rprint("[bold yellow]No scan has been run yet.[/bold yellow]")
        choice = input("Run the automatic scan now? [Y/n] > ").strip().lower()
        if choice in ("n", "no"):
            return
        autoScan()

    binTable = rich.table.Table(title="GTFO Bins", show_lines=True)
    binTable.add_column("#", style="bold white", no_wrap=True)
    binTable.add_column("Binary", style="cyan", no_wrap=True)
    binTable.add_column("Function", style="magenta")
    binTable.add_column("Privileges")
    binTable.add_column("Available")

    for bin in downloadedBins:
        available = bin.get("available", "Unknown")
        if onlyAvailable and available in ("none", "Unknown"):
            continue

        privileges = set()
        for variant in bin["variants"]:
            for context, value in variant["contexts"].items():
                if value is not None:
                    if context == "sudo": privileges.add("[bold red]sudo[/bold red]")
                    if context == "suid": privileges.add("[bold dark_orange]suid[/bold dark_orange]")
                    if context == "capabilities": privileges.add("[bold blue]capabilities[/bold blue]")

        if not privileges: privileges.add("Unprivileged")
        binTable.add_row(str(bin["id"]), bin["bin"], bin["function"], ", ".join(sorted(privileges)), available)

    rprint(binTable)


def showCoolShit():
    if not scanDone["done"]:
        rprint("[bold yellow]No scan has been run yet.[/bold yellow]")
        answer = input("Run the automatic scan now? [Y/n] > ").strip().lower()
        if answer in ("n", "no"):
            return
        autoScan()

    binTable = rich.table.Table(title="Cool GTFO Bins", show_lines=True)
    binTable.add_column("#", style="bold white", no_wrap=True)
    binTable.add_column("Binary", style="cyan", no_wrap=True)
    binTable.add_column("Function", style="magenta")
    binTable.add_column("Available")

    found = False
    for bin in downloadedBins:
        available = []
        if bin.get("sudo"): available.append("[bold red]sudo[/bold red]")
        if bin.get("suid"): available.append("[bold dark_orange]suid[/bold dark_orange]")
        if bin.get("capabilities"): available.append("[bold blue]capabilities[/bold blue]")

        if not available:
            continue

        found = True
        binTable.add_row(str(bin["id"]), bin["bin"], bin["function"], ", ".join(available))

    if not found:
        rprint("[bold yellow]No cool binaries found for the scanned contexts.[/bold yellow]")
        return

    rprint(binTable)

def handleShow(id):
    if id < 1 or id > len(downloadedBins):
        rprint(f"[bold red]Error! No bin found at index {id}.[/bold red]")
        return

    bin = downloadedBins[id-1]
    binName = bin["bin"]
    function = bin["function"]
    description = bin.get("description") or "No description available."

    rprint(rich.panel.Panel(
        f"[bold cyan]Binary:[/bold cyan] {binName}\n"
        f"[bold magenta]Function:[/bold magenta] {function}\n"
        f"[bold]Description:[/bold] {description}",
        title=f"#{id}",
        border_style="blue"
    ))

    for i, variant in enumerate(bin["variants"], start=1):
        variantTable = rich.table.Table(title=f"Variant {i}", show_lines=True)
        variantTable.add_column("Context", style="bold yellow", no_wrap=True)
        variantTable.add_column("Code")
        variantTable.add_column("Comment", style="dim")

        baseCode = variant.get("code") or "N/A"
        baseComment = variant.get("comment") or ""
        variantTable.add_row("base", baseCode, baseComment)

        for context, value in variant.get("contexts", {}).items():
            if value is None:
                variantTable.add_row(context, "[dim]Not applicable[/dim]", "")
            elif isinstance(value, dict):
                code = value.get("code") or baseCode
                comment = value.get("comment") or ""
                variantTable.add_row(context, code, comment)
            else:
                variantTable.add_row(context, baseCode, "")

        rprint(variantTable)

def printMenu():
    rprint("[bold blue]1.[/bold blue] [bold yellow]Automatic scan[/bold yellow]")
    rprint("[bold blue]2.[/bold blue] Show every bin")
    rprint("[bold blue]3.[/bold blue] Show every available bin")
    rprint("[bold blue]4. Show every cool shit[/bold blue]")
    rprint("[bold yellow]show [[bold green]id[/bold green][bold yellow]][/bold yellow]")

    choice = input('> ')
    choice = choice.split(' ')

    if choice[0] == '1':
        autoScan()
    elif choice[0] == '2':
        printEveryBin(False)
    elif choice[0] == '3':
        printEveryBin(True)
    elif choice[0] == '4':
        showCoolShit()

    elif choice[0] == 'show':
        if len(choice) < 2 or not choice[1].isdigit():
            rprint("[bold red]Usage: show [[bold yellow]id[/bold yellow]][/bold red]")
        else:
            handleShow(int(choice[1]))

# They fear what they can't trace. Knowledge is freedom.

if __name__ == "__main__":
    intro()
    getBins()
    while True:
        printMenu()
