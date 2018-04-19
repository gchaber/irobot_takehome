# IRobot Takehome

This program does the following:
~~~
1. The user enters a series of ingredients (It has a spell checker)
2. The program will use Food2Fork to find the most popular recipe that contains most if not all of those ingredients
3. Finally, the program will retrieve this recipe and print out any ingredients that weren't in the recipe
~~~
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development, testing, and running.

### Prerequisites

* Python 3 Installation required (python3 is the assumed executable name in the examples below)
* Doxygen required to generate HTML documentation of the code
* No other special dependencies are required

### Installing

First clone the repository
```
cd <install directory>
git clone https://github.com/gchaber/irobot_takehome ./irobot_takehome
```
No need to create a virtual environment since there are no special requirements

### Running

You can then start the application in the terminal
```
cd <root directory>
python3 takehome.py
```

## Unit Tests

To run all unit tests:
```
cd <root directory>
python3 run_tests.py all
```
Below lists how you can test each component individually.

### API Tests

To run the tests relating to the API
```
cd <root directory>
python3 run_tests.py api
```

### Spellcheck Tests

To run the tests relating to the spell checker
```
cd <root directory>
python3 run_tests.py spellcheck
```

### User Interface Tests

To run the tests relating to the user interface/input flow
```
cd <root directory>
python3 run_tests.py user_interface
```

## Documentation (Doxygen)

You can build the developer documentation by running:
```
cd <root directory>
doxygen doxygen.conf
```
The HTML documentation is generated with at the path: /docs/html

## Built With

* [Adambom Dictionary](https://github.com/adambom/dictionary/) - The English dictionary used

## Authors

* **Greg Chaber** - [gchaber](https://github.com/gchaber)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details