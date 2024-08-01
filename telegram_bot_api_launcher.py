import subprocess
import os


def run_telegram_bot():
    # Change directory to the specified path
    os.chdir('./telegram-bot-api/bin')

    # Define the command to run the executable with the required arguments
    command = [
        './telegram-bot-api',
        '--api-id=your-api-id',
        '--api-hash=your-hash',
        '--http-port=8081',
        '--local'
    ]

    # Run the command in a new subprocess.
    subprocess.run(command)


if __name__ == '__main__':
    run_telegram_bot()
