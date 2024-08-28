# N-Multi-Bot

[日本語: README.md](README.md)

This project is a command handler system for a multi-functional bot that operates in LINE group chats.

## Install

1. Clone repository:

   ```bash
   git clone https://github.com/nezumi0627/N-Multi-Bot.git
   cd N-Multi-Bot
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install CHRLINE-Patch library:

   ```bash
   pip install git+https://github.com/WEDeach/CHRLINE-Patch.git
   ```

4. Run `main.py` and set bot information.

## Usage

1. Edit `main.py` and set bot information.
2. Run `main.py` and start bot.
3. Use `!help` command in LINE group chat to check available commands.

## Dependencies

- Python 3.x
- CHRLINE-Patch library
- Other dependencies are listed in `requirements.txt`

## Setup

1. Create `./data/auther.json` file and set MID of admin and owner:

   ```json
   {
     "admin": ["adminMID1", "adminMID2"],
     "owner": ["ownerMID1", "ownerMID2"]
   }
   ```

2. Set LINE account authentication information in environment variables or `config.json` file.

## Security

- There is an automatic setup function for E2EE keys.
- Supports encryption and decryption of messages.

## Project structure

- `main.py`: Main bot logic and command handler
- `messenger.py`: Manage message sending functions
- `data/auther.json`: Admin and owner settings file

## Notes

- This bot can only use commands for admins and owners.
- The responsibility for using the CHRLINE-Patch library is not ours. This project has no relationship with the CHRLINE-Patch library.
- This project was created for debugging purposes. We recommend using the official LINE API for actual bot operation.

## Troubleshooting

- If there is a problem with the E2EE key setup, check the `setup_e2ee_key` method.
- If a database read error occurs, check the existence and contents of the `data/auther.json` file.

## Contact

If you have any questions or suggestions, please contact us via [Issues](https://github.com/nezumi0627/N-Multi-Bot/issues).

## Update history

- vβ (2023-08-29): Initial release

## Acknowledgments

We would like to express our gratitude to the developers of the CHRLINE-Patch library.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

This software is provided "as is", without warranty of any kind, express or implied. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the software.

When using this project, please comply with the relevant laws and instructions.
