# In-Memory Database Project

This project is a simple implementation of an in-memory database in Python. It provides a basic set of operations to interact with the data stored in memory. The project also includes a cursor implementation that allows for transactional operations.

## Features

- **In-Memory Storage**: The data is stored in memory, providing fast access times.
- **Thread-Safe Operations**: The operations on the data are thread-safe, using locks to prevent race conditions.
- **Transactional Operations**: The cursor implementation allows for transactional operations, including commit and rollback.
- **Key Expiry**: Keys can be set to expire after a certain amount of time.
- **Backup and Restore**: The data can be backed up to a JSON file and restored from it.

## Usage

The main entry point of the application is the `main.py` script. This script provides a command-line interface to interact with the in-memory database. The available commands are:

- `SET <key> <value>`: Set the value for a given key.
- `GET <key>`: Get the value for a given key.
- `DELETE <key>`: Delete the value for a given key.
- `SET_EXPIRY <key> <seconds>`: Set the expiry time for a given key.
- `GET_EXPIRY <key>`: Get the expiry time for a given key.
- `EXIT`: Exit the application.

## Code Structure

The code is organized into two main modules:

- `pyinmem.py`: This module contains the `MemStore` class, which represents the in-memory database, and the `Cursor` class, which allows for transactional operations on the database.
- `main.py`: This module contains the main function that runs the command-line interface.

## Running the Project

To run the project, simply execute the `main.py` script:

```bash
python main.py
```

## Dependencies

This project is written in Python and does not require any external libraries.

## Contact

- **Name**: Erfan Rezaee
- **Email**: rezaee.e2002@gmail.com