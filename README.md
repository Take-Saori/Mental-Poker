# Mental Poker
This is a simple implementation of Mental Poker implemented on streamlit.

This app requires images of poker cards (named \<number\>\_of\_\<suit\>.png, e.g. 2_of_clubs.png, ace_of_spades.png), however I have not upload the images yet. (May upload later)

## Instructions to run app

To run the app:
1. Git clone this repo.
```
git clone https://github.com/Take-Saori/Mental-Poker.git
```
2. Navigate into the project folder.
```
cd Mental-Poker
```
3. Create Python environment 
```
pip install virtualenv
virtualenv pyenv
```
4. Start Python env
```
pyenv\Scripts\activate
```
5. Download dependencies
```
pip install -r /path/to/requirements.txt
```
6. Run ``bob_server.py`` first.
```
streamlit run /path/to/repo/bob_server.py
```
7. Run ``alice_client.py`` next on another terminal, using the same environment.
```
streamlit run /path/to/repo/alice_client.py
```
8. Follow the app's instructions to play Mental Poker.

9. The game of Mental Poker ends when the winner is decided. If you want to play again, stop running both scripts (``bob_server.py`` and ``alice_client.py``), then follow the instructions from step 6.