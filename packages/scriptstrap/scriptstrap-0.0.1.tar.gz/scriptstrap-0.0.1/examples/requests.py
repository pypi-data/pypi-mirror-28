#!/usr/bin/env python3

import scriptstrap

scriptstrap.running('requests')

print(requests.get('http://google.com').content)
