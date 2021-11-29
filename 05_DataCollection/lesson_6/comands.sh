#!/bin/bash

# Create project
scrapy startproject jobparser .

# Create Spider
scrapy genspider hhru hh.ru

# Run
scrapy crwal hhru