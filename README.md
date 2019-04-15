## capstone-project-a-team

## Description

This service provides generation of new course learning outcomes for courses existing in UNSW. Additionally, users are able to evaluate existing course learning outcomes and recognise which outcomes need to be improved. This system is built on Python 3 with data that was preprocessed with NLP provided by AWS Comprehend API (https://docs.aws.amazon.com/comprehend/latest/dg/API_Reference.html).

## Getting Started

### Prerequisites

It is assumed that:

Python 3.6.5 or above is installed (https://www.python.org/downloads/)

### Installation

pip3 install -r requirements.txt

## How to use

For generating outcomes:
1. Find the UNSW course you are after
2. Choose appropriate active verbs 
3. View key phrases, remove any unnecessary ones
4. Fill in the context and complete the sentence
5. View the generated outcomes and download for later use
* TIP: in the downloaded file, the service also recommends appropriate assessments for outcomes

For evaluating outcomes:
1. Find the UNSW course you want to evaluate
2. See which outcomes might need improvements 
* TIP: information on how we evaluate the outcomes is explained on the page in more detail.


## License

Copyright (C) 2019 Sharon Park, Tiancong Liu, Yitong Xiao, and Yun Lu
