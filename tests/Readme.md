# API Tests

This directory contains Postman collections for API testing.

## Running tests

1. Install Postman: https://www.postman.com/downloads/
2. Import the collection: File > Import > Upload Files
3. Run the collection in Postman

## Automated testing

To run tests via command line:

1. Install Newman: `npm install -g newman`
2. Run: `newman run crud-master.postman_collection.json`

This can be integrated into CI/CD pipelines for automated testing.