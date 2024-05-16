#!/usr/bin/env python
import os
from dotenv import load_dotenv
load_dotenv()
from FinLat import FinLat


#agentops.init()


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': "What's the difference between saving and investing, and how do I decide which one is right for me?"
    }
    FinLat().crew().kickoff(inputs=inputs)


if __name__== "__main__":
    run()