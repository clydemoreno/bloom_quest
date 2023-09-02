# bloom_quest
A distributed bloom filter based cache engine

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A Python-based system designed for implementing a bloom filter caching endpoint. This system is designed with durability, scalability, reliability, cost-effectiveness, and performance in mind.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Bloom filter support for distributed systems.
- Multiple data population methods:
  - Direct DB connections (supports MySQL, DynamoDB, etc. through plug-ins).
  - Loading data from files (auto-loads on folder changes).
  - Snapshot data creation and recovery.
  - Data replication and validation.
- Immutable bloom filter array with read and write copies.
- Quick recovery from built-in snapshots.
- Factory pattern for creating new filters.
- ...

## Getting Started

### Prerequisites

- Python 3.x
- [pip](https://pip.pypa.io/en/stable/installing/) (Python package manager)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/clydemoreno/bloom_quest.git
   cd bloomfilter-caching


Convention. Event driven, concurrent, SOLID principles. Clean architecture. Test driven development. 
1. Asynchronous code on I/O bound operations
2. Multi-threaded on CPU bound operations
3. Use of memoization in loading config file
4. Double buffer to improve predictability during bit array import
5. use paging when getting data to reduce memory footprint
6. use yield keyword during processing of data to reduce memory footprint
7. use worker threads to process chunk of data coming
8. Use abstract classes to enforce contract. Gives ability to switch different implementation
9. Use of decorators to add functionality. 