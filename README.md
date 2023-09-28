# Lanista-Statistics (Beta)

## Description

A Python program that provides an easy-to-use interface to fetch and analyze statistics from the game [Lanista](https://beta.lanista.se). Utilizes a simple GUI to input login credentials and fetch data. The program will gather information about what stat points were placed into which statistic when increasing your "Grad" (level) and give you grade by grade overview. Data can be exported in either JSON or CSV format. Permission was given to create this program by Lanista Developers, but it is by all means unofficial. 

Example of csv output can be found here: [Lanista-Statistics-Example-CSV](https://docs.google.com/spreadsheets/d/1mdavIbndFyGw0294GwJUKw97IAgoVKZkpwG_yXGs4J4/edit?usp=sharing) 

![Lanista-Statistics-GUI](https://cdn.discordapp.com/attachments/1068228784584654988/1157081561162850395/Lanista_Glad_Info_v02.png?ex=65174fad&is=6515fe2d&hm=b1b1b2e6b3d80d1f4304df8b08749c09a4b97f8faf0d9a6d90698b477bb1d8f4)

## Installation

1. Clone the repository
2. Run GUI.py

## Usage
1. Run `GUI.py`
2. Enter your username and password in the text fields.
3. Click the "Hämta Gradinfo" button.
4. Once you see the message "Data inhämtad", you can export your data as either a JSON or CSV file by clicking the respective buttons.
5. The files will be exported to the project folder

## Dependencies
- Python
- bs4
- requests
  

## Contribution

Feel free to contribute to this project by opening issues or submitting pull requests. 
The code in its current form is a bit messy, I hope to have some time over to refactor it soon™. 
It should run for one gladiator at least, however, I haven't had a chance to test it out with more than one gladiator on an account. 

## Possible future implementations

* Code refactoring for better maintainability
* Test support for multiple Gladiators
* Add visual representations of statistics
* Add more customization for data exports
* GUI updates
* Add Gladiator Planner (showing needed stats for weapons, items, calculating stats with race bonuses etc)


   
