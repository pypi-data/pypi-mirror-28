import sys
import paperspace

if not paperspace.login():
    sys.exit(1)

print("paperspace.jobs.getJobs({'project': 'all'})")
jobs = paperspace.jobs.getJobs({'project': 'all'})
if 'error' in jobs:
    paperspace.print_json_pretty(jobs)
else:
    if jobs:
        print(jobs[-1]['id'])
