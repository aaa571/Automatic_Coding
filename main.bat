@echo off


REM Anacondaの仮想環境を有効化します。
call C:\ProgramData\Anaconda3\Scripts\activate.bat

REM Studyは仮想環境名です。適宜変更してください。
call activate Study

REM Pythonスクリプトを実行します。
python "C:\Automatic_code_generation\program\main.py"

REM 仮想環境を無効化します。
call conda deactivate


pause