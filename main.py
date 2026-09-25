from assistant.commands import handle_command


def main():
    print("JARVIS se zaganja...")
    print("Vpiši 'pomoč' za seznam ukazov ali 'izhod' za konec.\n")

    while True:
        try:
            command = input("Ti > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nJARVIS > Nasvidenje.")
            break

        if not command:
            continue

        if command.lower() in {"izhod", "exit", "quit"}:
            print("JARVIS > Nasvidenje.")
            break

        print(f"JARVIS > {handle_command(command)}")


if __name__ == "__main__":
    main()
